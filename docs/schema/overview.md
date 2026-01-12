# Schema System Overview

The Pyvider schema system provides a type-safe, declarative way to define the structure and constraints of your provider's resources, data sources, and functions. It bridges Python and Terraform's type systems, enabling proper validation and documentation.

## What is a Schema?

A schema defines:

- **Structure**: What attributes and blocks your component has
- **Types**: What kind of data each attribute holds (string, number, list, etc.)
- **Constraints**: What values are valid (required, optional, validators)
- **Behavior**: How attributes work (computed, sensitive, default values)
- **Documentation**: Descriptions shown to users

## Schema Hierarchy

Pyvider schemas are hierarchical:

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

## Factory Functions

Pyvider uses **factory functions** (not classes) to build schemas:

### Attribute Factories

Create attributes with `a_*` functions:

```python
from pyvider.schema import a_str, a_num, a_bool, a_list, a_map, a_obj

# Simple types
name = a_str(description="Server name", required=True)
port = a_num(description="Port number", default=8080)
enabled = a_bool(description="Whether server is enabled", default=True)

# Collection types
tags = a_list(a_str(), description="List of tags")
metadata = a_map(a_str(), description="Arbitrary metadata")

# Complex types
config = a_obj({
    "timeout": a_num(default=30),
    "retries": a_num(default=3),
}, description="Configuration object")
```

### Block Factories

Create nested blocks with `b_*` functions:

```python
from pyvider.schema import b_main, b_list, b_single

# Main block (unnested, attributes at top level)
schema = b_main({
    "name": a_str(required=True),
    "port": a_num(default=8080),
})

# List of blocks (0 or more)
schema_with_rules = b_main({
    "name": a_str(required=True),
    "rule": b_list("rule"),  # Multiple rule blocks allowed
})

# Single block (0 or 1)
schema_with_config = b_main({
    "name": a_str(required=True),
    "config": b_single("config"),  # At most one config block
})
```

### Schema Factories

Create complete schemas with `s_*` functions:

```python
from pyvider.schema import s_resource, s_data_source, s_provider

# Resource schema
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),
        "port": a_num(default=8080),
        "enabled": a_bool(default=True),
    })

# Data source schema
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        "filter": a_str(required=True),
        "limit": a_num(default=100),
    })

# Provider schema
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_endpoint": a_str(required=True),
        "api_key": a_str(required=True, sensitive=True),
        "timeout": a_num(default=30),
    })
```

## Complete Example

Here's a complete resource schema demonstrating various features:

```python
from pyvider.schema import (
    s_resource,
    a_str, a_num, a_bool, a_list, a_map, a_obj,
    b_list, b_single,
)

@register_resource("mycloud_server")
class ServerResource(BaseResource):

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # Required string
            "name": a_str(
                required=True,
                description="Server name"
            ),

            # Optional number with default
            "port": a_num(
                default=8080,
                description="Port number",
                validators=[
                    lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
                ]
            ),

            # Optional boolean
            "enabled": a_bool(
                default=True,
                description="Whether server is enabled"
            ),

            # Computed attribute (provider sets this)
            "ip_address": a_str(
                computed=True,
                description="Server IP address"
            ),

            # Sensitive attribute (masked in logs)
            "admin_password": a_str(
                required=True,
                sensitive=True,
                description="Administrator password"
            ),

            # List of strings
            "tags": a_list(
                a_str(),
                default=[],
                description="Tags for the server"
            ),

            # Map of strings
            "labels": a_map(
                a_str(),
                default={},
                description="Label key-value pairs"
            ),

            # Complex object
            "config": a_obj({
                "timeout": a_num(default=30),
                "retries": a_num(default=3),
                "debug": a_bool(default=False),
            }, description="Server configuration"),

            # Nested block (list)
            "rule": b_list("rule"),  # Multiple firewall rules

            # Nested block (single)
            "backup": b_single("backup"),  # At most one backup config
        })
```

Corresponding Terraform configuration:

```hcl
resource "mycloud_server" "web" {
  name            = "web-server"
  port            = 443
  enabled         = true
  admin_password  = var.admin_password
  tags            = ["web", "production"]
  labels          = {
    env = "prod"
    team = "platform"
  }

  config {
    timeout = 60
    retries = 5
    debug   = false
  }

  rule {
    protocol = "tcp"
    port     = 443
    source   = "0.0.0.0/0"
  }

  rule {
    protocol = "tcp"
    port     = 80
    source   = "0.0.0.0/0"
  }

  backup {
    enabled   = true
    schedule  = "daily"
    retention = 7
  }
}
```

## Key Concepts

### Attributes vs Blocks

**Attributes** are simple key-value pairs:
- Scalar values (string, number, boolean)
- Collections (list, map, set)
- Complex objects (nested attributes)

