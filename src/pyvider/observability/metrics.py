#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider Observability - Metrics Collection.

Provides centralized metrics for provider operations, resource lifecycle,
and handler performance monitoring."""

from __future__ import annotations

from provide.foundation.metrics import counter, histogram

# Resource lifecycle metrics
resource_operations = counter(
    "pyvider.resource.operations.total",
    description="Total number of resource operations",
)

resource_create_total = counter(
    "pyvider.resource.create.total",
    description="Total number of resource create operations",
)

resource_read_total = counter(
    "pyvider.resource.read.total",
    description="Total number of resource read operations",
)

resource_update_total = counter(
    "pyvider.resource.update.total",
    description="Total number of resource update operations",
)

resource_delete_total = counter(
    "pyvider.resource.delete.total",
    description="Total number of resource delete operations",
)

resource_errors = counter(
    "pyvider.resource.errors.total",
    description="Total number of resource operation errors",
)

# Handler performance metrics
handler_duration = histogram(
    "pyvider.handler.duration.seconds",
    description="Handler execution duration in seconds",
    unit="s",
)

handler_requests = counter(
    "pyvider.handler.requests.total",
    description="Total number of handler requests",
)

handler_errors = counter(
    "pyvider.handler.errors.total",
    description="Total number of handler errors",
)

# Discovery metrics
discovery_duration = histogram(
    "pyvider.discovery.duration.seconds",
    description="Component discovery duration in seconds",
    unit="s",
)

components_discovered = counter(
    "pyvider.discovery.components.total",
    description="Total number of components discovered",
)

discovery_errors = counter(
    "pyvider.discovery.errors.total",
    description="Total number of discovery errors",
)

# Schema metrics
schema_generation_duration = histogram(
    "pyvider.schema.generation.duration.seconds",
    description="Schema generation duration in seconds",
    unit="s",
)

schema_cache_hits = counter(
    "pyvider.schema.cache.hits.total",
    description="Total number of schema cache hits",
)

# Data source metrics
datasource_read_total = counter(
    "pyvider.datasource.read.total",
    description="Total number of data source read operations",
)

datasource_errors = counter(
    "pyvider.datasource.errors.total",
    description="Total number of data source errors",
)

# Function metrics
function_calls = counter(
    "pyvider.function.calls.total",
    description="Total number of function calls",
)

function_duration = histogram(
    "pyvider.function.duration.seconds",
    description="Function execution duration in seconds",
    unit="s",
)

function_errors = counter(
    "pyvider.function.errors.total",
    description="Total number of function errors",
)

# Ephemeral resource metrics
ephemeral_open_total = counter(
    "pyvider.ephemeral.open.total",
    description="Total number of ephemeral resource open operations",
)

ephemeral_renew_total = counter(
    "pyvider.ephemeral.renew.total",
    description="Total number of ephemeral resource renew operations",
)

ephemeral_close_total = counter(
    "pyvider.ephemeral.close.total",
    description="Total number of ephemeral resource close operations",
)

ephemeral_errors = counter(
    "pyvider.ephemeral.errors.total",
    description="Total number of ephemeral resource errors",
)

# Provider metrics
provider_configure_total = counter(
    "pyvider.provider.configure.total",
    description="Total number of provider configure operations",
)

provider_configure_errors = counter(
    "pyvider.provider.configure.errors.total",
    description="Total number of provider configure errors",
)

# 🐍🏗️🔚
