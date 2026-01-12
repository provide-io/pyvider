# Schema Types Reference

This guide provides a complete reference of all attribute types available in Pyvider's schema system.

## Type Categories

Pyvider provides three categories of types:

1. **Simple Types**: String (`a_str`), Number (`a_num`), Boolean (`a_bool`), Dynamic (`a_dyn`)
2. **Collection Types**: List (`a_list`), Map (`a_map`), Set (`a_set`), Tuple (`a_tuple`)
3. **Complex Types**: Object (`a_obj`)

## Simple Types

### String - `a_str()`

Text values.

```python
from pyvider.schema import a_str

# Basic usage
"name": a_str(required=True, description="Server name")
"description": a_str(default="", description="Server description")
"id": a_str(computed=True, description="Generated ID")
"api_key": a_str(required=True, sensitive=True)
```

**Terraform**: `name = "my-server"`

### Number - `a_num()`

Numeric values (integers or floats).

```python
from pyvider.schema import a_num

"port": a_num(default=8080, description="Port number")
"timeout": a_num(default=30.5, description="Seconds")
"replicas": a_num(required=True, validators=[
    lambda x: 1 <= x <= 10 or "Must be 1-10"
])
```

**Terraform**: `port = 443`

### Boolean - `a_bool()`

True/false values.

```python
from pyvider.schema import a_bool

"enabled": a_bool(default=True)
"is_healthy": a_bool(computed=True)
```

**Terraform**: `enabled = true`

### Dynamic - `a_dyn()`

Accepts any type. Use sparingly.

```python
from pyvider.schema import a_dyn

"metadata": a_dyn(description="Arbitrary metadata")
```

**Terraform**: `metadata = "string"` or `metadata = {key = "value"}`

### Null - `a_null()`

Explicitly represents a null value.

```python
from pyvider.schema import a_null

"placeholder": a_null(description="Explicitly null field")
```

**Use Cases:**
- Representing optional fields that can be explicitly set to null
- Schema placeholders
- Conditional nullability in complex schemas

**Terraform**: Not commonly used in HCL configurations - most often used internally.

**Note**: In most cases, you should use `optional=True` on regular attributes rather than `a_null()`.

### Unknown - `a_unknown()`

Represents values that are unknown during planning phase.

```python
from pyvider.schema import a_unknown

"computed_value": a_unknown(description="Value unknown until apply")
```

**Use Cases:**
- Values computed during apply that can't be known during plan
- Handling Terraform's unknown value semantics
- Advanced provider scenarios with deferred computation

**Terraform**: Terraform internally represents these as unknown values during the plan phase.

**Note**: This is an advanced type primarily used for complex provider scenarios. Most computed values should use `a_str(computed=True)` or similar instead.

## Collection Types

### List - `a_list(element_type)`

Ordered collection of same-typed elements.

```python
from pyvider.schema import a_list, a_str, a_num

"tags": a_list(a_str(), default=[], description="Tags")
"ports": a_list(a_num(), description="Allowed ports")
"matrix": a_list(a_list(a_num()), description="2D matrix")
```

**Terraform**:
```hcl
tags   = ["web", "production"]
ports  = [80, 443, 8080]
matrix = [[1, 2], [3, 4]]
```

### Map - `a_map(value_type)`

Key-value pairs (keys are strings).

```python
from pyvider.schema import a_map, a_str, a_num

"labels": a_map(a_str(), default={})
"quotas": a_map(a_num())
"permissions": a_map(a_list(a_str()))
```

**Terraform**:
```hcl
labels = {
  env  = "production"
  team = "platform"
}

quotas = {
  cpu    = 4
  memory = 8192
}
```

### Set - `a_set(element_type)`

Unordered, unique elements.

```python
from pyvider.schema import a_set, a_str

"security_groups": a_set(a_str(), default=set())
"allowed_ports": a_set(a_num())
```

**Terraform**:
```hcl
security_groups = ["sg-123", "sg-456"]  # Duplicates auto-removed
```

### Tuple - `a_tuple([type1, type2, ...])`

Fixed-length, mixed-type collection.

```python
from pyvider.schema import a_tuple, a_str, a_num, a_bool

"connection": a_tuple([a_str(), a_num(), a_bool()])  # [host, port, ssl]
"location": a_tuple([a_num(), a_num()])  # [lat, lon]
```

