# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Set up development environment (creates venv, installs dependencies)
source ./env.sh

# Alternative for PowerShell
. ./env.ps1
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/path/to/test_file.py

# Run with coverage
pytest --cov=pyvider

# Run tests in parallel
pytest -n auto

# Run specific test by name
pytest -k "test_name"

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code
ruff format

# Lint code
ruff check

# Auto-fix linting issues
ruff check --fix

# Type checking with mypy
mypy src/pyvider

# Type checking with pyright
pyright
```

### Building & Packaging
```bash
# Build distribution packages
uv build

# Build provider binary using flavor
python scripts/build_provider.py

# Install in editable mode
uv pip install -e .
```

### Development Tools
```bash
# pyvider CLI
pyvider --help

# Check component registry
pyvider components list

# Launch provider service
pyvider provide
```

## Architecture Overview

### Core Component Model
Pyvider uses a **hub-based discovery system** where components self-register via decorators:

- **Provider**: Entry point that configures authentication and shared settings (`@provider` decorator)
- **Resources**: CRUD lifecycle management for infrastructure (`@resource` decorator)  
- **Data Sources**: Read-only data fetchers (`@data_source` decorator)
- **Functions**: Callable logic for transformations (`@function` decorator)
- **Ephemerals**: Short-lived resources with open/renew/close lifecycle (`@ephemeral` decorator)

### Protocol Layer
The `protocols/tfprotov6/` directory implements the Terraform Plugin Protocol v6:
- gRPC service implementation via `service.py`
- Handler functions for each RPC method in `handlers/`
- Protocol buffer definitions in `protobuf/`

### Schema System
Located in `schema/`, provides type-safe data modeling:
- Attributes with validation via `types/attribute.py`
- Nested blocks support via `types/blocks.py`
- Schema factory for building definitions in `factory.py`
- Transformation utilities in `transforms.py`

### Conversion Layer
The `conversion/` module handles bidirectional data transformation:
- CTY (Terraform's type system) to Python native types
- Protocol buffer message marshaling
- Schema adaptation between formats

### State Management
- **Private State**: Encrypted storage for sensitive provider data via `resources/private_state.py`
- Encryption handled by `common/encryption.py` using cryptography library

### Capabilities System
Reusable, composable components in `capabilities/`:
- Base capability protocol in `base.py`
- Decorator-based registration in `decorators.py`
- Can extend providers, resources, and other components

## Key Development Patterns

### Component Registration
Components must use decorators to register with the hub:
```python
from pyvider import provider, resource, data_source, function

@provider
class MyProvider(Provider):
    pass

@resource  
class MyResource(Resource):
    pass
```

### Schema Definition
Use attrs-based models with type annotations:
```python
import attrs
from pyvider.schema import Schema, Attribute

@attrs.define
class ResourceConfig:
    name: str = Attribute(required=True, description="Resource name")
```

### Testing Approach
- Unit tests for individual components
- Integration tests for protocol handlers
- Property-based testing with Hypothesis
- TDD test files prefixed with `test_tdd_`

## Important Notes

- **Python 3.11+ required** (moving from 3.12+ to broaden compatibility)
- Uses `uv` for fast dependency management
- Protocol buffer files (`*pb2*.py`) are auto-generated - do not edit directly
- Environment-specific virtual environments in `workenv/` directory
- Sibling projects: TofuSoup (testing), Flavor (packaging), wrkenv (dev environment)

## Testing Verification
After making changes, always run:
```bash
# Lint and format check
ruff check
ruff format --check

# Type checking  
mypy src/pyvider

# Tests
pytest
```

## Rebuild flavor helpers every time before testing/verifying to ensure accuracy