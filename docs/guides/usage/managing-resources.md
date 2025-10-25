# Managing Resources

This guide covers how to effectively manage infrastructure resources using Pyvider providers, including lifecycle operations, state management, dependencies, and advanced patterns.

## Resource Lifecycle Overview

Pyvider resources implement a CRUD (Create, Read, Update, Delete) lifecycle that integrates with Terraform's plan-apply workflow.

### Lifecycle Methods

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext

@register_resource("server")
class Server(BaseResource):
    config_class = ServerConfig
    state_class = ServerState

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        """Create a new resource during terraform apply."""
        # Create infrastructure
        server = await create_server(ctx.config)
        return ServerState(...), None

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        """Refresh resource state during terraform plan/refresh."""
        # Fetch current state from infrastructure
        server = await get_server(ctx.state.id)
        return ServerState(...) if server else None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        """Update existing resource during terraform apply."""
        # Update infrastructure
        server = await update_server(ctx.state.id, ctx.config)
        return ServerState(...), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete resource during terraform destroy."""
        # Remove infrastructure
        await delete_server(ctx.state.id)
```

### Lifecycle Flow

```
terraform plan
├── read() - Refresh existing resources
└── _create_plan() / _update_plan() - Generate plan

terraform apply
├── _create_apply() - Create new resources
├── _update_apply() - Update changed resources
└── _delete_apply() - Delete removed resources

terraform destroy
└── _delete_apply() - Delete all resources
```

## State Management

### Resource State

State represents the current status of managed infrastructure:

```python
import attrs
from pyvider.schema import a_str, a_num, a_bool

@attrs.define
class ServerState:
    """Server resource state."""
    id: str                    # Required: unique identifier
    name: str                  # Configuration attribute
    size: str                  # Configuration attribute
    ip_address: str            # Computed attribute
    status: str                # Computed attribute
    created_at: str            # Computed attribute
```

**Key Principles:**
- Include resource ID (required)
- Store configuration values
- Store computed values that may change
- Avoid storing temporary or derivable data

### Accessing State

In lifecycle methods, access state via `ResourceContext`:

```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    """Read current resource state."""
    if not ctx.state:
        return None  # Resource doesn't exist yet

    # Access state attributes
    server_id = ctx.state.id
    current_name = ctx.state.name

    # Fetch fresh data from infrastructure
    server = await self.api.get_server(server_id)

    if not server:
        return None  # Resource was deleted outside Terraform

    return ServerState(
        id=server.id,
        name=server.name,
        size=server.size,
        ip_address=server.ip,
        status=server.status,
        created_at=server.created_at,
    )
```

### Handling Missing Resources

Resources may be deleted outside of Terraform. Handle gracefully:

```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    """Read resource with drift detection."""
    if not ctx.state:
        return None

    try:
        server = await self.api.get_server(ctx.state.id)
        return ServerState(...)
    except NotFoundError:
        # Resource deleted outside Terraform - return None to mark as deleted
        return None
    except APIError as e:
        # Transient error - raise to retry
        raise ResourceError(f"Failed to read server: {e}")
```

## Resource Configuration

Access desired configuration via `ResourceContext`:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Create resource from configuration."""
    if not ctx.config:
        return None, None

    # Access configuration
    name = ctx.config.name
    size = ctx.config.size
    tags = ctx.config.tags

    # Create resource
    server = await self.api.create_server(
        name=name,
        size=size,
        tags=tags,
    )

    return ServerState(
        id=server.id,
        name=server.name,
        size=server.size,
        ip_address=server.ip,
        status="creating",
        created_at=server.created_at,
    ), None
```

## Resource Dependencies

### Implicit Dependencies

Terraform automatically detects dependencies through attribute references:

```hcl
resource "mycloud_network" "main" {
  name = "main-network"
  cidr = "10.0.0.0/16"
}

resource "mycloud_server" "web" {
  name       = "web-server"
  network_id = mycloud_network.main.id  # Implicit dependency
}
```

Terraform creates `main` network before `web` server.

### Explicit Dependencies

Use `depends_on` for dependencies not expressed through attributes:

```hcl
resource "mycloud_server" "web" {
  name = "web-server"

  depends_on = [
    mycloud_firewall_rule.allow_http,
  ]
}
```

### Handling Dependencies in Code

When a resource depends on another, the dependency's state is available:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Create server with network dependency."""
    if not ctx.config:
        return None, None

    # network_id will be populated from referenced resource
    network_id = ctx.config.network_id

    if not network_id:
        raise ResourceError("network_id is required")

    server = await self.api.create_server(
        name=ctx.config.name,
        network_id=network_id,  # Use dependency's output
    )

    return ServerState(...), None
```

