# Using Capabilities

Capabilities provide a way to extend components with reusable functionality. They allow you to add common behaviors like authentication, caching, validation, or data transformation to your resources, data sources, and providers.

!!! note "Capabilities Status"
    The capabilities system is **fully implemented and working**. Provider developers can create and use capabilities in their providers. Some advanced features (like a capability marketplace) are planned for future releases.

## Overview

Capabilities in Pyvider work through the decorator system and can be applied to:
- Providers
- Resources
- Data Sources
- Ephemeral Resources

## Applying Capabilities

Capabilities are applied using the `requires_capability` decorator:

```python
from pyvider.resources import register_resource
from pyvider.capabilities import requires_capability

@register_resource("my_resource")
@requires_capability("authentication")
class MyResource:
    """A resource that requires authentication capability."""

    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Access capability through self.capabilities
        auth_token = await self.capabilities.authentication.get_token()
        # Use the token to create resource
        return State(...), None
```

## Creating Custom Capabilities

See [Creating Capabilities](creating-capabilities.md) for details on implementing your own capabilities.

## Available Capabilities

Pyvider provides the capability infrastructure (`@register_capability`, `@requires_capability` decorators and `BaseCapability` class), but does not include built-in capability implementations in the core framework.

**Create your own capabilities for:**
- Authentication flows and token management
- Caching for expensive operations
- Request rate limiting
- Custom validation logic
- Logging and observability enhancements
- Retry and error handling patterns

**Example capabilities in the community:**
- See [pyvider-components](https://github.com/provide-io/pyvider-components) for example capability implementations

## Configuration

Capabilities can be configured through the `pyvider.toml` configuration file:

```toml
# pyvider.toml

# Private state encryption (required for some capabilities)
private_state_shared_secret = "your-secret-key-here"

[logging]
level = "INFO"
format = "emoji"
```

For more configuration options, see the example `pyvider.toml` in the repository root.

## Related Documentation

- [Creating Capabilities](creating-capabilities.md)
- [Capability Lifecycle](capability-lifecycle.md)
- [Capability Composition](capability-composition.md)
