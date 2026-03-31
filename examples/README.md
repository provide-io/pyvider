# Pyvider Examples

This directory contains working examples demonstrating Pyvider's capabilities for building Terraform providers in Python.

## Available Examples

### Demo Provider

**Location**: [`demo-provider/`](https://github.com/provide-io/pyvider/tree/main/examples/demo-provider/)

A comprehensive example showcasing all major Pyvider features:

- **Provider Configuration** - Setup and authentication patterns
- **Resources** (3) - Server, Database, and Network management with full CRUD operations
- **Data Sources** (2) - Regions and Instance Types for read-only queries
- **Functions** (4) - Utility functions for name generation, tag formatting, cost calculation, and CIDR validation

**Quick Start**:
```bash
cd demo-provider
uv sync
uv run pyvider install
cd tf
terraform init
terraform plan
```

See the [demo-provider README](https://github.com/provide-io/pyvider/blob/main/examples/demo-provider/README.md) for complete documentation, verification steps, and troubleshooting.

## Using the Examples

### Installation

Each example is a standalone Python package that can be installed with:

```bash
cd <example-directory>
uv sync
```

### Running Examples

1. **Install the provider**:
   ```bash
   uv run pyvider install
   ```

2. **Navigate to the Terraform configuration**:
   ```bash
   cd tf
   ```

3. **Initialize and test**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### Development Workflow

When making changes to a provider:

```bash
# Reinstall the provider
uv run pyvider install --reinstall

# Reinitialize Terraform
cd tf
rm .terraform.lock.hcl
terraform init
terraform plan
```

## Example Structure

Each example follows the standard Pyvider project structure:

```
example-provider/
├── src/
│   └── <provider_name>/
│       ├── __init__.py      # Package init with main entry point
│       ├── provider.py      # Provider configuration (optional)
│       ├── resources.py     # Resource definitions
│       ├── data_sources.py  # Data source definitions
│       └── functions.py     # Function definitions
├── tests/
│   └── test_*.py            # Python tests
├── tf/
│   └── main.tf              # Sample Terraform configuration
├── pyproject.toml           # Package metadata and pyvider configuration
├── pyvider.toml             # Runtime configuration (optional)
└── README.md                # Example documentation
```

## Key Configuration Files

### pyproject.toml

Defines the provider name and entry points:

```toml
[tool.pyvider]
provider_name = "demo"

[project.entry-points."pyvider"]
demo = "demo"

[project.scripts]
terraform-provider-demo = "demo:main"
```

### pyvider.toml (Optional)

Runtime configuration for logging, server settings, and secrets:

```toml
[logging]
level = "INFO"

[server]
port = 50051
```

## Learning Path

1. **Start with the Demo Provider** - Explore [`demo-provider/`](https://github.com/provide-io/pyvider/tree/main/examples/demo-provider/) to see all features in action
2. **Read the Documentation** - Visit [Getting Started](https://github.com/provide-io/pyvider/blob/main/docs/getting-started/index.md) for conceptual overview
3. **Follow the Quick Start** - Work through the [Quick Start Guide](https://github.com/provide-io/pyvider/blob/main/docs/getting-started/quick-start.md) for hands-on learning
4. **Review Core Concepts** - Understand the [architecture and patterns](https://github.com/provide-io/pyvider/blob/main/docs/explanation/architecture.md)
5. **Explore the API** - Dive into the [API Reference](https://github.com/provide-io/pyvider/blob/main/docs/api/index.md) for detailed documentation

## Common Patterns

### Component Registration

All components use decorators for self-registration:

```python
from pyvider import register_resource, ResourceBase

@register_resource("my_resource")
class MyResource(ResourceBase):
    """My custom resource."""
    # Implementation here
```

### Schema Definitions

Type-safe schemas using attrs:

```python
from attrs import define
from pyvider.schema import Field

@define
class MyResourceConfig:
    """Configuration for my resource."""
    name: str = Field(description="Resource name")
    enabled: bool = Field(default=False, description="Enable feature")
```

### Async Operations

Pyvider supports async/await for efficient I/O:

```python
async def create(self, config: MyResourceConfig) -> MyResourceState:
    """Create the resource."""
    # Async operations here
    result = await api_client.create_resource(config.name)
    return MyResourceState(id=result.id, name=config.name)
```

## Testing Examples

Each example includes Python tests demonstrating component testing:

```bash
cd <example-directory>
python tests/test_provider.py
```

For integration testing with Terraform, use the included `tf/` configurations.

## Troubleshooting

### Provider Not Found

Ensure the package is installed with entry points:
```bash
uv pip install -e .
pyvider install
```

### Version Mismatch

Delete the Terraform lock file and reinitialize:
```bash
rm .terraform.lock.hcl
terraform init
```

### Configuration Errors

Verify `pyproject.toml` contains the correct `[tool.pyvider]` configuration and entry points.

## Contributing Examples

To contribute a new example:

1. Follow the standard project structure
2. Include comprehensive README.md
3. Add Python tests in `tests/`
4. Provide working Terraform configuration in `tf/`
5. Document all components and usage patterns

## Additional Resources

- **[Pyvider Documentation](https://github.com/provide-io/pyvider/tree/main/docs/)** - Complete framework documentation
- **[Getting Started](https://github.com/provide-io/pyvider/blob/main/docs/getting-started/index.md)** - Introduction and installation
- **[Quick Start Guide](https://github.com/provide-io/pyvider/blob/main/docs/getting-started/quick-start.md)** - 5-minute tutorial
- **[API Reference](https://github.com/provide-io/pyvider/blob/main/docs/api/index.md)** - Detailed API documentation
- **[GitHub Repository](https://github.com/provide-io/pyvider)** - Source code and issues

---

**Ready to build your first provider?** Start with the [demo-provider](https://github.com/provide-io/pyvider/tree/main/examples/demo-provider/) example!
