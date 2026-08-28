# Resource Lifecycle API Reference

Complete API reference for resource lifecycle methods and the ResourceContext object.

---

## Base Resource Class

```python
from pyvider.resources import BaseResource
```

### Class Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `config_class` | `Type[attrs.define]` | Yes | Configuration attrs class |
| `state_class` | `Type[attrs.define]` | Yes | State attrs class |

---

## Lifecycle Methods

### Required Methods

#### `read()`

```python
async def read(self, ctx: ResourceContext) -> StateType | None:
    """Refresh state from remote system."""
```

**Purpose:** Check if the resource still exists and return its current state.

**Parameters:**
- `ctx`: ResourceContext with current state

**Returns:**
- `StateType`: Current state if resource exists
- `None`: Resource no longer exists (deleted outside Terraform)

**When Called:** During `terraform plan` and `terraform refresh`

**Example:**
```python
async def read(self, ctx: ResourceContext) -> ServerState | None:
    if not ctx.state:
        return None

    try:
        server = await api.get_server(ctx.state.id)
        return ServerState(
            id=server["id"],
            name=server["name"],
            status=server["status"],
        )
    except NotFoundError:
        return None  # Server deleted
```

---

#### `_delete_apply()`

```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    """Delete the resource."""
```

**Purpose:** Remove the resource from the remote system.

**Parameters:**
- `ctx`: ResourceContext with current state

**Returns:** `None`

**When Called:** During `terraform destroy` or when resource removed from config

**Example:**
```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    if not ctx.state:
        return

    await api.delete_server(ctx.state.id)
```

---

### Optional Methods

#### `_create_apply()`

```python
async def _create_apply(
    self,
    ctx: ResourceContext
) -> tuple[StateType | None, PrivateData | None]:
    """Create the resource."""
```

**Purpose:** Create a new resource.

**Parameters:**
- `ctx`: ResourceContext with configuration

**Returns:**
- Tuple of `(state, private_data)`
  - `state`: New state to track
  - `private_data`: Sensitive data (not in state file)

**When Called:** During `terraform apply` when creating new resource

**Default Behavior:** Calls `_update_apply()` if not overridden

**Example:**
```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    if not ctx.config:
        return None, None

    server = await api.create_server(
        name=ctx.config.name,
        size=ctx.config.size,
    )

    return ServerState(
        id=server["id"],
        name=server["name"],
        size=server["size"],
        status=server["status"],
    ), None
```

---

#### `_update_apply()`

```python
async def _update_apply(
    self,
    ctx: ResourceContext
) -> tuple[StateType | None, PrivateData | None]:
    """Update the resource."""
```

**Purpose:** Modify an existing resource.

**Parameters:**
- `ctx`: ResourceContext with configuration and current state

**Returns:**
- Tuple of `(state, private_data)`
  - `state`: Updated state
  - `private_data`: Sensitive data (not in state file)

**When Called:** During `terraform apply` when updating existing resource

**Example:**
```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
    if not ctx.config or not ctx.state:
        return None, None

    server = await api.update_server(
        id=ctx.state.id,
        name=ctx.config.name,
        size=ctx.config.size,
    )

    return ServerState(
        id=ctx.state.id,
        name=server["name"],
        size=server["size"],
        status=server["status"],
    ), None
```

---

#### `_validate_config()`

```python
async def _validate_config(self, config: ConfigType) -> list[str]:
    """Validate configuration."""
```

**Purpose:** Validate user configuration before applying.

**Parameters:**
- `config`: Typed configuration object

**Returns:**
- List of error messages (empty list = valid)

**When Called:** During `terraform plan` and `terraform apply`

**Example:**
```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    errors = []

    if len(config.name) < 3:
        errors.append("Name must be at least 3 characters")

    if config.size not in ["small", "medium", "large"]:
        errors.append("Size must be small, medium, or large")

    return errors
```

---

## ResourceContext API

### Properties

#### `config`

```python
ctx.config: ConfigType | None
```

Typed configuration attrs instance. `None` if configuration contains unknown values.

**Example:**
```python
if ctx.config:
    print(f"Server name: {ctx.config.name}")
```

---