**Blocks** are named, structured containers:
- Can contain attributes and other blocks
- Support nesting modes (list, set, map, single, group)
- Represented as HCL blocks in Terraform

```hcl
# Attributes
name = "example"
port = 8080
tags = ["a", "b"]

# Blocks
config {
  timeout = 30
}

rule {
  port = 80
}

rule {
  port = 443
}
```

### Required vs Optional vs Computed

**Required**: User must provide:
```python
"name": a_str(required=True)
```

**Optional**: User may provide, has default:
```python
"port": a_num(default=8080)
```

**Optional no default**: User may provide, no default:
```python
"description": a_str()  # No default
```

**Computed**: Provider calculates, user cannot set:
```python
"id": a_str(computed=True)
```

**Optional + Computed**: User may provide OR provider will compute:
```python
"timestamp": a_str(computed=True)  # Provider sets if not provided
```

### Sensitive Data

Mark sensitive attributes to mask them in logs and UI:

```python
"api_key": a_str(
    required=True,
    sensitive=True,  # Masked in Terraform output
    description="API authentication key"
)

"password": a_str(
    required=True,
    sensitive=True,
    description="Database password"
)
```

In Terraform output:
```
# mycloud_server.web will be created
+ resource "mycloud_server" "web" {
    + name     = "web-server"
    + api_key  = (sensitive value)
    + password = (sensitive value)
  }
```

### Validators

Add custom validation logic to attributes:

```python
"port": a_num(
    required=True,
    validators=[
        lambda x: 1 <= x <= 65535 or "Port must be between 1 and 65535",
        lambda x: x != 22 or "Port 22 is reserved for SSH",
    ]
)

"email": a_str(
    required=True,
    validators=[
        lambda x: "@" in x or "Must be a valid email address",
        lambda x: (x.endswith(".com") or x.endswith(".org")) or "Must end with .com or .org",
    ]
)
```

Validators return:
- `True` if valid
- Error message string if invalid

## Schema Building Patterns

### Pattern 1: Inline Schema

Define schema directly in `get_schema()`:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),
        "port": a_num(default=8080),
    })
```

### Pattern 2: Helper Method

Build schema with helper method for complex schemas:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return cls._build_schema()

@classmethod
def _build_schema(cls) -> PvsSchema:
    attributes = {
        "name": a_str(required=True),
        "port": a_num(default=8080),
    }

    # Add conditional attributes
    if cls.supports_encryption:
        attributes["encryption_key"] = a_str(required=True, sensitive=True)

    return s_resource(attributes)
```

### Pattern 3: Shared Attribute Definitions

Reuse attribute definitions across components:

```python
# Common attributes module
def common_name_attr():
    return a_str(
        required=True,
        description="Resource name",
        validators=[
            lambda x: len(x) >= 3 or "Name must be at least 3 characters",
            lambda x: x.isalnum() or "Name must be alphanumeric",
        ]
    )

def common_tags_attr():
    return a_list(a_str(), default=[], description="Resource tags")

# Use in resources
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": common_name_attr(),
        "tags": common_tags_attr(),
        "port": a_num(default=8080),
    })
```

## Type System Integration

Pyvider's schema system integrates with:

### Python Types

Attributes map to Python types:
- `a_str()` → `str`
- `a_num()` → `int | float`
- `a_bool()` → `bool`
- `a_list(T)` → `list[T]`
- `a_map(T)` → `dict[str, T]`
- `a_obj({...})` → attrs class or dict

### Terraform Types (CTY)

Pyvider converts between Python and Terraform's CTY type system:
- `string` ↔ `str`
- `number` ↔ `int/float`
- `bool` ↔ `bool`
- `list(T)` ↔ `list[T]`
- `map(T)` ↔ `dict[str, T]`
- `object({...})` ↔ nested dict/attrs

This conversion happens automatically in the framework.

## Schema Validation

Schemas are validated at multiple points:

1. **Build time**: When schema is created
   - Structure validation
   - Type checking

2. **Terraform plan**: When user writes configuration
   - Required attributes present
   - Types match
   - Custom validators pass

3. **Provider operations**: When framework calls your code
   - Data conversion
   - Constraint checking

## Related Documentation

- [Types Reference](types.md) - All available attribute types
- [Attributes](attributes.md) - Attribute options and behavior
- [Blocks](blocks.md) - Nested block patterns
- [Validators](validators.md) - Custom validation
- [Sensitive Data](sensitive-data.md) - Handling secrets
- [Common Patterns](common-patterns.md) - Schema patterns
- [Best Practices](best-practices.md) - Schema design guidelines

## Next Steps

- Learn about [all available types](types.md)
- Understand [attribute options](attributes.md)
- Explore [nested blocks](blocks.md)
- Add [custom validators](validators.md)
- See [common patterns](common-patterns.md)

---

**Remember**: Schemas are the contract between your provider and Terraform. A well-designed schema makes your provider easy to use and understand.
