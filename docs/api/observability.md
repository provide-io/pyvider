# Observability API Reference

This page documents Pyvider's built-in metrics for monitoring provider operations, resource lifecycle, and performance.

## Overview

Pyvider provides automatic metrics collection for all provider operations using the `provide.foundation.metrics` library, wrapped by `pyvider.observability`. These metrics are exported as counters and histograms that can be integrated with monitoring systems like Prometheus, CloudWatch, or Datadog.

!!! note "Metrics vs Full Observability"
Pyvider currently provides **metrics only** through the `pyvider.observability` wrapper module. For structured logging, use `structlog` or `provide.foundation.logging` directly in your provider code. Advanced tracing and profiling features may be added later; availability may change or be removed.

## Available Metrics

All metrics are automatically collected by Pyvider's internal handlers. You don't need to manually instrument your provider code - these metrics are recorded as your resources, data sources, and functions execute.

### Resource Lifecycle Metrics

Track resource operations and their outcomes:

```python
from pyvider.observability import (
    resource_operations,      # Total resource operations
    resource_create_total,    # Create operations
    resource_read_total,      # Read operations
    resource_update_total,    # Update operations
    resource_delete_total,    # Delete operations
    resource_errors,          # Resource operation errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.resource.operations.total` | Counter | Total number of resource operations across all types |
| `pyvider.resource.create.total` | Counter | Total resource create (apply) operations |
| `pyvider.resource.read.total` | Counter | Total resource read/refresh operations |
| `pyvider.resource.update.total` | Counter | Total resource update (apply) operations |
| `pyvider.resource.delete.total` | Counter | Total resource delete operations |
| `pyvider.resource.errors.total` | Counter | Total resource operation errors |

**Tags**: Resource metrics include tags for `resource_type` (e.g., `mycloud_server`)

### Handler Performance Metrics

Monitor the performance of Terraform protocol handlers:

```python
from pyvider.observability import (
    handler_duration,         # Handler execution time (histogram)
    handler_requests,         # Total handler requests
    handler_errors,           # Handler errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.handler.duration.seconds` | Histogram | Handler execution duration in seconds |
| `pyvider.handler.requests.total` | Counter | Total number of handler requests |
| `pyvider.handler.errors.total` | Counter | Total number of handler errors |

**Tags**: Handler metrics include tags for `handler_name` (e.g., `ApplyResourceChange`)

### Discovery Metrics

Track component discovery performance:

```python
from pyvider.observability import (
    discovery_duration,       # Discovery time (histogram)
    components_discovered,    # Components found
    discovery_errors,         # Discovery errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.discovery.duration.seconds` | Histogram | Component discovery duration in seconds |
| `pyvider.discovery.components.total` | Counter | Total number of components discovered |
| `pyvider.discovery.errors.total` | Counter | Total number of discovery errors |

**Tags**: Discovery metrics include tags for `component_type` (e.g., `resource`, `data_source`)

### Schema Metrics

Monitor schema generation and caching:

```python
from pyvider.observability import (
    schema_generation_duration,  # Schema generation time
    schema_cache_hits,           # Schema cache hits
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.schema.generation.duration.seconds` | Histogram | Schema generation duration in seconds |
| `pyvider.schema.cache.hits.total` | Counter | Total number of schema cache hits |

### Data Source Metrics

Track data source operations:

```python
from pyvider.observability import (
    datasource_read_total,    # Data source reads
    datasource_errors,        # Data source errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.datasource.read.total` | Counter | Total number of data source read operations |
| `pyvider.datasource.errors.total` | Counter | Total number of data source errors |

**Tags**: Data source metrics include tags for `datasource_type` (e.g., `mycloud_images`)

### Function Metrics

Monitor provider function calls:

```python
from pyvider.observability import (
    function_calls,          # Function call count
    function_duration,       # Function execution time
    function_errors,         # Function errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.function.calls.total` | Counter | Total number of function calls |
| `pyvider.function.duration.seconds` | Histogram | Function execution duration in seconds |
| `pyvider.function.errors.total` | Counter | Total number of function errors |

**Tags**: Function metrics include tags for `function_name` (e.g., `hash_file`)

### Ephemeral Resource Metrics

Track ephemeral resource lifecycle:

```python
from pyvider.observability import (
    ephemeral_open_total,     # Open operations
    ephemeral_renew_total,    # Renew operations
    ephemeral_close_total,    # Close operations
    ephemeral_errors,         # Ephemeral errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.ephemeral.open.total` | Counter | Total ephemeral resource open operations |
