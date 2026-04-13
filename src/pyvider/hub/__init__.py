#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider Component Hub
=====================
This package provides the central registry and discovery mechanisms for all
provider components (resources, data sources, functions)."""

from pyvider.data_sources.decorators import register_data_source
from pyvider.functions.decorators import register_function
from pyvider.hub.components import registry as hub
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.hub.validators import Validators
from pyvider.resources.decorators import register_resource

# Hub singleton key for the asyncio.Event that signals component discovery
# has finished. The CLI registers it during bootstrap; the RPC handler and
# the schema handler wait on it before serving requests. Centralizing the
# name here turns a typo into an ImportError instead of a silent 55-second
# hang waiting on an event that was never registered.
DISCOVERY_READY_EVENT: str = "_discovery_ready_event"

__all__ = [
    "DISCOVERY_READY_EVENT",
    "ComponentDiscovery",
    "Validators",
    "hub",
    "register_data_source",
    "register_function",
    "register_resource",
]

# 🐍🏗️🔚
