# Logging

Pyvider uses the `provide.foundation` logging system for structured logging throughout your provider. This guide covers how to effectively log provider operations.

## Overview

Pyvider integrates with `provide.foundation`'s structured logging, providing:
- Structured log output (JSON or console)
- Contextual information binding
- Log level configuration
- Correlation IDs for request tracking
- Integration with observability tools

## Basic Logging

Import and use the logger:

```python
from provide.foundation import logger

def my_function():
    logger.info("Operation started")
    logger.debug("Detailed debug information")
    logger.warning("Something unexpected happened")
    logger.error("An error occurred")
```

## Log Levels

Available log levels in order of severity:

- `debug`: Detailed diagnostic information
- `info`: Confirmation that things are working as expected
- `warning`: Indication of potential issues
- `error`: Serious problems that prevented operations
- `critical`: System-level failures

### Setting Log Level

Configure via environment variable:

```bash
export FOUNDATION_LOG_LEVEL=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG
```

Or programmatically:

```python
import logging
logging.getLogger("provide.foundation").setLevel(logging.DEBUG)
```

## Structured Logging

Add contextual data to logs using `bind()`:

```python
from provide.foundation import logger

async def create_server(name: str, size: str):
    # Bind context for all subsequent logs
    log = logger.bind(
        operation="create_server",
        server_name=name,
        server_size=size,
    )

    log.info("Creating server")

    try:
        server = await api.create_server(name, size)
        log.info("Server created successfully", server_id=server.id)
        return server
    except Exception as e:
        log.error("Server creation failed", error=str(e))
        raise
```

## Logging in Provider Components

### Provider Logging

```python
from pyvider.providers import register_provider, BaseProvider
from provide.foundation import logger

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        log = logger.bind(
            component="provider",
            provider_name="mycloud"
        )

        log.info("Configuring provider", endpoint=config.get("endpoint"))

        try:
            await super().configure(config)
            self.client = MyCloudClient(config["api_key"])
            log.info("Provider configured successfully")
        except Exception as e:
            log.error("Provider configuration failed", error=str(e))
            raise
```

### Resource Logging

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from provide.foundation import logger

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        log = logger.bind(
            component="resource",
            resource_type="server",
            resource_name=ctx.config.name if ctx.config else "unknown"
        )

        log.info("Creating server")

        try:
            server = await self.api.create_server(ctx.config.name)
            log.info("Server created", server_id=server.id, status=server.status)
            return ServerState(...), None
        except Exception as e:
            log.error("Server creation failed", error=str(e))
            raise
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# Debug: Detailed diagnostic info
logger.debug("Request payload", payload=data)

# Info: Normal operations
logger.info("Server created successfully", server_id=server.id)

# Warning: Unexpected but handled
logger.warning("API rate limit approaching", current=95, limit=100)

# Error: Operation failed
logger.error("Failed to create server", error=str(e))
```

### 2. Add Context with bind()

```python
# Create contextual logger
log = logger.bind(
    operation="apply_resource",
    resource_type="server",
    resource_id="srv-123"
)

# All subsequent calls include context
log.info("Starting operation")  # Includes operation, resource_type, resource_id
log.info("Operation complete")  # Context automatically included
```

### 3. Never Log Sensitive Data

```python
# Bad: Logs sensitive data
logger.info("Creating API key", api_key=config.api_key)

# Good: Mask or omit sensitive data
logger.info("Creating API key", key_prefix=config.api_key[:4])
```

### 4. Log Operation Outcomes

```python
async def create_resource(config):
    log = logger.bind(operation="create_resource")

    log.info("Resource creation started")

    try:
        resource = await api.create(config)
        log.info("Resource created successfully", resource_id=resource.id)
        return resource
    except APIError as e:
        log.error("Resource creation failed", error=str(e), error_code=e.code)
        raise
```

### 5. Use Structured Fields

```python
# Good: Structured fields for easy parsing
logger.info("Server created",
    server_id="srv-123",
    server_name="web-01",
    server_size="large",
    creation_time=datetime.now().isoformat()
)

# Avoid: Unstructured strings
logger.info(f"Server srv-123 (web-01, large) created at {datetime.now()}")
```

## Integration with Terraform

Pyvider automatically includes Terraform context in logs when available:

```python
# Logs automatically include:
# - terraform_version
# - provider_version
# - resource_type
# - operation (plan, apply, destroy)
```

## Debugging

Enable debug logging for troubleshooting:

```bash
# Enable debug logs
export FOUNDATION_LOG_LEVEL=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG

# Run Terraform
terraform apply
```

Debug logs include:
- Detailed request/response data
- Protocol message details
- State transitions
- Internal operation flow

## Performance Logging

Log operation timing for performance analysis:

```python
import time
from provide.foundation import logger

async def slow_operation():
    start = time.time()
    log = logger.bind(operation="slow_operation")

    log.info("Operation started")

    # Perform operation
    result = await api.call()

    duration = time.time() - start
    log.info("Operation completed", duration_seconds=duration)

    return result
```

## Correlation IDs

Foundation automatically includes correlation IDs for request tracking:

```python
# Logs automatically include correlation_id
logger.info("Processing request")
# Output: {"message": "Processing request", "correlation_id": "abc-123", ...}
```

## Log Output Formats

Foundation supports multiple output formats:

```bash
# Console format (human-readable, default for development)
export FOUNDATION_LOG_FORMAT=console

# JSON format (machine-readable, for production)
export FOUNDATION_LOG_FORMAT=json
```

## Example: Complete Resource with Logging

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from provide.foundation import logger

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        if not ctx.config:
            return None, None

        log = logger.bind(
            component="resource",
            resource_type="server",
            operation="create",
            server_name=ctx.config.name,
        )

        log.info("Creating server resource")

        try:
            # Create server
            log.debug("Calling API to create server", size=ctx.config.size)
            server = await self.api.create_server(
                name=ctx.config.name,
                size=ctx.config.size,
            )

            log.info("Server created successfully",
                server_id=server.id,
                ip_address=server.ip,
                status=server.status
            )

            return ServerState(...), None

        except QuotaExceededError as e:
            log.error("Server creation failed: quota exceeded",
                current_usage=e.current,
                quota_limit=e.limit
            )
            raise ResourceError(f"Quota exceeded: {e}")

        except APIError as e:
            log.error("Server creation failed: API error",
                error_code=e.code,
                error_message=str(e)
            )
            raise ResourceError(f"API error: {e}")
```

## Common Patterns

### Timing Operations

```python
import time

start = time.time()
result = await operation()
duration = time.time() - start

logger.info("Operation completed", duration_ms=duration * 1000)
```

### Logging Retries

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        return await api_call()
    except TransientError as e:
        logger.warning("API call failed, retrying",
            attempt=attempt + 1,
            max_retries=max_retries,
            error=str(e)
        )
        if attempt == max_retries - 1:
            logger.error("Max retries exceeded")
            raise
```

### Progress Logging

```python
items = [...]
total = len(items)

for i, item in enumerate(items, 1):
    logger.info("Processing item",
        item_id=item.id,
        progress=f"{i}/{total}",
        percent_complete=int((i / total) * 100)
    )
```

## See Also

- [Debugging](../development/debugging.md) - Debugging techniques
- [Error Handling](../development/error-handling.md) - Error management patterns
- [Best Practices](../production/best-practices.md) - Provider development patterns
- [Observability API](../../api/observability.md) - Observability integration
