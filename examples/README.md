# Pyvider Examples

Canonical runnable provider examples live in a dedicated public repo, alongside the blog tutorial series that walks through building one step by step.

## Building a Provider from Scratch

A four-part tutorial series on [pyvider.com](https://pyvider.com/posts/building-your-first-provider/) with runnable provider code at every step:

**Location**: [`demo-provider/`](https://github.com/provide-io/pyvider/tree/main/examples/demo-provider/)

### Clone and run

```bash
git clone https://github.com/provide-io/pyvider-tutorial.git
cd pyvider-tutorial/part1-resource
uv sync
uv run pyvider install
tofu init -upgrade
tofu apply -auto-approve
```

See the [demo-provider README](https://github.com/provide-io/pyvider/blob/main/examples/demo-provider/README.md) for complete documentation, verification steps, and troubleshooting.

### Reproducing the asciinema casts

The same repo includes the recording pipeline that produces the casts embedded in the blog posts:

```bash
cd pyvider-tutorial
./scripts/record-all.sh            # → ./casts/tutorial-part{1..4}-*.cast
```

Requires `asciinema`, `uv`, `tofu` (or `terraform`), and Python 3 on PATH.

## Why this repo doesn't ship a demo provider anymore

Earlier Pyvider releases shipped an `examples/demo-provider/` in this repository. It was redundant with the tutorial series above — and quietly out of date because no one was running `tofu apply` against it. Keeping two canonical "full working provider" examples in sync wasn't paying off. The tutorial repo is now the single source of truth; it's public, it's tested end-to-end against each pyvider release, and each step has prose alongside the code.

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