**Terraform**:
```hcl
connection = ["localhost", 5432, true]
location   = [37.7749, -122.4194]
```

## Complex Types

### Object - `a_obj({...})`

Structured data with typed fields.

```python
from pyvider.schema import a_obj, a_str, a_num, a_bool

"config": a_obj({
    "timeout": a_num(default=30),
    "retries": a_num(default=3),
    "debug": a_bool(default=False),
})

"server": a_obj({
    "host": a_str(required=True),
    "port": a_num(default=80),
    "tls": a_obj({
        "enabled": a_bool(default=False),
        "cert_path": a_str(),
    }),
})
```

**Terraform**:
```hcl
config = {
  timeout = 60
  retries = 5
  debug   = true
}

server = {
  host = "api.example.com"
  port = 443
  tls = {
    enabled   = true
    cert_path = "/path/to/cert.pem"
  }
}
```

## Type Composition Examples

### List of Maps
```python
"rules": a_list(a_map(a_str()))
```
```hcl
rules = [
  { action = "allow", protocol = "tcp" },
  { action = "deny", protocol = "udp" }
]
```

### Map of Lists
```python
"groups": a_map(a_list(a_str()))
```
```hcl
groups = {
  admins = ["alice", "bob"]
  users  = ["charlie"]
}
```

### List of Objects
```python
"servers": a_list(a_obj({
    "name": a_str(required=True),
    "ip": a_str(required=True),
    "ports": a_list(a_num()),
}))
```
```hcl
servers = [
  {
    name  = "web-1"
    ip    = "10.0.1.10"
    ports = [80, 443]
  }
]
```

## Type Mapping Reference

| Pyvider Function | Python Type | Terraform Type | Example |
|------------------|-------------|----------------|---------|
| `a_str()` | `str` | `string` | `"hello"` |
| `a_num()` | `int \| float` | `number` | `42` |
| `a_bool()` | `bool` | `bool` | `true` |
| `a_list(T)` | `list[T]` | `list(T)` | `["a", "b"]` |
| `a_map(T)` | `dict[str, T]` | `map(T)` | `{k = "v"}` |
| `a_set(T)` | `set[T]` | `set(T)` | `["a"]` |
| `a_tuple([T...])` | `tuple` | `tuple([T...])` | `["a", 1]` |
| `a_obj({...})` | `dict` | `object({...})` | `{k = "v"}` |
| `a_dyn()` | `Any` | `dynamic` | any |
| `a_null()` | `None` | `null` | `null` |
| `a_unknown()` | N/A | `unknown` | (plan-time) |

## Choosing the Right Type

**Use String for**: Names, IDs, URLs, text, enums
**Use Number for**: Counts, ports, timeouts, sizes, percentages
**Use Boolean for**: Flags, toggles, conditions
**Use List for**: Ordered collections, duplicates OK
**Use Map for**: Key-value lookups, labels, config dicts
**Use Set for**: Unique values, order doesn't matter
**Use Object for**: Structured config, multiple related fields
**Use Dynamic for**: Truly arbitrary data (use sparingly!)

## Best Practices

### Be Specific
```python
# Good
"port": a_num(validators=[lambda x: 1 <= x <= 65535])

# Bad
"port": a_dyn()
```

### Use Appropriate Collections
```python
# Good - Set for unique IDs
"security_group_ids": a_set(a_str())

# Bad - List allows duplicates
"security_group_ids": a_list(a_str())
```

### Structure with Objects
```python
# Good
"database": a_obj({
    "host": a_str(required=True),
    "port": a_num(default=5432),
})

# Bad - Flat
"db_host": a_str(required=True),
"db_port": a_num(default=5432),
```

### Provide Defaults
```python
# Good
"timeout": a_num(default=30)
"tags": a_list(a_str(), default=[])

# Bad - Unnecessary required
"timeout": a_num(required=True)
```

## Related Documentation

- [Overview](overview.md) - Schema system introduction
- [Attributes](attributes.md) - Attribute options
- [Validators](validators.md) - Custom validation
- [Best Practices](best-practices.md) - Design guidelines

---

**Remember**: Choose the most specific type for your data. This provides better validation and user experience.
