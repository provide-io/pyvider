# Best Practices for Provider Development

This guide provides foundational best practices for developing Pyvider providers, focusing on design patterns, code organization, and development standards. These patterns are derived from real-world usage and the battle-tested [pyvider-components](https://github.com/provide-io/pyvider-components) repository.

For operational concerns like error handling, logging, performance, testing, and security, see the [Production Readiness Guide](../production/production-readiness.md).

## Table of Contents

- [Provider Design Patterns](#provider-design-patterns)
- [Schema Design Best Practices](#schema-design-best-practices)
- [Resource Implementation Patterns](#resource-implementation-patterns)
- [Type Safety](#type-safety)
- [Code Organization](#code-organization)
- [Documentation Standards](#documentation-standards)
- [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)

---

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

- [Production Readiness Guide](../production/production-readiness.md) - Error handling, logging, performance, testing, and security
- [Creating Resources](../building-components/creating-resources.md) - Resource implementation guide
- [Schema Best Practices](../../schema/best-practices.md) - Schema-specific guidance
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Production-focused examples

## Learn by Example

The best way to learn is by studying working code. Check out [pyvider-components](https://github.com/provide-io/pyvider-components) for:

- **Production-focused implementations**: file_content, local_directory, http_api, and more
- **100+ working examples**: Complete Terraform configurations
- **Comprehensive tests**: See how to test every scenario
- **Real-world patterns**: Learn from battle-tested code

---

**Remember**: The goal is to build providers that are reliable, secure, maintainable, and delightful to use. Follow these best practices, and your users will thank you!
