# Capabilities Overview

!!! danger "Experimental Feature - Not Fully Implemented"
    **The Capabilities system is currently experimental and not fully implemented in v0.0.1000.**

    - The API shown here represents planned functionality
    - Not all features may work as documented
    - Significant changes expected before stable release
    - **Not recommended for production use**

    For working examples of code reuse patterns, see [pyvider-components](https://github.com/provide-io/pyvider-components).

## What are Capabilities?

Capabilities are a planned composition mechanism in Pyvider that will allow you to create reusable, modular components that extend the functionality of providers, resources, data sources, and functions.

**Planned concept**: Think of capabilities as mixins or plugins that you can attach to your components to enhance their behavior without modifying their core implementation.

## Why Capabilities? (Planned)

The capabilities system aims to enable:

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

## Current Alternatives

While the capabilities system is under development, you can achieve similar goals using:

### 1. **Base Class Inheritance**
Create shared base classes for common functionality:

```python
class BaseCloudResource(BaseResource):
    """Shared functionality for cloud resources."""

    async def apply_common_tags(self, resource_id: str, tags: dict):
        # Common tagging logic
        pass

    async def setup_monitoring(self, resource_id: str):
        # Common monitoring setup
        pass

@register_resource("server")
class Server(BaseCloudResource):
    # Inherits common functionality
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Resource-specific logic
        server = await self.create_server(ctx.config)

        # Use inherited methods
        await self.apply_common_tags(server.id, ctx.config.tags)
        await self.setup_monitoring(server.id)

        return State(...), None
```

### 2. **Composition with Helper Classes**
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
        # Use composition for retry logic
        server = await self.retry_handler.with_retry(
            lambda: self.create_server(ctx.config)
        )
        return State(...), None
```

### 3. **Utility Modules**
Create shared utility modules:

```python
# utils/caching.py
class Cache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl

    async def get(self, key):
        # Cache logic
        pass

    async def set(self, key, value):
        # Cache logic
        pass

# In your resource
from utils.caching import Cache

@register_resource("server")
class Server(BaseResource):
    def __init__(self):
        super().__init__()
        self.cache = Cache(ttl=600)
```

### 4. **pyvider-components Examples**
See the [pyvider-components](https://github.com/provide-io/pyvider-components) repository for 100+ working examples of:
- Resources with common patterns
- Data sources with shared logic
- Functions demonstrating reusability
- Complete provider implementations

## Future Plans

The full capabilities system is planned for a future release. See the [Roadmap](../development/roadmap.md) for timeline and details.

When implemented, the capabilities system will provide:
- Decorator-based capability attachment (`@use_capability`)
- Automatic dependency injection
- Lifecycle hooks (setup, teardown, before/after operations)
- Capability composition and inheritance
- Discovery and registration via the hub system

## Experimental Documentation

Detailed documentation for the planned capabilities system (including API design and usage examples) has been moved to the experimental folder:

- Implementation concepts and lifecycle
- Planned API patterns
- Advanced composition techniques
- Marketplace and distribution plans

These docs represent the **vision** for capabilities, not current functionality.

## See Also

- [pyvider-components](https://github.com/provide-io/pyvider-components) - Working examples of reusable patterns
- [Best Practices](../guides/best-practices.md) - Current patterns for code reuse
- [Roadmap](../development/roadmap.md) - Feature status and timeline
- [Advanced Patterns](../guides/advanced-patterns.md) - Advanced implementation techniques

---

**Note**: If you're interested in contributing to the capabilities system design or implementation, please join the discussion on [GitHub Discussions](https://github.com/provide-io/pyvider/discussions).
