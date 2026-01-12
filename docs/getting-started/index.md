# Getting Started with Pyvider

Welcome to Pyvider! This guide will help you get started building Terraform providers in Python.

## What is Pyvider?

Pyvider is a Python framework for building Terraform providers. It lets you create fully functional Terraform providers using Python instead of Go, making provider development more accessible and leveraging Python's rich ecosystem.

## Key Features

- 🐍 **Build Providers in Python** - Use Python instead of Go for Terraform provider development
- 🔧 **Type-Safe Components** - Strong typing with attrs-based schema definitions
- ⚡ **Async-First Design** - Native async/await support for efficient I/O operations
- 🧩 **Component System** - Modular, reusable components with decorator-based registration
- 📊 **Protocol v6 Support** - Full Terraform Plugin Protocol v6 implementation
- 🔌 **gRPC Infrastructure** - Built on pyvider-rpcplugin for reliable communication

## Installation

### Using uv (Recommended)

```bash
uv add pyvider
```

## Quick Start

Ready to build your first provider? Check out the [Quick Start Guide](quick-start.md) for a hands-on introduction that walks you through creating a working provider in about 5 minutes!

## Documentation Structure

- **[Quick Start Guide](quick-start.md)** - Build your first provider in 5 minutes
- **[Core Concepts](../explanation/architecture.md)** - Understanding Pyvider architecture
- **[API Reference](../api/index.md)** - Complete API documentation
- **[Examples](../../examples/README.md)** - Working examples and patterns

## Prerequisites

Before getting started with Pyvider, you should have:

- ✅ Python 3.11 or higher installed
- ✅ Basic understanding of Terraform concepts (providers, resources, data sources)
- ✅ Familiarity with Python async/await patterns
- ✅ Basic knowledge of type hints and attrs

## Core Concepts

### Component Types

Pyvider supports four main component types:

1. **Providers** - Configure and authenticate provider instances
2. **Resources** - Manage infrastructure with full CRUD operations
3. **Data Sources** - Read-only queries for external data
4. **Functions** - Callable utilities for data transformation

### Hub-Based Discovery

Components self-register using decorators:

```python
from pyvider import register_resource, ResourceBase

@register_resource("my_resource")
class MyResource(ResourceBase):
    """My custom resource."""
    # Implementation here
```

### Schema System

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

## Architecture Overview

Pyvider is built on several key technologies:

- **Terraform Plugin Protocol v6** - Industry-standard provider protocol
- **gRPC** - High-performance RPC via pyvider-rpcplugin
- **attrs** - Type-safe data modeling
- **asyncio** - Efficient async operations
- **provide-foundation** - Logging, configuration, and utilities

## Example: Simple Data Source

Here's a minimal example to give you a taste of Pyvider:

```python
from attrs import define
from pyvider import register_data_source, DataSourceBase

@define
class EnvVarConfig:
    """Configuration for environment variable data source."""
    key: str

@define
class EnvVarData:
    """Output data for environment variable."""
    value: str | None

@register_data_source("env_var")
class EnvVarDataSource(DataSourceBase[EnvVarConfig, EnvVarData]):
    """Read environment variables."""

    async def read(self, config: EnvVarConfig) -> EnvVarData:
        import os
        return EnvVarData(value=os.getenv(config.key))
```

## Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/provide-io/pyvider/issues)
- **Documentation**: Comprehensive guides in the `docs/` directory
- **Examples**: Working examples in the `examples/` directory

## Related Projects

- **[pyvider-components](https://github.com/provide-io/pyvider-components)** - Example components library
- **[terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider)** - pre-release provider for testing
- **[pyvider-rpcplugin](https://github.com/provide-io/pyvider-rpcplugin)** - RPC plugin framework
- **[pyvider-cty](https://github.com/provide-io/pyvider-cty)** - CTY type system
- **[pyvider-hcl](https://github.com/provide-io/pyvider-hcl)** - HCL parsing

## Next Steps

1. **[Quick Start Guide](quick-start.md)** - Build your first provider
2. **[Core Concepts](../explanation/architecture.md)** - Understand Pyvider architecture
3. **[Examples](../../examples/README.md)** - Explore working examples
4. **[API Reference](../api/index.md)** - Dive into the API

---

**Ready to build your first provider?** Head over to the [Quick Start Guide](quick-start.md)!
