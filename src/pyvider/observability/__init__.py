#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider Observability Module.

Provides metrics, tracing, and profiling capabilities for the Pyvider framework."""

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
    # Data source metrics
    "components_discovered",
    "datasource_errors",
    "datasource_read_total",
    # Discovery metrics
    "discovery_duration",
    "discovery_errors",
    # Ephemeral metrics
    "ephemeral_close_total",
    "ephemeral_errors",
    "ephemeral_open_total",
    "ephemeral_renew_total",
    # Function metrics
    "function_calls",
    "function_duration",
    "function_errors",
    # Handler metrics
    "handler_duration",
    "handler_errors",
    "handler_requests",
    # Provider metrics
    "provider_configure_errors",
    "provider_configure_total",
    # Resource metrics
    "resource_create_total",
    "resource_delete_total",
    "resource_errors",
    "resource_operations",
    "resource_read_total",
    "resource_update_total",
    # Schema metrics
    "schema_cache_hits",
    "schema_generation_duration",
]

# 🐍🏗️🔚
