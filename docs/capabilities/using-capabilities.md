# Using Capabilities

> **Note**: The capabilities system is currently under active development. This documentation describes the planned functionality.

Capabilities provide a way to extend components with reusable functionality. They allow you to add common behaviors like authentication, logging, or data transformation to your resources, data sources, and providers.

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

    async def create(self, config):
        # Access capability through self.capabilities
        auth_token = await self.capabilities.authentication.get_token()
        # Use the token to create resource
        pass
```

## Creating Custom Capabilities

See [Creating Capabilities](creating-capabilities.md) for details on implementing your own capabilities.

## Built-in Capabilities

Pyvider provides several built-in capabilities:

### Authentication Capability
Handles authentication flows and token management.

### Logging Capability
Enhanced logging with structured output and context.

### Caching Capability
Provides caching for expensive operations.

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
