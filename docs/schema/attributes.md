# Attributes

Attributes define the individual fields in your provider's schemas. Pyvider uses **factory functions** to create attributes with proper typing and validation.

## Overview

Attributes represent simple and complex values in Terraform configurations:
- **Simple types**: strings, numbers, booleans
- **Collection types**: lists, maps, sets
- **Complex types**: objects, tuples
- **Special types**: dynamic, unknown, null

## Factory Functions

Pyvider provides `a_*` factory functions to create attributes:

```python
from pyvider.schema import (
    a_str, a_num, a_bool,          # Simple types
    a_list, a_map, a_set, a_tuple, # Collections
    a_obj,                          # Complex objects
    a_dyn,                          # Dynamic type
)
```

## Simple Types

### String Attributes

Use `a_str()` for text values:

```python
from pyvider.schema import a_str, s_resource

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(
            required=True,
            description="Resource name"
        ),
        "region": a_str(
            default="us-east-1",
            description="AWS region"
        ),
        "password": a_str(
            required=True,
            sensitive=True,  # Masked in logs
            description="Admin password"
        ),
    })
```

### Number Attributes

Use `a_num()` for numeric values (integers or floats):

```python
port = a_num(
    default=8080,
    description="Port number",
    validators=[
        lambda x: 1 <= x <= 65535 or "Port must be between 1 and 65535"
    ]
)

timeout = a_num(
    default=30.5,
    description="Timeout in seconds"
)
```

### Boolean Attributes

Use `a_bool()` for true/false values:

```python
enabled = a_bool(
    default=True,
    description="Whether the feature is enabled"
)

debug_mode = a_bool(
    default=False,
    description="Enable debug logging"
)
```

## Collection Types

### Lists

Use `a_list()` for ordered collections:

```python
# List of strings
tags = a_list(
    a_str(),
    default=[],
    description="Resource tags"
)

# List of numbers
ports = a_list(
    a_num(),
    description="Allowed ports"
)

# List of objects
rules = a_list(
    a_obj({
        "port": a_num(required=True),
        "protocol": a_str(required=True),
    }),
    description="Firewall rules"
)
```

### Maps

Use `a_map()` for key-value pairs:

```python
# Map of strings
labels = a_map(
    a_str(),
    default={},
    description="Label key-value pairs"
)

# Map of numbers
quotas = a_map(
    a_num(),
    description="Resource quotas by type"
)
```

### Sets

Use `a_set()` for unordered unique collections:

```python
# Set of strings
allowed_ips = a_set(
    a_str(),
    description="Allowed IP addresses"
)
```

### Tuples

Use `a_tuple()` for fixed-length ordered collections with different types:

```python
# Tuple with specific types for each element
coordinates = a_tuple(
    [a_num(), a_num()],  # [latitude, longitude]
    description="Geographic coordinates"
)

# Mixed types
metadata = a_tuple(
    [a_str(), a_num(), a_bool()],  # [name, count, active]
    description="Resource metadata tuple"
)
```

## Complex Types

### Objects

Use `a_obj()` for nested structures:

```python
config = a_obj({
    "timeout": a_num(default=30),
    "retries": a_num(default=3),
    "endpoint": a_str(required=True),
    "tls_enabled": a_bool(default=True),
}, description="Connection configuration")

# Nested objects
server_config = a_obj({
    "host": a_str(required=True),
    "port": a_num(default=443),
    "auth": a_obj({
        "username": a_str(required=True),
        "password": a_str(required=True, sensitive=True),
    }, description="Authentication credentials"),
}, description="Server configuration")
```

## Attribute Properties

### Required vs Optional

```python
# Required attribute (must be provided)
name = a_str(
    required=True,
    description="Required resource name"
)

# Optional attribute with default
region = a_str(
    default="us-east-1",
    description="Optional AWS region"
)

# Optional attribute without default (can be null)
description = a_str(
    description="Optional description"
)
```

### Computed Attributes

Computed attributes are set by the provider, not by users:

```python
@classmethod
def get_schema(cls):
    return s_resource({
        # User provides this
        "name": a_str(required=True, description="Server name"),

        # Provider computes these
        "id": a_str(computed=True, description="Unique identifier"),
        "ip_address": a_str(computed=True, description="Assigned IP"),
        "created_at": a_str(computed=True, description="Creation timestamp"),
    })
```

### Sensitive Attributes

Sensitive attributes are masked in logs and outputs:

```python
api_key = a_str(
    required=True,
    sensitive=True,  # Value will be masked
    description="API key for authentication"
)

credentials = a_obj({
    "username": a_str(required=True),
    "password": a_str(required=True, sensitive=True),
}, description="Login credentials")
```

### Default Values

```python
# Simple defaults
port = a_num(default=8080)
enabled = a_bool(default=True)
region = a_str(default="us-east-1")

# Collection defaults
tags = a_list(a_str(), default=[])
labels = a_map(a_str(), default={})

# Object defaults
config = a_obj({
    "timeout": a_num(default=30),
    "retries": a_num(default=3),
}, description="Configuration with defaults")
```

A default is the value the framework substitutes when the practitioner omits the
argument. It reaches the configuration the resource reads and the state it plans, so
the plan shows `"us-east-1"` rather than nothing at all.

Five things follow:

