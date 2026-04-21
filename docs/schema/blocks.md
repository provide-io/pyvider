# Blocks

Blocks are nested structures in Terraform schemas that allow repeatable, complex configurations. Pyvider uses block factory functions to create nested blocks.

## What are Blocks?

Blocks in Terraform:
- **Group related attributes** into nested structures
- **Can repeat** (lists, sets, maps of blocks)
- **Can be optional or required**
- **Support nesting** (blocks within blocks)

## Block Factory Functions

Pyvider provides `b_*` factory functions:

```python
from pyvider.schema import (
    b_list,    # List of blocks (0 or more)
    b_single,  # Single block (0 or 1)
    b_set,     # Set of blocks
    b_map,     # Map of blocks
    b_group,   # Group block (exactly 1)
)
```

## Basic Example

### Single Block (0 or 1)

```python
from pyvider.schema import s_resource, a_str, a_num, b_single, PvsSchema

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True, description="Server name"),

        # Single optional configuration block
        "config": b_single("config",
            attributes={
                "timeout": a_num(default=30, description="Timeout seconds"),
                "retries": a_num(default=3, description="Retry attempts"),
            },
            description="Optional configuration settings"
        ),
    })
```

**Terraform usage:**

```hcl
resource "mycloud_server" "web" {
  name = "web-server"

  config {
    timeout = 60
    retries = 5
  }
}
```

### List of Blocks (0 or more)

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True, description="Load balancer name"),

        # List of listener blocks
        "listener": b_list("listener",
            attributes={
                "port": a_num(required=True, description="Listen port"),
                "protocol": a_str(required=True, description="Protocol"),
                "ssl_cert": a_str(description="SSL certificate ARN"),
            },
            description="Listener configuration"
        ),
    })
```

**Terraform usage:**

```hcl
resource "mycloud_lb" "main" {
  name = "main-lb"

  listener {
    port     = 80
    protocol = "HTTP"
  }

  listener {
    port     = 443
    protocol = "HTTPS"
    ssl_cert = "arn:aws:iam::..."
  }
}
```

## Block Types

### b_single - Optional Single Block

A block that can appear 0 or 1 times:

```python
"database": b_single("database",
    attributes={
        "host": a_str(required=True, description="Database host"),
        "port": a_num(default=5432, description="Database port"),
        "name": a_str(required=True, description="Database name"),
    },
    description="Database connection configuration"
)
```

### b_list - List of Blocks

Blocks that can appear 0 or more times, order preserved:

```python
"rule": b_list("rule",
    attributes={
        "port": a_num(required=True, description="Port number"),
        "protocol": a_str(required=True, description="Protocol"),
        "source": a_str(required=True, description="Source CIDR"),
    },
    description="Firewall rules"
)
```

### b_set - Set of Blocks

Blocks that can appear 0 or more times, no guaranteed order:

```python
"tag": b_set("tag",
    attributes={
        "key": a_str(required=True, description="Tag key"),
        "value": a_str(required=True, description="Tag value"),
    },
    description="Resource tags"
)
```

### b_map - Map of Blocks

Blocks indexed by a key:

```python
"endpoint": b_map("endpoint",
    attributes={
        "url": a_str(required=True, description="Endpoint URL"),
        "weight": a_num(default=100, description="Traffic weight"),
    },
    description="Named endpoints"
)
```

### b_group - Required Group Block

A block that must appear exactly once:

```python
"network": b_group("network",
    attributes={
        "vpc_id": a_str(required=True, description="VPC ID"),
        "subnet_id": a_str(required=True, description="Subnet ID"),
    },
    description="Network configuration (required)"
)
```

## Nested Blocks

Blocks can contain other blocks:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(required=True),

        # Outer block
        "security": b_single("security",
            attributes={
                "enabled": a_bool(default=True),
            },
            # Nested blocks inside security block
            block_types=[
                b_list("firewall_rule",
                    attributes={
                        "port": a_num(required=True),
                        "protocol": a_str(required=True),
                    }
                ),
                b_single("encryption",
                    attributes={
                        "algorithm": a_str(default="AES256"),
                        "key_id": a_str(required=True),
                    }
                ),
            ],
            description="Security configuration"
        ),
    })
```

**Terraform usage:**

```hcl
resource "mycloud_server" "web" {
  name = "web-server"

  security {
    enabled = true

    firewall_rule {
      port     = 80
      protocol = "TCP"
    }

    firewall_rule {
      port     = 443
      protocol = "TCP"
    }

    encryption {
      algorithm = "AES256"
      key_id    = "key-12345"
    }
  }
}
```

## Complete Example: Complex Resource

Here's a comprehensive example with multiple block types:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import (
    s_resource, a_str, a_num, a_bool, a_list,
    b_single, b_list, PvsSchema
)
import attrs

@attrs.define
class ServerConfig:
    name: str
    instance_type: str = "t2.micro"

@attrs.define
class ServerState:
    id: str
    name: str
    instance_type: str

