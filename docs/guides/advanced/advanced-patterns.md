# 🚀 Advanced Patterns & Examples

This comprehensive guide covers advanced patterns, techniques, and best practices for building sophisticated Terraform providers with Pyvider.

## Terraform Meta-Arguments

### `depends_on` - Explicit Dependencies

The `depends_on` meta-argument creates explicit dependencies between resources when implicit dependencies aren't sufficient:

```terraform
resource "mycloud_database" "main" {
  name = "production"
  size = "large"
}

resource "mycloud_backup_policy" "db_backup" {
  database_id = mycloud_database.main.id
  schedule    = "daily"

  # Explicit dependency ensures database is fully configured
  depends_on = [mycloud_database.main]
}
```

**Provider Implementation:**
```python
class BackupPolicy(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # The depends_on is handled by Terraform
        # Resource creation happens after dependencies
        state = await self._create_backup_policy(ctx.config)
        return state, None
```

### `count` - Multiple Instances

Create multiple instances of a resource using `count`:

```terraform
variable "server_count" {
  default = 3
}

resource "mycloud_server" "web" {
  count = var.server_count

  name = "web-${count.index}"
  size = "medium"

  # Access specific instance: mycloud_server.web[0]
}

# Use all instances
output "server_ips" {
  value = mycloud_server.web[*].ip_address
}
```

### `for_each` - Map/Set Based Instances

Create resources based on maps or sets:

```terraform
variable "environments" {
  default = {
    dev = "t2.micro"
    staging = "t3.small"
    prod = "t3.large"
  }
}

resource "mycloud_server" "app" {
  for_each = var.environments

  name = "app-${each.key}"
  size = each.value

  tags = {
    environment = each.key
  }
}

# Access: mycloud_server.app["dev"]
```

## Composing Resources and Functions

### Complex Resource Composition

```terraform
# Generate secure password
resource "random_password" "db_pass" {
  length  = 32
  special = true
}

# Create database with generated password
resource "mycloud_database" "main" {
  name     = "production"
  password = random_password.db_pass.result
}

# Store connection string using function
resource "mycloud_secret" "db_connection" {
  name = "db-connection-string"
  value = mycloud_format_connection_string(
    host     = mycloud_database.main.endpoint,
    port     = mycloud_database.main.port,
    database = mycloud_database.main.name,
    username = "admin",
    password = random_password.db_pass.result
  )
}
```

**Provider Implementation:**
```python
@register_function(name="format_connection_string")
class FormatConnectionString(BaseFunction):
    @attrs.define
    class Input:
        host: str = a_str(required=True)
        port: int = a_num(required=True)
        database: str = a_str(required=True)
        username: str = a_str(required=True)
        password: str = a_str(required=True, sensitive=True)

    @attrs.define
    class Output:
        connection_string: str = a_str(sensitive=True)

    async def call(self, input: Input) -> Output:
        conn_str = (
            f"postgresql://{input.username}:{input.password}"
            f"@{input.host}:{input.port}/{input.database}"
        )
        return self.Output(connection_string=conn_str)
```

### Data Source Chaining

```terraform
# Find latest AMI
data "mycloud_ami" "ubuntu" {
  filters = {
    name = "ubuntu-22.04-*"
    architecture = "x86_64"
  }

  most_recent = true
}

# Use AMI in server configuration
resource "mycloud_server" "app" {
  ami = data.mycloud_ami.ubuntu.id
  size = "t3.medium"

  user_data = templatefile("${path.module}/init.sh", {
    ami_name = data.mycloud_ami.ubuntu.name
    ami_created = data.mycloud_ami.ubuntu.created_at
  })
}
```

## Dynamic Configuration Patterns

### Dynamic Blocks

```terraform
resource "mycloud_firewall" "web" {
  name = "web-firewall"

  # Static rule
  rule {
    priority = 100
    action   = "allow"
    source   = "10.0.0.0/8"
    port     = 22
  }

  # Dynamic rules from variable
  dynamic "rule" {
    for_each = var.allowed_ports
    content {
      priority = rule.value.priority
      action   = "allow"
      source   = rule.value.source
      port     = rule.value.port
    }
  }
}
```

