# Observability API Reference

This page documents Pyvider's observability features for monitoring, metrics, and telemetry in Terraform providers.

## Overview

Pyvider provides comprehensive observability through:
- Structured logging via `provide.foundation`
- Metrics collection and export
- Distributed tracing support
- Performance profiling
- Request/response tracking

## Metrics System

### Metric Types

Pyvider tracks various metric types:

```python
from pyvider.observability import metrics

# Counter - Cumulative values
metrics.increment_counter(
    "provider.api_calls",
    tags={"method": "create", "resource": "server"}
)

# Gauge - Point-in-time values
metrics.set_gauge(
    "provider.active_connections",
    value=42,
    tags={"region": "us-east-1"}
)

# Histogram - Distribution of values
metrics.record_histogram(
    "provider.request_duration_ms",
    value=127.5,
    tags={"operation": "create_resource"}
)

# Summary - Statistical distribution
metrics.record_summary(
    "provider.response_size_bytes",
    value=2048,
    tags={"endpoint": "/api/v1/resources"}
)
```

### Built-in Metrics

Pyvider automatically tracks:

| Metric Name | Type | Description | Tags |
|------------|------|-------------|------|
| `pyvider.requests.total` | Counter | Total provider requests | `method`, `resource_type` |
| `pyvider.requests.duration_ms` | Histogram | Request duration | `method`, `resource_type`, `status` |
| `pyvider.requests.errors` | Counter | Request errors | `method`, `resource_type`, `error_type` |
| `pyvider.resources.created` | Counter | Resources created | `resource_type` |
| `pyvider.resources.updated` | Counter | Resources updated | `resource_type` |
| `pyvider.resources.deleted` | Counter | Resources deleted | `resource_type` |
| `pyvider.grpc.connections` | Gauge | Active gRPC connections | `state` |
| `pyvider.grpc.message_size` | Histogram | gRPC message sizes | `direction`, `type` |

## Structured Logging

### Logger Configuration

```python
import structlog
from pyvider.observability import configure_logging

# Configure logging with custom settings
configure_logging(
    level="DEBUG",
    format="json",  # or "console" for development
    include_timestamp=True,
    include_caller=True,
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
)
```

### Using the Logger

```python
import structlog

logger = structlog.get_logger()

class MyResource(BaseResource):
    async def create(self, config: Config) -> State:
        # Bind context to all logs in this method
        log = logger.bind(
            resource_type="mycloud_server",
            resource_name=config.name,
            operation="create"
        )

        log.info("Creating resource", config=config.__dict__)

        try:
            # Create resource
            result = await self.provider.api.create_server(...)

            log.info(
                "Resource created successfully",
                resource_id=result.id,
                duration_ms=elapsed_time
            )

            return State(...)

        except Exception as e:
            log.error(
                "Resource creation failed",
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True  # Include stack trace
            )
            raise
```

### Log Levels

```python
# Log levels in order of severity
logger.debug("Detailed diagnostic information")
logger.info("General informational messages")
logger.warning("Warning messages for potential issues")
logger.error("Error messages for failures")
logger.critical("Critical failures requiring immediate attention")
```

## Tracing

### Distributed Tracing with OpenTelemetry

```python
from opentelemetry import trace
from pyvider.observability import get_tracer

tracer = get_tracer("my_provider")

class MyResource(BaseResource):
    async def create(self, config: Config) -> State:
        # Start a span for the operation
        with tracer.start_as_current_span(
            "resource.create",
            attributes={
                "resource.type": "server",
                "resource.name": config.name,
                "provider.name": "mycloud"
            }
        ) as span:
            try:
                # Nested span for API call
                with tracer.start_as_current_span("api.create_server") as api_span:
                    api_span.set_attribute("api.endpoint", "/servers")
                    api_span.set_attribute("api.method", "POST")

                    result = await self.provider.api.create_server(...)

                    api_span.set_attribute("api.response.id", result.id)
                    api_span.set_status(trace.Status(trace.StatusCode.OK))

                span.set_attribute("resource.id", result.id)
                return State(...)

            except Exception as e:
                span.record_exception(e)
                span.set_status(
                    trace.Status(
                        trace.StatusCode.ERROR,
                        str(e)
                    )
                )
                raise
```

