# 🛠️ Development Guide

This guide covers everything you need to contribute to Pyvider or set up a development environment for building providers.

## 📋 Prerequisites

- Python 3.11 or higher
- Git
- Make (optional but recommended)
- Docker (for integration testing)

## 🚀 Quick Setup

```bash
# Clone the repository
git clone https://github.com/provide-io/pyvider.git
cd pyvider

# Set up development environment with uv
uv sync

# Verify installation
uv run pyvider --version
uv run pytest --version
uv run ruff --version
```

## 📁 Project Structure

```
pyvider/
├── src/
│   └── pyvider/
│       ├── __init__.py           # Namespace package
│       ├── capabilities/         # Capability system
│       ├── cli/                  # Command-line interface
│       ├── common/               # Shared utilities
│       ├── conversion/           # Type conversion layer
│       ├── data_sources/         # Data source base classes
│       ├── ephemerals/          # Ephemeral resource support
│       ├── exceptions/          # Custom exceptions
│       ├── functions/           # Provider functions
│       ├── hub/                 # Component registry
│       ├── protocols/           # Protocol implementation
│       │   └── tfprotov6/      # Terraform Protocol v6
│       ├── providers/           # Provider base classes
│       ├── resources/           # Resource base classes
│       └── schema/             # Schema system
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test fixtures
├── docs/                       # Documentation
├── examples/                   # Example providers
├── scripts/                    # Build and utility scripts
├── pyproject.toml             # Project configuration
└── README.md                  # Project README
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyvider --cov-report=html

# Run specific test file
pytest tests/test_resources.py

# Run specific test
pytest tests/test_resources.py::test_create_resource

# Run tests in parallel
pytest -n auto

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

### Test Categories

- **Unit Tests**: Fast, isolated tests for individual components
- **Integration Tests**: Test component interactions
- **Protocol Tests**: Verify protocol implementation
- **E2E Tests**: Full provider testing with Terraform

### Writing Tests

```python
# tests/test_my_resource.py
import pytest
from pyvider.resources.context import ResourceContext
from my_provider.resources import MyResource


class TestMyResource:
    """Test suite for MyResource."""

    @pytest.fixture
    def resource(self) -> MyResource:
        return MyResource()

    async def test_create_resource(self, resource):
        """Test resource creation."""
        ctx = ResourceContext(
            config=MyResource.Config(name="test-resource", size=10)
        )
        state, _ = await resource._create_apply(ctx)

        assert state is not None
        assert state.id is not None
        assert state.name == "test-resource"

    async def test_read_missing_resource(self, resource):
        """Test reading non-existent resource."""
        ctx = ResourceContext(state=MyResource.State(id="missing", name="", size=0))
        assert await resource.read(ctx) is None
```

### Test Fixtures

```python
# tests/conftest.py
import pytest
from pyvider.hub import ComponentHub

@pytest.fixture
async def hub():
    """Provide a fresh component hub."""
    hub = ComponentHub()
    await hub.discover_all()
    return hub

@pytest.fixture
def mock_provider():
    """Provide a mock provider instance."""
    from tests.mocks import MockProvider
    return MockProvider()
```

## 🔍 Code Quality

### Linting

```bash
# Run linter
ruff check

# Auto-fix issues
ruff check --fix

# Format code
ruff format

# Check formatting
ruff format --check
```

### Type Checking

```bash
# Run mypy
mypy src/pyvider

# Run pyright
pyright

# Type check specific module
mypy src/pyvider/resources
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

Configuration in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 🏗️ Building

### Build Distribution

```bash
# Build wheel and sdist
python -m build

# Output in dist/
# - pyvider-1.0.0-py3-none-any.whl
# - pyvider-1.0.0.tar.gz
```

### Build Provider Binary

```bash
# Build with flavor
python scripts/build_provider.py

# Creates standalone binary
# - terraform-provider-pyvider
```

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

Follow the coding standards:

```python
# Good: Clear, typed, documented
from pyvider.resources import BaseResource
from pyvider.schema import Attribute
import attrs

@register_resource("my_resource")
class MyResource(BaseResource):
    """Manages my custom resource.
    
    This resource provides...
    """
    
    @attrs.define
    class Config:
        """Resource configuration."""
        name: str = Attribute(
            required=True,
            description="Resource name"
        )
```

