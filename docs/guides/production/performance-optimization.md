# Performance Optimization

Building fast, efficient Terraform providers is essential for a good user experience. This guide covers performance optimization techniques for Pyvider providers.

## Table of Contents

- [Async Best Practices](#async-best-practices)
- [Caching Strategies](#caching-strategies)
- [Batching Operations](#batching-operations)
- [Connection Pooling](#connection-pooling)
- [Schema Optimization](#schema-optimization)
- [State Management](#state-management)
- [Profiling and Monitoring](#profiling-and-monitoring)
- [Common Performance Pitfalls](#common-performance-pitfalls)

---

## Async Best Practices

### Always Use Async for I/O

**Bad - Blocking I/O:**
```python
import requests  # Synchronous library

async def read(self, ctx: ResourceContext):
    # This BLOCKS the entire event loop!
    response = requests.get(f"{self.api_url}/resource/{ctx.state.id}")
    return State(...)
```

**Good - Non-blocking I/O:**
```python
import httpx  # Async library

async def read(self, ctx: ResourceContext):
    # Non-blocking, allows other operations to proceed
    response = await self.http_client.get(f"{self.api_url}/resource/{ctx.state.id}")
    return State(...)
```

### Parallelize Independent Operations

When operations don't depend on each other, run them concurrently:

**Bad - Sequential:**
```python
async def _create_apply(self, ctx: ResourceContext):
    # These run one after another (slow)
    network = await self.create_network(ctx.config.network)
    storage = await self.create_storage(ctx.config.storage)
    compute = await self.create_compute(ctx.config.compute)

    return State(...), None
```

**Good - Parallel:**
```python
import asyncio

async def _create_apply(self, ctx: ResourceContext):
    # These run concurrently (fast)
    network, storage, compute = await asyncio.gather(
        self.create_network(ctx.config.network),
        self.create_storage(ctx.config.storage),
        self.create_compute(ctx.config.compute),
    )

    return State(...), None
```

### Use asyncio.gather() Effectively

```python
async def read_multiple_resources(self, resource_ids: list[str]):
    """Read multiple resources in parallel."""
    # Create tasks for all reads
    tasks = [
        self.api.get_resource(resource_id)
        for resource_id in resource_ids
    ]

    # Execute in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle results
    resources = []
    for result in results:
        if isinstance(result, Exception):
            logger.warning("Resource read failed", error=str(result))
            continue
        resources.append(result)

    return resources
```

### Avoid Blocking Calls

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# If you MUST use a blocking library
executor = ThreadPoolExecutor(max_workers=4)

async def expensive_blocking_operation(self, data):
    """Run blocking operation in thread pool."""
    loop = asyncio.get_event_loop()

    # Run in separate thread to avoid blocking event loop
    result = await loop.run_in_executor(
        executor,
        self._blocking_function,
        data
    )

    return result

def _blocking_function(self, data):
    """Actual blocking operation."""
    # Blocking code here
    return processed_data
```

---

## Caching Strategies

### Cache Expensive Lookups

```python
from functools import lru_cache
from datetime import datetime, timedelta

class MyProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self._cache = {}
        self._cache_ttl = {}

    async def get_with_cache(
        self,
        key: str,
        fetcher: callable,
        ttl: int = 300
    ):
        """Get data with time-based caching."""
        now = datetime.now()

        # Check cache
        if key in self._cache:
            cached_at = self._cache_ttl.get(key)
            if cached_at and (now - cached_at).total_seconds() < ttl:
                logger.debug("Cache hit", key=key)
                return self._cache[key]

        # Fetch fresh data
        logger.debug("Cache miss", key=key)
        data = await fetcher()

        # Update cache
        self._cache[key] = data
        self._cache_ttl[key] = now

        return data

# Usage
async def read(self, ctx: ResourceContext):
    # Cache region data for 5 minutes
    region_info = await self.get_with_cache(
        key=f"region:{self.config.region}",
        fetcher=lambda: self.api.get_region_info(self.config.region),
        ttl=300
    )

    return State(...)
```

### Cache Provider Configuration

```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self._api_metadata_cache = None
        self._cache_expiry = None

    async def get_api_metadata(self):
        """Get API metadata with caching."""
        now = datetime.now()

        # Return cached if still valid
        if (self._api_metadata_cache and
            self._cache_expiry and
            now < self._cache_expiry):
            return self._api_metadata_cache

        # Fetch fresh metadata
        metadata = await self.api.get_metadata()

        # Cache for 1 hour
        self._api_metadata_cache = metadata
        self._cache_expiry = now + timedelta(hours=1)

        return metadata
```

### Invalidate Cache Appropriately

```python
class CacheManager:
    def __init__(self):
        self._cache = {}
        self._ttl = {}

    async def get(self, key: str, fetcher: callable, ttl: int = 300):
        """Get from cache or fetch."""
        now = datetime.now()

        if key in self._cache:
            if (now - self._ttl[key]).total_seconds() < ttl:
                return self._cache[key]

        data = await fetcher()
        self._cache[key] = data
        self._ttl[key] = now
        return data

    def invalidate(self, key: str):
        """Invalidate specific cache entry."""
        self._cache.pop(key, None)
        self._ttl.pop(key, None)

    def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern."""
        keys_to_remove = [
            key for key in self._cache.keys()
            if pattern in key
        ]
        for key in keys_to_remove:
            self.invalidate(key)

    def clear(self):
        """Clear entire cache."""
        self._cache.clear()
        self._ttl.clear()

# Usage
async def _update_apply(self, ctx: ResourceContext):
    result = await self.api.update_resource(ctx.state.id, ctx.config)

    # Invalidate cache for this resource
    self.cache_manager.invalidate(f"resource:{ctx.state.id}")

    return State(...), None
```

---

## Batching Operations

### Batch API Calls

**Bad - N+1 Query Problem:**
```python
async def read_all_servers(self, server_ids: list[str]):
    servers = []
    for server_id in server_ids:
        # Makes N API calls!
        server = await self.api.get_server(server_id)
        servers.append(server)
    return servers
```

**Good - Single Batch Call:**
```python
async def read_all_servers(self, server_ids: list[str]):
    # Single API call for all servers
    servers = await self.api.batch_get_servers(server_ids)
    return servers
```

### Implement Request Batching

```python
from collections import defaultdict
import asyncio

class BatchingProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self._pending_reads = defaultdict(list)
        self._batch_lock = asyncio.Lock()
        self._batch_delay = 0.1  # 100ms batching window

    async def get_resource_batched(self, resource_id: str):
        """Get resource with automatic batching."""
        # Create future for this request
        future = asyncio.Future()

        async with self._batch_lock:
            self._pending_reads[resource_id].append(future)

            # Schedule batch execution
            if len(self._pending_reads) == 1:
                asyncio.create_task(self._execute_batch())

        # Wait for result
        return await future

    async def _execute_batch(self):
        """Execute batched reads after delay."""
        # Wait for batch window
        await asyncio.sleep(self._batch_delay)

        async with self._batch_lock:
            if not self._pending_reads:
                return

            # Collect all IDs
            resource_ids = list(self._pending_reads.keys())
            futures_by_id = dict(self._pending_reads)

            # Clear pending
            self._pending_reads.clear()

        # Execute batch read
        try:
            results = await self.api.batch_get_resources(resource_ids)

            # Resolve futures
            for resource_id, result in results.items():
                for future in futures_by_id[resource_id]:
                    future.set_result(result)

        except Exception as e:
            # Reject all futures
            for futures in futures_by_id.values():
                for future in futures:
                    future.set_exception(e)
```

---

## Connection Pooling

### Reuse HTTP Connections

```python
import httpx

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        await super().configure(config)

        # Create connection pool
        self.http_client = httpx.AsyncClient(
            base_url=config["api_endpoint"],
            headers={"Authorization": f"Bearer {config['api_key']}"},
            timeout=30.0,
            # Connection pool settings
            limits=httpx.Limits(
                max_connections=100,      # Total connections
                max_keepalive_connections=20,  # Persistent connections
                keepalive_expiry=30.0,    # Keep-alive timeout
            ),
        )

    async def close(self) -> None:
        """Clean up connection pool."""
        if self.http_client:
            await self.http_client.aclose()
```

### Configure Pool Sizes Appropriately

```python
# For high-traffic providers
limits = httpx.Limits(
    max_connections=200,
    max_keepalive_connections=50,
)

# For low-traffic providers
limits = httpx.Limits(
    max_connections=20,
    max_keepalive_connections=5,
)
```

---

## Schema Optimization

### Lazy Schema Generation

```python
from functools import cached_property

@register_resource("server")
class Server(BaseResource):
    @classmethod
    @cached_property
    def _schema(cls) -> PvsSchema:
        """Cache schema - only computed once."""
        return s_resource({
            "name": a_str(required=True),
            "size": a_str(default="medium"),
            # ... large schema definition
        })

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return cls._schema
```

### Simplify Complex Schemas

**Bad - Over-complicated:**
```python
# Deeply nested with many validations
@classmethod
def get_schema(cls):
    return s_resource({
        "config": a_obj({
            "network": a_obj({
                "vpc": a_obj({
                    "subnets": a_list(a_obj({
                        "cidr": a_str(validators=[...]),
                        "az": a_str(validators=[...]),
                        # etc...
                    }))
                })
            })
        })
    })
```

**Good - Flattened when possible:**
```python
@classmethod
def get_schema(cls):
    return s_resource({
        "vpc_id": a_str(required=True),
        "subnet_ids": a_list(a_str()),
        "availability_zones": a_list(a_str()),
    })
```

---

## State Management

### Minimize State Size

```python
# Bad - Storing unnecessary data
@attrs.define
class ServerState:
    id: str
    full_config: dict  # Don't store entire config
    api_response: dict  # Don't store raw API response
    internal_metadata: dict  # Don't store internal data

# Good - Only essential data
@attrs.define
class ServerState:
    id: str
    name: str
    status: str
    public_ip: str
```

### Use Private State Sparingly

Private state requires encryption/decryption overhead:

```python
# Only use for truly sensitive data
async def _create_apply(self, ctx):
    # Public state - fast
    state = State(id="srv-123", status="running")

    # Private state - slower due to encryption
    # Only for sensitive data
    private = {
        "admin_password": "secret123",
        "internal_token": "tok_abc",
    } if ctx.config.store_credentials else None

    return state, private
```

---

## Profiling and Monitoring

### Use Structured Logging with Timing

```python
from provide.foundation import logger
import time

async def _create_apply(self, ctx: ResourceContext):
    start = time.time()

    try:
        result = await self.api.create_resource(ctx.config)

        # Log operation timing
        duration = time.time() - start
        logger.info(
            "Resource created successfully",
            duration_ms=duration * 1000,
            resource_id=result.id,
        )

        return State(...), None

    except Exception as e:
        duration = time.time() - start
        logger.error(
            "Resource creation failed",
            duration_ms=duration * 1000,
            error=str(e),
        )
        raise
```

### Profile with py-spy

```bash
# Install py-spy
uv tool install py-spy

# Profile running provider
py-spy top --pid $(pgrep -f terraform-provider-pyvider)

# Generate flame graph
py-spy record -o profile.svg --pid $(pgrep -f terraform-provider-pyvider)
```

### Use Context Managers for Timing

```python
from contextlib import asynccontextmanager
import time

@asynccontextmanager
async def timed_operation(operation_name: str):
    """Context manager for timing operations."""
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        logger.debug(
            f"{operation_name} completed",
            operation=operation_name,
            duration_ms=duration * 1000,
        )

# Usage
async def _create_apply(self, ctx):
    async with timed_operation("create_network"):
        network = await self.create_network(ctx.config.network)

    async with timed_operation("create_storage"):
        storage = await self.create_storage(ctx.config.storage)

    return State(...), None
```

---

## Common Performance Pitfalls

### 1. Synchronous I/O in Async Functions

**Problem:**
```python
async def read(self, ctx):
    import time
    time.sleep(5)  # BLOCKS EVERYTHING!
    return State(...)
```

**Solution:**
```python
import asyncio

async def read(self, ctx):
    await asyncio.sleep(5)  # Non-blocking
    return State(...)
```

### 2. Not Using Connection Pooling

**Problem:**
```python
async def _api_call(self):
    # Creates new connection every time
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

**Solution:**
```python
# Reuse client with connection pool (configured in provider)
async def _api_call(self):
    return await self.http_client.get(url)
```

### 3. Sequential When Could Be Parallel

**Problem:**
```python
async def validate_all(self, resources):
    results = []
    for resource in resources:
        result = await self.validate_resource(resource)
        results.append(result)
    return results
```

**Solution:**
```python
async def validate_all(self, resources):
    tasks = [self.validate_resource(r) for r in resources]
    return await asyncio.gather(*tasks)
```

### 4. Over-fetching Data

**Problem:**
```python
async def read(self, ctx):
    # Fetches entire object graph
    full_data = await self.api.get_resource_with_all_related(ctx.state.id)
    return State(id=full_data.id)  # Only uses ID!
```

**Solution:**
```python
async def read(self, ctx):
    # Only fetch what you need
    resource = await self.api.get_resource(ctx.state.id, fields=["id", "status"])
    return State(id=resource.id, status=resource.status)
```

### 5. Not Setting Timeouts

**Problem:**
```python
# No timeout - can hang forever
self.http_client = httpx.AsyncClient()
```

**Solution:**
```python
# Always set reasonable timeouts
self.http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,
        read=30.0,
        write=10.0,
        pool=5.0,
    )
)
```

---

## Performance Checklist

Before releasing your provider:

- [ ] All I/O operations use async/await
- [ ] No blocking calls (time.sleep, requests, etc.)
- [ ] Independent operations run in parallel (asyncio.gather)
- [ ] HTTP client connection pooling configured
- [ ] Expensive lookups are cached appropriately
- [ ] Batch operations when possible (no N+1 queries)
- [ ] Timeouts set on all network operations
- [ ] State kept minimal (only essential data)
- [ ] Schemas are cached/optimized
- [ ] Performance logging in place
- [ ] Profiled with realistic workload

---

## Benchmarking Example

```python
import asyncio
import time

async def benchmark_provider():
    """Benchmark provider operations."""
    provider = MyCloudProvider()
    await provider.configure({
        "api_endpoint": "https://api.example.com",
        "api_key": "test_key",
    })

    # Benchmark resource creation
    iterations = 100
    start = time.time()

    tasks = [
        create_test_resource(provider, i)
        for i in range(iterations)
    ]

    results = await asyncio.gather(*tasks)

    duration = time.time() - start
    ops_per_second = iterations / duration

    print(f"Created {iterations} resources in {duration:.2f}s")
    print(f"Throughput: {ops_per_second:.2f} ops/sec")

async def create_test_resource(provider, i):
    """Create a test resource."""
    config = ResourceConfig(name=f"test-{i}")
    state, _ = await provider.create_resource(config)
    return state
```

---

## Related Documentation

- [Architecture Overview](../../explanation/architecture.md) - System design
- [Async Patterns Guide](../advanced/advanced-patterns.md) - Advanced async usage
- [Best Practices](../production/best-practices.md) - General best practices
- [Logging Guide](../development/logging.md) - Performance logging
- [Testing Providers](../development/testing-providers.md) - Performance testing