- **An attribute with a default is Computed.** Pyvider marks it so automatically.
  Terraform only lets a provider plan a value the configuration does not contain for a
  computed attribute; `required=True`, `write_only=True` and computed-only attributes are
  rejected with a default, as is a default whose type does not match the attribute.
- **Removing the argument reverts it to the default** rather than keeping the value it
  last had. This matches terraform-plugin-framework: Terraform Core builds the proposed
  new state by falling back to prior state for an Optional + Computed attribute, and the
  framework's `Default` then overwrites that, keying on configuration nullness rather
  than plan nullness. (Inside a `b_set` block the value is kept instead: a set has no
  element order, so an element cannot be matched back to the configuration that produced
  it.)
- **`default=None` means "no default".** There is no way to declare an explicit null
  default, and none is needed: an optional attribute is already null when omitted.
- **Nothing absent is invented.** A default nested inside an object attribute or a block
  is filled only when the practitioner wrote that object or block; a value that is not
  yet known ("known after apply") is never replaced.
- **Every direct `a_obj()` is a nested type.** This applies whether or not the object or
  its members declare defaults, and exposes each member's required/optional/computed flags
  to Terraform. Compared with the former opaque `cty.Object` encoding, members marked
  optional can be omitted individually instead of every member having to appear in
  configuration. The configuration syntax and resulting cty object shape are unchanged.

## Validators

Add validation logic to attributes:

```python
from pyvider.schema import a_str, a_num

# Single validator
port = a_num(
    validators=[
        lambda x: 1 <= x <= 65535 or "Port must be between 1 and 65535"
    ]
)

# Multiple validators
username = a_str(
    required=True,
    validators=[
        lambda x: len(x) >= 3 or "Username must be at least 3 characters",
        lambda x: x.isalnum() or "Username must be alphanumeric",
        lambda x: not x.startswith("_") or "Username cannot start with underscore",
    ]
)

# Validators for collections
tags = a_list(
    a_str(),
    validators=[
        lambda x: len(x) <= 10 or "Maximum 10 tags allowed",
        lambda x: all(len(tag) <= 50 for tag in x) or "Tag length must be <= 50 chars",
    ]
)
```

## Special Types

### Dynamic Type

Use `a_dyn()` when the type is not known until runtime:

```python
metadata = a_dyn(
    description="Arbitrary metadata (type determined at runtime)"
)
```

### Unknown and Null Values

For testing and advanced scenarios:

```python
from pyvider.schema import a_unknown, a_null, a_str

# Create unknown values
unknown_string = a_unknown(a_str())

# Create null values
null_number = a_null(a_num())
```

## Complete Example

Here's a comprehensive resource schema using various attribute types:

```python
from pyvider.schema import (
    s_resource,
    a_str, a_num, a_bool,
    a_list, a_map, a_obj,
)

@classmethod
def get_schema(cls):
    return s_resource({
        # Required simple types
        "name": a_str(
            required=True,
            description="Server name"
        ),
        "instance_type": a_str(
            required=True,
            description="Instance type (e.g., t2.micro)"
        ),

        # Optional with defaults
        "port": a_num(
            default=8080,
            description="Port number",
            validators=[lambda x: 1 <= x <= 65535 or "Invalid port"]
        ),
        "enabled": a_bool(
            default=True,
            description="Whether server is enabled"
        ),

        # Sensitive
        "admin_password": a_str(
            required=True,
            sensitive=True,
            description="Administrator password"
        ),

        # Computed
        "id": a_str(
            computed=True,
            description="Unique identifier"
        ),
        "ip_address": a_str(
            computed=True,
            description="Assigned IP address"
        ),

        # Collections
        "tags": a_list(
            a_str(),
            default=[],
            description="Resource tags"
        ),
        "labels": a_map(
            a_str(),
            default={},
            description="Key-value labels"
        ),

        # Complex objects
        "config": a_obj({
            "timeout": a_num(default=30),
            "retries": a_num(default=3),
            "endpoints": a_list(a_str(), default=[]),
        }, description="Server configuration"),

        # Nested complex structure
        "monitoring": a_obj({
            "enabled": a_bool(default=True),
            "interval": a_num(default=60),
            "alerts": a_list(
                a_obj({
                    "type": a_str(required=True),
                    "threshold": a_num(required=True),
                    "email": a_str(required=True),
                }),
                default=[]
            ),
        }, description="Monitoring configuration"),
    })
```

## Corresponding Terraform Configuration

The schema above would be used in Terraform like this:

```hcl
resource "mycloud_server" "web" {
  name          = "web-server"
  instance_type = "t2.micro"
  port          = 8080
  enabled       = true
  admin_password = "secure-password"  # Sensitive

  tags = ["production", "web"]

  labels = {
    environment = "prod"
    team        = "platform"
  }

  config {
    timeout   = 60
    retries   = 5
    endpoints = ["https://api.example.com"]
  }

  monitoring {
    enabled  = true
    interval = 120

    alerts {
      type      = "cpu"
      threshold = 80
      email     = "ops@example.com"
    }

    alerts {
      type      = "memory"
      threshold = 90
      email     = "ops@example.com"
    }
  }
}
```

## See Also

- [Schema Overview](overview.md) - Complete schema system guide
- [Blocks](blocks.md) - Nested block structures
- [Types](types.md) - Detailed type reference
- [Validators](validators.md) - Validation patterns
- [Best Practices](best-practices.md) - Schema design recommendations
