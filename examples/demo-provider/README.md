# Demo Provider - Pyvider Example

A complete example Terraform provider built with **Pyvider**, demonstrating all major features of the framework.

## Features Demonstrated

This example provider showcases:

### ✅ Provider Configuration
- Provider-level configuration
- Sensitive attribute handling
- Optional parameters with defaults

### ✅ Resource Management (CRUD)
- **Create:** Provision new servers
- **Read:** Query server state
- **Update:** Modify server configuration
- **Delete:** Remove servers
- Computed attributes (IPs, timestamps)
- State management

### ✅ Data Sources
- Read-only queries
- Computed values
- External data integration

### ✅ Provider Functions
- Custom Terraform functions
- String manipulation
- Numeric calculations
- Type-safe parameters

### ✅ Best Practices
- Type-safe configuration with `attrs`
- Async/await patterns
- Clear schema definitions
- Comprehensive documentation

---

## Quick Start

### 1. Install Dependencies

```bash
cd examples/demo-provider
pip install pyvider
```

Or using `uv`:
```bash
uv sync
```

### 2. Install the Provider

Install the provider for local development:

```bash
pyvider install
```

This creates a symlink in your Terraform plugins directory:
```
~/.terraform.d/plugins/local/provide/demo/1.0.0/<platform>/
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Apply Configuration

```bash
terraform plan
terraform apply
```

### 5. Explore Outputs

```bash
terraform output
```

Example output:
```
web_server_id = "srv-000001"
web_server_public_ip = "54.1.1.1"
web_server_status = "running"
web_server_uptime = 42
web_tags_formatted = <<EOT
{
  "Environment": "production",
  "ManagedBy": "terraform",
  "Team": "platform"
}
EOT
estimated_monthly_cost = "$50.14"
```

---

## Project Structure

```
demo-provider/
├── provider.py          # Provider implementation
├── pyproject.toml       # Python project configuration
├── pyvider.toml         # Pyvider runtime configuration
├── example.tf           # Example Terraform configuration
└── README.md            # This file
```

---

## Provider Implementation

### Provider Definition

```python
@register_provider("demo")
class DemoProvider(BaseProvider):
    def __init__(self) -> None:
        super().__init__(
            metadata=ProviderMetadata(
                name="demo",
                version="1.0.0",
                protocol_version="6",
            )
        )

    @classmethod
    def get_schema(cls):
        return s_provider({
            "api_url": a_str(required=False),
            "api_token": a_str(required=False, sensitive=True),
            "timeout": a_num(required=False),
            "debug": a_bool(required=False),
        })
```

### Resource Definition

```python
@register_resource("server")
class DemoServer(BaseResource):
    @define
    class Config:
        name: str
        instance_type: str = "t2.micro"
        region: str = "us-east-1"

    @define
    class State:
        id: str
        name: str
        # ... other attributes
        public_ip: str  # Computed
        created_at: str  # Computed

    @classmethod
    def get_schema(cls):
        return s_resource({
            "id": a_str(computed=True),
            "name": a_str(required=True),
            "instance_type": a_str(optional=True),
            "public_ip": a_str(computed=True),
            # ... other attributes
        })

    async def _create_apply(self, ctx: ResourceContext):
        # Create logic here
        return state, None

    async def read(self, ctx: ResourceContext):
        # Read logic here
        return state

    async def _update_apply(self, ctx: ResourceContext):
        # Update logic here
        return state, None

    async def delete(self, ctx: ResourceContext):
        # Delete logic here
        pass
```

### Data Source Definition

```python
@register_data_source("server_info")
class DemoServerInfo(BaseDataSource):
    @define
    class Config:
        server_id: str

    @define
    class State:
        id: str
        name: str
        uptime_seconds: int

    @classmethod
    def get_schema(cls):
        return s_data_source({
            "server_id": a_str(required=True),
            "id": a_str(computed=True),
            "uptime_seconds": a_num(computed=True),
        })

    async def read(self, ctx):
        # Query logic here
        return state
```

### Function Definition

```python
@register_function("format_tags")
class FormatTagsFunction(BaseFunction):
    @classmethod
    def get_schema(cls):
        return s_function(
            description="Format tags as JSON",
            parameters=[
                FunctionParameter(name="tags", type=CtyMap(CtyString())),
                FunctionParameter(name="pretty", type=CtyBool()),
            ],
            return_type=FunctionReturnType(type=CtyString()),
        )

    async def call(self, tags: dict, pretty: bool = False):
        return json.dumps(tags, indent=2 if pretty else None)
```

---

## Terraform Usage

### Provider Configuration

```hcl
provider "demo" {
  api_url   = "https://api.demo.example.com"
  api_token = var.demo_api_token
  timeout   = 30
  debug     = true
}
```

### Resource Usage

```hcl
resource "demo_server" "web" {
  name          = "web-server-01"
  instance_type = "t2.small"
  region        = "us-east-1"

  tags = {
    Environment = "production"
    Team        = "platform"
  }

  enable_monitoring = true
}
```

### Data Source Usage

```hcl
data "demo_server_info" "web_info" {
  server_id = demo_server.web.id
}