### Trace Context Propagation

```python
from opentelemetry import propagate

async def make_api_call(self, endpoint: str, data: dict):
    """Make API call with trace context propagation."""

    # Extract trace context
    headers = {}
    propagate.inject(headers)

    # Include trace headers in API call
    response = await self.client.post(
        endpoint,
        json=data,
        headers=headers
    )

    return response
```

## Performance Profiling

### Method Timing Decorator

```python
from pyvider.observability import timed

class MyResource(BaseResource):
    @timed("resource.create")
    async def create(self, config: Config) -> State:
        """Create method with automatic timing."""
        # Method execution time automatically recorded
        result = await self._create_impl(config)
        return result

    @timed("api.call", include_args=True)
    async def api_call(self, method: str, endpoint: str):
        """API call with detailed timing."""
        # Records timing with method and endpoint as tags
        return await self.client.request(method, endpoint)
```

### Manual Timing

```python
from pyvider.observability import Timer

async def complex_operation(self):
    """Operation with manual timing points."""
    timer = Timer()

    # Time initialization
    with timer.measure("init"):
        await self.initialize()

    # Time main operation
    with timer.measure("process"):
        result = await self.process_data()

    # Log all timings
    logger.info("Operation complete", timings=timer.get_all())

    # Record as metrics
    for name, duration in timer.get_all().items():
        metrics.record_histogram(
            f"operation.{name}.duration_ms",
            value=duration
        )
```

## Request/Response Tracking

### Middleware for Request Tracking

```python
from pyvider.observability import RequestTracker

class TrackedProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.tracker = RequestTracker()

    async def handle_request(self, request):
        """Handle request with tracking."""
        # Start tracking
        request_id = self.tracker.start_request(
            method=request.method,
            resource_type=request.resource_type
        )

        try:
            # Process request
            response = await self.process(request)

            # Record success
            self.tracker.complete_request(
                request_id,
                status="success",
                response_size=len(response)
            )

            return response

        except Exception as e:
            # Record failure
            self.tracker.complete_request(
                request_id,
                status="error",
                error=str(e)
            )
            raise
```

## Health Checks

### Health Status Reporting

```python
from pyvider.observability import HealthCheck, HealthStatus

class MyProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.health = HealthCheck()

    async def check_health(self) -> HealthStatus:
        """Perform health checks."""
        status = HealthStatus()

        # Check API connectivity
        try:
            await self.api_client.ping()
            status.add_check("api", "healthy", {"endpoint": self.api_endpoint})
        except Exception as e:
            status.add_check("api", "unhealthy", {"error": str(e)})

        # Check database
        try:
            await self.db.query("SELECT 1")
            status.add_check("database", "healthy")
        except Exception as e:
            status.add_check("database", "unhealthy", {"error": str(e)})

        return status
```

## Metrics Export

### Prometheus Export

```python
from pyvider.observability import PrometheusExporter

# Configure Prometheus exporter
exporter = PrometheusExporter(
    port=9090,
    path="/metrics",
    namespace="pyvider"
)

# Start exporter
await exporter.start()

# Metrics available at http://localhost:9090/metrics
```

### Custom Metric Exporters

```python
from pyvider.observability import MetricExporter

class CloudWatchExporter(MetricExporter):
    """Export metrics to AWS CloudWatch."""

    async def export(self, metrics: list[Metric]):
        """Send metrics to CloudWatch."""
        for metric in metrics:
            await self.cloudwatch.put_metric_data(
                Namespace="Pyvider",
                MetricData=[
                    {
                        "MetricName": metric.name,
                        "Value": metric.value,
                        "Timestamp": metric.timestamp,
                        "Dimensions": [
                            {"Name": k, "Value": v}
                            for k, v in metric.tags.items()
                        ]
                    }
                ]
            )
```

