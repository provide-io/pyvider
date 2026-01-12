# Resources API

Base classes and utilities for creating Terraform resources with full CRUD lifecycle management.

## Overview

Resources in Pyvider represent manageable infrastructure components that Terraform can plan and apply through Pyvider's async lifecycle.

### Key Components

- **`BaseResource`** - Base class for all resources
- **`@register_resource`** - Decorator for resource registration
- **Resource Context** - Per-operation context with provider access
- **Private State** - Encrypted storage for sensitive data
- **Lifecycle Protocols** - Standard CRUD interfaces

### Lifecycle Methods

Resources interact with Terraform via a plan/apply cycle:
- `read(ctx: ResourceContext)` — refresh the latest state (called by Terraform refresh and after apply)
- `plan(ctx)` — framework-provided method that calls `_create/_update/_delete_plan` hooks to build a planned state
- `apply(ctx)` — framework-provided method that calls `_create_apply/_update_apply/_delete_apply` hooks to enact the plan

Resource authors typically override:
- `_create(ctx, base_plan)` / `_update(ctx, base_plan)` / `_delete_plan(ctx)` to shape the plan output
- `_create_apply(ctx)` / `_update_apply(ctx)` / `_delete_apply(ctx)` to perform real API calls and return final state/private state tuples

See `src/pyvider/resources/base.py` for the exact signatures.

## Usage Examples

### Basic Resource Implementation

```python
import attrs
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema


@attrs.define
class ServerConfig:
    """Resource configuration."""
    name: str
    size: str = "medium"


@attrs.define
class ServerState:
    """Resource state."""
    id: str
    name: str
    size: str
    status: str


@register_resource("server")
class Server(BaseResource):
    """Manages a server resource."""

    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # Config attributes
            "name": a_str(required=True, description="Server name"),
            "size": a_str(default="medium", description="Server size"),

            # Computed attributes
            "id": a_str(computed=True, description="Server ID"),
            "status": a_str(computed=True, description="Server status"),
        })

    async def _create_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[ServerState | None, None]:
        """Create a server."""
        # Get provider instance
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Create server via API
        server = await provider.api.create_server(
            name=ctx.config.name,
            size=ctx.config.size,
        )

        # Return state
        return ServerState(
            id=server.id,
            name=server.name,
            size=server.size,
            status=server.status,
        ), None

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        """Read current server state."""
        if not ctx.state:
            return None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        try:
            server = await provider.api.get_server(ctx.state.id)
            return ServerState(
                id=server.id,
                name=server.name,
                size=server.size,
                status=server.status,
            )
        except ResourceNotFoundError:
            return None  # Server was deleted

    async def _update_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[ServerState | None, None]:
        """Update a server."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        server = await provider.api.update_server(
            server_id=ctx.state.id,
            name=ctx.config.name,
            size=ctx.config.size,
        )

        return ServerState(
            id=server.id,
            name=server.name,
            size=server.size,
            status=server.status,
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete a server."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        await provider.api.delete_server(ctx.state.id)
```

### Resource with Private State

```python
@register_resource("database")
class Database(BaseResource):
    """Database with encrypted credentials in private state."""

    async def _create_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[State | None, dict | None]:
        """Create database with credentials."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        db = await provider.api.create_database(ctx.config)

        # Public state (visible in terraform.tfstate)
        state = State(
            id=db.id,
            endpoint=db.endpoint,
            port=db.port,
        )

        # Private state (encrypted, not in terraform.tfstate)
        private = {
            "master_password": db.master_password,
            "admin_token": db.admin_token,
        }

        return state, private

    async def _update_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[State | None, dict | None]:
        """Update with access to private state."""
        # Access private state
        current_password = ctx.private_state.get("master_password") if ctx.private_state else None

        # Update logic here
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        db = await provider.api.update_database(
            db_id=ctx.state.id,
            config=ctx.config,
        )

        # Return updated state and private state
        state = State(
            id=db.id,
            endpoint=db.endpoint,
            port=db.port,
        )

        # Keep or update private state
        private = ctx.private_state or {}

        return state, private
```

### Resource with Validation

```python
@register_resource("validated_resource")
class ValidatedResource(BaseResource):
    """Resource with custom validation."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "name": a_str(
                required=True,
                validators=[
                    lambda x: len(x) >= 3 or "Name too short",
                    lambda x: len(x) <= 64 or "Name too long",
                    lambda x: x.isalnum() or "Name must be alphanumeric",
                ],
            ),
            "port": a_num(
                required=True,
                validators=[
                    lambda x: 1 <= x <= 65535 or "Invalid port number",
                ],
            ),
        })
```

### Resource with Import Support

```python
@register_resource("importable_resource")
class ImportableResource(BaseResource):
    """Resource that supports Terraform import."""

    async def import_resource(
        self,
        import_id: str,
    ) -> tuple[dict, None]:
        """Import existing resource by ID."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Fetch existing resource
        resource = await provider.api.get_resource(import_id)

        if not resource:
            raise ResourceNotFoundError(f"Resource {import_id} not found")

        # Return state as dict
        return {
            "id": resource.id,
            "name": resource.name,
            "status": resource.status,
        }, None
```

### Testing Resources

```python
import pytest
from pyvider.resources.context import ResourceContext


@pytest.mark.asyncio
async def test_server_create():
    """Test server creation."""
    server = Server()

    ctx = ResourceContext(
        config=ServerConfig(name="test-server", size="large")
    )

    state, private = await server._create_apply(ctx)

    assert state is not None
    assert state.name == "test-server"
    assert state.size == "large"
    assert state.id


@pytest.mark.asyncio
async def test_server_lifecycle():
    """Test full server lifecycle."""
    server = Server()

    # Create
    create_ctx = ResourceContext(
        config=ServerConfig(name="test-server")
    )
    state, _ = await server._create_apply(create_ctx)
    assert state.status == "running"

    # Read
    read_ctx = ResourceContext(state=state)
    read_state = await server.read(read_ctx)
    assert read_state.id == state.id

    # Update
    update_ctx = ResourceContext(
        config=ServerConfig(name="test-server", size="xlarge"),
        state=state,
    )
    updated_state, _ = await server._update_apply(update_ctx)
    assert updated_state.size == "xlarge"

    # Delete
    delete_ctx = ResourceContext(state=updated_state)
    await server._delete_apply(delete_ctx)
```

## Related Guides

- [Creating Resources](../guides/building-components/creating-resources.md) - Complete resource development guide
- [Best Practices](../guides/production/best-practices.md) - Resource best practices
- [Testing Providers](../guides/development/testing-providers.md) - Testing resources
- [Error Handling](../guides/development/error-handling.md) - Resource error handling
- [Security Best Practices](../guides/production/security-best-practices.md) - Secure resources

## Module Reference