output "uptime" {
  value = data.demo_server_info.web_info.uptime_seconds
}
```

### Function Usage

```hcl
locals {
  tags_json = provider::demo::format_tags(demo_server.web.tags, true)
  monthly_cost = provider::demo::calculate_cost("t2.small", 730)
}
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=provider

# Run specific test
pytest -k test_server_create
```

### Type Checking

```bash
mypy provider.py
```

### Linting

```bash
ruff check provider.py
ruff format provider.py
```

### Debugging

Enable debug logging in `pyvider.toml`:

```toml
[logging]
level = "DEBUG"
format = "json"
```

Or set environment variable:

```bash
export PYVIDER_LOG_LEVEL=DEBUG
terraform plan
```

---

## Architecture

### Component Flow

```
Terraform CLI
     ↓
  gRPC (Protocol v6)
     ↓
Pyvider Framework
     ↓
  Provider Handler
     ↓
  ┌─────────────────┬──────────────┬───────────────┐
  ↓                 ↓              ↓               ↓
Provider      Resources     Data Sources    Functions
(config)      (CRUD)        (read-only)     (compute)
  ↓                 ↓              ↓               ↓
        Your Implementation (provider.py)
```

### State Management

```
User Config (HCL) → Terraform → Provider → Python attrs → State
                                    ↓
                            Private State (encrypted)
                                    ↓
                              msgpack + AES-256
```

---

## Configuration Reference

### Provider Block

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `api_url` | string | No | API endpoint URL |
| `api_token` | string | No | Authentication token (sensitive) |
| `timeout` | number | No | Request timeout in seconds |
| `debug` | bool | No | Enable debug logging |

### Resource: demo_server

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `id` | string | No | Yes | Server ID |
| `name` | string | Yes | No | Server name |
| `instance_type` | string | No | No | Instance type (default: t2.micro) |
| `region` | string | No | No | AWS region (default: us-east-1) |
| `tags` | map(string) | No | No | Resource tags |
| `enable_monitoring` | bool | No | No | Enable monitoring (default: false) |
| `public_ip` | string | No | Yes | Public IP address |
| `private_ip` | string | No | Yes | Private IP address |
| `status` | string | No | Yes | Server status |
| `created_at` | string | No | Yes | Creation timestamp |

### Data Source: demo_server_info

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `server_id` | string | Yes | No | Server ID to query |
| `id` | string | No | Yes | Server ID |
| `name` | string | No | Yes | Server name |
| `instance_type` | string | No | Yes | Instance type |
| `region` | string | No | Yes | Region |
| `status` | string | No | Yes | Server status |
| `public_ip` | string | No | Yes | Public IP |
| `private_ip` | string | No | Yes | Private IP |
| `uptime_seconds` | number | No | Yes | Server uptime |

### Functions

#### format_tags(tags, pretty)

Format a map of tags as JSON string.

**Parameters:**
- `tags` (map(string)) - Tags to format
- `pretty` (bool) - Pretty print the JSON

**Returns:** string

#### calculate_cost(instance_type, hours_per_month)

Calculate estimated monthly cost.

**Parameters:**
- `instance_type` (string) - Instance type
- `hours_per_month` (number) - Expected hours per month

**Returns:** number

---

## Troubleshooting

### Provider Not Found

**Error:**
```
Error: Failed to query available provider packages
```

**Solution:**
Ensure the provider is installed:
```bash
pyvider install
ls -la ~/.terraform.d/plugins/local/provide/demo/
```

### Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'pyvider'
```

**Solution:**
Install pyvider in the same environment:
```bash
pip install pyvider
# or
uv sync
```

### State Encryption Errors

**Error:**
```
FrameworkConfigurationError: private_state_shared_secret is required
```

**Solution:**
Set the secret in `pyvider.toml` or environment variable:
```bash
export PYVIDER_PRIVATE_STATE_SHARED_SECRET="your-secret-key"
```

---

## Next Steps

### Extend This Provider

1. **Add More Resources**
   - Databases
   - Load balancers
   - Security groups

2. **Add More Data Sources**
   - Account information
   - Resource listings
   - Quotas and limits

3. **Add More Functions**
   - Validation functions
   - Transformation functions
   - Calculation functions

4. **Add Validators**
   - Custom validation logic
   - Cross-field validation
   - Business rule validation

### Production Deployment

1. **Build Binary**
   ```bash
   python scripts/build_provider.py
   ```

2. **Publish to Registry**
   - Sign the binary
   - Create GitHub release
   - Submit to Terraform Registry

3. **CI/CD Integration**
   - Automated testing
   - Automated releases
   - Version management

---

## Resources

### Documentation
- [Pyvider Documentation](https://foundry.provide.io/pyvider/)
- [Terraform Provider Protocol](https://developer.hashicorp.com/terraform/plugin/terraform-plugin-protocol)
- [Provider Development](https://developer.hashicorp.com/terraform/plugin)

### Examples
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - More examples
- [Official Providers](https://registry.terraform.io/browse/providers) - Terraform registry

### Community
- [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- [Issues](https://github.com/provide-io/pyvider/issues)

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.

---

**Made with ❤️ using [Pyvider](https://github.com/provide-io/pyvider)**
