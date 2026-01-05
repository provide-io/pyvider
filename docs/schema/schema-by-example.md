# Schema by Example

This guide walks you through building schemas from simple to complex, using real-world examples at each step.

## Starting Simple: A Basic Resource

Let's build a simple file resource:

### Step 1: Just a Name

```python
from pyvider.schema import s_resource, a_str

@classmethod
def get_schema(cls):
    return s_resource({
        "path": a_str(required=True, description="File path"),
    })
```

**Terraform:**
```hcl
resource "local_file" "example" {
  path = "/tmp/hello.txt"
}
```

### Step 2: Add Optional Content

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "path": a_str(required=True, description="File path"),
        "content": a_str(default="", description="File content"),
    })
```

**Terraform:**
```hcl
resource "local_file" "example" {
  path    = "/tmp/hello.txt"
  content = "Hello, World!"
}
```

### Step 3: Add Computed ID

```python
@classmethod
def get_schema(cls):
    return s_resource({
        # Inputs
        "path": a_str(required=True, description="File path"),
        "content": a_str(default="", description="File content"),

        # Outputs
        "id": a_str(computed=True, description="File ID"),
    })
```

**Terraform:**
```hcl
resource "local_file" "example" {
  path    = "/tmp/hello.txt"
  content = "Hello, World!"
}

output "file_id" {
  value = local_file.example.id
}
```

## Adding Complexity: Collections

### Lists of Strings

```python
from pyvider.schema import s_resource, a_str, a_list

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Server name"),
        "tags": a_list(
            a_str(),
            default=[],
            description="Resource tags"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  tags = ["production", "web", "public"]
}
```

### Maps of Strings

```python
from pyvider.schema import a_map

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Server name"),
        "labels": a_map(
            a_str(),
            default={},
            description="Key-value labels"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  labels = {
    environment = "production"
    team        = "platform"
    cost_center = "engineering"
  }
}
```

### Lists of Numbers

```python
from pyvider.schema import a_num

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Firewall rule name"),
        "ports": a_list(
            a_num(),
            default=[],
            description="Allowed ports"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_firewall_rule" "web" {
  name  = "web-ports"
  ports = [80, 443, 8080]
}
```

## Next Level: Nested Objects

### Simple Nested Object

```python
from pyvider.schema import a_obj, a_bool

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Server name"),
        "database": a_obj({
            "host": a_str(required=True, description="Database host"),
            "port": a_num(default=5432, description="Database port"),
            "ssl": a_bool(default=True, description="Enable SSL"),
        }, description="Database connection configuration"),
    })
```

**Terraform:**
```hcl
resource "mycloud_app" "api" {
  name = "api-server"

  database = {
    host = "db.example.com"
    port = 5432
    ssl  = true
  }
}
```

### List of Objects

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Load balancer name"),
        "endpoints": a_list(
            a_obj({
                "url": a_str(required=True, description="Endpoint URL"),
                "weight": a_num(default=100, description="Traffic weight"),
                "healthy": a_bool(default=True, description="Health status"),
            }),
            default=[],
            description="Backend endpoints"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_lb" "main" {
  name = "main-lb"

  endpoints = [
    {
      url    = "https://backend1.example.com"
      weight = 100
    },
    {
      url    = "https://backend2.example.com"
      weight = 50
    }
  ]
}
```

## Advanced: Using Blocks

### Single Optional Block

```python
from pyvider.schema import b_single

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Server name"),

        "logging": b_single("logging",
            attributes={
                "enabled": a_bool(default=True, description="Enable logging"),
                "level": a_str(default="INFO", description="Log level"),
                "destination": a_str(required=True, description="Log destination"),
            },
            description="Logging configuration"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_server" "web" {
  name = "web-server"

  logging {
    enabled     = true
    level       = "DEBUG"
    destination = "cloudwatch"
  }
}
```

### Multiple Repeatable Blocks

```python
from pyvider.schema import b_list

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Security group name"),

        "ingress_rule": b_list("ingress_rule",
            attributes={
                "from_port": a_num(required=True, description="Start port"),
                "to_port": a_num(required=True, description="End port"),
                "protocol": a_str(required=True, description="Protocol"),
                "cidr_blocks": a_list(a_str(), description="CIDR blocks"),
            },
            description="Ingress rules"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_security_group" "web" {
  name = "web-sg"

  ingress_rule {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress_rule {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Nested Blocks

```python
@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True, description="Server name"),

        "monitoring": b_single("monitoring",
            attributes={
                "enabled": a_bool(default=True, description="Enable monitoring"),
                "interval": a_num(default=60, description="Check interval (seconds)"),
            },
            block_types=[
                b_list("alert",
                    attributes={
                        "metric": a_str(required=True, description="Metric to monitor"),
                        "threshold": a_num(required=True, description="Alert threshold"),
                        "email": a_str(required=True, description="Alert email"),
                    },
                    description="Alert rules"
                )
            ],
            description="Monitoring configuration"
        ),
    })
