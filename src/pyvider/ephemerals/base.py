#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

from pyvider.ephemerals.context import EphemeralResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema

ResultType = TypeVar("ResultType")
PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)
ConfigType = TypeVar("ConfigType")


class BaseEphemeralResource(ABC, Generic[ResultType, PrivateStateType, ConfigType]):
    """
    Abstract base class for an ephemeral resource.

    Ephemeral resources manage temporary, stateful objects like API clients
    or database connections that have a limited lifetime and may need to be
    periodically renewed.
    """

    config_class: type[ConfigType] | None = None
    result_class: type[ResultType] | None = None
    private_state_class: type[PrivateStateType] | None = None

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema:
        """Returns the schema for the resource's configuration and result."""
        ...

    async def validate(self, config: ConfigType) -> list[str]:
        """
        Performs custom validation on the configuration.

        Returns:
            A list of error messages. An empty list indicates success.
        """
        return []

    @abstractmethod
    async def open(
        self, ctx: EphemeralResourceContext[ConfigType, None]
    ) -> tuple[ResultType, PrivateStateType, datetime]:
        """
        Opens the ephemeral resource.

        Args:
            ctx: The context containing the resource's configuration.

        Returns:
            A tuple containing:
            - The result data to be returned to Terraform.
            - The private state needed to manage the resource.
            - A UTC datetime indicating when the resource must be renewed.
        """
        ...

    @abstractmethod
    async def renew(
        self, ctx: EphemeralResourceContext[None, PrivateStateType]
    ) -> tuple[PrivateStateType, datetime]:
        """
        Renews the ephemeral resource's lease or session.

        Args:
            ctx: The context containing the current private state.

        Returns:
            A tuple containing:
            - The *new* private state after renewal.
            - A new UTC datetime indicating the next renewal time.
        """
        ...

    @abstractmethod
    async def close(self, ctx: EphemeralResourceContext[None, PrivateStateType]) -> None:
        """
        Closes the ephemeral resource and cleans up any connections.

        Args:
            ctx: The context containing the final private state.
        """
        ...


# 🐍🏗️🔚