## Environment Variables

Configure observability via environment variables:

```bash
# Logging
export PYVIDER_LOG_LEVEL=DEBUG
export PYVIDER_LOG_FORMAT=json
export PYVIDER_LOG_FILE=/var/log/pyvider.log

# Metrics
export PYVIDER_METRICS_ENABLED=true
export PYVIDER_METRICS_EXPORT=prometheus
export PYVIDER_METRICS_PORT=9090

# Tracing
export PYVIDER_TRACING_ENABLED=true
export PYVIDER_TRACING_EXPORTER=otlp
export PYVIDER_TRACING_ENDPOINT=http://localhost:4317
export PYVIDER_TRACING_SAMPLE_RATE=0.1

# Profiling
export PYVIDER_PROFILE=true
export PYVIDER_PROFILE_OUTPUT=/tmp/pyvider.prof
```

## Best Practices

### 1. Consistent Metric Naming

```python
# Good - Consistent naming convention
metrics.increment_counter("pyvider.resource.create.success")
metrics.increment_counter("pyvider.resource.create.failure")
metrics.record_histogram("pyvider.resource.create.duration_ms")

# Bad - Inconsistent naming
metrics.increment_counter("created_resources")
metrics.increment_counter("ResourceCreateFail")
metrics.record_histogram("create_time")
```

### 2. Meaningful Log Context

```python
# Good - Rich context
logger.info(
    "Resource operation completed",
    operation="create",
    resource_type="server",
    resource_id=result.id,
    duration_ms=elapsed,
    api_calls=3,
    cache_hits=2
)

# Bad - Minimal context
logger.info(f"Created {result.id}")
```

### 3. Appropriate Log Levels

```python
# Debug - Detailed diagnostic info
logger.debug("Parsing configuration", raw_config=config_dict)

# Info - Normal operations
logger.info("Resource created", resource_id=resource.id)

# Warning - Potential issues
logger.warning("API rate limit approaching", remaining=10)

# Error - Failures that are handled
logger.error("API call failed, retrying", attempt=2, error=str(e))

# Critical - Unrecoverable failures
logger.critical("Cannot connect to database", error=str(e))
```

## Testing Observability

```python
import pytest
from unittest.mock import Mock, patch
from pyvider.observability import metrics, configure_logging

def test_metrics_recording():
    """Test that metrics are properly recorded."""
    with patch.object(metrics, 'increment_counter') as mock_counter:
        # Perform operation that should record metrics
        resource.create(config)

        # Verify metric was recorded
        mock_counter.assert_called_with(
            "pyvider.resources.created",
            tags={"resource_type": "server"}
        )

def test_error_logging():
    """Test that errors are properly logged."""
    with patch('structlog.get_logger') as mock_logger:
        logger = Mock()
        mock_logger.return_value = logger

        # Trigger an error
        with pytest.raises(ResourceError):
            resource.create(invalid_config)

        # Verify error was logged
        logger.error.assert_called()
        call_args = logger.error.call_args
        assert "creation failed" in call_args[0][0]
        assert "error" in call_args[1]
```

## Related Documentation

- [Logging Guide](../guides/logging.md) - Detailed logging patterns
- [Debugging](../guides/debugging.md) - Debug with observability tools
- [Error Handling](../guides/error-handling.md) - Error tracking and reporting

## Auto-Generated API Documentation

::: pyvider.observability
    options:
      show_source: true
      show_bases: true
      members:
        - metrics
        - configure_logging
        - get_tracer
        - Timer
        - timed
        - RequestTracker
        - HealthCheck
        - HealthStatus
        - MetricExporter
        - PrometheusExporter