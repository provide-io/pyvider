# How to Create a Resource

Quick reference for creating Terraform resources with pyvider. For a step-by-step learning tutorial, see [Building Your First Resource](../../tutorials/building-your-first-resource.md).

---

## Quick Steps

1. Define runtime types (config and state)
2. Create resource class with `@register_resource()`
3. Define schema with `get_schema()`
4. Implement lifecycle methods
5. Test with Terraform

---

## Minimal Example

```python
import attrs
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, PvsSchema
from pathlib import Path

@attrs.define
class FileConfig:
    path: str
    content: str

@attrs.define
class FileState:
    id: str
    path: str
    content: str

@register_resource("file")
class File(BaseResource):
    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "path": a_str(required=True),
            "content": a_str(required=True),
            "id": a_str(computed=True),
        })

    async def read(self, ctx: ResourceContext) -> FileState | None:
        if not ctx.state:
            return None
        file_path = Path(ctx.state.path)
        if not file_path.exists():
            return None
        return FileState(
            id=ctx.state.id,
            path=str(file_path),
            content=file_path.read_text(),
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        if not ctx.config:
            return None, None
        file_path = Path(ctx.config.path)
        file_path.write_text(ctx.config.content)
        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path),
            content=ctx.config.content,
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None
        Path(ctx.state.path).write_text(ctx.config.content)
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if ctx.state and Path(ctx.state.path).exists():
            Path(ctx.state.path).unlink()
```

---

## API Resource Example

For resources that manage remote API objects:

```python
import attrs
import httpx
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_bool, PvsSchema

@attrs.define
class ServerConfig:
    name: str
    enabled: bool = True

@attrs.define
class ServerState:
    id: str
    name: str
    enabled: bool
    status: str

@register_resource("server")
class Server(BaseResource):
    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "name": a_str(required=True, description="Server name"),
            "enabled": a_bool(default=True, description="Enabled status"),
            "id": a_str(computed=True, description="Server ID"),
            "status": a_str(computed=True, description="Server status"),
        })

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        if not ctx.state:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/servers/{ctx.state.id}")
            if response.status_code == 404:
                return None

            data = response.json()
            return ServerState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                status=data["status"],
            )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        if not ctx.config:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.example.com/servers",
                json={"name": ctx.config.name, "enabled": ctx.config.enabled}
            )
            data = response.json()

            return ServerState(
                id=data["id"],
                name=data["name"],
                enabled=data["enabled"],
                status=data["status"],
            ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"https://api.example.com/servers/{ctx.state.id}",
                json={"name": ctx.config.name, "enabled": ctx.config.enabled}
            )
            data = response.json()

            return ServerState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                status=data["status"],
            ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return

        async with httpx.AsyncClient() as client:
            await client.delete(f"https://api.example.com/servers/{ctx.state.id}")
```

---

## Required Methods

| Method | Purpose | Return Type |
|--------|---------|-------------|
| `read()` | Refresh state from remote system | `State \| None` |
| `_delete_apply()` | Delete the resource | `None` |

---

## Optional Methods

| Method | Purpose | Default Behavior |
|--------|---------|------------------|
| `_create_apply()` | Custom create logic | Uses `_update_apply()` |
| `_update_apply()` | Custom update logic | Uses generic update |
| `_validate_config()` | Validate configuration | No validation |

---

## ResourceContext API

The `ctx` parameter provides:

```python
async def _create_apply(self, ctx: ResourceContext):
    # Access configuration
    ctx.config          # Typed attrs instance (or None)
    ctx.config_cty      # Raw CTY value from Terraform

    # Access state
    ctx.state           # Current state (None during create)
    ctx.planned_state   # Planned state from plan phase

    # Check for unknown values
    if ctx.is_field_unknown("field_name"):
        pass  # Handle unknown value

    # Add diagnostics
    ctx.add_error("Error message")
    ctx.add_warning("Warning message")
```

---

## Common Patterns

### Handle Unknown Values

During planning, some values may be unknown:

```python
async def _create_apply(self, ctx: ResourceContext):
    if ctx.is_field_unknown("api_key"):
        # Can't create yet, return null state
        return None, None

    # Proceed with known values
    ...
```

### Return Private Data

Store sensitive data that shouldn't be in state:

```python
async def _create_apply(self, ctx: ResourceContext):
    api_key = generate_api_key()

    state = ServerState(id="123", name="server")
    private_data = {"api_key": api_key}

    return state, private_data
```

### Handle API Errors

```python
async def _create_apply(self, ctx: ResourceContext):
    try:
        response = await api.create(...)
    except APIError as e:
        ctx.add_error(f"Failed to create: {e}")
        return None, None

    return state, None
```

---

## See Also

- [Building Your First Resource](../../tutorials/building-your-first-resource.md) - Step-by-step tutorial
- [Add Validation](add-validation.md) - Validation patterns
- [Resource Lifecycle Reference](../../reference/resource-lifecycle.md) - Complete API docs
- [Testing Resources](../../guides/development/testing-providers.md) - Testing strategies
