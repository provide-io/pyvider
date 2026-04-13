# CLI Reference

The Pyvider CLI provides commands for managing providers, components, and configuration.

## Available Commands

### `pyvider provide`

Starts the provider in gRPC server mode for Terraform communication.

**Usage:**

```bash
pyvider provide [--force]
```

**Options:**

- `--force` - Force server mode ignoring magic cookie check (for testing)

**Description:** This is the default command when running the provider binary. Terraform automatically invokes this when using the provider. In development mode without the magic cookie, it displays interactive help.

______________________________________________________________________

### `pyvider components`

Manage and inspect Pyvider components.

#### `pyvider components list`

Lists all discovered components (providers, resources, data sources, functions).

**Usage:**

```bash
pyvider components list
```

**Output:**

```
Providers:
  - mycloud

Resources:
  - server
  - database

Data Sources:
  - image_catalog
```

#### `pyvider components show <type> <name>`

Shows detailed schema information for a specific component.

**Usage:**

```bash
pyvider components show <component_type> <component_name>
```

**Arguments:**

- `component_type` - Type of component (provider, resource, data_source, function)
- `component_name` - Name of the component

**Example:**

```bash
pyvider components show resource server
```

#### `pyvider components diagnostics`

Shows detailed autodiscovery diagnostics from the component hub.

**Usage:**

```bash
pyvider components diagnostics
```

**Output includes:**

- Total component count
- Component breakdown by type
- Discovery time
- Performance metrics

______________________________________________________________________

### `pyvider config`

Manage and display Pyvider configuration.

#### `pyvider config show`

Displays the current configuration from all sources (TOML files and environment variables).

**Usage:**

```bash
pyvider config show
```

**Shows:**

- TOML configuration file location and contents
- Environment variables (PYVIDER\_\*)
- Derived settings (OS, architecture, plugin directory)

______________________________________________________________________

### `pyvider install`

Installs the provider for use with Terraform.

**Usage:**

```bash
pyvider install
```

**Description:**

- In **binary mode**: Copies the executable to Terraform's plugin directory
- In **development mode**: Places a wrapper script that activates the venv and runs the provider

**Requirements:**
- Must be run from a directory containing `pyvider.toml` or `pyproject.toml` with `[tool.pyvider]` section
- In development mode, requires a virtual environment with Pyvider installed

- Must be run from a directory containing `pyvider.toml` or `pyproject.toml` with `[tool.pyvider]` section
- In development mode, requires a virtual environment with Pyvider installed

______________________________________________________________________

### `pyvider launch-context`

Display detailed information about how Pyvider was launched.

**Usage:**

```bash
pyvider launch-context [--format {human|json}] [--verbose]
```

**Options:**

- `--format` - Output format: `human` (default) or `json`
- `--verbose` - Show detailed environment information

**Description:** Analyzes the execution environment and reports:

- Launch method (PSPF package, script, module, editable install)
- Executable paths and Python environment
- Relevant environment variables
- Method-specific context details

**Example:**

```bash
pyvider launch-context --format json --verbose
```

______________________________________________________________________

## Global Options

These options are available for all commands:

- `--log-level {DEBUG|INFO|WARNING|ERROR}` - Set logging level
- `--log-format {json|key_value|console}` - Set log output format
- `--log-file PATH` - Write logs to file
- `--output {json|yaml|table|text}` - Set output format for command results

______________________________________________________________________

## Module API Reference