**Provider Schema:**
```python
from pyvider.schema import a_str, a_num, b_list

@attrs.define
class FirewallConfig:
    name: str = a_str(required=True)
    rule: list[Rule] = b_list(
        "rule",
        Rule,  # Nested attrs class
        min_items=1
    )

@attrs.define
class Rule:
    priority: int = a_num(required=True)
    action: str = a_str(required=True)
    source: str = a_str(required=True)
    port: int = a_num(required=True)
```

### Conditional Resources

```terraform
variable "enable_monitoring" {
  type    = bool
  default = false
}

resource "mycloud_monitoring" "server" {
  count = var.enable_monitoring ? 1 : 0

  target_id = mycloud_server.main.id
  metrics   = ["cpu", "memory", "disk"]
}

# Safe reference to optional resource
output "monitoring_dashboard" {
  value = try(mycloud_monitoring.server[0].dashboard_url, "Monitoring not enabled")
}
```

## State Management Patterns

### Import Existing Resources

Support importing existing infrastructure:

```python
class Server(BaseResource):
    async def import_resource(self, id: str) -> State:
        """Import existing server by ID."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        try:
            server = await provider.api.get_server(id)
            return self.State(
                id=server.id,
                name=server.name,
                size=server.instance_type,
                ip_address=server.public_ip,
                status=server.status
            )
        except NotFoundError:
            raise ResourceError(f"Server {id} not found")
```

**Terraform Usage:**
```bash
# Import existing server
terraform import mycloud_server.imported i-1234567890abcdef0
```

### State Migration

Handle schema changes gracefully:

```python
class Database(BaseResource):
    @attrs.define
    class State:
        # Version 2 schema
        id: str = a_str(computed=True)
        name: str = a_str()
        size: str = a_str()
        # New field in v2
        backup_enabled: bool = a_bool(default=False)

    async def read(self, state: State) -> State:
        """Read with state migration."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        db = await provider.api.get_database(state.id)

        # Migrate from v1 to v2
        if not hasattr(state, 'backup_enabled'):
            state.backup_enabled = db.backup_config is not None

        return state
```

## Provider Capabilities

### Cross-Resource References

Share data between resources:

```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        # Shared cache for cross-resource data
        self.resource_cache = {}

    def cache_resource(self, key: str, data: dict):
        """Cache resource data for other resources."""
        self.resource_cache[key] = data

    def get_cached(self, key: str) -> dict | None:
        """Retrieve cached resource data."""
        return self.resource_cache.get(key)
```

### Resource Tagging System

Implement consistent tagging:

```python
from pyvider.capabilities import register_capability

@register_capability("taggable")
class TaggableCapability:
    """Adds tagging support to resources."""

    def build_tags(self, base_tags: dict, extra_tags: dict) -> dict:
        """Merge and validate tags."""
        # Add default tags
        tags = {
            "ManagedBy": "Terraform",
            "Provider": "MyCloud",
            "CreatedAt": datetime.utcnow().isoformat()
        }
        tags.update(base_tags)
        tags.update(extra_tags)

        # Validate tag limits
        if len(tags) > 50:
            raise ValidationError("Maximum 50 tags allowed")

        return tags

# Apply to resources
@register_resource("server", capabilities=["taggable"])
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        tags = self.capabilities.taggable.build_tags(
            ctx.config.tags,
            {"ResourceType": "Server"}
        )
        # Use tags in creation...
        return State(...), None
```

## Advanced Validation

### Custom Validators

```python
from pyvider.schema import a_str, a_list

def validate_cidr(value: str) -> None:
    """Validate CIDR notation."""
    import ipaddress
    try:
        ipaddress.ip_network(value)
    except ValueError as e:
        raise ValidationError(f"Invalid CIDR: {e}")

@attrs.define
class NetworkConfig:
    cidr_block: str = a_str(
        required=True,
        validators=[validate_cidr]
    )

    allowed_cidrs: list[str] = a_list(
        a_str(validators=[validate_cidr]),
        min_items=1
    )
```

### Cross-Field Validation