## Resource Import

Import existing infrastructure into Terraform management:

### Implementing Import

```python
async def import_state(self, resource_id: str) -> ServerState | None:
    """Import existing server into Terraform state."""
    try:
        server = await self.api.get_server(resource_id)
    except NotFoundError:
        raise ResourceError(f"Server {resource_id} not found")

    return ServerState(
        id=server.id,
        name=server.name,
        size=server.size,
        ip_address=server.ip,
        status=server.status,
        created_at=server.created_at,
    )
```

### Using Import

```bash
# Import existing server
terraform import mycloud_server.web server-12345

# Verify import
terraform plan
```

After import, add corresponding configuration:

```hcl
resource "mycloud_server" "web" {
  name = "web-server"  # Must match imported resource
  size = "small"
}
```

## Resource Updates

### Detecting Changes

Terraform compares configuration with state to detect changes:

```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Update resource with changed configuration."""
    if not ctx.config or not ctx.state:
        return None, None

    # Detect which attributes changed
    updates = {}

    if ctx.config.name != ctx.state.name:
        updates["name"] = ctx.config.name

    if ctx.config.tags != ctx.state.tags:
        updates["tags"] = ctx.config.tags

    # Apply updates
    if updates:
        server = await self.api.update_server(ctx.state.id, **updates)
    else:
        # No changes needed
        server = await self.api.get_server(ctx.state.id)

    return ServerState(...), None
```

### Force Replacement

Some changes require resource replacement (destroy + recreate). Define in schema:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(
            required=True,
            description="Server name (forces replacement if changed)"
        ),
        "size": a_str(
            required=True,
            description="Server size (forces replacement if changed)"
        ),
        "tags": a_map(a_str(), description="Tags (can be updated in-place)"),
    })
```

By default, changing any required attribute triggers replacement. To allow in-place updates, implement `_update_apply()` appropriately.

### In-Place vs Replace

**In-Place Update:**
- Modifiable attributes (tags, labels, etc.)
- No service disruption
- Implemented in `_update_apply()`

**Force Replace:**
- Immutable attributes (name, size, region, etc.)
- Resource destroyed then recreated
- Specify in schema or raise error in `_update_apply()`

```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Update with replacement detection."""
    if not ctx.config or not ctx.state:
        return None, None

    # Check for attributes that require replacement
    if ctx.config.size != ctx.state.size:
        raise ResourceError(
            "Server size cannot be changed in-place. "
            "Terraform will destroy and recreate the resource."
        )

    # Handle in-place updates
    # ... update logic ...
```

## Resource Drift Detection

Drift occurs when infrastructure changes outside Terraform:

### Detecting Drift

```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    """Detect configuration drift."""
    if not ctx.state:
        return None

    # Fetch current infrastructure state
    server = await self.api.get_server(ctx.state.id)

    if not server:
        return None  # Resource deleted - Terraform will recreate

    # Return current state - Terraform compares with config
    return ServerState(
        id=server.id,
        name=server.name,        # May differ from config
        size=server.size,        # May differ from config
        ip_address=server.ip,    # Computed, OK to change
        status=server.status,    # Computed, OK to change
        created_at=server.created_at,
    )
```

### Handling Drift

```bash
# Detect drift
terraform plan
# Shows resources out of sync

# Correct drift (apply configuration)
terraform apply

# Or update configuration to match reality
# Edit .tf files then apply
```

## Resource Targeting

Target specific resources for operations:

```bash
# Apply only specific resource
terraform apply -target=mycloud_server.web

# Destroy specific resource
terraform destroy -target=mycloud_server.web

# Plan for specific resource
terraform plan -target=mycloud_server.web
```

**Use Cases:**
- Debugging specific resources
- Partial deployments
- Emergency fixes

**Warning:** Breaks dependency guarantees. Use sparingly.

## Advanced Patterns

### Conditional Resource Creation

```hcl
resource "mycloud_server" "optional" {
  count = var.create_server ? 1 : 0

  name = "optional-server"
  size = "small"
}
```

### Resource Lifecycle Customization

```hcl
resource "mycloud_server" "protected" {
  name = "production-server"

  lifecycle {
    prevent_destroy = true        # Prevent accidental deletion
    create_before_destroy = true  # Create replacement before destroying
    ignore_changes = [tags]       # Ignore tag drift
  }
}
```

### Dynamic Blocks

```hcl
resource "mycloud_server" "web" {
  name = "web-server"

  dynamic "disk" {
    for_each = var.additional_disks
    content {
      size = disk.value.size
      type = disk.value.type
    }
  }
}
```

## Resource Validation

Validate configuration before creating resources:

```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    """Validate server configuration."""
    errors = []

    # Validate name format
    if not config.name.isalnum():
        errors.append("Server name must be alphanumeric")

    # Validate size
    valid_sizes = ["small", "medium", "large"]
    if config.size not in valid_sizes:
        errors.append(f"Size must be one of: {', '.join(valid_sizes)}")

    # Validate disk size
    if config.disk_size < 10 or config.disk_size > 1000:
        errors.append("Disk size must be between 10 and 1000 GB")

    return errors
```

## Error Handling

Handle errors gracefully during resource operations:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Create server with error handling."""
    if not ctx.config:
        return None, None

    try:
        server = await self.api.create_server(
            name=ctx.config.name,
            size=ctx.config.size,
        )
    except QuotaExceededError as e:
        raise ResourceError(
            f"Cannot create server: quota exceeded. "
            f"Current: {e.current}, Limit: {e.limit}"
        )
    except APIError as e:
        raise ResourceError(f"Failed to create server: {e}")

    return ServerState(...), None
