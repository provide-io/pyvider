#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Protocol, runtime_checkable

from pyvider.common.types import ConfigType, StateType
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.resources.types import ResourceType


@runtime_checkable
class ResourceProtocol(Protocol[ResourceType, StateType, ConfigType]):
    """Protocol defining resource lifecycle operations."""

    async def validate(self, config: ConfigType) -> None:
        """Validate resource configuration."""
        ...

    async def read(self, ctx: ResourceContext[ConfigType, StateType, PrivateState]) -> StateType:
        """Read resource state."""
        ...

    async def plan(self, ctx: ResourceContext[ConfigType, StateType, PrivateState]) -> tuple[StateType, bytes]:
        """Plan resource changes."""
        ...

    async def apply(
        self, ctx: ResourceContext[ConfigType, StateType, PrivateState]
    ) -> tuple[StateType, bytes]:
        """Apply resource changes."""
        ...

    async def delete(self, ctx: ResourceContext[ConfigType, StateType, PrivateState]) -> None:
        """Delete the resource."""
        ...


# 🐍🏗️🔚
