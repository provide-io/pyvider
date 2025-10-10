"""
Pyvider Observability Module.

Provides metrics, tracing, and profiling capabilities for the Pyvider framework.
"""

from pyvider.observability.metrics import (
    components_discovered,
    datasource_errors,
    datasource_read_total,
    discovery_duration,
    discovery_errors,
    ephemeral_close_total,
    ephemeral_errors,
    ephemeral_open_total,
    ephemeral_renew_total,
    function_calls,
    function_duration,
    function_errors,
    handler_duration,
    handler_errors,
    handler_requests,
    provider_configure_errors,
    provider_configure_total,
    resource_create_total,
    resource_delete_total,
    resource_errors,
    resource_operations,
    resource_read_total,
    resource_update_total,
    schema_cache_hits,
    schema_generation_duration,
)

__all__ = [
    # Resource metrics
    "resource_operations",
    "resource_create_total",
    "resource_read_total",
    "resource_update_total",
    "resource_delete_total",
    "resource_errors",
    # Handler metrics
    "handler_duration",
    "handler_requests",
    "handler_errors",
    # Discovery metrics
    "discovery_duration",
    "components_discovered",
    "discovery_errors",
    # Schema metrics
    "schema_generation_duration",
    "schema_cache_hits",
    # Data source metrics
    "datasource_read_total",
    "datasource_errors",
    # Function metrics
    "function_calls",
    "function_duration",
    "function_errors",
    # Ephemeral metrics
    "ephemeral_open_total",
    "ephemeral_renew_total",
    "ephemeral_close_total",
    "ephemeral_errors",
    # Provider metrics
    "provider_configure_total",
    "provider_configure_errors",
]
