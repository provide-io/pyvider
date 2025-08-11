# Pyvider - Python Terraform Provider Framework

Pyvider is a comprehensive framework for building Terraform providers in Python. It enables Python developers to create infrastructure-as-code components without dealing with the complexity of the Terraform plugin protocol.

## Overview

Pyvider bridges the gap between Python's rich ecosystem and Terraform's infrastructure management capabilities by providing:

- **Native Python API** for building Terraform providers
- **Type-safe data models** using attrs and modern Python features
- **Built-in testing framework** with lifecycle contract validation
- **Encrypted private state management** for sensitive data
- **Full tfplugin6 protocol support** via gRPC

## Core Components

### Providers
Collections of related infrastructure components that configure authentication and shared settings.

### Resources
Manageable infrastructure objects with full CRUD lifecycle:
- Create
- Read
- Update
- Delete

### Data Sources
Read-only views of external APIs or services for fetching configuration data.

### Functions
Custom logic callable from Terraform configurations for calculations and transformations.

### Capabilities
Reusable components that extend provider functionality:
- Authentication strategies
- Logging and telemetry
- Caching mechanisms
- Error handling

## Architecture

Pyvider uses a hub-based architecture where components register themselves for discovery:

```python
from pyvider import Provider, Resource, hub

@provider
class MyProvider(Provider):
    """My infrastructure provider"""
    
@resource
class MyResource(Resource):
    """Manages my infrastructure resources"""
```

## Related Projects

- **[TofuSoup](../tofusoup)** - Testing and conformance suite for providers
- **[Flavor](../flavor)** - Optional packaging system for distributing providers as binaries
- **[wrkenv](../wrkenv)** - Development environment management

## Supporting Libraries

- **pyvider-cty** - Python implementation of Terraform's type system
- **pyvider-rpcplugin** - RPC plugin framework
- **pyvider-telemetry** - Structured logging and telemetry
- **pyvider-hcl** - HCL parsing and generation

## Requirements

- Python 3.12+
- Terraform 1.5+ or OpenTofu 1.6+

## Documentation

See the [docs](docs/) directory for comprehensive guides and API documentation.

## License

See LICENSE file for details.