```

## Best Practices

### 1. Implement Complete Lifecycle

Implement all lifecycle methods:

```python
@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx): ...
    async def read(self, ctx): ...
    async def _update_apply(self, ctx): ...
    async def _delete_apply(self, ctx): ...
    async def import_state(self, resource_id): ...
```

### 2. Handle Missing Resources

Always check for resource existence:

```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    if not ctx.state:
        return None

    server = await self.api.get_server(ctx.state.id)
    return ServerState(...) if server else None
```

### 3. Use Descriptive State

Include all relevant state information:

```python
@attrs.define
class ServerState:
    id: str              # Unique identifier
    name: str            # User-provided config
    size: str            # User-provided config
    ip_address: str      # Computed by provider
    status: str          # Current resource status
    created_at: str      # Creation timestamp
```

### 4. Validate Early

Validate in `_validate_config()` before apply:

```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    errors = []
    if not config.name:
        errors.append("Server name is required")
    return errors
```

### 5. Provide Clear Errors

Give actionable error messages:

```python
raise ResourceError(
    f"Server '{ctx.config.name}' already exists. "
    f"Choose a different name or import the existing server with: "
    f"terraform import mycloud_server.{resource_name} {existing_id}"
)
```

### 6. Handle Async Operations

Some resources take time to provision:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    """Create server and wait for ready state."""
    server = await self.api.create_server(ctx.config.name)

    # Poll until ready
    while server.status != "running":
        await asyncio.sleep(5)
        server = await self.api.get_server(server.id)

        if server.status == "error":
            raise ResourceError(f"Server creation failed: {server.error}")

    return ServerState(...), None
```

## Common Issues

### Resource Already Exists

**Error:** Trying to create a resource that already exists

**Solution:** Implement idempotency or check existence:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    # Check if server already exists
    existing = await self.api.find_server_by_name(ctx.config.name)
    if existing:
        raise ResourceError(
            f"Server '{ctx.config.name}' already exists. "
            f"Import it with: terraform import mycloud_server.name {existing.id}"
        )

    server = await self.api.create_server(ctx.config.name)
    return ServerState(...), None
```

### Resource Not Found on Update

**Error:** Resource missing during update

**Solution:** Handle in `read()`:

```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    try:
        server = await self.api.get_server(ctx.state.id)
        return ServerState(...)
    except NotFoundError:
        return None  # Terraform will recreate
```

### Incomplete Deletion

**Error:** Resource partially deleted

**Solution:** Make deletion idempotent:

```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    if not ctx.state:
        return

    try:
        await self.api.delete_server(ctx.state.id)
    except NotFoundError:
        # Already deleted - success
        pass
    except APIError as e:
        raise ResourceError(f"Failed to delete server: {e}")
```

## See Also

- [Creating Resources](../building-components/creating-resources.md) - Detailed resource development guide
- [Best Practices](../production/best-practices.md) - Production patterns
- [Error Handling](../development/error-handling.md) - Error management strategies
- [Schema System](../../schema/overview.md) - Schema definition reference
- [Testing Providers](../development/testing-providers.md) - Resource testing strategies
