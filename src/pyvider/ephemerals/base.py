#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from typing import Generic, TypeVar

from pyvider.ephemerals.context import EphemeralResourceContext
from pyvider.lint import LintContext, LintFinding
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

    async def validate(self, config: ConfigType | None) -> list[str]:
        """
        Performs custom validation on the configuration.

        ``config`` is None when the configuration is not wholly known -- an
        attribute referencing a not-yet-created resource, for instance. That is
        deliberate: `cty_to_attrs_instance` collapses a half-known object rather
        than handing over one whose fields are silently None. Every other
        component type already declares this; ephemeral resources did not, so
        the annotation promised something the handler does not deliver and an
        implementation written against it raised AttributeError at plan time.

        Returns:
            A list of error messages. An empty list indicates success.
        """
        return []

    async def lint(self, ctx: LintContext[ConfigType]) -> Sequence[LintFinding]:
        """Return opt-in advisory findings for a semantically valid configuration."""
        return ()

    @abstractmethod
    async def open(
        self,
        ctx: EphemeralResourceContext[ConfigType, None],  # type: ignore[type-var]
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