```

**Terraform:**
```hcl
resource "mycloud_server" "web" {
  name = "web-server"

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

## Real-World Example: Complete Web Server

Let's build a complete, production-focused web server resource schema:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import (
    s_resource, a_str, a_num, a_bool, a_list, a_map,
    b_single, b_list, PvsSchema
)
import attrs

@attrs.define
class WebServerConfig:
    name: str
    instance_type: str = "t2.micro"
    ami: str | None = None

@attrs.define
class WebServerState:
    id: str
    name: str
    instance_type: str
    ami: str
    public_ip: str
    private_ip: str
    status: str
    created_at: str

@register_resource("web_server")
class WebServer(BaseResource):
    config_class = WebServerConfig
    state_class = WebServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # ===== BASIC CONFIGURATION =====
            "name": a_str(
                required=True,
                description="Server name (must be unique)"
            ),
            "instance_type": a_str(
                default="t2.micro",
                description="EC2 instance type"
            ),
            "ami": a_str(
                description="Amazon Machine Image ID (defaults to latest Ubuntu)"
            ),

            # ===== TAGS AND LABELS =====
            "tags": a_list(
                a_str(),
                default=[],
                description="Resource tags for organization"
            ),
            "labels": a_map(
                a_str(),
                default={},
                description="Key-value labels for metadata"
            ),

            # ===== NETWORK CONFIGURATION =====
            "network": b_single("network",
                attributes={
                    "vpc_id": a_str(
                        required=True,
                        description="VPC to launch server in"
                    ),
                    "subnet_id": a_str(
                        required=True,
                        description="Subnet for server placement"
                    ),
                    "public_ip": a_bool(
                        default=True,
                        description="Assign public IP address"
                    ),
                    "security_groups": a_list(
                        a_str(),
                        default=[],
                        description="Security group IDs"
                    ),
                },
                description="Network configuration"
            ),

            # ===== STORAGE CONFIGURATION =====
            "root_volume": b_single("root_volume",
                attributes={
                    "size": a_num(
                        default=20,
                        description="Root volume size in GB"
                    ),
                    "type": a_str(
                        default="gp3",
                        description="Volume type (gp2, gp3, io1, io2)"
                    ),
                    "encrypted": a_bool(
                        default=True,
                        description="Enable encryption"
                    ),
                },
                description="Root volume configuration"
            ),

            "data_volume": b_list("data_volume",
                attributes={
                    "size": a_num(
                        required=True,
                        description="Volume size in GB"
                    ),
                    "type": a_str(
                        default="gp3",
                        description="Volume type"
                    ),
                    "device": a_str(
                        required=True,
                        description="Device name (e.g., /dev/sdb)"
                    ),
                    "mount_point": a_str(
                        description="Mount point (e.g., /data)"
                    ),
                },
                description="Additional data volumes"
            ),

            # ===== APPLICATION CONFIGURATION =====
            "application": b_single("application",
                attributes={
                    "port": a_num(
                        default=8080,
                        description="Application port"
                    ),
                    "protocol": a_str(
                        default="HTTP",
                        description="Protocol (HTTP, HTTPS)"
                    ),
                    "health_check_path": a_str(
                        default="/health",
                        description="Health check endpoint"
                    ),
                },
                block_types=[
                    b_single("ssl",
                        attributes={
                            "cert_arn": a_str(
                                required=True,
                                description="SSL certificate ARN"
                            ),
                            "min_tls_version": a_str(
                                default="TLSv1.2",
                                description="Minimum TLS version"
                            ),
                        },
                        description="SSL/TLS configuration"
                    ),
                    b_list("environment_variable",
                        attributes={
                            "name": a_str(
                                required=True,
                                description="Variable name"
                            ),
                            "value": a_str(
                                required=True,
                                description="Variable value"
                            ),
                            "sensitive": a_bool(
                                default=False,
                                description="Mark as sensitive"
                            ),
                        },
                        description="Environment variables"
                    ),
                ],
                description="Application configuration"
            ),

            # ===== MONITORING & LOGGING =====
            "monitoring": b_single("monitoring",
                attributes={
                    "enabled": a_bool(
                        default=True,
                        description="Enable CloudWatch monitoring"
                    ),
                    "detailed": a_bool(
                        default=False,
                        description="Enable detailed monitoring (1-minute intervals)"
                    ),
                },
                block_types=[
                    b_list("alarm",
                        attributes={
                            "name": a_str(
                                required=True,
                                description="Alarm name"
                            ),
                            "metric": a_str(
                                required=True,
                                description="CloudWatch metric"
                            ),
                            "threshold": a_num(
                                required=True,
                                description="Threshold value"
                            ),
                            "comparison": a_str(
                                default="GreaterThanThreshold",
                                description="Comparison operator"
                            ),
                            "sns_topic": a_str(
                                description="SNS topic ARN for notifications"
                            ),
                        },
                        description="CloudWatch alarms"
                    )
                ],
                description="Monitoring configuration"
            ),

            # ===== COMPUTED OUTPUTS =====
            "id": a_str(
                computed=True,
                description="EC2 instance ID"
            ),
            "public_ip": a_str(
                computed=True,
                description="Public IP address"
            ),
            "private_ip": a_str(
                computed=True,
                description="Private IP address"
            ),
            "status": a_str(
                computed=True,
                description="Instance status (pending, running, stopped, terminated)"
            ),
            "created_at": a_str(
                computed=True,
                description="Creation timestamp"
            ),
        })

    async def _validate_config(self, config: WebServerConfig) -> list[str]:
        errors = []

        # Validate instance type
        valid_types = ["t2.micro", "t2.small", "t2.medium", "t3.micro", "t3.small"]
        if config.instance_type not in valid_types:
            errors.append(f"instance_type must be one of: {', '.join(valid_types)}")

        return errors

    async def read(self, ctx: ResourceContext) -> WebServerState | None:
        if not ctx.state:
            return None
        # Implementation here
        pass

    async def _create_apply(self, ctx: ResourceContext) -> tuple[WebServerState | None, None]:
        if not ctx.config:
            return None, None
        # Implementation here
        pass

    async def _update_apply(self, ctx: ResourceContext) -> tuple[WebServerState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None
        # Implementation here
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return
        # Implementation here
        pass
```

**Complete Terraform Example:**

```hcl
resource "mycloud_web_server" "production" {
  name          = "prod-web-01"
  instance_type = "t3.small"
  ami           = "ami-0c55b159cbfafe1f0"

  tags = ["production", "web", "critical"]

  labels = {
    environment = "production"
    team        = "platform"
    cost_center = "engineering"
    managed_by  = "terraform"
  }

  network {
    vpc_id          = "vpc-12345"
    subnet_id       = "subnet-67890"
    public_ip       = true
    security_groups = ["sg-web", "sg-ssh"]
  }

  root_volume {
    size      = 30
    type      = "gp3"
    encrypted = true
  }

  data_volume {
    size        = 100
    type        = "gp3"
    device      = "/dev/sdb"
    mount_point = "/var/www"
  }

  data_volume {
    size        = 50
    type        = "gp3"
    device      = "/dev/sdc"
    mount_point = "/var/log"
  }

  application {
    port              = 443
    protocol          = "HTTPS"
    health_check_path = "/api/health"

    ssl {
      cert_arn        = "arn:aws:acm:us-east-1:123456789:certificate/abcd-1234"
      min_tls_version = "TLSv1.3"
    }

    environment_variable {
      name  = "APP_ENV"
      value = "production"
    }

    environment_variable {
      name      = "DATABASE_URL"
      value     = "postgres://db.internal:5432/app"
      sensitive = true
    }
  }

  monitoring {
    enabled  = true
    detailed = true

    alarm {
      name       = "high-cpu"
      metric     = "CPUUtilization"
      threshold  = 80
      comparison = "GreaterThanThreshold"
      sns_topic  = "arn:aws:sns:us-east-1:123456789:alerts"
    }

    alarm {
      name       = "low-disk"
      metric     = "DiskSpaceUtilization"
      threshold  = 90
      comparison = "GreaterThanThreshold"
      sns_topic  = "arn:aws:sns:us-east-1:123456789:alerts"
    }
  }
}

# Use computed outputs
output "server_public_ip" {
  value = mycloud_web_server.production.public_ip
}

output "server_id" {
  value = mycloud_web_server.production.id
}
```

## Key Takeaways

1. **Start Simple** - Begin with required attributes, add complexity gradually
2. **Use Defaults** - Provide sensible defaults for optional attributes
3. **Organize Logically** - Group related attributes into blocks
4. **Validate Early** - Add validators to catch errors during planning
5. **Document Thoroughly** - Every attribute should have a clear description
6. **Use Appropriate Types** - Lists for ordered items, maps for key-value, blocks for nested structures
7. **Mark Computed Fields** - Clearly indicate what the provider generates vs what users provide

## See Also

- [Schema Overview](overview.md) - Complete schema system guide
- [Attributes](attributes.md) - All attribute types
- [Blocks](blocks.md) - Nested block patterns
- [Creating Resources](../guides/building-components/creating-resources.md) - Implementing resources
