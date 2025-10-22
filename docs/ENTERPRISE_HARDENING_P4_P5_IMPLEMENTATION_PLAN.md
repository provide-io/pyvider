# Enterprise Hardening Implementation Plan
## Priority #4: Resource Lifecycle & Cleanup
## Priority #5: Input Validation & Sanitization

**Date Created:** 2025-10-22
**Status:** Ready for Implementation
**Estimated Effort:** 3-4 weeks (2 engineers)
**Risk Level:** Medium (requires careful testing)

---

## Executive Summary

This document provides a detailed implementation plan for two critical enterprise hardening priorities:

- **Priority #4:** Resource Lifecycle & Cleanup - Prevent memory leaks and ensure graceful shutdown
- **Priority #5:** Input Validation & Sanitization - Prevent DoS attacks and injection vulnerabilities

**Business Impact:**
- Prevents production outages from memory leaks
- Eliminates DoS attack vectors
- Ensures compliance with security standards (SOC2, ISO 27001)
- Reduces operational costs from resource leaks

---

## Table of Contents

1. [Priority #4: Resource Lifecycle & Cleanup](#priority-4-resource-lifecycle--cleanup)
   - [Current Problems](#p4-current-problems)
   - [Solutions](#p4-solutions)
   - [Implementation Checklist](#p4-implementation-checklist)
2. [Priority #5: Input Validation & Sanitization](#priority-5-input-validation--sanitization)
   - [Current Problems](#p5-current-problems)
   - [Solutions](#p5-solutions)
   - [Implementation Checklist](#p5-implementation-checklist)
3. [Testing Strategy](#testing-strategy)
4. [Rollout Plan](#rollout-plan)
5. [Success Metrics](#success-metrics)

---

# Priority #4: Resource Lifecycle & Cleanup

## P4: Current Problems

### Problem 1: Unbounded Cache Growth ⚠️ CRITICAL

**Location:** `src/pyvider/common/encryption.py:125-151`

**Current Code:**
```python
class EncryptionManager:
    def __init__(self) -> None:
        self._key_cache: dict[bytes, bytes] = {}  # ⚠️ Grows forever!
        self._lock = threading.Lock()

    def _derive_key(self, salt: bytes) -> bytes:
        with self._lock:
            if salt in self._key_cache:
                return self._key_cache[salt]

        derived_key = hkdf.derive(key_material)

        with self._lock:
            self._key_cache[salt] = derived_key  # ⚠️ Never expires!

        return derived_key
```

**Impact:**
- Memory grows unbounded in long-running processes
- Could reach gigabytes after months of operation
- Each unique salt creates a new cache entry
- No mechanism to remove old entries

**Real-World Scenario:**
```
Day 1:   1,000 encryptions  = 32 KB cache
Week 1:  10,000 encryptions = 320 KB cache
Month 1: 100,000 encryptions = 3.2 MB cache
Year 1:  1,000,000+ encryptions = 32+ MB cache (and growing)
```

---

### Problem 2: Background Tasks Without Cleanup ⚠️ HIGH

**Location:** `src/pyvider/protocols/service.py:115-123`

**Current Code:**
```python
async def _heartbeat(self) -> None:
    while self._stream_active:  # ⚠️ What if stream crashes but flag stays True?
        try:
            await asyncio.sleep(5)
            if self._stream_active:
                await self._message_queue.put(b"")
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            break  # Good! But no cleanup notification
```

**Impact:**
- Orphaned async tasks after exceptions
- No tracking of background tasks
- Potential resource leaks on shutdown
- No graceful shutdown guarantee

---

### Problem 3: No Resource Context Managers ⚠️ MEDIUM

**Current Code Pattern:**
```python
# Resources created but cleanup uncertain
service = ProtocolService(shutdown_event)
# ... service used ...
# ⚠️ Who cleans up _message_queue? What if exception occurs?
```

**Impact:**
- Cleanup depends on manual calls
- Exception in code path = leaked resources
- No RAII (Resource Acquisition Is Initialization) pattern
- Difficult to audit resource usage

---

## P4: Solutions

### Solution 1: LRU Cache with TTL ✅

**New File:** `src/pyvider/common/encryption.py` (enhanced)

**Key Features:**
- Bounded cache size (max 1,000 entries)
- Time-to-live (1 hour expiry)
- LRU eviction policy
- Automatic cleanup every 5 minutes
- Performance metrics

**Implementation:**

```python
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Final

@dataclass
class CacheEntry:
    """Cache entry with expiry."""
    key: bytes
    created_at: float
    last_accessed: float
    access_count: int = 0


class EncryptionManager:
    """Thread-safe encryption manager with bounded cache and TTL."""

    # Enterprise-grade limits
    MAX_CACHE_SIZE: Final[int] = 1000  # Prevent unbounded growth
    CACHE_TTL_SECONDS: Final[int] = 3600  # 1 hour expiry
    CLEANUP_INTERVAL: Final[int] = 300  # Cleanup every 5 minutes

    def __init__(self) -> None:
        # LRU cache with metadata
        self._key_cache: OrderedDict[bytes, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self._last_cleanup = time.time()
        self._metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "evictions": 0,
            "expirations": 0,
        }
        logger.debug("Encryption manager initialized with TTL cache")

    def _derive_key(self, salt: bytes) -> bytes:
        """Derive encryption key with LRU cache and TTL."""
        current_time = time.time()

        # Periodic cleanup
        if current_time - self._last_cleanup > self.CLEANUP_INTERVAL:
            self._cleanup_expired_entries()

        # Check cache (thread-safe)
        with self._lock:
            if salt in self._key_cache:
                entry = self._key_cache[salt]

                # Check if expired
                if current_time - entry.created_at > self.CACHE_TTL_SECONDS:
                    logger.debug("Cache entry expired", salt_hash=salt[:8].hex())
                    self._key_cache.pop(salt)
                    self._metrics["expirations"] += 1
                else:
                    # Cache hit - update LRU
                    entry.last_accessed = current_time
                    entry.access_count += 1
                    self._key_cache.move_to_end(salt)
                    self._metrics["cache_hits"] += 1

                    logger.debug(
                        "Using cached encryption key",
                        salt_hash=salt[:8].hex(),
                        age_seconds=int(current_time - entry.created_at),
                        access_count=entry.access_count,
                    )
                    return entry.key

        # Cache miss - derive new key
        self._metrics["cache_misses"] += 1
        secret = self._get_shared_secret()
        key_material = secret.encode("utf-8")

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            info=HKDF_INFO,
        )
        derived_key = hkdf.derive(key_material)

        # Store with LRU eviction (thread-safe)
        with self._lock:
            # Evict oldest if at capacity
            if len(self._key_cache) >= self.MAX_CACHE_SIZE:
                evicted_salt, evicted_entry = self._key_cache.popitem(last=False)
                self._metrics["evictions"] += 1
                logger.info(
                    "Evicted oldest cache entry",
                    evicted_salt_hash=evicted_salt[:8].hex(),
                    age_seconds=int(current_time - evicted_entry.created_at),
                    access_count=evicted_entry.access_count,
                )

            # Add new entry
            self._key_cache[salt] = CacheEntry(
                key=derived_key,
                created_at=current_time,
                last_accessed=current_time,
            )

            logger.debug(
                "Derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
                metrics=self._metrics,
            )

        return derived_key

    def _cleanup_expired_entries(self) -> None:
        """Remove expired cache entries."""
        current_time = time.time()

        with self._lock:
            expired_salts = [
                salt
                for salt, entry in self._key_cache.items()
                if current_time - entry.created_at > self.CACHE_TTL_SECONDS
            ]

            for salt in expired_salts:
                self._key_cache.pop(salt)
                self._metrics["expirations"] += 1

            self._last_cleanup = current_time

            if expired_salts:
                logger.info(
                    "Cleaned up expired cache entries",
                    count=len(expired_salts),
                    remaining=len(self._key_cache),
                )

    def get_metrics(self) -> dict:
        """Get cache performance metrics."""
        with self._lock:
            hit_rate = (
                self._metrics["cache_hits"]
                / (self._metrics["cache_hits"] + self._metrics["cache_misses"])
                if self._metrics["cache_hits"] + self._metrics["cache_misses"] > 0
                else 0
            )

            return {
                **self._metrics,
                "cache_size": len(self._key_cache),
                "hit_rate": f"{hit_rate:.2%}",
            }
```

---

### Solution 2: Async Context Manager for Service ✅

**File:** `src/pyvider/protocols/service.py` (enhanced)

**Key Features:**
- Async context manager (`__aenter__`/`__aexit__`)
- Background task tracking
- Graceful shutdown with timeout
- Queue draining on shutdown
- Guaranteed cleanup

**Implementation:**

```python
class ProtocolService:
    """Service with proper resource lifecycle management."""

    def __init__(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = True
        self._shutdown_event = shutdown_event
        self._message_queue = asyncio.Queue()
        self._background_tasks: set[asyncio.Task] = set()  # Track tasks
        self._cleanup_done = asyncio.Event()

        # Resource limits
        self.MAX_QUEUE_SIZE = 10000
        self.HEARTBEAT_INTERVAL = 5
        self.SHUTDOWN_TIMEOUT = 30

    async def __aenter__(self):
        """Async context manager entry."""
        logger.info("ProtocolService starting")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - guaranteed cleanup."""
        logger.info("ProtocolService shutting down", exception=exc_type)

        try:
            await self.graceful_shutdown(timeout=self.SHUTDOWN_TIMEOUT)
        except Exception as e:
            logger.error("Error during shutdown", error=e, exc_info=True)
        finally:
            self._cleanup_done.set()
            logger.info("ProtocolService cleanup complete")

        return False  # Don't suppress exceptions

    async def start_heartbeat(self) -> asyncio.Task:
        """Start heartbeat task with tracking."""
        task = asyncio.create_task(self._heartbeat())
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

        logger.debug("Started heartbeat task", task_id=id(task))
        return task

    async def _heartbeat(self) -> None:
        """Heartbeat with proper cleanup."""
        logger.debug("Heartbeat started")
        heartbeat_count = 0

        try:
            while self._stream_active and not self._shutdown_event.is_set():
                try:
                    await asyncio.sleep(self.HEARTBEAT_INTERVAL)

                    if self._stream_active and not self._shutdown_event.is_set():
                        # Check queue size before adding
                        if self._message_queue.qsize() < self.MAX_QUEUE_SIZE:
                            await self._message_queue.put(b"")
                            heartbeat_count += 1
                        else:
                            logger.warning(
                                "Queue full, skipping heartbeat",
                                queue_size=self._message_queue.qsize(),
                            )

                except asyncio.CancelledError:
                    logger.info("Heartbeat cancelled", beats_sent=heartbeat_count)
                    raise
                except Exception as e:
                    logger.error("Heartbeat error", error=e, exc_info=True)
                    break
        finally:
            logger.info("Heartbeat stopped", beats_sent=heartbeat_count)

    async def graceful_shutdown(self, timeout: float = 30) -> None:
        """Gracefully shutdown all resources."""
        logger.info("Starting graceful shutdown", timeout=timeout)

        # 1. Stop accepting new work
        self._stream_active = False

        # 2. Cancel background tasks
        if self._background_tasks:
            logger.debug("Cancelling background tasks", count=len(self._background_tasks))

            for task in self._background_tasks:
                task.cancel()

            # Wait for cancellation with timeout
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._background_tasks, return_exceptions=True),
                    timeout=timeout / 2,
                )
            except asyncio.TimeoutError:
                logger.warning("Background tasks did not cancel in time")

        # 3. Drain message queue
        drained = 0
        try:
            while not self._message_queue.empty() and drained < 1000:
                self._message_queue.get_nowait()
                drained += 1
        except asyncio.QueueEmpty:
            pass

        if drained > 0:
            logger.info("Drained message queue", messages=drained)

        # 4. Final cleanup
        self._message_queue = asyncio.Queue()  # Fresh queue
        logger.info("Graceful shutdown complete")


# USAGE EXAMPLE
async def run_provider_with_cleanup():
    """Example of proper resource management."""
    shutdown_event = asyncio.Event()

    async with ProtocolService(shutdown_event) as service:
        # Start background tasks
        heartbeat_task = await service.start_heartbeat()

        try:
            # Run service
            await service.StreamStdio(...)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error("Service error", error=e)
            raise
        # Automatic cleanup happens here via __aexit__
```

---

## P4: Implementation Checklist

### Phase 1: Encryption Manager Enhancement (Week 1)

- [ ] **Day 1-2: Implement LRU Cache**
  - [ ] Add `CacheEntry` dataclass with metadata
  - [ ] Replace `dict` with `OrderedDict` for LRU
  - [ ] Implement TTL checking in `_derive_key`
  - [ ] Add configuration constants (MAX_CACHE_SIZE, TTL)
  - [ ] Update unit tests

- [ ] **Day 3: Implement Cleanup Logic**
  - [ ] Add `_cleanup_expired_entries()` method
  - [ ] Implement periodic cleanup in `_derive_key`
  - [ ] Add metrics tracking
  - [ ] Add logging for evictions/expirations

- [ ] **Day 4: Add Metrics & Monitoring**
  - [ ] Implement `get_metrics()` method
  - [ ] Expose metrics via observability module
  - [ ] Add Prometheus metrics export
  - [ ] Create Grafana dashboard

- [ ] **Day 5: Testing & Validation**
  - [ ] Unit tests for TTL expiry
  - [ ] Unit tests for LRU eviction
  - [ ] Load test with 10,000+ operations
  - [ ] Memory profiling to verify no leaks
  - [ ] Performance benchmarks

### Phase 2: Service Context Manager (Week 2)

- [ ] **Day 1-2: Context Manager Implementation**
  - [ ] Add `__aenter__` and `__aexit__` methods
  - [ ] Implement background task tracking
  - [ ] Add `_background_tasks` set
  - [ ] Update `start_heartbeat()` method

- [ ] **Day 3: Graceful Shutdown**
  - [ ] Implement `graceful_shutdown()` method
  - [ ] Add task cancellation logic
  - [ ] Add queue draining logic
  - [ ] Add timeout handling

- [ ] **Day 4: Update Usage Sites**
  - [ ] Update `cli/provide_command.py`
  - [ ] Update all service instantiations
  - [ ] Add context manager usage examples
  - [ ] Update documentation

- [ ] **Day 5: Testing**
  - [ ] Unit tests for context manager
  - [ ] Integration tests for graceful shutdown
  - [ ] Chaos testing (kill -9, network failures)
  - [ ] Verify no resource leaks

### Phase 3: Rollout (Week 3)

- [ ] **Monitoring Setup**
  - [ ] Add metrics dashboards
  - [ ] Configure alerts for cache size
  - [ ] Configure alerts for task leaks
  - [ ] Set up resource usage monitoring

- [ ] **Staged Rollout**
  - [ ] Deploy to dev environment
  - [ ] Run soak test (48 hours)
  - [ ] Deploy to staging
  - [ ] Run load tests
  - [ ] Deploy to production (canary)
  - [ ] Monitor for 1 week
  - [ ] Full production rollout

---

# Priority #5: Input Validation & Sanitization

## P5: Current Problems

### Problem 1: No Depth Limits (DoS Risk) ⚠️ CRITICAL

**Location:** `src/pyvider/common/config.py:117-125`

**Current Code:**
```python
def get(self, key: str, default: Any = None) -> Any:
    key_parts = key.split(".")  # ⚠️ Could be 10,000 parts!
    value = self._config_data
    for part in key_parts:  # ⚠️ Stack overflow risk
        if isinstance(value, dict):
            value = value.get(part)
        else:
            value = None
            break
    return value if value is not None else default
```

**Attack Scenario:**
```python
# Attacker provides malicious config key:
key = "a." * 100000 + "value"  # 100,000 levels deep!
config.get(key)  # Stack overflow or infinite loop
```

**Impact:**
- DoS via stack overflow
- CPU exhaustion
- Memory exhaustion
- Service unavailability

---

### Problem 2: No Size Limits ⚠️ HIGH

**Location:** Multiple handlers (e.g., `call_function.py`)

**Current Code:**
```python
async def _call_function_impl(request: pb.CallFunction.Request, context: Any):
    # ⚠️ request.arguments could be gigabytes!
    # ⚠️ No validation before processing
    for arg in request.arguments:
        unmarshal(arg.value, ...)  # Could cause OOM
```

**Attack Scenario:**
```python
# Attacker sends massive payload:
arguments = [
    DynamicValue(msgpack=b"x" * 1_000_000_000)  # 1GB per argument
    for _ in range(100)  # 100GB total
]
```

**Impact:**
- Out of memory errors
- Service crash
- DoS attack
- Cloud cost inflation

---

### Problem 3: Log Injection Risk ⚠️ MEDIUM

**Current Code Pattern:**
```python
logger.error(f"Failed to process: {user_input}")  # ⚠️ Could inject ANSI codes
```

**Attack Scenario:**
```python
user_input = "\x1b[31mFAKE ERROR\x1b[0m\n\x1b[32mReal message"
# Logs show: colored "FAKE ERROR" followed by "Real message"
# Could hide real errors or inject fake ones
```

**Impact:**
- Log poisoning
- Security audit bypass
- Misleading debugging information
- Compliance violations

---

## P5: Solutions

### Solution 1: Validation Framework ✅

**New File:** `src/pyvider/common/validation.py`

**Key Features:**
- String length validation
- Collection size validation
- Nesting depth validation
- Pattern matching (safe characters)
- Log sanitization

**Implementation:**

```python
# src/pyvider/common/validation.py - NEW FILE

from dataclasses import dataclass
from typing import Any, Callable, Final
import re

from provide.foundation import logger
from pyvider.exceptions import ValidationError


@dataclass
class ValidationRule:
    """Validation rule with name and validator function."""
    name: str
    validator: Callable[[Any], bool]
    error_message: str


class InputValidator:
    """Enterprise-grade input validation."""

    # Security limits
    MAX_STRING_LENGTH: Final[int] = 1_000_000  # 1MB
    MAX_COLLECTION_SIZE: Final[int] = 10_000  # Items
    MAX_NESTING_DEPTH: Final[int] = 32  # Levels
    MAX_KEY_LENGTH: Final[int] = 256  # Config keys
    MAX_PATH_DEPTH: Final[int] = 10  # Nested config

    # Patterns
    SAFE_KEY_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')
    LOG_SAFE_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_\.,:;@/]+$')

    @classmethod
    def validate_string(
        cls,
        value: str,
        field_name: str,
        max_length: int | None = None,
        pattern: re.Pattern | None = None,
    ) -> str:
        """Validate and sanitize string input."""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string, got {type(value)}")

        # Length check
        max_len = max_length or cls.MAX_STRING_LENGTH
        if len(value) > max_len:
            raise ValidationError(
                f"{field_name} exceeds maximum length {max_len} "
                f"(got {len(value)} characters)"
            )

        # Pattern check
        if pattern and not pattern.match(value):
            raise ValidationError(
                f"{field_name} contains invalid characters "
                f"(must match pattern: {pattern.pattern})"
            )

        return value

    @classmethod
    def validate_collection(
        cls,
        value: list | dict | set,
        field_name: str,
        max_size: int | None = None,
    ) -> list | dict | set:
        """Validate collection size."""
        if not isinstance(value, (list, dict, set)):
            raise ValidationError(
                f"{field_name} must be a collection, got {type(value)}"
            )

        max_items = max_size or cls.MAX_COLLECTION_SIZE
        size = len(value)

        if size > max_items:
            raise ValidationError(
                f"{field_name} exceeds maximum size {max_items} "
                f"(got {size} items)"
            )

        return value

    @classmethod
    def validate_nesting_depth(
        cls,
        value: dict | list,
        field_name: str,
        max_depth: int | None = None,
    ) -> dict | list:
        """Validate nesting depth to prevent stack overflow."""
        max_levels = max_depth or cls.MAX_NESTING_DEPTH

        def check_depth(obj: Any, current_depth: int = 0) -> int:
            if current_depth > max_levels:
                raise ValidationError(
                    f"{field_name} exceeds maximum nesting depth {max_levels}"
                )

            if isinstance(obj, dict):
                if not obj:
                    return current_depth
                return max(
                    check_depth(v, current_depth + 1)
                    for v in obj.values()
                )
            elif isinstance(obj, list):
                if not obj:
                    return current_depth
                return max(
                    check_depth(item, current_depth + 1)
                    for item in obj
                )
            else:
                return current_depth

        actual_depth = check_depth(value)

        logger.debug(
            "Validated nesting depth",
            field=field_name,
            depth=actual_depth,
            max_allowed=max_levels,
        )

        return value

    @classmethod
    def sanitize_for_logging(cls, value: str, max_length: int = 200) -> str:
        """Sanitize string for safe logging (prevent injection)."""
        if not isinstance(value, str):
            value = str(value)

        # Truncate
        if len(value) > max_length:
            value = value[:max_length] + "...[truncated]"

        # Remove non-printable characters
        value = "".join(c if c.isprintable() else "?" for c in value)

        # Remove ANSI escape codes
        value = re.sub(r'\x1b\[[0-9;]*m', '', value)

        # Escape newlines and tabs
        value = value.replace('\n', '\\n').replace('\t', '\\t')

        return value

    @classmethod
    def validate_config_key(cls, key: str) -> str:
        """Validate configuration key format."""
        # Length check
        if len(key) > cls.MAX_KEY_LENGTH:
            raise ValidationError(
                f"Config key too long: {len(key)} > {cls.MAX_KEY_LENGTH}"
            )

        # Depth check
        parts = key.split(".")
        if len(parts) > cls.MAX_PATH_DEPTH:
            raise ValidationError(
                f"Config key too deeply nested: {len(parts)} > {cls.MAX_PATH_DEPTH}"
            )

        # Pattern check
        if not cls.SAFE_KEY_PATTERN.match(key):
            raise ValidationError(
                f"Config key contains invalid characters: {key!r}"
            )

        return key


# Add to src/pyvider/exceptions/__init__.py
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass
```

---

### Solution 2: Hardened Config with Validation ✅

**File:** `src/pyvider/common/config.py` (enhanced)

**Implementation:**

```python
from pyvider.common.validation import InputValidator, ValidationError

class PyviderConfig(BaseConfig):
    """Enhanced configuration with input validation."""

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value with validation."""

        # SECURITY: Validate key format
        try:
            key = InputValidator.validate_config_key(key)
        except ValidationError as e:
            logger.error("Invalid config key", key=key, error=str(e))
            return default

        logger.debug(f"⚙️  Config: Requesting key '{key}'")

        # First check if this is a typed field
        from attrs import fields

        for fld in fields(type(self)):
            if fld.name == key and not fld.name.startswith("_"):
                value = getattr(self, key)
                logger.debug(f"⚙️  Config: Found typed field '{key}'", value=value)
                return value

        # Fallback to legacy behavior for dynamic keys
        env_var_name = f"PYVIDER_{key.upper()}"
        if (env_val := get_env(env_var_name)) is not None:
            # SECURITY: Validate environment variable value
            if isinstance(env_val, str):
                try:
                    env_val = InputValidator.validate_string(
                        env_val,
                        field_name=env_var_name,
                        max_length=10_000,  # Reasonable limit
                    )
                except ValidationError as e:
                    logger.error("Invalid env var value", var=env_var_name, error=str(e))
                    return default

            logger.debug(
                f"⚙️  Config: Found value for '{key}' in environment variable",
                source=env_var_name,
                value=InputValidator.sanitize_for_logging(str(env_val)),
            )
            return env_val

        # TOML config keys are nested (e.g., logging.level)
        # SECURITY: Validate depth already checked in validate_config_key
        key_parts = key.split(".")
        value = self._config_data

        for part in key_parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break

        if value is not None:
            # SECURITY: Validate complex values
            if isinstance(value, dict):
                try:
                    InputValidator.validate_nesting_depth(value, f"config.{key}")
                except ValidationError as e:
                    logger.error("Config value too deeply nested", key=key, error=str(e))
                    return default

            logger.debug(
                f"⚙️  Config: Found value for '{key}' in config file",
                source=str(self._loaded_from_path),
                value=InputValidator.sanitize_for_logging(str(value)),
            )
            return value

        logger.debug(f"⚙️  Config: Using default value for '{key}'", default_value=default)
        return default
```

---

### Solution 3: Handler Input Validation ✅

**Files to Update:** All handler files in `src/pyvider/protocols/tfprotov6/handlers/`

**Example - call_function.py:**

```python
from pyvider.common.validation import InputValidator, ValidationError

async def _call_function_impl(
    request: pb.CallFunction.Request,
    context: Any,
) -> pb.CallFunction.Response:
    """Implementation with input validation."""
    response = pb.CallFunction.Response()

    try:
        # SECURITY: Validate input sizes
        if len(request.arguments) > InputValidator.MAX_COLLECTION_SIZE:
            raise ValidationError(
                f"Too many function arguments: {len(request.arguments)} > "
                f"{InputValidator.MAX_COLLECTION_SIZE}"
            )

        # SECURITY: Validate function name
        function_name = InputValidator.validate_string(
            request.name,
            field_name="function_name",
            max_length=256,
            pattern=InputValidator.SAFE_KEY_PATTERN,
        )

        # Get function from hub
        function_obj = hub.get_component("function", function_name)
        if not function_obj:
            raise ValueError(
                f"Function '{InputValidator.sanitize_for_logging(function_name)}' "
                f"not registered"
            )

        # SECURITY: Validate each argument size
        for idx, arg in enumerate(request.arguments):
            if len(arg.value.msgpack) > InputValidator.MAX_STRING_LENGTH:
                raise ValidationError(
                    f"Argument {idx} exceeds maximum size "
                    f"({len(arg.value.msgpack)} bytes)"
                )

        # Rest of implementation...

    except ValidationError as e:
        logger.error(
            "Input validation failed",
            function=InputValidator.sanitize_for_logging(request.name),
            error=str(e),
        )
        diag = pb.Diagnostic(
            severity=pb.Diagnostic.ERROR,
            summary="Invalid Input",
            detail=str(e),
        )
        response.diagnostics.append(diag)
    except Exception as e:
        # ... existing error handling
        pass

    return response
```

---

## P5: Implementation Checklist

### Phase 1: Validation Framework (Week 1)

- [ ] **Day 1: Create Validation Module**
  - [ ] Create `src/pyvider/common/validation.py`
  - [ ] Add `ValidationError` to exceptions
  - [ ] Implement `InputValidator` class
  - [ ] Add constants (MAX_STRING_LENGTH, etc.)
  - [ ] Add regex patterns

- [ ] **Day 2: Implement Validators**
  - [ ] Implement `validate_string()`
  - [ ] Implement `validate_collection()`
  - [ ] Implement `validate_nesting_depth()`
  - [ ] Implement `validate_config_key()`
  - [ ] Add unit tests

- [ ] **Day 3: Implement Sanitization**
  - [ ] Implement `sanitize_for_logging()`
  - [ ] Test with various injection attempts
  - [ ] Add fuzzing tests
  - [ ] Document safe usage patterns

- [ ] **Day 4-5: Testing**
  - [ ] Unit tests for all validators
  - [ ] Property-based tests with Hypothesis
  - [ ] Fuzzing with malicious inputs
  - [ ] Performance benchmarks

### Phase 2: Apply to Config Module (Week 2)

- [ ] **Day 1-2: Update PyviderConfig**
  - [ ] Add validation to `get()` method
  - [ ] Add validation to `__attrs_post_init__()`
  - [ ] Update all logging to use sanitization
  - [ ] Add tests

- [ ] **Day 3: Configuration Limits**
  - [ ] Add max file size for TOML config
  - [ ] Add max depth for nested config
  - [ ] Add validation for all typed fields
  - [ ] Document limits

- [ ] **Day 4-5: Testing & Validation**
  - [ ] Test with malicious config files
  - [ ] Test with deeply nested structures
  - [ ] Test with oversized configs
  - [ ] Verify no regressions

### Phase 3: Apply to Handlers (Week 3)

- [ ] **Handler Validation Rollout**
  - [ ] apply_resource_change.py
  - [ ] call_function.py
  - [ ] configure_provider.py
  - [ ] get_provider_schema.py
  - [ ] read_data_source.py
  - [ ] read_resource.py
  - [ ] plan_resource_change.py
  - [ ] validate_*_config.py handlers
  - [ ] All ephemeral handlers

- [ ] **Common Patterns**
  - [ ] Validate request sizes
  - [ ] Validate string fields
  - [ ] Validate collection sizes
  - [ ] Sanitize all logged user input
  - [ ] Add tests for each handler

### Phase 4: Monitoring & Rollout (Week 4)

- [ ] **Metrics & Monitoring**
  - [ ] Add validation failure metrics
  - [ ] Add validation performance metrics
  - [ ] Create alerting for validation failures
  - [ ] Create dashboard

- [ ] **Documentation**
  - [ ] Document validation limits
  - [ ] Create security guidelines
  - [ ] Update API docs
  - [ ] Create runbook for validation errors

- [ ] **Staged Rollout**
  - [ ] Deploy to dev
  - [ ] Security testing (pen test)
  - [ ] Deploy to staging
  - [ ] Load testing
  - [ ] Deploy to production (canary)
  - [ ] Monitor for 1 week
  - [ ] Full rollout

---

# Testing Strategy

## Priority #4 Testing

### Unit Tests
```python
# tests/common/test_encryption_cache.py

def test_cache_ttl_expiry():
    """Test that cache entries expire after TTL."""
    manager = EncryptionManager()
    salt = os.urandom(16)

    # Cache key
    key1 = manager._derive_key(salt)

    # Fast-forward time
    with patch('time.time', return_value=time.time() + 3700):
        key2 = manager._derive_key(salt)

    # Should have re-derived (different object)
    assert key2 == key1  # Same value
    assert manager._metrics["expirations"] == 1


def test_cache_lru_eviction():
    """Test LRU eviction at capacity."""
    manager = EncryptionManager()
    manager.MAX_CACHE_SIZE = 3

    salts = [os.urandom(16) for _ in range(5)]

    # Fill cache beyond capacity
    for salt in salts:
        manager._derive_key(salt)

    # First 2 should be evicted
    assert len(manager._key_cache) == 3
    assert manager._metrics["evictions"] == 2


def test_graceful_shutdown():
    """Test service graceful shutdown."""
    shutdown_event = asyncio.Event()

    async def test():
        async with ProtocolService(shutdown_event) as service:
            task = await service.start_heartbeat()
            await asyncio.sleep(0.1)

        # Should be cleaned up
        assert service._cleanup_done.is_set()

    asyncio.run(test())
```

### Load Tests
```python
# tests/load/test_encryption_performance.py

def test_cache_under_load():
    """Test cache performance under load."""
    manager = EncryptionManager()

    # 100,000 operations
    for _ in range(100_000):
        salt = os.urandom(16)
        manager._derive_key(salt)

    metrics = manager.get_metrics()

    # Should maintain size limit
    assert metrics["cache_size"] <= manager.MAX_CACHE_SIZE

    # Should have reasonable hit rate (>10% with random salts)
    assert float(metrics["hit_rate"].rstrip('%')) > 10.0
```

### Memory Tests
```python
# tests/load/test_memory_stability.py

def test_no_memory_leak():
    """Test that cache doesn't leak memory."""
    import tracemalloc

    tracemalloc.start()
    manager = EncryptionManager()

    # Baseline
    snapshot1 = tracemalloc.take_snapshot()

    # 1 million operations
    for _ in range(1_000_000):
        salt = os.urandom(16)
        manager._derive_key(salt)

    snapshot2 = tracemalloc.take_snapshot()

    # Should not grow beyond cache size * entry size
    max_expected = manager.MAX_CACHE_SIZE * 64  # bytes per entry

    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_growth = sum(stat.size_diff for stat in top_stats)

    assert total_growth < max_expected * 2  # 2x margin
```

---

## Priority #5 Testing

### Unit Tests
```python
# tests/common/test_validation.py

def test_string_length_validation():
    """Test string length limits."""
    # Valid
    InputValidator.validate_string("hello", "test", max_length=10)

    # Too long
    with pytest.raises(ValidationError):
        InputValidator.validate_string("x" * 1001, "test", max_length=1000)


def test_nesting_depth_validation():
    """Test nesting depth limits."""
    # Valid
    data = {"a": {"b": {"c": 1}}}
    InputValidator.validate_nesting_depth(data, "test", max_depth=5)

    # Too deep
    deep = {}
    current = deep
    for _ in range(100):
        current["level"] = {}
        current = current["level"]

    with pytest.raises(ValidationError):
        InputValidator.validate_nesting_depth(deep, "test", max_depth=32)


def test_log_sanitization():
    """Test log injection prevention."""
    malicious = "\x1b[31mFAKE\x1b[0m\nInjection"

    safe = InputValidator.sanitize_for_logging(malicious)

    assert "\x1b" not in safe  # No ANSI codes
    assert "\\n" in safe  # Newline escaped
```

### Fuzzing Tests
```python
# tests/security/test_fuzzing.py

from hypothesis import given, strategies as st

@given(st.text())
def test_string_validation_never_crashes(s):
    """Fuzz test: validation should never crash."""
    try:
        InputValidator.validate_string(s, "fuzz")
    except ValidationError:
        pass  # Expected


@given(st.recursive(
    st.none() | st.booleans() | st.integers() | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=1000,
))
def test_depth_validation_never_crashes(obj):
    """Fuzz test: depth validation should handle any structure."""
    try:
        if isinstance(obj, (dict, list)):
            InputValidator.validate_nesting_depth(obj, "fuzz")
    except ValidationError:
        pass  # Expected
```

### Security Tests
```python
# tests/security/test_dos_prevention.py

def test_config_key_dos_prevention():
    """Test that malicious config keys are rejected."""
    config = PyviderConfig()

    # Attempt DoS with deep nesting
    malicious_key = "a." * 10000 + "value"

    # Should reject, not crash
    result = config.get(malicious_key, default="safe")
    assert result == "safe"


def test_handler_size_dos_prevention():
    """Test that oversized requests are rejected."""
    request = pb.CallFunction.Request(
        name="test",
        arguments=[
            pb.DynamicValue(msgpack=b"x" * 10_000_000)  # 10MB
        ]
    )

    response = asyncio.run(_call_function_impl(request, None))

    # Should have validation error, not crash
    assert len(response.diagnostics) > 0
    assert "exceeds maximum size" in response.diagnostics[0].detail
```

---

# Rollout Plan

## Pre-Rollout Checklist

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Load tests completed
- [ ] Security tests completed
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Runbooks created
- [ ] Rollback plan documented

## Stage 1: Development (Week 1)

- [ ] Deploy to dev environment
- [ ] Run full test suite
- [ ] Manual testing
- [ ] Performance testing
- [ ] Fix any issues

## Stage 2: Staging (Week 2)

- [ ] Deploy to staging
- [ ] Run load tests (10x production traffic)
- [ ] Run security scans
- [ ] Penetration testing
- [ ] Soak test (48 hours)

## Stage 3: Canary (Week 3)

- [ ] Deploy to 5% of production
- [ ] Monitor metrics for 48 hours:
  - [ ] Error rates
  - [ ] Latency (p50, p95, p99)
  - [ ] Memory usage
  - [ ] Cache hit rates
  - [ ] Validation failure rates
- [ ] Verify no regressions
- [ ] Increase to 25%
- [ ] Monitor for 48 hours
- [ ] Increase to 50%

## Stage 4: Full Rollout (Week 4)

- [ ] Deploy to 100% of production
- [ ] Monitor for 1 week:
  - [ ] Daily metrics review
  - [ ] Weekly performance report
  - [ ] Security incident monitoring
- [ ] Declare success or rollback

## Rollback Criteria

Rollback immediately if:
- Error rate increases > 5%
- P99 latency increases > 50%
- Memory usage increases > 30%
- Any security incidents
- Cache hit rate < 50%

---

# Success Metrics

## Priority #4 Success Criteria

### Memory Metrics
- [ ] Cache size bounded to MAX_CACHE_SIZE (1,000 entries)
- [ ] Memory usage stable over 30 days
- [ ] No memory leaks detected
- [ ] Cache hit rate > 60%

### Performance Metrics
- [ ] P95 latency impact < 5%
- [ ] P99 latency impact < 10%
- [ ] Throughput unchanged
- [ ] CPU usage impact < 5%

### Reliability Metrics
- [ ] Zero resource leak incidents
- [ ] 100% graceful shutdowns
- [ ] Background task cleanup success rate = 100%
- [ ] Service restart time < 5 seconds

## Priority #5 Success Criteria

### Security Metrics
- [ ] Zero DoS incidents from input validation
- [ ] Zero log injection incidents
- [ ] 100% of requests validated
- [ ] Validation failure rate < 0.1%

### Performance Metrics
- [ ] Validation overhead < 1ms per request
- [ ] No impact on P95 latency
- [ ] Throughput unchanged

### Coverage Metrics
- [ ] 100% of handlers have validation
- [ ] 100% of user input sanitized in logs
- [ ] All config keys validated
- [ ] All collection sizes validated

---

# Appendix

## Configuration Reference

### Encryption Manager
```python
MAX_CACHE_SIZE = 1000         # Maximum cache entries
CACHE_TTL_SECONDS = 3600      # 1 hour
CLEANUP_INTERVAL = 300        # 5 minutes
```

### Service Manager
```python
MAX_QUEUE_SIZE = 10000        # Maximum queue size
HEARTBEAT_INTERVAL = 5        # Seconds
SHUTDOWN_TIMEOUT = 30         # Seconds
```

### Input Validator
```python
MAX_STRING_LENGTH = 1_000_000   # 1 MB
MAX_COLLECTION_SIZE = 10_000    # Items
MAX_NESTING_DEPTH = 32          # Levels
MAX_KEY_LENGTH = 256            # Characters
MAX_PATH_DEPTH = 10             # Nested levels
```

## Monitoring Dashboards

### Cache Performance
- Cache size over time
- Hit rate over time
- Eviction rate
- Expiration rate
- Memory usage

### Service Health
- Active background tasks
- Queue size over time
- Shutdown success rate
- Task cancellation success rate

### Validation Metrics
- Validation failures by type
- Validation latency
- Input size distribution
- Rejected request rate

---

**Document Version:** 1.0
**Last Updated:** 2025-10-22
**Next Review:** After Phase 1 completion

> What are the 7 most incredibly important things that I should address to make sure this is stable, and enterprise hardened? 

⏺ I'll analyze the codebase to identify the most critical stability and enterprise hardening concerns. Let me examine key areas:

⏺ Search(pattern: "TODO|FIXME|XXX|HACK|DEPRECATED", path: "src/pyvider", glob: "*.py", output_mode: "content")
  ⎿  Found 0 lines 

⏺ Read(src/pyvider/common/encryption.py)
  ⎿  Read 370 lines

⏺ Read(src/pyvider/cli/provide_command.py)
  ⎿  Read 224 lines

⏺ Search(pattern: "raise|except Exception", path: "src/pyvider", glob: "*.py", output_mode: "count")
  ⎿  Found 216 matches across 51 files (ctrl+o to expand)

⏺ Read(src/pyvider/server/__init__.py)
  ⎿  Error reading file

⏺ Search(pattern: "asyncio.create_task|background_task|spawn", path: "src/pyvider", glob: "*.py")
  ⎿  Found 1 file (ctrl+o to expand)

⏺ Read(src/pyvider/common/config.py)
  ⎿  Read 174 lines

⏺ Search(pattern: "secret|password|credential|token|key", path: "src/pyvider", glob: "*.py", output_mode: "count")
  ⎿  Found 259 matches across 23 files (ctrl+o to expand)

⏺ Search(pattern: "rate.?limit|throttle|backoff|retry", path: "src/pyvider", glob: "*.py", output_mode: "count")
  ⎿  Found 9 matches across 3 files (ctrl+o to expand)

⏺ Search(pattern: "close|cleanup|dispose|shutdown", path: "src/pyvider", glob: "*.py", output_mode: "count")
  ⎿  Found 72 matches across 13 files (ctrl+o to expand)

⏺ Search(pattern: "**/*metrics*.py", path: "src/pyvider")
  ⎿  Found 1 file (ctrl+o to expand)

⏺ Read(src/pyvider/observability/__init__.py)
  ⎿  Read 70 lines

⏺ Bash(find /Users/tim/code/gh/provide-io/pyvider -name "*.md" -type f | head -20)
  ⎿  /Users/tim/code/gh/provide-io/pyvider/FUTURE_PHASES.md               
     /Users/tim/code/gh/provide-io/pyvider/mutants/.pytest_cache/README.md
     /Users/tim/code/gh/provide-io/pyvider/.pytest_cache/README.md
     … +17 lines (ctrl+o to expand)

⏺ Read(pyproject.toml)
  ⎿  Read 100 lines

⏺ Search(pattern: "validate|sanitize|escape", path: "src/pyvider", glob: "*.py", output_mode: "count")
  ⎿  Found 221 matches across 29 files (ctrl+o to expand)

⏺ Based on my comprehensive analysis of the pyvider codebase, here are the 7 most critical areas you should address for enterprise hardening and stability:

  7 Critical Enterprise Hardening Priorities

  1. Test Coverage & Quality Assurance ⚠️ HIGHEST PRIORITY

  Current State: 54% coverage (4,049/10,115 missing statements)Risk: Production bugs, regression issues, unreliable deployments

  Critical Issues:
  - cli/provide_command.py: 14% coverage - Main entry point barely tested
  - common/config.py: 74% coverage - Configuration errors could be catastrophic
  - common/launch_context.py: 74% coverage - Initialization failures
  - Many handler exceptions paths untested (potential silent failures)

  Enterprise Impact:
  - Undetected bugs in production
  - Difficult rollbacks
  - Customer data at risk
  - Compliance failures

  Action Required:
  - Increase to 80%+ coverage (2,343 more statements)
  - Add integration tests for end-to-end provider flows
  - Implement contract tests for Terraform protocol compliance
  - Add chaos/fault injection testing

  ---
  2. Secrets & Encryption Key Management 🔐 CRITICAL SECURITY

  Current State: Good encryption implementation, but key lifecycle needs hardening

  Critical Gaps:
  # src/pyvider/common/encryption.py:132-148
  # Key rotation not implemented
  # Cache persists indefinitely
  # No key versioning beyond encryption format

  Enterprise Risks:
  - Key compromise: No rotation strategy
  - Memory leaks: Keys cached without expiry
  - Audit trail: No key usage logging
  - Compliance: GDPR/SOC2 require key rotation

  Action Required:
  - Implement automatic key rotation (30/90 day cycles)
  - Add key versioning and migration strategy
  - Integrate with enterprise secret managers (Vault, AWS Secrets Manager, Azure Key Vault)
  - Add audit logging for all key operations
  - Implement key expiry/TTL for cache
  - Add key backup and recovery procedures

  ---
  3. Resilience & Circuit Breaking 🔄 MISSING

  Current State: Minimal retry logic, no circuit breakers

  What's Missing:
  - No rate limiting on provider operations
  - No circuit breakers for external dependencies
  - Limited backoff strategies (only in hub/discovery.py)
  - No bulkhead patterns for resource isolation

  Enterprise Impact:
  - Cascade failures from single component
  - DDoS vulnerability in provider endpoints
  - No graceful degradation
  - Resource exhaustion under load

  Action Required:
  # Need to implement:
  from circuitbreaker import circuit
  from ratelimit import limits, sleep_and_retry

  @circuit(failure_threshold=5, recovery_timeout=60)
  @sleep_and_retry
  @limits(calls=100, period=60)
  async def resource_operation(...):
      # Protected operation

  - Add circuit breakers for all external calls
  - Implement rate limiting per resource type
  - Add exponential backoff with jitter
  - Set resource operation timeouts (currently missing)
  - Implement bulkhead pattern for resource pools

  ---
  4. Resource Lifecycle & Cleanup 💾 LEAK RISK

  Current State: Inconsistent cleanup patterns

  Critical Issues:
  - Encryption key cache grows unbounded (line encryption.py:144)
  - No automatic cleanup of stale connections
  - gRPC channels may not close properly
  - Background tasks (_heartbeat) lack cleanup hooks

  Observable Risks:
  # protocols/service.py:115-123
  async def _heartbeat(self) -> None:
      while self._stream_active:  # What stops this if stream crashes?
          try:
              await asyncio.sleep(5)
              if self._stream_active:
                  await self._message_queue.put(b"")
          except Exception as e:
              logger.error(f"Heartbeat error: {e}")
              break  # Good! But need cleanup here

  Enterprise Impact:
  - Memory leaks in long-running processes
  - File descriptor exhaustion
  - Connection pool exhaustion
  - Increased cloud costs

  Action Required:
  - Implement context managers for all resources
  - Add async cleanup hooks (__aenter__/__aexit__)
  - Set TTL on all caches
  - Add resource monitoring and alerts
  - Implement graceful shutdown protocol
  - Add health checks for resource state

  ---
  5. Input Validation & Sanitization 🛡️ SECURITY GAP

  Current State: Inconsistent validation, potential injection risks

  Critical Gaps:
  - Schema validation exists but not comprehensive
  - No input size limits (DoS risk)
  - Path traversal risks in file operations
  - No sanitization before logging (log injection)

  Example Vulnerabilities:
  # common/config.py:118-125
  # No validation on nested key depth - stack overflow risk
  key_parts = key.split(".")  # Unlimited depth!
  value = self._config_data
  for part in key_parts:  # Could be 10,000 parts
      if isinstance(value, dict):
          value = value.get(part)

  Enterprise Impact:
  - DoS via malformed inputs
  - Log injection attacks
  - Path traversal vulnerabilities
  - Schema validation bypass

  Action Required:
  - Add input size limits (max depth, max length)
  - Implement comprehensive schema validation
  - Sanitize all inputs before logging
  - Add path validation (no traversal)
  - Implement request signature verification
  - Add input fuzzing to test suite

  ---
  6. Observability & Monitoring 📊 OPERATIONAL RISK

  Current State: Good metrics foundation, but gaps in critical areas

  What's Missing:
  - No distributed tracing (OpenTelemetry)
  - No SLA/SLO monitoring
  - Limited error context in metrics
  - No performance profiling in production
  - Alert thresholds not defined

  Critical for Operations:
  # Need to add:
  - Request tracing across handler boundaries
  - Performance budgets (p95, p99 latency)
  - Error rate thresholds with alerting
  - Resource utilization metrics
  - Business metrics (operations/minute)
  - Audit logs for compliance

  Enterprise Impact:
  - Slow MTTR (Mean Time To Recovery)
  - No SLA enforcement
  - Difficult debugging in production
  - Compliance audit failures
  - No capacity planning data

  Action Required:
  - Integrate OpenTelemetry for distributed tracing
  - Add structured logging with correlation IDs
  - Define and monitor SLOs (99.9% uptime target)
  - Add performance profiling (continuous)
  - Implement audit logging for all state changes
  - Set up alerting with runbooks
  - Add business metrics dashboard

  ---
  7. Error Handling Consistency ⚡ RELIABILITY

  Current State: Mixed error handling patterns

  Inconsistencies Found:
  - Some handlers use @resilient() decorator, others don't
  - Inconsistent exception types (216 except Exception blocks)
  - Error context often lost in exception chains
  - No error budget tracking

