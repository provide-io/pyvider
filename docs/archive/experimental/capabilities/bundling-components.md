# Bundling Components

> **Note**: Component bundling is currently under development. This documentation describes the planned functionality.

Component bundling allows you to package multiple related components (resources, data sources, functions) together for distribution and reuse.

## Overview

Bundled components can be:
- Distributed as Python packages
- Shared across multiple providers
- Version-controlled independently
- Composed with capabilities

## Creating a Bundle

Bundles are created as standard Python packages with proper entry points:

```python
# src/my_bundle/__init__.py
from pyvider.resources import register_resource
from pyvider.data_sources import register_data_source

@register_resource("bundled_resource")
class BundledResource:
    """A resource from the bundle."""
    pass

@register_data_source("bundled_data_source")
class BundledDataSource:
    """A data source from the bundle."""
    pass
```

## Package Structure

```
my-bundle/
├── pyproject.toml
├── src/
│   └── my_bundle/
│       ├── __init__.py
│       ├── resources/
│       ├── data_sources/
│       └── functions/
└── tests/
```

## Configuration in pyproject.toml

```toml
[project]
name = "my-pyvider-bundle"
version = "0.1.0"
dependencies = [
    "pyvider>=1.0.0",
]

[project.entry-points."pyvider.components"]
my_bundle = "my_bundle"
```

## Using Bundled Components

Install the bundle package:

```bash
pip install my-pyvider-bundle
```

The components will be automatically discovered by Pyvider through the entry points system.

## Example Bundles

See the [pyvider-components](https://github.com/provide-io/pyvider-components) repository for a comprehensive example of bundled components with:
- Resources (file_content, local_directory, etc.)
- Data sources (env_variables, file_info, http_api, etc.)
- Functions (string manipulation, numeric operations, jq transformations)
- Complete examples and documentation

## Related Documentation

- [Using Capabilities](using-capabilities.md)
- [Creating Capabilities](creating-capabilities.md)
- [Capability Composition](capability-composition.md)