```python
@attrs.define
class DatabaseConfig:
    engine: str = a_str(required=True)
    version: str = a_str(required=True)

    def __attrs_post_init__(self):
        """Validate field combinations."""
        valid_versions = {
            "postgres": ["13", "14", "15"],
            "mysql": ["5.7", "8.0"],
            "mariadb": ["10.6", "10.11"]
        }

        if self.engine not in valid_versions:
            raise ValidationError(f"Unsupported engine: {self.engine}")

        if self.version not in valid_versions[self.engine]:
            raise ValidationError(
                f"Invalid version {self.version} for {self.engine}"
            )
```

## Testing Advanced Scenarios

### Integration Testing

```python
import pytest
from pyvider.resources.context import ResourceContext
from mycloud_provider.resources import Network, Subnet, NetworkConfig, SubnetConfig

@pytest.mark.integration
async def test_resource_dependencies():
    """Test complex resource dependencies."""
    network_resource = Network()
    subnet_resource = Subnet()

    # Create parent resource
    network_state, _ = await network_resource._create_apply(
        ResourceContext(config=NetworkConfig(cidr="10.0.0.0/16"))
    )

    # Create dependent resource
    subnet_state, _ = await subnet_resource._create_apply(
        ResourceContext(
            config=SubnetConfig(network_id=network_state.id, cidr="10.0.1.0/24")
        )
    )

    # Verify relationship
    assert subnet_state.network_id == network_state.id

    # Test deletion order
    await subnet_resource._delete_apply(ResourceContext(state=subnet_state))
    await network_resource._delete_apply(ResourceContext(state=network_state))
```

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(
    port=st.integers(min_value=1, max_value=65535),
    protocol=st.sampled_from(["tcp", "udp", "icmp"])
)
def test_firewall_rule_validation(port, protocol):
    """Test firewall rules with random inputs."""
    rule = FirewallRule(
        port=port,
        protocol=protocol,
        action="allow"
    )

    # Should always produce valid rule
    assert rule.port == port
    assert rule.protocol in ["tcp", "udp", "icmp"]
```

## Performance Optimization

### Batch Operations

```python
class ServerGroup(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        """Create multiple servers efficiently."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Batch API call
        servers = await provider.api.create_servers_batch(
            [
                {"name": f"{ctx.config.name}-{i}", "size": ctx.config.size}
                for i in range(ctx.config.count)
            ]
        )

        return State(
            server_ids=[s.id for s in servers],
            count=len(servers)
        ), None
```

### Caching and Memoization

```python
from functools import lru_cache

class ImageDataSource(BaseDataSource):
    @lru_cache(maxsize=128)
    async def get_image_by_name(self, name: str) -> Image:
        """Cache image lookups."""
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        return await provider.api.find_image(name)

    async def read(self, config: Config) -> State:
        # Uses cached result if called multiple times
        image = await self.get_image_by_name(config.name)
        return State(id=image.id, name=image.name)
```

## Security Patterns

### Secret Management

```python
from pyvider.resources.private_state import encrypt_value, decrypt_value

class ApiKey(BaseResource):
    @attrs.define
    class PrivateState:
        """Encrypted state storage."""
        encrypted_key: str = a_str()

    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, PrivateState | None]:
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Generate API key
        api_key = await provider.generate_api_key()

        # Store encrypted
        private_state = self.PrivateState(
            encrypted_key=encrypt_value(api_key.secret)
        )

        return State(
            id=api_key.id,
            name=ctx.config.name,
            # Don't store secret in regular state
        ), private_state

    async def read(self, state: State) -> State:
        # Decrypt when needed
        secret = decrypt_value(self.private_state.encrypted_key)
        # Use secret...
        return state
```

## Related Documentation

- [Provider Lifecycle](../advanced/provider-lifecycle.md) - Detailed lifecycle documentation
- [Testing Providers](../development/testing-providers.md) - Comprehensive testing guide
- [Best Practices](../production/best-practices.md) - General best practices
- [Schema System](../../explanation/schema-system.md) - Schema details
- [Error Handling](../development/error-handling.md) - Error management patterns