#### `config_cty`

```python
ctx.config_cty: CtyValue
```

Raw CTY value from Terraform, always available even with unknown values.

**Example:**
```python
raw_value = ctx.config_cty
```

---

#### `state`

```python
ctx.state: StateType | None
```

Current state. `None` during create operations.

**Example:**
```python
if ctx.state:
    existing_id = ctx.state.id
```

---

#### `planned_state`

```python
ctx.planned_state: StateType | None
```

Planned state from plan phase.

**Example:**
```python
planned_name = ctx.planned_state.name if ctx.planned_state else None
```

---

### Methods

#### `is_field_unknown()`

```python
ctx.is_field_unknown(field_name: str) -> bool
```

Check if a configuration field has an unknown value (e.g., depends on another resource).

**Parameters:**
- `field_name`: Name of the configuration field

**Returns:** `True` if value is unknown

**Example:**
```python
if ctx.is_field_unknown("api_key"):
    # Can't create yet, api_key not known
    return None, None
```

---

#### `add_error()`

```python
ctx.add_error(message: str) -> None
```

Add an error diagnostic to show in Terraform output.

**Parameters:**
- `message`: Error message

**Example:**
```python
ctx.add_error("Failed to create server: API returned 500")
```

---

#### `add_warning()`

```python
ctx.add_warning(message: str) -> None
```

Add a warning diagnostic to show in Terraform output.

**Parameters:**
- `message`: Warning message

**Example:**
```python
ctx.add_warning("This configuration is deprecated, use new_config instead")
```

---

#### `require_replace()`

```python
ctx.require_replace(attribute_path: str) -> None
```

Force Terraform to destroy and recreate the resource instead of updating it in
place. Use this from `_update()` when replacement depends on the values
themselves; for "any change to this attribute forces replacement", prefer the
declarative `requires_replace=True` schema flag below.

**Parameters:**
- `attribute_path`: Attribute path that forces replacement, e.g. `"size_gb"` or `"disks[0].type"`. An empty or whitespace-only path raises `ValueError`, so a typo cannot masquerade as a working call. Surrounding whitespace is stripped, so `"  size_gb  "` records `"size_gb"` rather than a path that matches nothing.

**Notes:**
- Calling it during a create is a no-op: a resource with no prior state cannot be replaced.
- Repeated calls with the same path are de-duplicated.
- `_update()` is a plan-time hook, so it still runs on a plan that ends in
  replacement; it is the apply-time `_update_apply()` that Terraform skips in
  favour of `_delete_apply()` then `_create_apply()`.

**Example:**
```python
async def _update(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict, None]:
    if ctx.config.size_gb < ctx.state.size_gb:
        ctx.require_replace("size_gb")  # volumes cannot shrink
    return base_plan, None
```

---

## Schema Definition

### `get_schema()`

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    """Define Terraform schema."""
```

**Returns:** `PvsSchema` object defining the resource schema

**Example:**
```python
from pyvider.schema import s_resource, a_str, a_num, a_bool

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        # User inputs
        "name": a_str(required=True, description="Server name"),
        "size": a_str(default="small", description="Server size"),
        "enabled": a_bool(default=True, description="Enabled status"),

        # Provider outputs
        "id": a_str(computed=True, description="Server ID"),
        "status": a_str(computed=True, description="Server status"),
        "created_at": a_num(computed=True, description="Creation timestamp"),
    })
```

---

### Forcing Replacement (`requires_replace`)

Some attributes cannot be changed on an existing remote object. Mark them
`requires_replace=True` and Terraform plans a destroy-and-create whenever the
planned value differs from the value in state — the equivalent of the SDK's
`ForceNew` and the plugin framework's `RequiresReplace()` plan modifier.

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "region": a_str(required=True, requires_replace=True),  # servers can't move
        "name": a_str(required=True),                           # renaming is in-place
        "id": a_str(computed=True),
    })
```

**Behaviour:**
- Reported to Terraform in `PlanResourceChange.Response.requires_replace`. The
  plan-time `_update()` hook still runs — replacement paths are collected from
  its result — but Terraform then applies the change as a destroy-and-create, so
  the apply-time `_update_apply()` is never called; `_delete_apply()` and
  `_create_apply()` run instead.
