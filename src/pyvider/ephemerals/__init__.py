#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""This package defines the core abstractions for implementing ephemeral resources,
which are temporary, stateful components like API clients or database connections."""

from pyvider.ephemerals.base import BaseEphemeralResource
from pyvider.ephemerals.context import EphemeralResourceContext
from pyvider.ephemerals.decorators import register_ephemeral_resource

__all__ = [
    "BaseEphemeralResource",
    "EphemeralResourceContext",
    "register_ephemeral_resource",
]

# 🐍🏗️🔚
