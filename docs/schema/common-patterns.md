# Common Schema Patterns

This guide presents common schema design patterns used across successful Pyvider providers. Learn from real-world examples to build better schemas.

## Pattern 1: Required + Computed ID

Every resource needs an ID that's computed after creation:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True, description="Resource name"),
        "id": a_str(computed=True, description="Unique identifier"),
    })
```

**Usage**:
```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  # id is computed, don't set it
}

output "server_id" {
  value = mycloud_server.web.id
}
```

## Pattern 2: Optional with Sensible Defaults

Provide defaults for common configurations:

```python
"port": a_num(default=8080, description="Port number")
"enabled": a_bool(default=True, description="Whether enabled")
"timeout": a_num(default=30, description="Timeout in seconds")
"retries": a_num(default=3, description="Retry attempts")
```

**Benefit**: Users only specify what differs from defaults.

## Pattern 3: Tags and Labels

Standard pattern for resource tagging:

```python
"tags": a_list(a_str(), default=[], description="Resource tags")
"labels": a_map(a_str(), default={}, description="Key-value labels")
```

**Usage**:
```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  tags = ["production", "web", "critical"]
  labels = {
    environment = "prod"
    team        = "platform"
    cost_center = "engineering"
  }
}
```

## Pattern 4: Connection Configuration Object

Group related connection settings:

```python
"connection": a_obj({
    "host": a_str(required=True),
    "port": a_num(default=5432),
    "ssl": a_bool(default=True),
    "timeout": a_num(default=30),
}, description="Connection configuration")
```

**Usage**:
```hcl
connection {
  host    = "db.example.com"
  port    = 5432
  ssl     = true
  timeout = 60
}
```

## Pattern 5: Repeated Configuration Blocks

Use `b_list` for repeatable configuration:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),
        "rule": b_list("rule"),  # 0 or more
    })
```

**Rule block definition**:
```python
"rule": b_list("rule", attributes={
    "protocol": a_str(required=True),
    "port": a_num(required=True),
    "source": a_str(default="0.0.0.0/0"),
})
```

**Usage**:
```hcl
resource "mycloud_firewall" "web" {
  name = "web-firewall"

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
}
```

## Pattern 6: Optional Single Configuration Block

Use `b_single` for optional advanced config:

```python
"advanced": b_single("advanced", attributes={
    "cache_ttl": a_num(default=300),
    "compression": a_bool(default=True),
    "worker_count": a_num(default=4),
})
```

**Usage**:
```hcl
resource "mycloud_api" "main" {
  name = "api-gateway"

  # Optional advanced configuration
  advanced {
    cache_ttl    = 600
    compression  = true
    worker_count = 8
  }
}
```

## Pattern 7: Computed Status Fields

Report current status as computed attributes:

```python
"status": a_str(computed=True, description="Current status")
"health": a_str(computed=True, description="Health check status")
"last_updated": a_str(computed=True, description="Last update timestamp")
"version": a_str(computed=True, description="Current version")
```

## Pattern 8: Secret Management

Separate public IDs from sensitive secrets:

```python
"username": a_str(required=True)  # Public
"password": a_str(required=True, sensitive=True)  # Secret
"connection_string": a_str(computed=True, sensitive=True)  # Generated secret
```

## Pattern 9: Size/Tier Selection

Enum-like validation for tiers:

```python
"size": a_str(
    default="medium",
    validators=[
        lambda x: x in ["small", "medium", "large", "xlarge"]
        or "Must be small, medium, large, or xlarge"
    ],
    description="Instance size"
)
```

## Pattern 10: Timeouts Configuration

Standard timeout block pattern:

```python
"timeouts": a_obj({
    "create": a_str(default="30m"),
    "update": a_str(default="30m"),
    "delete": a_str(default="10m"),
}, description="Operation timeouts")
```

## Pattern 11: Conditional Requirements

Use resource-level validation for conditional requirements:

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    if config.ssl_enabled and not config.ssl_cert_path:
        errors.append("ssl_cert_path required when ssl_enabled is true")

    if config.backup_enabled and config.backup_retention < 1:
        errors.append("backup_retention must be >= 1 when backup_enabled")

    return errors
