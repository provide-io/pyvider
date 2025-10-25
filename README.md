# 🐍 Pyvider: Build Terraform Providers in Pure Python

<p align="center">
    <a href="https://pypi.org/project/pyvider/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/pyvider.svg">
    </a>
    <a href="https://github.com/provide-io/pyvider/actions/workflows/ci.yml">
        <img alt="CI Status" src="https://github.com/provide-io/pyvider/actions/workflows/ci.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/provide-io/pyvider">
        <img src="https://codecov.io/gh/provide-io/pyvider/branch/main/graph/badge.svg"/>
    </a>
    <a href="https://github.com/provide-io/pyvider/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/provide-io/pyvider.svg">
    </a>
    <a href="https://www.python.org/downloads/">
        <img alt="Python Version" src="https://img.shields.io/badge/python-3.11%2B-blue">
    </a>
</p>

**Pyvider** is a Python framework for building Terraform providers. Write infrastructure providers using Python's elegance, type safety, and rich ecosystem while maintaining full compatibility with Terraform Plugin Protocol v6.

## ✨ Key Features

- **🐍 Pure Python** - Write providers using familiar Python patterns and libraries
- **🎯 Type-Safe** - Leverage type hints and attrs for robust code
- **🚀 Decorator-Based** - Simple registration system handles protocol complexity
- **📦 Protocol v6** - Full Terraform Plugin Protocol v6 implementation
- **⚡ Async** - Built on modern async/await for high performance
- **🧪 Testable** - Comprehensive testing with pytest integration

## 📦 Installation

```bash
# Using pip
pip install pyvider

# Using uv (recommended)
uv add pyvider
```

## 🚀 Quick Start

```python
from pyvider.providers import register_provider, BaseProvider
from pyvider.resources import register_resource, BaseResource
from pyvider.schema import s_resource, a_str
import attrs

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """Your cloud provider"""
    pass

@register_resource("server")
class Server(BaseResource):
    """Manages a server"""

    @classmethod
    def get_schema(cls):
        return s_resource({
            "name": a_str(required=True),
            "id": a_str(computed=True),
        })

    async def _create_apply(self, ctx):
        # Create your resource
        return State(id="srv-123", name=ctx.config.name), None

    async def read(self, ctx):
        # Read current state
        return ctx.state
```

**See the full example in the [Quick Start Guide →](https://foundry.provide.io/pyvider/getting-started/quick-start/)**

## 📚 Documentation

**📖 [Read the Full Documentation →](https://foundry.provide.io/pyvider/)**

### Quick Links
- **[Installation Guide](https://foundry.provide.io/pyvider/getting-started/installation/)** - Get up and running
- **[Quick Start Tutorial](https://foundry.provide.io/pyvider/getting-started/quick-start/)** - Build your first provider in 5 minutes
- **[Architecture Overview](https://foundry.provide.io/pyvider/core-concepts/architecture/)** - Understand how Pyvider works
- **[API Reference](https://foundry.provide.io/pyvider/api/)** - Complete API documentation
- **[Examples](https://github.com/provide-io/pyvider-components)** - 100+ working examples

## 🚦 Project Status

**Version**: 0.0.x (Alpha)
**Protocol**: Terraform Plugin Protocol v6
**Python**: 3.11+

⚠️ **Alpha Software** - APIs may change before 1.0 release. Best suited for internal tooling, experimentation, and learning. See the [Roadmap](https://foundry.provide.io/pyvider/development/roadmap/) for details.

## 🤝 Contributing

Contributions welcome! See [Contributing Guidelines](CONTRIBUTING.md).

```bash
# Development setup
uv sync
uv run pytest
uv run ruff check
```

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## 🔗 Links

- **[Documentation](https://foundry.provide.io/pyvider/)** - Complete documentation
- **[Examples](https://github.com/provide-io/pyvider-components)** - Working examples
- **[PyPI](https://pypi.org/project/pyvider/)** - Package repository
- **[Discussions](https://github.com/provide-io/pyvider/discussions)** - Community support

---

<p align="center">
  Made with ❤️ by <a href="https://provide.io">Provide</a>
</p>
