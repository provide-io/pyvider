#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
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

__all__ = [
    "ComponentDiscovery",
    "Validators",
    "hub",
    "register_data_source",
    "register_function",
    "register_resource",
]

# 🐍🏗️🔚
