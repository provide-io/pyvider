# Error Handling

This guide explains how to handle errors effectively in your Pyvider provider.

## Overview

Pyvider provides a comprehensive exception hierarchy for handling errors. Proper error handling ensures users receive clear, actionable error messages.

## Available Exceptions

Pyvider's exception hierarchy:

```
PyviderError (base)
├── ConversionError
├── FrameworkConfigurationError
├── PluginError
├── PyviderValueError
├── InvalidTypeError
├── UnsupportedTypeError
├── ComponentConfigurationError
├── FunctionError
│   ├── FunctionRegistrationError
│   └── FunctionValidationError
├── GRPCError
├── ProviderError
│   ├── ProviderConfigurationError
│   └── ProviderInitializationError
├── ComponentRegistryError
├── ValidatorRegistrationError
├── ResourceError
│   ├── ResourceValidationError
│   ├── ResourceNotFoundError
│   ├── ResourceOperationError
│   └── ResourceLifecycleContractError
├── DataSourceError
├── CapabilityError
├── SchemaError
│   ├── SchemaValidationError
│   ├── SchemaRegistrationError
│   ├── SchemaParseError
│   └── SchemaConversionError
├── SerializationError
├── DeserializationError
├── ValidationError
└── AttributeValidationError
```

## Basic Error Handling

### Raising Exceptions

```python
from pyvider.exceptions import ResourceError, ProviderConfigurationError

async def create_server(config):
    if not config.name:
        raise ResourceError("Server name is required")

    try:
        server = await api.create_server(config.name)
        return server
    except APIError as e:
        raise ResourceError(f"Failed to create server: {e}")
```

### Provider Configuration Errors

```python
from pyvider.providers import BaseProvider
from pyvider.exceptions import ProviderConfigurationError

class MyProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        if not config.get("api_key"):
            raise ProviderConfigurationError("api_key is required")

        if not config["api_key"].startswith("sk_"):
            raise ProviderConfigurationError("Invalid API key format")

        try:
            self.client = APIClient(config["api_key"])
            await self.client.test_connection()
        except ConnectionError as e:
            raise ProviderConfigurationError(
                f"Failed to connect to API: {e}"
            )
```

### Resource Errors

```python
from pyvider.resources import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.exceptions import ResourceError, ResourceNotFoundError

class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext):
        if not ctx.config:
            return None, None

        try:
            server = await self.api.create_server(ctx.config.name)
        except QuotaExceeded as e:
            raise ResourceError(
                f"Cannot create server: quota exceeded. "
                f"Current: {e.current}, Limit: {e.limit}"
            )
        except AlreadyExists:
            raise ResourceError(
                f"Server '{ctx.config.name}' already exists. "
                f"Import it with: terraform import mycloud_server.name <id>"
            )
        except APIError as e:
            raise ResourceError(f"API error: {e}")

        return ServerState(...), None

    async def read(self, ctx: ResourceContext):
        try:
            server = await self.api.get_server(ctx.state.id)
            return ServerState(...)
        except NotFound:
            return None  # Resource deleted outside Terraform
        except APIError as e:
            raise ResourceError(f"Failed to read server: {e}")
```

## Best Practices

### 1. Provide Actionable Error Messages

```python
# Bad: Vague error
raise ResourceError("Creation failed")

# Good: Specific error with solution
raise ResourceError(
    f"Cannot create server '{name}': quota exceeded. "
    f"Current usage: {current}/{limit}. "
    f"Request quota increase at https://console.example.com/quotas"
)
```

### 2. Include Context

```python
# Bad: Missing context
raise ResourceError("Invalid size")

# Good: Clear context
raise ResourceError(
    f"Invalid server size '{config.size}'. "
    f"Valid sizes: small, medium, large"
)
```

### 3. Wrap External Errors

```python
try:
    result = await external_api.call()
except ExternalAPIError as e:
    raise ResourceError(
        f"External API call failed: {e}",
        details={"api_error_code": e.code, "retry_after": e.retry_after}
    )
```

### 4. Handle Validation Errors

