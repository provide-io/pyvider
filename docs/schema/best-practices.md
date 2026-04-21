# Schema Best Practices

This guide provides best practices for designing clean, maintainable, and user-friendly schemas.

## Keep It Simple

The best schemas are simple and easy to understand. Avoid unnecessary complexity.

**Good:**
```python
s_resource({
    "name": a_str(required=True, description="Resource name"),
    "size": a_str(required=True, description="Resource size"),
    "tags": a_map(a_str(), description="Resource tags"),
})
```

**Avoid:**
```python
s_resource({
    "config": a_obj({
        "settings": a_obj({
            "advanced": a_obj({
                "nested": a_obj({  # Too many levels
                    "value": a_str()
                })
            })
        })
    })
})
```

## Be Consistent

Use consistent naming conventions across your schemas.

### Naming Conventions

- Use `snake_case` for attribute names
- Use descriptive names that match Terraform conventions
- Use plural names for collections (`tags`, `rules`, `endpoints`)
- Use `_id` suffix for identifiers (`vpc_id`, `network_id`)

**Good:**
```python
"server_name": a_str()
"network_id": a_str()
"security_rules": a_list(...)
```

**Avoid:**
```python
"serverName": a_str()  # camelCase
"netID": a_str()  # abbreviation
"rule": a_list(...)  # singular for collection
```

## Always Add Descriptions

Provide clear descriptions for all attributes and blocks.

**Good:**
```python
"timeout": a_num(
    default=30,
    description="Request timeout in seconds. Must be between 1 and 300."
)
```

**Avoid:**
```python
"timeout": a_num(default=30)  # No description
```

## Use Appropriate Defaults

Provide sensible defaults for optional attributes.

**Good:**
```python
"port": a_num(default=8080, description="Server port")
"retries": a_num(default=3, description="Max retry attempts")
"enabled": a_bool(default=True, description="Enable feature")
```

**Avoid:**
```python
"name": a_str(default="server")  # Names should be unique, no default
"password": a_str(default="admin123")  # Never default sensitive data
```

## Mark Sensitive Data

Always mark sensitive attributes as sensitive.

**Critical:**
```python
"api_key": a_str(required=True, sensitive=True)
"password": a_str(required=True, sensitive=True)
"private_key": a_str(required=True, sensitive=True)
```

## Use Validators

Add validators to enforce constraints early.

```python
from pyvider.schema import a_str, a_num

"port": a_num(
    required=True,
    validators=[
        lambda x: 1 <= x <= 65535 or "Port must be 1-65535"
    ],
    description="Server port number"
)

"email": a_str(
    required=True,
    validators=[
        lambda x: "@" in x or "Invalid email address"
    ],
    description="Contact email address"
)
```

## Group Related Attributes

Use blocks to group related configuration.

**Good:**
```python
s_resource({
    "name": a_str(required=True),

    "network_config": b_single("network_config", attributes={
        "vpc_id": a_str(required=True),
        "subnet_ids": a_list(a_str()),
        "security_group_ids": a_list(a_str()),
    }),

    "logging_config": b_single("logging_config", attributes={
        "level": a_str(default="INFO"),
        "format": a_str(default="json"),
    }),
})
```

## Document Computed Attributes

Clearly explain the source and purpose of computed values.

```python
"ip_address": a_str(
    computed=True,
    description="Public IP address assigned by the provider after creation"
)

"created_at": a_str(
    computed=True,
    description="ISO 8601 timestamp of resource creation"
)
```

## Use Semantic Types

Choose types that match the semantic meaning.

```python
# Strings for identifiers
"id": a_str()
"vpc_id": a_str()

# Numbers for quantities
"port": a_num()
"timeout_seconds": a_num()
"replica_count": a_num()

# Booleans for flags
"enabled": a_bool()
"auto_scaling": a_bool()

# Lists for ordered collections
"availability_zones": a_list(a_str())

# Maps for key-value pairs
"tags": a_map(a_str())
"environment_variables": a_map(a_str())
```

## Avoid Overly Permissive Types

Don't use `a_dyn()` unless absolutely necessary.

**Avoid:**
```python
"config": a_dyn()  # Too permissive, lose type safety
```

**Prefer:**
```python
"config": a_obj({
    "timeout": a_num(),
    "retries": a_num(),
})
```

## Document Breaking Changes

When attributes require replacement, document clearly.

```python
"size": a_str(
    required=True,
    description="Instance size. Changing this forces replacement of the resource."
)

"region": a_str(
    required=True,
    description="AWS region. Cannot be changed after creation - forces replacement."
)
```

## Provide Examples in Descriptions

Include examples in descriptions when helpful.

```python
"cidr_block": a_str(
    required=True,
    description="CIDR block for the VPC (e.g., '10.0.0.0/16')"
)

"schedule": a_str(
    required=True,
    description="Cron expression for schedule (e.g., '0 2 * * *' for daily at 2am)"
)
```

## Schema Evolution

Design schemas for forward evolution.

### Version Schema

```python
"schema_version": a_str(
    computed=True,
    description="Schema version for state migration"
)
```

### Optional New Fields

```python
# Add new fields as optional to maintain compatibility
"new_feature": a_str(
    description="New feature added in v1.5.0"
)
```

## Common Anti-Patterns

### ❌ Too Many Required Fields

```python
# Bad: Forces users to provide everything
s_resource({
    "field1": a_str(required=True),
    "field2": a_str(required=True),
    "field3": a_str(required=True),
    # ... 20 more required fields
})
```

### ❌ Unclear Attribute Names

```python
# Bad: Ambiguous names
"data": a_str()
"config": a_str()
"value": a_str()
```

### ❌ Missing Validation

```python
# Bad: No validation
"port": a_num()  # Could be negative or > 65535
```

### ❌ Inconsistent Naming

```python
# Bad: Mixed conventions
"serverName": a_str()  # camelCase
"network_id": a_str()  # snake_case
"TimeOut": a_num()  # PascalCase
```

## Testing Schemas

Test your schemas to ensure they work correctly.

```python
def test_server_schema():
    schema = Server.get_schema()

    # Test required fields
    assert "name" in schema.attributes
    assert schema.attributes["name"].required

    # Test defaults
    assert schema.attributes["port"].default == 8080

    # Test descriptions
    assert "Server port" in schema.attributes["port"].description
```

## Documentation

Document your schema in multiple places:

1. **Code**: Description in schema definition
2. **Docs**: User-facing documentation
3. **Examples**: Working Terraform configurations

## See Also

- [Schema Overview](overview.md) - Schema system introduction
- [Attributes](attributes.md) - Attribute reference
- [Blocks](blocks.md) - Block patterns
- [Validators](validators.md) - Validation techniques