```

## Pattern 12: Resource References

Link to other resources:

```python
"vpc_id": a_str(required=True, description="VPC identifier")
"subnet_ids": a_list(a_str(), required=True, description="Subnet identifiers")
"security_group_ids": a_set(a_str(), description="Security group IDs")
```

**Usage**:
```hcl
resource "mycloud_instance" "web" {
  vpc_id             = mycloud_vpc.main.id
  subnet_ids         = [mycloud_subnet.public.id]
  security_group_ids = [mycloud_sg.web.id, mycloud_sg.common.id]
}
```

## Pattern 13: Min/Max Constraints

Scaling and sizing constraints:

```python
"min_replicas": a_num(
    default=1,
    validators=[lambda x: x >= 1 or "Min 1 replica"]
)
"max_replicas": a_num(
    default=10,
    validators=[lambda x: x >= 1 or "Min 1 replica"]
)

# Then validate min <= max
async def _validate_config(self, config: Config) -> list[str]:
    if config.min_replicas > config.max_replicas:
        return ["min_replicas cannot exceed max_replicas"]
    return []
```

## Pattern 14: Feature Flags

Boolean flags for optional features:

```python
"monitoring_enabled": a_bool(default=True)
"backup_enabled": a_bool(default=False)
"auto_scaling_enabled": a_bool(default=False)
"encryption_enabled": a_bool(default=True)
```

## Pattern 15: Lifecycle Customization

Allow users to control lifecycle behavior:

```python
"lifecycle": a_obj({
    "prevent_destroy": a_bool(default=False),
    "create_before_destroy": a_bool(default=False),
    "ignore_changes": a_list(a_str(), default=[]),
}, description="Lifecycle configuration")
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Everything Required

```python
# Bad: Forces users to specify everything
"timeout": a_num(required=True)
"retries": a_num(required=True)
"buffer_size": a_num(required=True)

# Good: Sensible defaults
"timeout": a_num(default=30)
"retries": a_num(default=3)
"buffer_size": a_num(default=4096)
```

### ❌ Anti-Pattern 2: Too Many Top-Level Attributes

```python
# Bad: Flat namespace
"db_host": a_str()
"db_port": a_num()
"db_user": a_str()
"db_password": a_str()
"db_ssl": a_bool()

# Good: Grouped in object
"database": a_obj({
    "host": a_str(required=True),
    "port": a_num(default=5432),
    "username": a_str(required=True),
    "password": a_str(required=True, sensitive=True),
    "ssl": a_bool(default=True),
})
```

### ❌ Anti-Pattern 3: Unclear Computed Attributes

```python
# Bad: User might try to set these
"id": a_str()  # Should be computed
"status": a_str()  # Should be computed

# Good: Clearly marked as computed
"id": a_str(computed=True)
"status": a_str(computed=True)
```

### ❌ Anti-Pattern 4: No Validation

```python
# Bad: No validation
"port": a_num()
"email": a_str()

# Good: With validation
"port": a_num(validators=[lambda x: 1 <= x <= 65535])
"email": a_str(validators=[lambda x: "@" in x])
```

## Real-World Example

Complete resource combining multiple patterns:

```python
@register_resource("mycloud_api_gateway")
class ApiGatewayResource(BaseResource):

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # Pattern 1: Required + Computed ID
            "name": a_str(required=True),
            "id": a_str(computed=True),

            # Pattern 2: Defaults
            "port": a_num(default=443),
            "enabled": a_bool(default=True),

            # Pattern 3: Tags/Labels
            "tags": a_list(a_str(), default=[]),
            "labels": a_map(a_str(), default={}),

            # Pattern 6: Secret Management
            "api_key": a_str(required=True, sensitive=True),

            # Pattern 7: Status
            "status": a_str(computed=True),
            "health": a_str(computed=True),

            # Pattern 5: Repeated Blocks
            "route": b_list("route"),

            # Pattern 6: Optional Single Block
            "advanced": b_single("advanced"),
        })
```

## Related Documentation

- [Overview](overview.md) - Schema system introduction
- [Types](types.md) - Available types
- [Validators](validators.md) - Custom validation
- [Best Practices](best-practices.md) - Schema design guidelines
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Real examples

---

**Remember**: Good schema patterns make your provider intuitive and easy to use. Follow these patterns to create consistent, user-friendly resources.
