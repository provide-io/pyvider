# Quick Reference

This page provides quick lookup tables for common Pyvider APIs. For complete documentation, see the [API Reference](api/index.md).

## Schema Factory Functions

### Attribute Types

| Function | Type | Example |
|----------|------|---------|
| `a_str()` | String | `a_str(required=True, description="Name")` |
| `a_num()` | Number (int/float) | `a_num(default=8080, description="Port")` |
| `a_bool()` | Boolean | `a_bool(default=True, description="Enabled")` |
| `a_list(T)` | List of T | `a_list(a_str(), description="Tags")` |
| `a_map(T)` | Map of string → T | `a_map(a_str(), description="Labels")` |
| `a_set(T)` | Set of T | `a_set(a_str(), description="Unique IDs")` |
| `a_tuple([T...])` | Tuple (fixed types) | `a_tuple([a_str(), a_num()], description="Pair")` |
| `a_obj({...})` | Nested object | `a_obj({"port": a_num()}, description="Config")` |
| `a_dyn()` | Dynamic (any type) | `a_dyn(description="Metadata")` |
| `a_null()` | Null value | `a_null(description="Explicitly null")` |
| `a_unknown()` | Unknown (planning) | `a_unknown(description="Value unknown during plan")` |

### Attribute Modifiers

| Modifier | Purpose | Example |
|----------|---------|---------|
| `required=True` | User must provide value | `a_str(required=True)` |
| `default=value` | Default if not provided | `a_num(default=8080)` |
| `computed=True` | Provider calculates value | `a_str(computed=True)` |
| `sensitive=True` | Never show in logs/output | `a_str(sensitive=True)` |
| `description="..."` | User-facing documentation | `a_str(description="Server name")` |
| `validators=[...]` | Validation functions | `a_num(validators=[lambda x: x > 0 or "Must be positive"])` |

### Schema Builders

| Function | Use Case | Example |
|----------|----------|---------|
| `s_resource({...})` | Resource schema | `s_resource({"name": a_str(required=True)})` |
| `s_data_source({...})` | Data source schema | `s_data_source({"id": a_str(required=True)})` |
| `s_provider({...})` | Provider schema | `s_provider({"api_key": a_str(required=True)})` |

### Block Types

| Function | Nesting | Example |
|----------|---------|---------|
| `b_main({...})` | Top-level block | `b_main({"name": a_str()})` |
| `b_list("name", ...)` | 0 or more blocks | `b_list("rule", attributes={"port": a_num()})` |
| `b_set("name", ...)` | 0 or more (unordered) | `b_set("tag", attributes={"key": a_str()})` |
| `b_single("name", ...)` | 0 or 1 block | `b_single("config", attributes={"timeout": a_num()})` |
| `b_map("name", ...)` | Keyed blocks | `b_map("metadata", attributes={"value": a_str()})` |
| `b_group("name", ...)` | Grouped attributes | `b_group("advanced", attributes={"debug": a_bool()})` |

## Resource Lifecycle Methods

### Required Methods

All resources must implement these async methods:

```python
class MyResource(BaseResource):
    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define the resource schema."""
        return s_resource({...})

    async def read(
        self,
        ctx: ResourceContext
    ) -> State | None:
        """Read current resource state from infrastructure."""
        pass

    async def _create_apply(
        self,
        ctx: ResourceContext
    ) -> tuple[State | None, PrivateState | None]:
        """Create the resource."""
        pass

    async def _update_apply(
        self,
        ctx: ResourceContext
    ) -> tuple[State | None, PrivateState | None]:
        """Update the resource."""
        pass

    async def _delete_apply(
        self,
        ctx: ResourceContext
    ) -> None:
        """Delete the resource."""
        pass
```

### Context Object

