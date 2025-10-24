# Best Practices for Provider Development

This guide provides comprehensive best practices for developing production-ready Pyvider providers. These patterns are derived from real-world usage and the battle-tested [pyvider-components](https://github.com/provide-io/pyvider-components) repository.

## Provider Design Patterns

### Single Responsibility Principle

Keep each component focused on a single, well-defined responsibility:

```python
# Good: Focused resource
@register_resource("pyvider_file_content")
class FileContentResource(BaseResource):
    """Manages file content with atomic writes."""
    pass

# Bad: Resource doing too much
@register_resource("pyvider_file_manager")
class FileManager(BaseResource):
    """Manages files, directories, permissions, and backups."""  # Too much!
    pass
```

### Component Selection

Choose the right component type for your use case:

| Component | Use When | Example |
|-----------|----------|---------|
| **Resource** | Managing infrastructure with lifecycle (CRUD) | file_content, local_directory |
| **Data Source** | Reading existing data | env_variables, file_info, http_api |
| **Function** | Stateless transformations | string formatting, jq queries |
| **Ephemeral** | Short-lived resources (sessions, tokens) | timed_token, database_connection |

### Naming Conventions

Follow consistent naming patterns:

```python
# Good naming
@register_resource("pyvider_file_content")  # prefix_noun
@register_data_source("pyvider_env_variables")  # prefix_noun_plural
@register_function(name="format_string")  # verb_noun

# Bad naming
@register_resource("pyvider_manage_file")  # don't use verbs for resources
@register_data_source("pyvider_api")  # too generic
```

### Provider Configuration Design

Keep provider configuration simple and focused:

```python
@define(frozen=True)
class ProviderConfig:
    # Core settings only
    api_endpoint: str = field(default="https://api.example.com")
    api_key: str = field(metadata={"sensitive": True})
    timeout: int = field(default=30)

    # Avoid: Complex nested structures, business logic
```

## Schema Design Best Practices

### Use Descriptive Names and Documentation

```python
# Good: Clear, documented schema
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "filename": a_str(
            required=True,
            description="Path to the file to manage"
        ),
        "content": a_str(
            required=True,
            description="Content to write to the file"
        ),
        "content_hash": a_str(
            computed=True,
            description="SHA256 hash of the file content"
        ),
        "exists": a_bool(
            computed=True,
            description="Whether the file exists on disk"
        ),
    })

# Bad: No descriptions, unclear names
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "f": a_str(required=True),  # What is 'f'?
        "c": a_str(required=True),  # What is 'c'?
        "h": a_str(computed=True),  # No context
    })
```

### Mark Computed Attributes Correctly

```python
# Computed attributes are calculated by the provider
"content_hash": a_str(computed=True)  # Provider calculates
"exists": a_bool(computed=True)  # Provider determines

# Required/optional attributes come from user
"filename": a_str(required=True)  # User must provide
"permissions": a_str(default="644")  # User can override
```

### Use Validators

```python
from pyvider.schema import a_str, a_num

# Validate inputs to prevent errors
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "port": a_num(
            required=True,
            validators=[
                lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
            ]
        ),
        "protocol": a_str(
            required=True,
            validators=[
                lambda x: x in ["http", "https"] or "Must be http or https"
            ]
        ),
    })
```

### Keep Schemas Simple

```python
# Good: Flat, focused schema
{
    "name": a_str(required=True),
    "size": a_num(default=10),
    "enabled": a_bool(default=True),
}

# Avoid: Deeply nested complexity without good reason
{
    "config": a_obj({
        "section1": a_obj({
            "subsection": a_obj({
                "deep_value": a_str()  # Too deep
            })
        })
    })
}
```

## Resource Implementation Patterns

### Implement All CRUD Methods

All resources must implement the complete lifecycle:

```python
@register_resource("pyvider_example")
class ExampleResource(BaseResource):

    async def read(self, ctx: ResourceContext) -> ExampleState | None:
        """
        Read current state. Return None if resource doesn't exist.
        Called during refresh and before updates.
        """
        if not resource_exists:
            return None
        return ExampleState(...)

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
        """
        Create new resource. Return (state_dict, None).
        """
        # Create the resource
        result = await self.api.create(...)
        return {**base_plan, "id": result.id}, None

    async def _update(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
        """
        Update existing resource. Return (state_dict, None).
        """
        # Update the resource
        await self.api.update(ctx.state.id, ...)
        return base_plan, None

    async def _delete(self, ctx: ResourceContext) -> None:
        """
        Delete resource. No return value.
        """
        await self.api.delete(ctx.state.id)
```

### Use Async/Await Consistently

```python
# Good: All I/O is async
async def read(self, ctx: ResourceContext) -> State | None:
    content = await async_read_file(path)
    result = await self.api_client.get(url)
    return State(...)

# Bad: Blocking I/O
async def read(self, ctx: ResourceContext) -> State | None:
    content = open(path).read()  # Blocks!
    result = requests.get(url)  # Blocks!
    return State(...)
```

### Handle Missing Resources Gracefully

```python
async def read(self, ctx: ResourceContext) -> FileContentState | None:
    """Return None if resource doesn't exist."""
    filename = ctx.state.filename if ctx.state else ctx.config.filename
    path = Path(filename)

    # Don't raise errors for missing resources
    if not path.is_file():
        logger.debug("File does not exist", path=str(path))
        return None  # Terraform will handle this

    # Read and return state
    content = safe_read_text(path)
    return FileContentState(...)
```

### Ensure Idempotency

Operations should be safe to run multiple times:

```python
async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
    path = Path(base_plan["filename"])

    # Ensure parent directory exists (idempotent)
    ensure_dir(path.parent)

    # Atomic write (idempotent - overwrites if exists)
    atomic_write_text(path, base_plan["content"])

    # Calculate hash
    content_hash = hashlib.sha256(base_plan["content"].encode()).hexdigest()

    return {**base_plan, "content_hash": content_hash, "exists": True}, None
```

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
    resource_type=ctx.resource_type,
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
from pyvider.testing import ResourceTestCase

class TestFileContent(ResourceTestCase):
    resource_class = FileContentResource

    async def test_create_success(self):
        """Test successful file creation."""
        config = FileContentConfig(
            filename="/tmp/test.txt",
            content="Hello, world!"
        )

        state = await self.resource._create(self.make_context(config), {})

        assert state["exists"] is True
        assert state["content_hash"] is not None
        assert Path("/tmp/test.txt").read_text() == "Hello, world!"

    async def test_read_missing_file(self):
        """Test reading non-existent file returns None."""
        state = FileContentState(filename="/tmp/missing.txt", content="")
        ctx = self.make_context(state=state)

        result = await self.resource.read(ctx)

        assert result is None

    async def test_update_content(self):
        """Test updating file content."""
        # Setup: Create initial file
        initial_state = await self.resource._create(...)

        # Update content
        new_config = FileContentConfig(
            filename="/tmp/test.txt",
            content="Updated content"
        )
        updated_state = await self.resource._update(...)

        assert updated_state["content"] == "Updated content"
        assert updated_state["content_hash"] != initial_state["content_hash"]
```

### Test Error Conditions

```python
async def test_permission_denied(self):
    """Test handling of permission errors."""
    config = FileContentConfig(
        filename="/root/forbidden.txt",  # No permission
        content="test"
    )

    with pytest.raises(ResourceError) as exc_info:
        await self.resource._create(self.make_context(config), {})

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

For comprehensive testing guidance, see [Testing Providers](testing-providers.md).

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

## Type Safety

### Use Attrs Classes for Data Models

```python
from attrs import define, field

@define(frozen=True)  # Immutable
class FileContentConfig:
    """Configuration for file content resource."""
    filename: str = field()
    content: str = field()

    @filename.validator
    def _validate_filename(self, attribute, value):
        if not value:
            raise ValueError("filename cannot be empty")

@define(frozen=True)
class FileContentState:
    """State for file content resource."""
    filename: str = field()
    content: str = field()
    exists: bool | None = field(default=None)
    content_hash: str | None = field(default=None)
```

### Leverage Type Hints

```python
from typing import Any

class MyResource(BaseResource["my_resource", MyState, MyConfig]):
    config_class = MyConfig
    state_class = MyState

    async def read(self, ctx: ResourceContext) -> MyState | None:
        """Type hints help catch errors early."""
        result: MyState | None = await self._fetch_state()
        return result

    async def _create(
        self,
        ctx: ResourceContext,
        base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, bytes | None]:
        """Clear parameter and return types."""
        pass
```

### Use Type Checkers

```bash
# Run type checking in CI/CD
uv run mypy src/pyvider --strict
uv run pyright src/pyvider
```

## Code Organization

### Single Responsibility Per File

```
my_provider/
├── resources/
│   ├── __init__.py
│   ├── file_content.py      # One resource
│   └── local_directory.py   # One resource
├── data_sources/
│   ├── __init__.py
│   ├── env_variables.py     # One data source
│   └── file_info.py         # One data source
└── functions/
    ├── __init__.py
    └── string_utils.py      # Related functions
```

### Use Capabilities for Shared Logic

```python
# Instead of duplicating code across resources
from pyvider.capabilities import requires_capability

@register_resource("my_resource")
@requires_capability("caching")
class MyResource(BaseResource):

    async def read(self, ctx: ResourceContext) -> State | None:
        # Use shared caching capability
        cached = await self.capabilities.caching.get(cache_key)
        if cached:
            return cached

        result = await self._fetch_from_api()
        await self.capabilities.caching.set(cache_key, result)
        return result
```

## Documentation Standards

### Write Clear Docstrings

```python
@register_resource("pyvider_file_content")
class FileContentResource(BaseResource):
    """
    Manages file content with atomic writes and content tracking.

    This resource creates and manages text files on the local filesystem.
    It provides:
    - Atomic write operations to prevent partial writes
    - SHA256 content hashing for change detection
    - Automatic existence checking

    Example:
        resource "pyvider_file_content" "config" {
          filename = "/tmp/app.conf"
          content  = "key=value"
        }

    Attributes:
        filename: Path to the file (relative paths recommended)
        content: Text content to write
        exists: (computed) Whether file exists
        content_hash: (computed) SHA256 hash of content
    """

    async def read(self, ctx: ResourceContext) -> FileContentState | None:
        """
        Read current file state.

        Returns None if the file doesn't exist, triggering Terraform
        to recreate it. This is the correct behavior for resources
        deleted outside of Terraform.

        Args:
            ctx: Resource context with state and config

        Returns:
            Current file state or None if file doesn't exist
        """
        pass
```

### Reference Working Examples

```python
"""
File Content Resource

For working examples, see:
https://github.com/provide-io/pyvider-components/tree/main/examples/resource/file_content

Examples include:
- Basic file creation
- Template-based content
- Multi-line configuration files
- Environment-specific files
"""
```

## Common Pitfalls to Avoid

### Don't Block on I/O

```python
# Wrong: Blocking I/O in async function
async def read(self, ctx: ResourceContext) -> State | None:
    data = requests.get(url).json()  # Blocks entire event loop!
    return State(data=data)

# Correct: Use async I/O
async def read(self, ctx: ResourceContext) -> State | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return State(data=data)
```

### Don't Store State Outside Terraform

```python
# Wrong: External state storage
class MyResource(BaseResource):
    _cache = {}  # Class variable - BAD!

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
        result = await self.api.create()
        self._cache[result.id] = result  # State leak!
        return {...}, None

# Correct: State only in Terraform
class MyResource(BaseResource):

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
        result = await self.api.create()
        # Return all state, don't store locally
        return {
            "id": result.id,
            "data": result.data,
        }, None
```

### Don't Make Breaking Schema Changes

```python
# Wrong: Removing required attribute
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        # "filename": a_str(required=True),  # REMOVED - breaks existing configs!
        "path": a_str(required=True),  # NEW NAME - breaking change
    })

# Correct: Add new attribute, deprecate old one
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "filename": a_str(description="(Deprecated) Use 'path' instead"),
        "path": a_str(description="Path to the file"),
        # Support both, migrate users gradually
    })
```

### Don't Ignore Errors

```python
# Wrong: Swallowing errors
async def read(self, ctx: ResourceContext) -> State | None:
    try:
        return await self._read_from_api()
    except Exception:
        return None  # User never knows what went wrong

# Correct: Handle specific errors, re-raise unexpected ones
async def read(self, ctx: ResourceContext) -> State | None:
    try:
        return await self._read_from_api()
    except NotFoundError:
        # Expected - resource was deleted
        return None
    except Exception as e:
        # Unexpected - let it propagate with context
        logger.error("Unexpected error reading resource", error=str(e))
        raise
```

### Don't Mix Sync and Async

```python
# Wrong: Sync in async context
async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
    time.sleep(1)  # Blocks!
    result = self.sync_api_call()  # Blocks!
    return {...}, None

# Correct: Async all the way
async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, None]:
    await asyncio.sleep(1)  # Doesn't block
    result = await self.async_api_call()  # Doesn't block
    return {...}, None
```

## Related Documentation

- [Testing Providers](testing-providers.md) - Comprehensive testing strategies
- [Error Handling](error-handling.md) - Error handling patterns
- [Logging](logging.md) - Structured logging guide
- [Schema Best Practices](../schema/best-practices.md) - Schema-specific guidance
- [Creating Resources](creating-resources.md) - Resource implementation guide
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Production-ready examples

## Learn by Example

The best way to learn is by studying working code. Check out [pyvider-components](https://github.com/provide-io/pyvider-components) for:

- **Production-ready implementations**: file_content, local_directory, http_api, and more
- **100+ working examples**: Complete Terraform configurations
- **Comprehensive tests**: See how to test every scenario
- **Real-world patterns**: Learn from battle-tested code

---

**Remember**: The goal is to build providers that are reliable, secure, maintainable, and delightful to use. Follow these best practices, and your users will thank you!