- Never reported on create (no prior state) or on destroy (no planned state).
- A planned value that is still unknown counts as a change, since the plan has
  to be decided before the value is resolved.
- Not valid on a computed-only attribute — the practitioner cannot change what
  they cannot set, so a schema that does this raises `ValueError`. Use
  `optional=True, computed=True` if the attribute is both settable and computed.
- Not valid on a write-only attribute either. Terraform requires write-only
  values to be null in both prior and planned state, so the comparison would
  always see `null == null` and replacement would silently never fire;
  a schema that combines the two raises `ValueError`. Terraform's own SDK
  rejects the same pairing (`WriteOnly cannot be set with ForceNew`). To rotate
  a write-only secret, pair it with a companion attribute the practitioner
  bumps — conventionally `<name>_wo_version` — and put `requires_replace=True`
  on that, or call `ctx.require_replace()` from the plan hook.
- Only top-level attributes are compared. Inside a nested block or an
  object-typed attribute the flag is unreachable — an attribute inside a block
  has no stable path until Terraform matches the block's elements between prior
  and planned state — so a schema that sets it there raises `ValueError`.
  Promote the attribute to the top level, or state the path with
  `ctx.require_replace("disks[0].type")` from the plan hook, which knows which
  element changed.
- On `optional=True, computed=True`, replacement fires if the planned value is
  unknown. The normal path carries prior state forward, so the value stays known
  and nothing happens; but a plan hook that deliberately leaves the attribute
  unknown gets a replacement on every plan. Leave it unknown only when the
  attribute genuinely may change, or set it to the prior value when it will not.

For conditional replacement — replace only when a value shrinks, crosses a
boundary, or the remote API cannot perform the update — use
[`ctx.require_replace()`](#require_replace) from `_update()` instead.

---

## Type Signatures

### Configuration Class

```python
import attrs

@attrs.define
class ServerConfig:
    """User-provided configuration."""
    name: str
    size: str = "small"
    enabled: bool = True
```

### State Class

```python
import attrs

@attrs.define
class ServerState:
    """Provider-managed state."""
    id: str
    name: str
    size: str
    enabled: bool
    status: str
    created_at: int
```

---

## Private Data

Sensitive data that shouldn't be stored in state:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[State, dict]:
    server = await api.create_server(...)

    state = ServerState(
        id=server["id"],
        name=server["name"],
    )

    private_data = {
        "api_key": server["api_key"],  # Not in state
        "password": server["password"],  # Not in state
    }

    return state, private_data
```

**Access private data:**
```python
async def _update_apply(self, ctx: ResourceContext):
    if hasattr(ctx, "private"):
        api_key = ctx.private.get("api_key")
```

---

## Lifecycle Sequence

### Create Resource

1. User adds resource to Terraform config
2. `terraform plan`:
   - Calls `_validate_config()` with configuration
   - Calls `get_schema()` to validate schema
3. `terraform apply`:
   - Calls `_create_apply()` with ctx.config
   - Stores returned state

### Update Resource

1. User modifies resource in Terraform config
2. `terraform plan`:
   - Calls `read()` to get current state
   - Calls `_validate_config()` with new configuration
   - Compares current state with planned state
3. `terraform apply`:
   - Calls `_update_apply()` with ctx.config and ctx.state
   - Stores returned state

### Delete Resource

1. User removes resource from Terraform config
2. `terraform plan`:
   - Shows resource will be deleted
3. `terraform apply`:
   - Calls `_delete_apply()` with ctx.state
   - Removes resource from state

### Refresh State

1. `terraform refresh` or `terraform plan`:
   - Calls `read()` with ctx.state
   - Updates state if changed
   - Removes from state if `read()` returns `None`

---

## See Also

- [Create a Resource](../how-to-guides/resources/create-resource.md) - How-to guide
- [Building Your First Resource](../tutorials/building-your-first-resource.md) - Tutorial
- [Add Validation](../how-to-guides/resources/add-validation.md) - Validation patterns
- [API Reference](../api/resources.md) - Auto-generated API docs
