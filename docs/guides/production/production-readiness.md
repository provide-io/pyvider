# Production Readiness Guide

This guide covers operational concerns for building production-focused Pyvider providers, including error handling, logging, performance optimization, testing, and security.

For foundational design patterns and code organization, see [Best Practices](../production/best-practices.md).

## Table of Contents

- [Error Handling and Diagnostics](#error-handling-and-diagnostics)
- [Logging Best Practices](#logging-best-practices)
- [Performance Considerations](#performance-considerations)
- [Testing Strategy](#testing-strategy)
- [Security Practices](#security-practices)

---

## Error Handling and Diagnostics

### Use Structured Error Messages

```python
from pyvider.common.errors import ResourceError

# Good: Actionable error with context
async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
    try:
        await self.api.create_resource(...)
    except PermissionError as e:
        raise ResourceError(
            f"Permission denied writing to {base_plan['filename']}. "
            f"Ensure the Terraform process has write access.",
            details={"path": base_plan['filename'], "error": str(e)}
        )
    except QuotaExceededError as e:
        raise ResourceError(
            f"Quota exceeded: {e.limit} resources allowed, {e.current} in use. "
            f"Contact your administrator or upgrade your plan.",
            details={"limit": e.limit, "current": e.current}
        )

# Bad: Generic, unhelpful errors
async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
    try:
        await self.api.create_resource(...)
    except Exception as e:
        raise Exception("Error")  # No context, not actionable
```

### Use Resilient Decorator for Fault Tolerance

```python
from provide.foundation.errors import resilient

@resilient()  # Auto-retry with exponential backoff
async def read(self, ctx: ResourceContext) -> State | None:
    """Read with automatic retry on transient failures."""
    return await self.api.get_resource(ctx.state.id)

# For operations that shouldn't retry:
async def _delete(self, ctx: ResourceContext) -> None:
    """Delete without retry - we want immediate feedback."""
    await self.api.delete(ctx.state.id)
```

### Validate Early, Fail Fast

```python
async def _validate_config(self, config: FileContentConfig) -> list[str]:
    """Validate configuration before any operations."""
    errors = []

    # Check for absolute paths
    if config.filename.startswith("/"):
        errors.append("Absolute paths not allowed, use relative paths")

    # Check for parent directory traversal
    if ".." in config.filename:
        errors.append("Parent directory access (..) not allowed")

    # Check content size
    if len(config.content) > 10 * 1024 * 1024:  # 10MB
        errors.append("Content exceeds 10MB limit")

    return errors
```

## Logging Best Practices

### Use Structured Logging

```python
from provide.foundation import logger

# Good: Structured with context
logger.debug(
    "Read file content",
    filename=filename,
    content_length=len(content),
    content_hash=content_hash[:8],
    operation="read"
)

# Good: Log state transitions
logger.info(
    "Resource created successfully",
    resource_class=self.__class__.__name__,
    resource_id=result_id
)

# Bad: String concatenation, no context
logger.debug(f"Read file {filename} with {len(content)} bytes")
```

### Log at Appropriate Levels

```python
# DEBUG: Detailed information for debugging
logger.debug("File read operation started", path=str(path))

# INFO: Important state changes
logger.info("Resource created", resource_id=result.id)

# WARNING: Recoverable issues
logger.warning("Resource drift detected", expected=expected, actual=actual)

# ERROR: Failures requiring attention
logger.error("Failed to create resource", error=str(e))
```

### Never Log Sensitive Data

```python
# Good: Mask sensitive data
logger.debug("Authenticated with API key", key_prefix=api_key[:4] + "****")

# Bad: Logging secrets
logger.debug(f"API key: {api_key}")  # NEVER!

# Use sensitive=True in schema
@define(frozen=True)
class ProviderConfig:
    api_key: str = field(metadata={"sensitive": True})  # Won't be logged
```

## Performance Considerations

### Minimize API Calls

```python
# Good: Batch operations
async def _create_multiple(self, resources: list) -> list:
    return await self.api.batch_create(resources)

# Bad: Loop with individual calls
async def _create_multiple(self, resources: list) -> list:
    results = []
    for resource in resources:
        result = await self.api.create(resource)  # N API calls!
        results.append(result)
    return results
```

### Use Caching Appropriately

```python
from functools import lru_cache

class MyDataSource(BaseDataSource):

    @lru_cache(maxsize=128)
    def _parse_config_schema(self, schema_str: str) -> dict:
        """Cache expensive parsing operations."""
        return json.loads(schema_str)

    async def read(self, ctx: ResourceContext) -> State:
        # Use cached result if available
        parsed = self._parse_config_schema(config.schema)
        return State(...)
```

### Avoid Loading Large Files into Memory

```python
# Good: Stream large files
async def _process_large_file(self, path: Path) -> str:
    hash_obj = hashlib.sha256()
    async with aio.open(path, 'rb') as f:
        async for chunk in f:
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Bad: Load entire file
async def _process_large_file(self, path: Path) -> str:
    content = await path.read_bytes()  # Could be gigabytes!
    return hashlib.sha256(content).hexdigest()
```

### Use Connection Pooling

```python
import httpx

class MyProvider(BaseProvider):

    async def configure(self, config: ProviderConfig) -> None:
        # Good: Reusable async client with connection pooling
        self.http_client = httpx.AsyncClient(
            base_url=config.api_endpoint,
            timeout=config.timeout,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )

    async def cleanup(self) -> None:
        """Clean up resources on shutdown."""
        await self.http_client.aclose()
```

## Testing Strategy

### Write Comprehensive Unit Tests

```python
import pytest
from pathlib import Path
from pyvider.resources.context import ResourceContext
from my_provider.resources import FileContentResource, FileContentConfig, FileContentState

class TestFileContent:
    async def test_create_success(self):
        """Test successful file creation."""
        resource = FileContentResource()
        ctx = ResourceContext(
            config=FileContentConfig(filename="/tmp/test.txt", content="Hello, world!")
        )

        state, _ = await resource._create_apply(ctx)

        assert state.exists is True
        assert state.content_hash is not None
        assert Path("/tmp/test.txt").read_text() == "Hello, world!"

    async def test_read_missing_file(self):
        """Test reading non-existent file returns None."""
        resource = FileContentResource()
        ctx = ResourceContext(state=FileContentState(filename="/tmp/missing.txt", content=""))

        assert await resource.read(ctx) is None

    async def test_update_content(self):
        """Test updating file content."""
        resource = FileContentResource()
        initial_ctx = ResourceContext(
            config=FileContentConfig(filename="/tmp/test.txt", content="Hello")
        )
        state, _ = await resource._create_apply(initial_ctx)

        update_ctx = ResourceContext(
            config=FileContentConfig(filename="/tmp/test.txt", content="Updated content"),
            state=state,
            planned_state=state,
        )
        updated_state, _ = await resource._update_apply(update_ctx)

        assert updated_state.content == "Updated content"
        assert updated_state.content_hash != state.content_hash
```

### Test Error Conditions

```python
async def test_permission_denied(self):
    """Test handling of permission errors."""
    config = FileContentConfig(
        filename="/root/forbidden.txt",  # No permission
        content="test"
    )

    resource = FileContentResource()
    ctx = ResourceContext(config=config)
    with pytest.raises(ResourceError) as exc_info:
        await resource._create_apply(ctx)

    assert "Permission denied" in str(exc_info.value)
    assert "write access" in str(exc_info.value)

async def test_invalid_filename(self):
    """Test validation of invalid filenames."""
    config = FileContentConfig(
        filename="../etc/passwd",  # Path traversal attempt
        content="malicious"
    )

    errors = await self.resource._validate_config(config)
    assert len(errors) > 0
    assert any(".." in error for error in errors)
```

For comprehensive testing guidance, see [Testing Providers](../development/testing-providers.md).

## Security Practices

### Mark Sensitive Attributes

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "api_key": a_str(
            required=True,
            sensitive=True,  # Masked in logs and state files
            description="API authentication key"
        ),
        "password": a_str(
            required=True,
            sensitive=True,
            description="Database password"
        ),
    })
```

### Validate All User Inputs

```python
async def _validate_config(self, config: Config) -> list[str]:
    """Never trust user input - validate everything."""
    errors = []

    # Validate URL format
    if config.url:
        try:
            parsed = urlparse(config.url)
            if parsed.scheme not in ("http", "https"):
                errors.append("URL must use http or https scheme")
        except Exception:
            errors.append("Invalid URL format")

    # Validate file paths
    if hasattr(config, 'filename'):
        if os.path.isabs(config.filename):
            errors.append("Absolute paths not allowed")
        if ".." in config.filename:
            errors.append("Parent directory traversal not allowed")

    return errors
```

### Use Private State for Sensitive Data

```python
from pyvider.resources import PrivateState

class MyResource(BaseResource):

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, bytes | None]:
        # Create resource and get credentials
        result = await self.api.create_with_credentials(...)

        # Store sensitive data in encrypted private state
        private_data = {
            "access_token": result.access_token,
            "refresh_token": result.refresh_token,
            "secret_key": result.secret_key
        }
        encrypted_private_state = PrivateState.encrypt(private_data)

        # Return public state and encrypted private state
        public_state = {
            **base_plan,
            "id": result.id,
            "created_at": result.created_at
            # NO sensitive data here
        }

        return public_state, encrypted_private_state
```

### Use Secure File Operations

```python
from provide.foundation.file import atomic_write_text, safe_read_text, safe_delete

# Good: Atomic write prevents partial writes
atomic_write_text(path, content)

# Good: Safe read with error handling
content = safe_read_text(path, default="")

# Good: Safe delete checks existence first
safe_delete(path)

# Bad: Direct file operations
with open(path, 'w') as f:
    f.write(content)  # Not atomic, can fail mid-write
```

For comprehensive security guidance, see [Security Best Practices](../production/security-best-practices.md).

## Related Documentation

- [Best Practices](../production/best-practices.md) - Foundational design patterns
- [Testing Providers](../development/testing-providers.md) - Comprehensive testing strategies
- [Security Best Practices](../production/security-best-practices.md) - Detailed security guidance
- [Performance Optimization](../production/performance-optimization.md) - In-depth performance tuning
- [Error Handling](../development/error-handling.md) - Error handling patterns
- [Logging](../development/logging.md) - Structured logging guide
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Production-focused examples

## Learn by Example

The best way to learn is by studying working code. Check out [pyvider-components](https://github.com/provide-io/pyvider-components) for:

- **Production-focused implementations**: file_content, local_directory, http_api, and more
- **100+ working examples**: Complete Terraform configurations
- **Comprehensive tests**: See how to test every scenario
- **Real-world patterns**: Learn from battle-tested code

---

**Remember**: Production readiness is about reliability, security, and maintainability. Follow these practices to build providers users can trust!
