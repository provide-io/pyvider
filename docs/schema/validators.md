# Schema Validators

Validators allow you to add custom validation logic to schema attributes, ensuring data meets your requirements before resource operations execute.

## Basic Validator Syntax

Validators are lambda functions or callables that return:
- `True` if the value is valid
- An error message string if invalid

```python
from pyvider.schema import a_str, a_num

"port": a_num(
    required=True,
    validators=[
        lambda x: 1 <= x <= 65535 or "Port must be between 1 and 65535"
    ]
)
```

## Simple Validators

### Range Validation

```python
"age": a_num(validators=[
    lambda x: x >= 0 or "Age cannot be negative",
    lambda x: x <= 120 or "Age must be realistic"
])

"percentage": a_num(validators=[
    lambda x: 0 <= x <= 100 or "Must be between 0 and 100"
])
```

### String Length

```python
"name": a_str(validators=[
    lambda x: len(x) >= 3 or "Name must be at least 3 characters",
    lambda x: len(x) <= 64 or "Name must not exceed 64 characters"
])
```

### String Format

```python
"email": a_str(validators=[
    lambda x: "@" in x or "Must be a valid email address",
    lambda x: "." in x.split("@")[1] or "Email domain must have extension"
])

"url": a_str(validators=[
    lambda x: x.startswith(("http://", "https://")) or "Must be HTTP(S) URL"
])

"slug": a_str(validators=[
    lambda x: x.islower() or "Must be lowercase",
    lambda x: "-" not in x or x.replace("-", "").isalnum() or "Only letters, numbers, hyphens"
])
```

### Enum-like Validation

```python
"environment": a_str(validators=[
    lambda x: x in ["dev", "staging", "prod"] or "Must be dev, staging, or prod"
])

"protocol": a_str(validators=[
    lambda x: x in ["tcp", "udp", "icmp"] or "Invalid protocol"
])
```

## Complex Validators

### Pattern Matching

```python
import re

"ipv4": a_str(validators=[
    lambda x: re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", x) or "Invalid IPv4 address"
])

"phone": a_str(validators=[
    lambda x: re.match(r"^\+?1?\d{10,15}$", x) or "Invalid phone number"
])
```

### Multiple Conditions

```python
"password": a_str(validators=[
    lambda x: len(x) >= 8 or "Password must be at least 8 characters",
    lambda x: any(c.isupper() for c in x) or "Password must contain uppercase letter",
    lambda x: any(c.islower() for c in x) or "Password must contain lowercase letter",
    lambda x: any(c.isdigit() for c in x) or "Password must contain number",
])
```

### Cross-Field Validation

While validators run on individual attributes, you can check related fields in resource validation:

```python
async def _validate_config(self, config: Config) -> list[str]:
    """Validate entire configuration."""
    errors = []

    # Cross-field validation
    if config.min_replicas > config.max_replicas:
        errors.append("min_replicas cannot exceed max_replicas")

    if config.ssl_enabled and not config.ssl_cert_path:
        errors.append("ssl_cert_path required when ssl_enabled is true")

    return errors
```

## Collection Validators

### List Validation

```python
"tags": a_list(a_str(), validators=[
    lambda x: len(x) > 0 or "At least one tag required",
    lambda x: len(x) <= 10 or "Maximum 10 tags allowed",
    lambda x: len(set(x)) == len(x) or "Tags must be unique"
])

"ports": a_list(a_num(), validators=[
    lambda x: all(1 <= p <= 65535 for p in x) or "All ports must be 1-65535"
])
```

### Map Validation

```python
"labels": a_map(a_str(), validators=[
    lambda x: len(x) <= 20 or "Maximum 20 labels allowed",
    lambda x: all(len(k) <= 63 for k in x.keys()) or "Label keys max 63 chars"
])
```

## Reusable Validators

### Define Common Validators

