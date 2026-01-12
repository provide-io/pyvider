# Code Reuse Patterns in Pyvider

!!! warning "Use Standard Python Patterns for Production"
    **For production providers, use these proven approaches:**

    - ✅ **Inheritance** - Base classes with shared functionality
    - ✅ **Composition** - Helper classes and utilities
    - ✅ **Utility Modules** - Shared functions and patterns

    **Capabilities are experimental** and not recommended for production use. See [Experimental Capabilities](#experimental-capabilities) below for details.

## Recommended Approaches

This guide shows you how to share code and functionality across your Pyvider components using standard Python patterns. These approaches are production-focused and well-tested.

### 1. Base Class Inheritance

Create shared base classes for common functionality:

```python
class BaseCloudResource(BaseResource):
    """Shared functionality for cloud resources."""

    async def apply_common_tags(self, resource_id: str, tags: dict):
        """Apply standard tags to resource."""
        pass

    async def setup_monitoring(self, resource_id: str):
        """Configure monitoring for resource."""
        pass

@register_resource("server")
class Server(BaseCloudResource):
    """Inherits tagging and monitoring."""
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        server = await self.create_server(ctx.config)
        await self.apply_common_tags(server.id, ctx.config.tags)
        await self.setup_monitoring(server.id)
        return State(...), None
```

### 2. Composition with Helper Classes

Use composition to share functionality:

```python
class RetryHandler:
    """Reusable retry logic."""

    async def with_retry(self, operation, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                return await operation()
            except RetryableError:
                if attempt == max_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

@register_resource("server")
class Server(BaseResource):
    def __init__(self):
        super().__init__()
        self.retry_handler = RetryHandler()

    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        server = await self.retry_handler.with_retry(
            lambda: self.create_server(ctx.config)
        )
        return State(...), None
```

### 3. Utility Modules

Create shared utility modules:

```python
# utils/caching.py
class Cache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl

    async def get(self, key):
        # Cache implementation
        pass

# In your resource
from utils.caching import Cache

@register_resource("server")
class Server(BaseResource):
    def __init__(self):
        super().__init__()
        self.cache = Cache(ttl=600)
```

## Component Bundling

You can package multiple related components together for distribution:

### Package Structure

```
my-pyvider-bundle/
├── pyproject.toml
├── src/
│   └── my_bundle/
│       ├── __init__.py
│       ├── resources/
│       ├── data_sources/
│       └── functions/
└── tests/
```

### Configuration

```toml
# pyproject.toml
[project]
name = "my-pyvider-bundle"
version = "0.1.0"
dependencies = [
    "pyvider>=0.0.3",
]

[project.entry-points."pyvider.components"]
my_bundle = "my_bundle"
```

### Using Bundled Components

```bash
# Install the bundle
uv add my-pyvider-bundle

# Components are automatically discovered
# Use them in Terraform configurations
```

### Example: pyvider-components

The **[pyvider-components](https://github.com/provide-io/pyvider-components)** repository provides a comprehensive collection of production-focused components:

- **Resources**: file_content, local_directory, timed_token
- **Data Sources**: env_variables, file_info, http_api, lens_jq
- **Functions**: String manipulation, numeric operations, JQ transformations
- **100+ Working Examples** with complete Terraform configurations

Perfect for:
- Learning by example
- Quick prototyping
- Production use
- Understanding best practices

## Experimental Capabilities

!!! warning "Experimental Feature"

    This feature is experimental and may change significantly in later releases; availability may change or be removed.
    Use in production at your own risk.

    **Stability:** ⚠️ Experimental

    Feedback welcome! [Report issues](https://github.com/provide-io/pyvider/issues)

### What are Capabilities?

Capabilities are a composition mechanism for reusable, modular components that extend provider functionality. Think of them as mixins or plugins.

**Current Status:**
- ✅ Basic infrastructure implemented (`BaseCapability`, decorators)
- ⚠️ Lifecycle hooks partially implemented
- 🔮 Advanced features remain exploratory

### Exploratory Features

### Capability Lifecycle

**Status:** Partial implementation

Exploratory lifecycle hooks:
- `setup()` - Initialize capability
- `configure()` - Configure with provider settings
- `teardown()` - Cleanup on shutdown

### Advanced Composition

**Status:** Exploratory

Features under consideration:
- Capability dependency management
- Composition ordering
- Conflict resolution
- Dynamic capability loading

## Configuration

Capabilities can be configured through provider configuration or environment:

```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config):
        # Configure capabilities
        if hasattr(self, 'capabilities'):
            for cap in self.capabilities.values():
                if hasattr(cap, 'configure'):
                    await cap.configure(config)
```

## Best Practices for Code Reuse

1. **Start Simple**: Use inheritance for straightforward shared functionality
2. **Prefer Composition**: Use helper classes for complex cross-cutting concerns
3. **Create Utility Modules**: Package commonly-used functions in shared modules
4. **Test in Isolation**: Test shared code independently from components
5. **Document Well**: Provide clear usage examples and docstrings
6. **Version Carefully**: Shared code is a dependency - version appropriately
7. **Avoid Over-Abstraction**: Don't create abstractions until you need them in 3+ places

## Exploratory Plans

Exploratory plans include:
- Advanced composition features
- Built-in capability library
- Integration with telemetry systems

## Related Documentation

- [pyvider-components](https://github.com/provide-io/pyvider-components) - Working examples
- [Best Practices](../guides/production/best-practices.md) - Code reuse patterns
- [Advanced Patterns](../guides/advanced/advanced-patterns.md) - Advanced implementation techniques

## Contributing

Interested in contributing to the capabilities system?

- Join the discussion on [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- Review the [Contributing Guidelines](../contributing/guidelines.md)
- Share feedback on exploratory capability features

---

**Note**: For production providers, we recommend using well-tested patterns (inheritance, composition, utilities) until the capabilities system reaches 1.0 maturity.