The `ResourceContext` provides access to configuration and state:

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.config` | ConfigClass \| None | User configuration from Terraform |
| `ctx.state` | StateClass \| None | Previous state (for updates) |
| `ctx.planned_state` | StateClass \| None | Planned state from terraform plan |
| `ctx.private_state` | PrivateStateClass \| None | Encrypted private data |
| `ctx.is_field_unknown(name)` | bool | Check if field value is unknown (during plan) |

## Data Source Methods

```python
class MyDataSource(BaseDataSource):
    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define the data source schema."""
        return s_data_source({...})

    async def read(
        self,
        ctx: ResourceContext
    ) -> State | None:
        """Fetch data from external system."""
        pass
```

## Function Definition

```python
@register_function(name="my_function")
class MyFunction(BaseFunction):
    @classmethod
    def get_schema(cls) -> FunctionSchema:
        """Define function parameters and return type."""
        return FunctionSchema(
            parameters=[
                FunctionParameter(name="input", type=a_str()),
            ],
            return_type=a_str()
        )

    async def call(
        self,
        ctx: FunctionContext
    ) -> Any:
        """Execute the function logic."""
        pass
```

## Provider Definition

```python
@register_provider("my_provider")
class MyProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="my_provider",
                version="1.0.0",
                protocol_version="6"
            )
        )

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({...})

    async def configure(self, config: dict) -> None:
        """Configure the provider instance."""
        await super().configure(config)
        # Initialize clients, validate config, etc.
```

## Registration Decorators

| Decorator | Use Case |
|-----------|----------|
| `@register_provider("name")` | Register a provider |
| `@register_resource("name")` | Register a resource |
| `@register_data_source("name")` | Register a data source |
| `@register_function(name="name")` | Register a function |
| `@register_ephemeral_resource("name")` | Register an ephemeral resource |
| `@register_capability("name")` | Register a capability (experimental) |

## Common Validators

```python
# Length validation
a_str(validators=[
    lambda x: len(x) >= 3 or "Must be at least 3 characters"
])

# Numeric range
a_num(validators=[
    lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
])

# Regex pattern
a_str(validators=[
    lambda x: bool(re.match(r'^[a-z0-9-]+$', x)) or "Invalid format"
])

# Choice/enum
a_str(validators=[
    lambda x: x in ["small", "medium", "large"] or "Invalid size"
])
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `pyvider provide` | Start provider gRPC server (default when run by Terraform) |
| `pyvider components list` | List all discovered components |
| `pyvider components show TYPE NAME` | Show details for a specific component |
| `pyvider components diagnostics` | Show component discovery diagnostics |
| `pyvider config show` | Display current configuration |
| `pyvider install` | Install provider for Terraform use |
| `pyvider launch-context` | Show launch environment details |
| `pyvider --help` | Show all available commands |

## Common Patterns

### Simple String Resource

```python
@register_resource("example")
class Example(BaseResource):
    config_class = ExampleConfig
    state_class = ExampleState

    @classmethod
    def get_schema(cls):
        return s_resource({
            "name": a_str(required=True),
            "id": a_str(computed=True),
        })
```

### Resource with Validation

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "port": a_num(
            required=True,
            validators=[
                lambda x: 1 <= x <= 65535 or "Invalid port"
            ]
        ),
    })
```

### Resource with Sensitive Data

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "password": a_str(
            required=True,
            sensitive=True,
            description="Database password"
        ),
    })
```

### Data Source

```python
@register_data_source("example")
class Example(BaseDataSource):
    @classmethod
    def get_schema(cls):
        return s_data_source({
            "filter": a_str(required=True),
            "results": a_list(a_str(), computed=True),
        })

    async def read(self, ctx):
        results = await self.api.search(ctx.config.filter)
        return State(
            filter=ctx.config.filter,
            results=[r.name for r in results]
        )
```

## See Also

- [Complete API Reference](api/index.md)
- [Schema System](schema/overview.md)
- [Creating Resources Guide](guides/building-components/creating-resources.md)
- [Creating Providers Guide](guides/building-components/creating-providers.md)
- [pyvider-components Examples](https://github.com/provide-io/pyvider-components)