```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    """Validate configuration and return error list."""
    errors = []

    if not config.name:
        errors.append("name is required")

    if not 1 <= config.port <= 65535:
        errors.append(f"port must be 1-65535, got {config.port}")

    if config.memory_gb < 1:
        errors.append(f"memory_gb must be >= 1, got {config.memory_gb}")

    return errors
```

### 5. Log Before Raising

```python
from provide.foundation import logger

async def create_resource(config):
    try:
        resource = await api.create(config)
        return resource
    except APIError as e:
        logger.error("Resource creation failed",
            error_type=type(e).__name__,
            error_message=str(e),
            resource_name=config.name
        )
        raise ResourceError(f"Failed to create resource: {e}")
```

## Error Patterns

### Quota Exceeded

```python
except QuotaExceeded as e:
    raise ResourceError(
        f"Cannot create {resource_type}: quota exceeded.\n"
        f"Current: {e.current_usage}\n"
        f"Limit: {e.quota_limit}\n"
        f"Request increase at: {e.quota_url}"
    )
```

### Resource Not Found

```python
async def read(self, ctx: ResourceContext):
    try:
        return await self.api.get_resource(ctx.state.id)
    except NotFoundError:
        # Return None - Terraform will recreate
        return None
```

### Conflict/Already Exists

```python
except ConflictError as e:
    raise ResourceError(
        f"Resource '{config.name}' already exists.\n"
        f"To manage it with Terraform, import it:\n"
        f"  terraform import mycloud_server.name {e.existing_id}"
    )
```

### Permission Denied

```python
except PermissionDenied as e:
    raise ResourceError(
        f"Permission denied: {e.message}\n"
        f"Required permissions: {', '.join(e.required_perms)}\n"
        f"Current permissions: {', '.join(e.current_perms)}"
    )
```

### Temporary Failures

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        return await api.create_resource(config)
    except TemporaryError as e:
        if attempt == max_retries - 1:
            raise ResourceError(
                f"Resource creation failed after {max_retries} attempts: {e}"
            )
        await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Testing Error Scenarios

```python
import pytest
from pyvider.exceptions import ResourceError

@pytest.mark.asyncio
async def test_create_server_quota_exceeded(server_resource, mock_api):
    # Arrange
    mock_api.create_server.side_effect = QuotaExceeded(current=10, limit=10)

    # Act & Assert
    with pytest.raises(ResourceError) as exc_info:
        await server_resource._create_apply(ctx)

    assert "quota exceeded" in str(exc_info.value).lower()
    assert "10" in str(exc_info.value)  # Shows limits
```

## Common Issues

### Missing Resource ID

```python
# Handle missing state gracefully
if not ctx.state or not ctx.state.id:
    return None
```

### Partial Update Failures

```python
async def _update_apply(self, ctx: ResourceContext):
    updated_fields = []
    try:
        if ctx.config.name != ctx.state.name:
            await api.update_name(ctx.state.id, ctx.config.name)
            updated_fields.append("name")

        if ctx.config.size != ctx.state.size:
            await api.update_size(ctx.state.id, ctx.config.size)
            updated_fields.append("size")

        return await self.read(ctx)
    except APIError as e:
        raise ResourceError(
            f"Update failed after updating: {', '.join(updated_fields)}. "
            f"Error: {e}. "
            f"Resource may be in inconsistent state."
        )
```

### Cascading Failures

```python
async def _delete_apply(self, ctx: ResourceContext):
    errors = []

    # Try to delete dependent resources
    for dep in ctx.state.dependencies:
        try:
            await api.delete_dependency(dep.id)
        except APIError as e:
            errors.append(f"Failed to delete {dep.type} {dep.id}: {e}")

    # Delete main resource
    try:
        await api.delete_resource(ctx.state.id)
    except APIError as e:
        errors.append(f"Failed to delete resource: {e}")

    if errors:
        raise ResourceError(
            f"Deletion completed with errors:\n" +
            "\n".join(f"  - {err}" for err in errors)
        )
```

## See Also

- [Logging](../development/logging.md) - Logging best practices
- [Debugging](../development/debugging.md) - Debugging techniques
- [Best Practices](../production/best-practices.md) - Provider development patterns
- [API Reference](../../api/exceptions.md) - Complete exception reference
