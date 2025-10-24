# Schema System

The Pyvider schema system provides a type-safe, declarative way to define the structure and constraints of your provider's resources, data sources, and functions. It bridges Python and Terraform's type systems, enabling proper validation and documentation.

## What is a Schema?

A schema defines:

- **Structure**: What attributes and blocks your component has
- **Types**: What kind of data each attribute holds (string, number, list, etc.)
- **Constraints**: What values are valid (required, optional, validators)
- **Behavior**: How attributes work (computed, sensitive, default values)
- **Documentation**: Descriptions shown to users

## Quick Example

Here's a simple resource with schema:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, a_bool, PvsSchema
import attrs

@attrs.define
class ServerConfig:
    """Configuration from Terraform."""
    name: str
    port: int = 8080
    enabled: bool = True

@attrs.define
class ServerState:
    """State tracked by Terraform."""
    id: str
    name: str
    port: int
    enabled: bool
    ip_address: str  # Computed by provider

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

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        # Implementation
        pass

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        # Implementation
        pass

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        # Implementation
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        # Implementation
        pass
```

## Key Components

### Schema Factories

Pyvider uses **factory functions** to build schemas:

```python
from pyvider.schema import (
    s_resource, s_data_source, s_provider,  # Schema builders
    a_str, a_num, a_bool, a_list, a_map,   # Attribute types
    b_list, b_single, b_main,               # Nested blocks
)
```

### Attribute Types

Define what data each field holds:

```python
# Simple types
a_str()   # String values
a_num()   # Numeric values (int or float)
a_bool()  # Boolean values

# Collection types
a_list(a_str())           # List of strings
a_map(a_num())            # Map of numbers
a_set(a_str())            # Set of strings

# Complex types
a_obj({
    "field1": a_str(),
    "field2": a_num(),
})
```

### Attribute Modifiers

Control attribute behavior:

```python
s_resource({
    # Required input
    "name": a_str(required=True),

    # Optional with default
    "port": a_num(default=8080),

    # Computed by provider
    "id": a_str(computed=True),

    # Sensitive (masked in logs)
    "password": a_str(sensitive=True),
})
```

### Schema Types

Different component types have different schema builders:

```python
# Resource schema (CRUD lifecycle)
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({...})

# Data source schema (read-only)
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({...})

# Provider schema (global configuration)
def _build_schema(self) -> PvsSchema:
    return s_provider({...})
```

## How Schemas Work

### 1. Schema Definition

You define schemas using factory functions in your component's `get_schema()` method.

### 2. Schema Generation

Pyvider automatically converts your Python schema to Terraform's protocol format (CTY types).

### 3. Runtime Conversion

When Terraform sends data:
- Pyvider converts CTY values → Python types
- Populates your `@attrs.define` classes
- Validates against schema constraints

When your provider returns data:
- Pyvider converts Python types → CTY values
- Sends back to Terraform via gRPC

### 4. Type Safety

The combination of schemas + attrs classes gives you:
- Compile-time type checking (mypy/pyright)
- Runtime validation (schema constraints)
- IDE autocomplete and type hints

## Best Practices

1. **Always add descriptions** - Users see these in documentation
2. **Use appropriate defaults** - Make common cases easy
3. **Validate early** - Use validators to catch errors before apply
4. **Keep schemas DRY** - Extract common attribute patterns
5. **Document computed fields** - Explain where values come from

## Learn More

This is a high-level introduction to Pyvider's schema system. For comprehensive documentation including:

- Detailed attribute reference
- Nested blocks and complex types
- Advanced validation techniques
- Schema patterns and examples
- Best practices and anti-patterns

See the **[Schema System Documentation →](../schema/overview.md)**

---

<p align="center">
  Continue to <a href="../guides/creating-providers.md">Creating Providers →</a>
</p>