### 3. Test Your Changes

```bash
# Run tests
pytest tests/

# Check coverage
pytest --cov=pyvider --cov-report=term-missing
```

### 4. Update Documentation

```bash
# Build docs locally
mkdocs serve

# View at http://localhost:11003
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add support for custom resources

- Implement BaseCustomResource class
- Add validation for custom attributes
- Update documentation"
```

### 6. Push and Create PR

```bash
git push origin feature/my-feature
# Create pull request on GitHub
```

## 🐛 Debugging

### Enable Debug Logging

```bash
# Set environment variables
export PYVIDER_LOG_LEVEL=DEBUG
export FOUNDATION_LOG_LEVEL=DEBUG

# Run with debug output
pyvider provide --debug
```

### Using Python Debugger

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

### VS Code Debugging

`.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Pyvider",
            "type": "python",
            "request": "launch",
            "module": "pyvider.cli",
            "args": ["provide", "--debug"],
            "env": {
                "PYVIDER_LOG_LEVEL": "DEBUG"
            }
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-xvs", "${file}"]
        }
    ]
}
```

### Performance Profiling

```bash
# Profile with cProfile
python -m cProfile -o profile.stats myscript.py

# Analyze with snakeviz
snakeviz profile.stats

# Memory profiling with memray
memray run -o output.bin python myscript.py
memray flamegraph output.bin
```

## 🔧 Environment Variables

### Development Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYVIDER_LOG_LEVEL` | Logging level | `INFO` |
| `PYVIDER_PLUGIN_DIR` | Plugin directory | `~/.terraform.d/plugins` |
| `PYVIDER_PROFILE` | Enable profiling | `0` |
| `PYVIDER_DEBUG_GRPC` | Debug gRPC calls | `0` |
| `FOUNDATION_LOG_LEVEL` | Foundation log level | `INFO` |
| `FOUNDATION_LOG_FORMAT` | Log format | `console` |

### Testing Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTEST_TIMEOUT` | Test timeout | `300` |
| `PYTEST_PARALLEL` | Parallel workers | `auto` |
| `COVERAGE_THRESHOLD` | Min coverage % | `80` |

## 📦 Dependencies

### Core Dependencies

- `attrs>=25.1.0` - Class definitions
- `grpcio>=1.73.0` - gRPC communication
- `cryptography>=42.0.8` - State encryption
- `provide-foundation` - Logging framework
- `pyvider-cty>=0.0.113` - CTY type system
- `pyvider-rpcplugin>=0.0.112` - RPC plugin support

### Development Dependencies

- `pytest>=8.3.0` - Testing framework
- `pytest-asyncio>=0.25.0` - Async test support
- `pytest-cov>=6.0.0` - Coverage reporting
- `mypy>=1.9.0` - Type checking
- `ruff>=0.9.0` - Linting and formatting
- `hypothesis>=6.131.0` - Property testing

## 🚢 Release Process

### Version Bumping

```bash
# Update version in pyproject.toml
# version = "1.2.3"

# Update CHANGELOG.md
# Add release notes

# Commit version bump
git commit -m "chore: bump version to 1.2.3"
git tag v1.2.3
```

### Publishing

```bash
# Build distributions
python -m build

# Upload to TestPyPI (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## 🤝 Contributing Guidelines

### Code Style

- Use type hints everywhere
- Add docstrings to all public functions/classes
- Follow PEP 8 (enforced by ruff)
- Use modern Python features (3.11+)

### Commit Messages

Follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Testing
- `refactor:` - Code refactoring
- `chore:` - Maintenance

### Pull Request Process

1. Create feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit PR with description
6. Address review feedback
7. Squash commits before merge

## 🔗 Useful Links

- [Issue Tracker](https://github.com/provide-io/pyvider/issues)
- [Discussions](https://github.com/provide-io/pyvider/discussions)
- [Discord Community](https://discord.gg/pyvider)
- [PyPI Package](https://pypi.org/project/pyvider/)

## 📄 License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.

---

<p align="center">
  Happy coding! 🚀
</p>