@register_resource("server")
class Server(BaseResource):
    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # Simple attributes
            "name": a_str(required=True, description="Server name"),
            "instance_type": a_str(default="t2.micro", description="Instance type"),

            # Single optional block
            "network": b_single("network",
                attributes={
                    "vpc_id": a_str(required=True, description="VPC ID"),
                    "subnet_id": a_str(required=True, description="Subnet ID"),
                    "security_groups": a_list(a_str(), default=[], description="Security groups"),
                },
                description="Network configuration"
            ),

            # List of blocks
            "volume": b_list("volume",
                attributes={
                    "size": a_num(required=True, description="Volume size in GB"),
                    "type": a_str(default="gp3", description="Volume type"),
                    "device": a_str(required=True, description="Device name"),
                },
                description="EBS volumes to attach"
            ),

            # Nested blocks
            "monitoring": b_single("monitoring",
                attributes={
                    "enabled": a_bool(default=True, description="Enable monitoring"),
                    "interval": a_num(default=60, description="Check interval"),
                },
                block_types=[
                    b_list("alert",
                        attributes={
                            "metric": a_str(required=True, description="Metric name"),
                            "threshold": a_num(required=True, description="Alert threshold"),
                            "email": a_str(required=True, description="Alert email"),
                        },
                        description="Alert rules"
                    )
                ],
                description="Monitoring configuration"
            ),

            # Computed outputs
            "id": a_str(computed=True, description="Server ID"),
        })

    async def _validate_config(self, config: ServerConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        pass

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        pass

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass
```

**Terraform usage:**

```hcl
resource "mycloud_server" "web" {
  name          = "web-server"
  instance_type = "t2.small"

  network {
    vpc_id          = "vpc-12345"
    subnet_id       = "subnet-67890"
    security_groups = ["sg-11111", "sg-22222"]
  }

  volume {
    size   = 100
    type   = "gp3"
    device = "/dev/sdb"
  }

  volume {
    size   = 50
    type   = "io2"
    device = "/dev/sdc"
  }

  monitoring {
    enabled  = true
    interval = 30

    alert {
      metric    = "cpu_utilization"
      threshold = 80
      email     = "ops@example.com"
    }

    alert {
      metric    = "memory_utilization"
      threshold = 90
      email     = "ops@example.com"
    }
  }
}
```

## Accessing Block Data

In your resource implementation, blocks are converted to Python objects:

```python
@attrs.define
class NetworkBlock:
    vpc_id: str
    subnet_id: str
    security_groups: list[str]

@attrs.define
class VolumeBlock:
    size: int
    type: str
    device: str

@attrs.define
class ServerConfig:
    name: str
    instance_type: str = "t2.micro"
    network: NetworkBlock | None = None
    volume: list[VolumeBlock] | None = None

async def _create_apply(self, ctx: ResourceContext):
    if not ctx.config:
        return None, None

    # Access single block
    if ctx.config.network:
        vpc_id = ctx.config.network.vpc_id
        subnet_id = ctx.config.network.subnet_id

    # Access list of blocks
    if ctx.config.volume:
        for vol in ctx.config.volume:
            await self.api.attach_volume(
                size=vol.size,
                type=vol.type,
                device=vol.device
            )

    return State(id="server-123", name=ctx.config.name), None
```

## Block Validation

Validate block contents in your resource:

```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    errors = []

    # Validate single block
    if config.network:
        if not config.network.vpc_id.startswith("vpc-"):
            errors.append("VPC ID must start with 'vpc-'")

    # Validate list of blocks
    if config.volume:
        if len(config.volume) > 10:
            errors.append("Maximum 10 volumes allowed")

        for i, vol in enumerate(config.volume):
            if vol.size < 1 or vol.size > 16384:
                errors.append(f"Volume {i}: size must be 1-16384 GB")

    return errors
```

## Block Best Practices

### 1. Use Descriptive Block Names

```python
# ✅ Good: Clear block name
"health_check": b_single("health_check", ...)

# ❌ Bad: Vague name
"config": b_single("config", ...)
```

### 2. Choose Appropriate Block Type

```python
# ✅ Good: List for ordered items
"listener": b_list("listener", ...)

# ✅ Good: Single for optional config
"logging": b_single("logging", ...)

# ✅ Good: Set for unordered unique items
"tag": b_set("tag", ...)
```

### 3. Limit Nesting Depth

```python
# ✅ Good: 2 levels of nesting
"monitoring": b_single("monitoring",
    block_types=[b_list("alert", ...)]
)

# ❌ Bad: Too deeply nested (3+ levels)
"config": b_single("config",
    block_types=[
        b_single("advanced",
            block_types=[
                b_list("option", ...)  # Too deep!
            ]
        )
    ]
)
```

### 4. Provide Good Descriptions

```python
"listener": b_list("listener",
    attributes={
        "port": a_num(required=True, description="TCP port to listen on (1-65535)"),
        "protocol": a_str(required=True, description="Protocol (HTTP, HTTPS, TCP)"),
    },
    description="Load balancer listener configuration. Define one block per listener."
)
```

### 5. Make Blocks Optional When Appropriate

```python
# ✅ Good: Optional monitoring configuration
"monitoring": b_single("monitoring", ...)  # Can be omitted

# ❌ Bad: Required block for optional feature
"monitoring": b_group("monitoring", ...)  # Forces users to configure
```

## Common Patterns

### Configuration Blocks

```python
"database": b_single("database",
    attributes={
        "host": a_str(required=True),
        "port": a_num(default=5432),
        "ssl": a_bool(default=True),
    }
)
```

### Repeatable Rule Blocks

```python
"ingress_rule": b_list("ingress_rule",
    attributes={
        "from_port": a_num(required=True),
        "to_port": a_num(required=True),
        "protocol": a_str(required=True),
        "cidr_blocks": a_list(a_str()),
    }
)
```

### Nested Configuration

```python
"backup": b_single("backup",
    attributes={
        "enabled": a_bool(default=False),
    },
    block_types=[
        b_single("schedule",
            attributes={
                "frequency": a_str(default="daily"),
                "time": a_str(default="02:00"),
            }
        )
    ]
)
```

## See Also

- [Schema Overview](overview.md) - Complete schema system guide
- [Attributes](attributes.md) - Attribute types and options
- [Best Practices](best-practices.md) - Schema design guidelines
- [Creating Resources](../guides/building-components/creating-resources.md) - Using blocks in resources
