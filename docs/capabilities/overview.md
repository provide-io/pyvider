# Capabilities Overview

!!! info "Implementation Status"
    **Basic capabilities infrastructure is implemented** in Pyvider v0.0.1000:

    - ✅ `BaseCapability` class
    - ✅ `@register_capability` decorator
    - ✅ `@requires_capability` decorator
    - ✅ Component capability access via `self.capabilities`

    **Advanced features are experimental or planned:**

    - ⚠️ Capability lifecycle hooks (partial)
    - 🔮 Capability marketplace (planned)
    - 🔮 Advanced composition patterns (planned)
    - 🔮 Built-in capability library (planned)

    For production use, prefer **inheritance, composition, and utility modules** as shown in the [Current Alternatives](#current-alternatives) section below.

## What are Capabilities?

Capabilities are a composition mechanism in Pyvider that allow you to create reusable, modular components that extend the functionality of providers, resources, data sources, and functions.

Think of capabilities as mixins or plugins that you can attach to your components to enhance their behavior without modifying their core implementation.

## Why Use Capabilities?

### Reusability
Write cross-cutting concerns once and apply them to multiple components:
- Authentication logic (OAuth, API keys, token management)
- Retry patterns (exponential backoff, circuit breakers)
- Caching strategies (response caching, state caching)
- Logging and observability
- Performance metrics collection

### Separation of Concerns
Keep your resource/provider implementations focused on core business logic while capabilities handle infrastructure concerns.

### Modularity
- Develop capabilities independently
- Test in isolation
- Version separately
- Share across projects
- Publish as packages

## Basic Usage

### Creating a Capability

```python
from pyvider.capabilities import BaseCapability, register_capability
import attrs

@register_capability("authentication")
class AuthenticationCapability(BaseCapability):
    """Provides authentication token management."""

    @attrs.define
    class Config:
        api_key: str
        endpoint: str = "https://api.example.com"

    async def setup(self, provider):
        """Initialize the capability."""
        self.provider = provider
        self.token = None

    async def get_token(self) -> str:
        """Get or refresh authentication token."""
        if not self.token:
            self.token = await self._fetch_token()
        return self.token

    async def _fetch_token(self) -> str:
        """Fetch new token from API."""
        # Implementation
        pass
```

### Using a Capability

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.capabilities import requires_capability

@register_resource("authenticated_resource")
class AuthenticatedResource(BaseResource):
    """A resource that uses authentication capability."""

    @requires_capability
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Access capability through context
        token = await ctx.capabilities.authentication.get_token()

        # Use token to create resource
        result = await self.api_call(token=token, config=ctx.config)
        return State(id=result.id), None
```

## Current Alternatives

While the capabilities system continues to evolve, you can achieve similar goals using standard Python patterns:

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
    "pyvider>=0.0.1000",
]

[project.entry-points."pyvider.components"]
my_bundle = "my_bundle"
```

### Using Bundled Components

```bash
# Install the bundle
pip install my-pyvider-bundle

# Components are automatically discovered
# Use them in Terraform configurations
```

### Example: pyvider-components

The **[pyvider-components](https://github.com/provide-io/pyvider-components)** repository provides a comprehensive collection of production-ready components:

- **Resources**: file_content, local_directory, timed_token
- **Data Sources**: env_variables, file_info, http_api, lens_jq
- **Functions**: String manipulation, numeric operations, JQ transformations
- **100+ Working Examples** with complete Terraform configurations

Perfect for:
- Learning by example
- Quick prototyping
- Production use
- Understanding best practices

## Experimental Features

The following features are planned for future releases:

### Capability Lifecycle

**Status:** Partial implementation

Planned lifecycle hooks:
- `setup()` - Initialize capability
- `configure()` - Configure with provider settings
- `teardown()` - Cleanup on shutdown

### Capability Marketplace

**Status:** Planned for post-1.0

A central hub for discovering and sharing reusable capabilities:
- Browse by category
- Search by functionality
- Community ratings
- One-command installation via PyPI

### Advanced Composition

**Status:** Planned

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

## Best Practices

1. **Start Simple**: Use inheritance or composition for simple cases
2. **Capabilities for Cross-Cutting**: Use capabilities for truly reusable, cross-cutting concerns
3. **Test in Isolation**: Test capabilities independently from components
4. **Document Well**: Provide clear usage examples
5. **Version Carefully**: Capabilities are shared code - version appropriately

## Future Plans

See the [Roadmap](../development/roadmap.md) for details on:
- Capability marketplace timeline
- Advanced composition features
- Built-in capability library
- Integration with telemetry systems

## Related Documentation

- [pyvider-components](https://github.com/provide-io/pyvider-components) - Working examples
- [Best Practices](../guides/best-practices.md) - Code reuse patterns
- [Roadmap](../development/roadmap.md) - Feature timeline
- [Advanced Patterns](../guides/advanced-patterns.md) - Advanced implementation techniques

## Contributing

Interested in contributing to the capabilities system?

- Join the discussion on [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- Review the [Contributing Guidelines](../contributing/guidelines.md)
- Check the [Roadmap](../development/roadmap.md) for upcoming features

---

**Note**: For production providers, we recommend using well-tested patterns (inheritance, composition, utilities) until the capabilities system reaches 1.0 maturity.