```python
# validators.py
def validate_port(x):
    return 1 <= x <= 65535 or "Port must be 1-65535"

def validate_cidr(x):
    import ipaddress
    try:
        ipaddress.ip_network(x)
        return True
    except ValueError:
        return "Invalid CIDR notation"

def validate_name(x):
    if len(x) < 3:
        return "Name must be at least 3 characters"
    if not x[0].isalpha():
        return "Name must start with a letter"
    if not x.replace("-", "").replace("_", "").isalnum():
        return "Name can only contain letters, numbers, hyphens, underscores"
    return True

# Use in schemas
"port": a_num(validators=[validate_port])
"cidr": a_str(validators=[validate_cidr])
"name": a_str(validators=[validate_name])
```

## Validator Best Practices

### 1. Clear Error Messages

```python
# Good: Specific error
lambda x: x > 0 or "Value must be positive"

# Bad: Vague error
lambda x: x > 0 or "Invalid value"
```

### 2. Early Exit for Performance

```python
# Good: Fast check first
lambda x: len(x) <= 100 and all(c.isalnum() for c in x) or "Invalid format"

# Bad: Expensive check first
lambda x: all(c.isalnum() for c in x) and len(x) <= 100 or "Invalid format"
```

### 3. Handle Edge Cases

```python
# Good: Handle empty/None
lambda x: (x and len(x) >= 3) or "Must be at least 3 characters"

# Bad: Assumes value exists
lambda x: len(x) >= 3 or "Must be at least 3 characters"  # Fails if x is None
```

### 4. Multiple Simple Validators

```python
# Good: Separate concerns
validators=[
    lambda x: len(x) >= 3 or "Min 3 characters",
    lambda x: len(x) <= 64 or "Max 64 characters",
    lambda x: x.isalnum() or "Alphanumeric only"
]

# Bad: One complex validator
validators=[
    lambda x: (3 <= len(x) <= 64 and x.isalnum()) or "Invalid name format"
]
```

## Validation Timing

Validators run at different times:

1. **Terraform plan**: Validates configuration before operations
2. **Provider operations**: Framework validates before calling your code
3. **Resource validation**: Your `_validate_config()` for custom logic

```python
@register_resource("mycloud_server")
class ServerResource(BaseResource):

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "port": a_num(
                required=True,
                validators=[  # Runs during Terraform plan
                    lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
                ]
            ),
        })

    async def _validate_config(self, config: Config) -> list[str]:
        """
        Additional validation after schema validation.
        Runs before create/update operations.
        """
        errors = []

        # Complex validation logic
        if config.port < 1024 and not config.privileged:
            errors.append("Ports below 1024 require privileged mode")

        return errors
```

## Common Validator Patterns

### Port Numbers

```python
lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
```

### IP Addresses

```python
import ipaddress

def validate_ipv4(x):
    try:
        ipaddress.IPv4Address(x)
        return True
    except ValueError:
        return "Invalid IPv4 address"
```

### URLs

```python
from urllib.parse import urlparse

def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc]) or "Invalid URL"
    except:
        return "Invalid URL format"
```

### File Paths

```python
from pathlib import Path

lambda x: not Path(x).is_absolute() or "Use relative paths only"
lambda x: ".." not in x or "Parent directory access not allowed"
```

### Resource Names

```python
lambda x: len(x) >= 3 or "Min 3 characters"
lambda x: len(x) <= 64 or "Max 64 characters"
lambda x: x[0].isalpha() or "Must start with letter"
lambda x: x.replace("-", "").replace("_", "").isalnum() or "Letters, numbers, hyphens, underscores only"
```

## Testing Validators

Test validators in your unit tests:

```python
def test_port_validator():
    schema = ServerResource.get_schema()
    port_attr = schema.attributes["port"]

    # Valid ports
    assert port_attr.validate(80) == []
    assert port_attr.validate(443) == []
    assert port_attr.validate(8080) == []

    # Invalid ports
    errors = port_attr.validate(0)
    assert len(errors) > 0
    assert "1-65535" in errors[0]

    errors = port_attr.validate(70000)
    assert len(errors) > 0
```

## Related Documentation

- [Overview](overview.md) - Schema system introduction
- [Types](types.md) - Available attribute types
- [Attributes](attributes.md) - Attribute options
- [Best Practices](best-practices.md) - Schema design guidelines

---

**Remember**: Validators provide immediate feedback to users during `terraform plan`, preventing runtime errors. Write clear, specific error messages to help users fix issues quickly.
