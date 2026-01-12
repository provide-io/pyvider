# Creating Resources

This guide shows you how to create resources for your Pyvider provider. Resources represent infrastructure components with full CRUD lifecycle management.

## What is a Resource?

A resource in Terraform is a managed infrastructure component with:
- **Configuration**: User-provided inputs
- **State**: Current state of the infrastructure
- **Lifecycle**: Create, read, update, delete operations

## Basic Resource Example

Here's a complete, working resource:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
import attrs

# Runtime configuration class (Python type safety)
@attrs.define
class FileConfig:
    path: str
    content: str
    mode: str = "644"

# Runtime state class (Python type safety)
@attrs.define
class FileState:
    id: str
    path: str
    content: str
    mode: str
    size: int

@register_resource("file")
class File(BaseResource):
    """Manages a local file."""

    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema."""
        return s_resource({
            # User inputs
            "path": a_str(required=True, description="File path"),
            "content": a_str(required=True, description="File content"),
            "mode": a_str(default="644", description="File mode"),

            # Provider outputs
            "id": a_str(computed=True, description="File ID"),
            "size": a_num(computed=True, description="File size in bytes"),
        })

    async def _validate_config(self, config: FileConfig) -> list[str]:
        """Validate configuration."""
        errors = []
        if ".." in config.path:
            errors.append("Path cannot contain '..'")
        return errors

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Refresh state from filesystem."""
        if not ctx.state:
            return None

        from pathlib import Path
        file_path = Path(ctx.state.path)

        if not file_path.exists():
            return None  # File deleted outside Terraform

        content = file_path.read_text()
        return FileState(
            id=ctx.state.id,
            path=str(file_path),
            content=content,
            mode=ctx.state.mode,
            size=len(content),
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Create file."""
        if not ctx.config:
            return None, None

        from pathlib import Path
        file_path = Path(ctx.config.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path),
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Update file."""
        if not ctx.config or not ctx.state:
            return None, None

        from pathlib import Path
        file_path = Path(ctx.state.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete file."""
        if not ctx.state:
            return

        from pathlib import Path
        file_path = Path(ctx.state.path)
        if file_path.exists():
            file_path.unlink()
```

## Resource Components

### 1. Schema Definition

Define what Terraform users see:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        # User inputs (required or with defaults)
        "name": a_str(required=True, description="Resource name"),
        "count": a_num(default=1, description="Instance count"),

        # Provider outputs (computed=True)
        "id": a_str(computed=True, description="Unique ID"),
        "status": a_str(computed=True, description="Current status"),
    })
```

### 2. Runtime Classes

Separate attrs classes for type safety:

```python
@attrs.define
class ServerConfig:
    """Configuration from user."""
    name: str
    count: int = 1

@attrs.define
class ServerState:
    """State managed by provider."""
    id: str
    name: str
    count: int
    status: str
```

### 3. Lifecycle Methods

Implement resource operations:

```python
# Required: Refresh state from remote system
async def read(self, ctx: ResourceContext) -> State | None:
    pass

# Required: Delete resource
async def _delete_apply(self, ctx: ResourceContext) -> None:
    pass

# Optional: Customize create behavior
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    pass

# Optional: Customize update behavior
async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    pass

# Optional: Validate configuration
async def _validate_config(self, config: ConfigType) -> list[str]:
    pass
```

## ResourceContext API

The `ResourceContext` object provides access to:

```python
async def _create_apply(self, ctx: ResourceContext):
    # Access configuration
    ctx.config          # Typed attrs instance (or None if unknown values)
    ctx.config_cty      # Raw CTY value from Terraform

    # Access state
    ctx.state           # Current state (None during create)
    ctx.planned_state   # Planned state from plan phase

    # Check for unknown values
    if ctx.is_field_unknown("field_name"):
        # Handle unknown value during planning
        pass

    # Add diagnostics
    ctx.add_error("Validation failed")
    ctx.add_warning("Deprecation notice")
```

## Complete Example: API Resource

Here's a resource that manages API objects:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_bool, a_map, PvsSchema
import attrs
import httpx

@attrs.define
class APIObjectConfig:
    name: str
    enabled: bool = True
    labels: dict[str, str] | None = None

@attrs.define
class APIObjectState:
    id: str
    name: str
    enabled: bool
    labels: dict[str, str]
    created_at: str

@register_resource("api_object")
class APIObject(BaseResource):
    """Manages an API object."""

    config_class = APIObjectConfig
    state_class = APIObjectState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "name": a_str(required=True, description="Object name"),
            "enabled": a_bool(default=True, description="Whether enabled"),
            "labels": a_map(a_str(), default={}, description="Labels"),

            "id": a_str(computed=True, description="Object ID"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
        })

    async def _validate_config(self, config: APIObjectConfig) -> list[str]:
        errors = []
        if len(config.name) < 3:
            errors.append("Name must be at least 3 characters")
        return errors

    async def read(self, ctx: ResourceContext) -> APIObjectState | None:
        if not ctx.state:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/objects/{ctx.state.id}")

            if response.status_code == 404:
                return None

            data = response.json()
            return APIObjectState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=ctx.state.created_at,
            )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[APIObjectState | None, None]:
        if not ctx.config:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.example.com/objects",
                json={
                    "name": ctx.config.name,
                    "enabled": ctx.config.enabled,
                    "labels": ctx.config.labels or {},
                }
            )
            data = response.json()

            return APIObjectState(
                id=data["id"],
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=data["created_at"],
            ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[APIObjectState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"https://api.example.com/objects/{ctx.state.id}",
                json={
                    "name": ctx.config.name,
                    "enabled": ctx.config.enabled,
                    "labels": ctx.config.labels or {},
                }
            )
            data = response.json()

            return APIObjectState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=ctx.state.created_at,
            ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return

        async with httpx.AsyncClient() as client:
            await client.delete(f"https://api.example.com/objects/{ctx.state.id}")
```

## Best Practices

1. **Always validate configuration** in `_validate_config()`
2. **Handle missing resources** in `read()` by returning `None`
3. **Use computed attributes** for provider-generated values
4. **Separate concerns**: Schema (Terraform) vs Runtime (Python)
5. **Add error handling** for API failures
6. **Use type hints** for better IDE support

## See Also

- [Schema System](../../explanation/schema-system.md) - Understanding schemas
- [Resource Context](../../api/resources.md) - ResourceContext API reference
- [Testing Resources](../development/testing-providers.md) - Testing strategies
- [Best Practices](../production/best-practices.md) - Production patterns
