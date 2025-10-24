# Schema System

The Pyvider schema system provides a type-safe, declarative way to define the structure and constraints of your provider's resources, data sources, and provider configuration. It bridges Python and Terraform's type systems.

## Core Concepts

### What is a Schema?

A schema defines:

- **Structure**: What attributes and blocks your component has
- **Types**: What kind of data each attribute holds (string, number, list, etc.)
- **Constraints**: What values are valid (required, optional, validators)
- **Behavior**: How attributes work (computed, sensitive, default values)
- **Documentation**: Descriptions shown to users

### Factory Functions Approach

Pyvider uses **factory functions** (not classes or decorators) to build schemas:

```python
from pyvider.schema import (
    s_resource, s_data_source, s_provider,  # Schema factories
    a_str, a_num, a_bool,                   # Attribute factories
    b_list, b_single, b_main,               # Block factories
)
```

This design provides:
- **Type safety**: Catch errors at design time
- **Composability**: Build complex schemas from simple parts
- **Clarity**: Explicit structure without magic
- **Testability**: Schemas are pure data structures

## Schema Hierarchy

```
Schema (s_resource, s_data_source, s_provider)
├── Attributes (a_str, a_num, a_bool, etc.)
│   ├── Simple types (string, number, boolean)
│   ├── Collection types (list, map, set)
│   ├── Complex types (object, tuple)
│   └── Special types (dynamic, unknown, null)
└── Nested Blocks (b_main, b_list, b_single, etc.)
    └── Contains more attributes and blocks (recursive)
```

## Quick Example

Here's a complete resource with schema:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, a_bool, PvsSchema
import attrs

@attrs.define
class ServerConfig:
    name: str
    port: int = 8080
    enabled: bool = True

@attrs.define
class ServerState:
    id: str
    name: str
    port: int
    enabled: bool
    ip_address: str

