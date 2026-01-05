# Demo Terraform Provider

A complete example of a Terraform provider built with Pyvider, demonstrating provider functions, resources, data sources, and best practices.

## Quick Start

```bash
# 1. Install dependencies
uv add --editable .

# 2. Install provider for Terraform
pyvider install

# 3. Initialize and test
terraform init
terraform plan
```

## Project Structure

```
demo-provider/
├── src/
│   └── demo/
│       ├── __init__.py      # Package init with main entry point
│       ├── provider.py      # Provider configuration
│       ├── resources.py     # Resource definitions (server, database, network)
│       ├── data_sources.py  # Data source definitions (regions, instance_types, server_info)
│       └── functions.py     # Function definitions (format_tags, calculate_cost, etc.)
├── tests/
│   └── test_provider.py     # Python tests for the provider
├── tf/
│   └── main.tf              # Sample Terraform configuration
├── terraform-provider-demo  # Entry point script
├── pyproject.toml           # Project metadata and pyvider configuration
├── pyvider.toml             # Runtime configuration (logging, secrets)
└── VERSION                  # Provider version
```

## Configuration

### pyproject.toml

```toml
[tool.pyvider]
provider_name = "demo"        # Name used in Terraform (local/providers/demo)

[tool.setuptools]
package-dir = {"" = "src"}
packages = ["demo"]

[project.entry-points."pyvider"]
demo = "demo"                  # Entry point for component discovery

[project.scripts]
terraform-provider-demo = "demo:main"  # CLI entry point
```

### pyvider.toml

Runtime configuration (logging, server settings, encryption secrets).

## Verification Steps

### 1. Uninstall (if previously installed)

```bash
pyvider install --uninstall
```

Expected output:
```
🗑️  Uninstalling provider...
  Provider script removed: ~/.terraform.d/plugins/local/providers/demo/1.0.0/darwin_arm64/terraform-provider-demo
✅ Provider uninstalled successfully
```

### 2. Verify removal

```bash
ls ~/.terraform.d/plugins/local/providers/demo/1.0.0/darwin_arm64/
```

Should be empty or show:
```
. ..
```

### 3. Install the provider

```bash
pyvider install
```

Expected output:
```
📦 Installing provider: demo
  Version: 1.0.0
  Platform: darwin_arm64
  Target: ~/.terraform.d/plugins/local/providers/demo/1.0.0/darwin_arm64
📝 Running in Development Mode.
  Script location: ~/.terraform.d/plugins/local/providers/demo/1.0.0/darwin_arm64/terraform-provider-demo
```

### 4. Verify installation

```bash
ls ~/.terraform.d/plugins/local/providers/demo/1.0.0/darwin_arm64/
```

Should show:
```
terraform-provider-demo
```

### 5. Initialize Terraform

```bash
cd tf
terraform init
```

Expected output includes:
```
Initializing provider plugins...
- Finding latest version of local/providers/demo...
- Installing local/providers/demo v1.0.0...
- Installed local/providers/demo v1.0.0
```

### 6. Run Terraform Plan

```bash
terraform plan
```

Expected output includes:
```
Changes to Outputs:
  + test_calculate_cost        = 33.872
  + test_format_tags           = jsonencode({...})
  + test_generate_name         = "web-prod-ue11-042"
  + test_validate_cidr_invalid = false
  + test_validate_cidr_valid   = true
```

## Provider Components

### Functions (4)

- **generate_name** - Generate standardized resource names
- **format_tags** - Format tags as JSON string
- **calculate_cost** - Calculate instance cost per month
- **validate_cidr** - Validate CIDR block format

### Data Sources (2)

- **regions** - List available cloud regions
- **instance_types** - List available instance types

### Resources (3)

- **server** - Manage virtual servers
- **database** - Manage databases
- **network** - Manage network configurations

## Environment Variables

Override provider name via environment variable:
```bash
export PYVIDER_PROVIDER_NAME=custom_name
pyvider install
```

## Reinstall (Common Workflow)

```bash
pyvider install --reinstall
cd tf
terraform init
terraform plan
```

## Troubleshooting

### "No providers found" error

Ensure the package is installed with entry points:
```bash
uv add --editable .
```

### Version mismatch in terraform init

Delete the lock file and reinitialize:
```bash
rm .terraform.lock.hcl
terraform init
```

### Provider name not being read

Check that `pyproject.toml` contains:
```toml
[tool.pyvider]
provider_name = "demo"
```

## Development

Run the Python test suite:
```bash
python tests/test_provider.py
```

Check provider components:
```bash
python -c "import sys; sys.path.insert(0, 'src'); import demo; from pyvider.hub import hub; print(hub.list_components())"
```