| `pyvider.ephemeral.renew.total` | Counter | Total ephemeral resource renew operations |
| `pyvider.ephemeral.close.total` | Counter | Total ephemeral resource close operations |
| `pyvider.ephemeral.errors.total` | Counter | Total ephemeral resource errors |

**Tags**: Ephemeral metrics include tags for `ephemeral_type`

### Provider Metrics

Monitor provider configuration:

```python
from pyvider.observability import (
    provider_configure_total,       # Configure operations
    provider_configure_errors,      # Configuration errors
)
```

| Metric Name | Type | Description |
|------------|------|-------------|
| `pyvider.provider.configure.total` | Counter | Total provider configure operations |
| `pyvider.provider.configure.errors.total` | Counter | Total provider configure errors |

## Using Metrics

### Automatic Collection

Metrics are automatically collected - you don't need to do anything:

```python
@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # resource_create_total is automatically incremented
        # handler_duration automatically records timing
        # resource_errors incremented on exception

        server = await self.api.create_server(ctx.config)
        return State(id=server.id, name=server.name), None
```

### Manual Metric Recording

If you need to record custom metrics in your provider, use `provide.foundation.metrics` directly:

```python
from provide.foundation.metrics import counter, histogram

# Define custom metrics
api_calls = counter(
    "mycloud.api.calls.total",
    description="Total API calls to cloud service"
)

api_latency = histogram(
    "mycloud.api.latency.seconds",
    description="API call latency",
    unit="s"
)

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Record custom metric
        api_calls.inc({"endpoint": "create_server", "region": "us-east-1"})

        start = time.time()
        server = await self.api.create_server(ctx.config)
        duration = time.time() - start

        api_latency.observe(duration, {"endpoint": "create_server"})

        return State(id=server.id), None
```

## Metrics Export

### Prometheus Export

Pyvider metrics can be exported to Prometheus via the `provide.foundation` library. Configure your provider's metrics endpoint:

```python
# In your provider startup code
from provide.foundation.metrics import start_metrics_server

# Start metrics server
start_metrics_server(port=9090)

# Metrics available at http://localhost:9090/metrics
```

### Other Exporters

The `provide.foundation.metrics` library supports multiple exporters. See the [provide.foundation documentation](https://github.com/provide-io/provide-foundation) for details on:

- CloudWatch export
- Datadog export
- StatsD export
- Custom exporters

## Metric Types

### Counter

Counters track cumulative totals that only increase:

```python
from provide.foundation.metrics import counter

requests = counter("mycloud.requests.total", description="Total requests")
requests.inc()  # Increment by 1
requests.inc({"status": "success"})  # With tags
```

### Histogram

Histograms track distributions of values (timing, sizes, etc.):

```python
from provide.foundation.metrics import histogram

latency = histogram("mycloud.latency.seconds", description="Latency", unit="s")
latency.observe(0.125)  # Record observation
latency.observe(0.250, {"endpoint": "create"})  # With tags
```

## Structured Logging

For structured logging in your provider, use `structlog` or `provide.foundation.logging`:

```python
import structlog

logger = structlog.get_logger()

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        log = logger.bind(
            operation="create",
            resource_type="server",
            resource_name=ctx.config.name
        )

        log.info("Creating server", size=ctx.config.size)

        try:
            server = await self.api.create_server(ctx.config)
            log.info("Server created", server_id=server.id, duration_ms=elapsed)
            return State(id=server.id), None
        except Exception as e:
            log.error("Server creation failed", error=str(e), exc_info=True)
            raise
```

## Environment Variables

Configure metrics behavior via environment variables:

```bash
# Enable/disable metrics
export PYVIDER_METRICS_ENABLED=true

# Metrics server port (if using built-in server)
export PYVIDER_METRICS_PORT=9090

# Log level (affects foundation logging)
export FOUNDATION_LOG_LEVEL=INFO
```

## Related Documentation

- [provide.foundation metrics](https://github.com/provide-io/provide-foundation) - Underlying metrics library
- [Logging Guide](../guides/development/logging.md) - Structured logging patterns
- [Debugging](../guides/development/debugging.md) - Debug with metrics
- [Error Handling](../guides/development/error-handling.md) - Error tracking

## Module Reference

### Exported Metrics