@register_resource("server")
class Server(BaseResource):
    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define the Terraform schema."""
        return s_resource({
            # User inputs
            "name": a_str(required=True, description="Server name"),
            "port": a_num(default=8080, description="Port number"),
            "enabled": a_bool(default=True, description="Whether enabled"),

            # Provider outputs
            "id": a_str(computed=True, description="Unique ID"),
            "ip_address": a_str(computed=True, description="Assigned IP"),
        })

    async def _validate_config(self, config: ServerConfig) -> list[str]:
        errors = []
        if config.port < 1 or config.port > 65535:
            errors.append("Port must be between 1 and 65535")
        return errors

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        # Implementation here
        pass

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        # Implementation here
        pass

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        # Implementation here
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        # Implementation here
        pass
```

## Key Principles

### 1. Separation of Concerns

**Schema** (Terraform interface) vs **Runtime Classes** (Python objects):

```python
# Schema: Defines Terraform's view of the resource
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),
        "port": a_num(default=8080),
        "id": a_str(computed=True),  # Computed by provider
    })

# Runtime: Python attrs classes for type safety
@attrs.define
class Config:
    name: str
    port: int = 8080

@attrs.define
class State:
    id: str
    name: str
    port: int
```

The framework automatically converts between Terraform's CTY values and your Python classes.

### 2. Explicit over Implicit

Everything is explicit in the schema:

```python
s_resource({
    # Explicit required
    "name": a_str(required=True, description="Server name"),

    # Explicit optional with default
    "port": a_num(default=8080, description="Port number"),

    # Explicit computed
    "id": a_str(computed=True, description="Unique identifier"),

    # Explicit sensitive
    "password": a_str(required=True, sensitive=True, description="Password"),
})
```

### 3. Type Safety

The schema system ensures type safety at multiple levels:

```python
# CTY Type (Terraform's type system)
a_num()  # Creates CtyNumber type

# Python Type (attrs classes)
@attrs.define
class Config:
    port: int  # Python type annotation

# Validation (runtime checks)
validators=[lambda x: 1 <= x <= 65535 or "Invalid port"]
```

## Schema Types

### Resource Schemas

Resources are managed infrastructure components with full CRUD lifecycle:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),
        "size": a_num(default=100),
        "id": a_str(computed=True),
        "created_at": a_str(computed=True),
    })
```

### Data Source Schemas

Data sources are read-only queries:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        # Input (filter criteria)
        "name_filter": a_str(required=True),
        "limit": a_num(default=10),

        # Output (computed results)
        "id": a_str(computed=True),
        "results": a_list(a_str(), computed=True),
        "count": a_num(computed=True),
    })
```

### Provider Schemas

Provider configuration for global settings:

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_endpoint": a_str(required=True, description="API URL"),
        "api_key": a_str(required=True, sensitive=True, description="API key"),
        "timeout": a_num(default=30, description="Request timeout"),
        "retry": a_bool(default=True, description="Enable retries"),
    })
```

## Attribute Types

### Simple Types

```python
a_str()   # String values
a_num()   # Numeric values (int or float)
a_bool()  # Boolean values
a_dyn()   # Dynamic (any type)
```

### Collection Types

```python
a_list(element_type)  # Ordered list
a_map(element_type)   # Key-value map
a_set(element_type)   # Unordered unique set
a_tuple([type1, type2])  # Fixed-length tuple
```

### Complex Types

```python
a_obj({
    "field1": a_str(),
    "field2": a_num(),
    "nested": a_obj({
        "inner": a_bool()
    })
})
```

## Nested Blocks

Blocks provide repeatable nested structures:

```python
s_resource({
    "name": a_str(required=True),

    # Single block (0 or 1)
    "config": b_single("config", attributes={
        "timeout": a_num(default=30),
        "retries": a_num(default=3),
    }),

    # List of blocks (0 or more)
    "rule": b_list("rule", attributes={
        "port": a_num(required=True),
        "protocol": a_str(required=True),
    }),
})
```

## Validation

### Built-in Validation

Required, optional, and type checking are automatic:

```python
s_resource({
    "name": a_str(required=True),  # Must be provided
    "port": a_num(),                # Optional (can be null)
})
```

### Custom Validators

Add custom validation logic:

```python
s_resource({
    "port": a_num(
        validators=[
            lambda x: 1 <= x <= 65535 or "Port must be 1-65535",
        ]
    ),
    "email": a_str(
        validators=[
            lambda x: "@" in x or "Invalid email address",
            lambda x: len(x) <= 255 or "Email too long",
        ]
    ),
})
```

### Resource-Level Validation

Implement complex validation in `_validate_config`:

```python
async def _validate_config(self, config: Config) -> list[str]:
    """Validate configuration logic."""
    errors = []

    if config.max_size < config.min_size:
        errors.append("max_size must be >= min_size")

    if config.backup_enabled and not config.backup_schedule:
        errors.append("backup_schedule required when backup_enabled=true")

    return errors
```

## Attribute Modifiers

### Required

Must be provided by user:

```python
"name": a_str(required=True)
```

### Default

Optional with fallback value:

```python
"port": a_num(default=8080)
"tags": a_list(a_str(), default=[])
```

### Computed

Set by provider, not user:

```python
"id": a_str(computed=True)
"ip_address": a_str(computed=True)
"created_at": a_str(computed=True)
```

### Sensitive

Masked in logs and UI:

```python
"password": a_str(sensitive=True)
"api_key": a_str(sensitive=True)
```

## Best Practices

### 1. Always Include Descriptions

```python
s_resource({
    "name": a_str(
        required=True,
        description="Unique name for the server"  # ✓ Good
    ),
    "port": a_num(default=8080),  # ✗ Missing description
})
```

### 2. Use Appropriate Defaults

```python
"port": a_num(default=8080)        # ✓ Sensible default
"name": a_str(default="server")    # ✗ Bad - names should be unique
"enabled": a_bool(default=True)    # ✓ Reasonable default
```

### 3. Validate Early

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "port": a_num(
            required=True,
            validators=[
                lambda x: 1 <= x <= 65535 or "Invalid port"
            ]
        )
    })
```

### 4. Keep Schemas DRY

```python
# Reuse common attribute definitions
def common_metadata_attrs():
    return {
        "tags": a_list(a_str(), default=[]),
        "labels": a_map(a_str(), default={}),
        "created_at": a_str(computed=True),
        "updated_at": a_str(computed=True),
    }

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True),
        **common_metadata_attrs(),  # Reuse common fields
    })
```

### 5. Document Computed Fields

```python
"id": a_str(
    computed=True,
    description="Unique identifier assigned by the provider"  # ✓ Explain source
)
```

## Advanced Topics

### CTY Type System (Internal)

> **Note**: The CTY type system is an internal implementation detail. Users should **not** import from `pyvider-cty` directly. Always use the factory functions provided by `pyvider.schema`.

Pyvider uses Terraform's CTY type system internally for type representation:

```python
# CORRECT: Use factory functions
from pyvider.schema import a_str, a_num, a_list

# These factory functions handle CTY types internally
name = a_str()  # Creates a string attribute with CTY type
count = a_num()  # Creates a number attribute with CTY type
items = a_list(a_str())  # Creates a list of strings with CTY types

# INCORRECT: Don't import CTY types directly
# from pyvider.cty import CtyString  # ❌ Don't do this
# from pyvider-cty import CtyNumber  # ❌ Don't do this
```

The `pyvider-cty` package is an internal dependency that handles the low-level type system communication with Terraform. All type creation and manipulation should be done through Pyvider's public API.

### Schema Caching

Schemas are built once and cached:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    # This is called once during provider initialization
    # Result is cached for performance
    return s_resource({...})
```

### Unknown Values

During planning, some values may be unknown:

```python
# Terraform will show these as (known after apply)
async def read(self, ctx: ResourceContext):
    # Check if a field is unknown
    if ctx.is_field_unknown("some_field"):
        # Handle unknown value during planning
        pass
```

## Common Patterns

### Optional Configuration Block

```python
"database": b_single("database", attributes={
    "host": a_str(required=True),
    "port": a_num(default=5432),
    "name": a_str(required=True),
})
```

### List of Complex Objects

```python
"endpoints": a_list(
    a_obj({
        "url": a_str(required=True),
        "weight": a_num(default=100),
        "health_check": a_bool(default=True),
    }),
    default=[],
    description="Load balancer endpoints"
)
```

### Conditional Requirements

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []
    if config.ssl_enabled and not config.ssl_certificate:
        errors.append("ssl_certificate required when ssl_enabled=true")
    return errors
```

## See Also

- **[Schema Overview](../schema/overview.md)** - Detailed schema guide with examples
- **[Attributes](../schema/attributes.md)** - Complete attribute reference
- **[Blocks](../schema/blocks.md)** - Nested block patterns
- **[Validators](../schema/validators.md)** - Validation techniques
- **[Best Practices](../schema/best-practices.md)** - Schema design guidelines
