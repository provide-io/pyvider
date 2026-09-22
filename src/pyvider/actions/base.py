#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The action contract.

An action is a provider-defined operation Terraform can invoke on its own,
outside any resource lifecycle. It is validated, then planned, then invoked as
a stream of progress events.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence
from typing import Generic, TypeVar

from pyvider.actions.types import ActionContext, ActionPlan, ActionProgress
from pyvider.lint import LintContext, LintFinding
from pyvider.schema import PvsSchema

ConfigType = TypeVar("ConfigType")


class BaseAction(ABC, Generic[ConfigType]):
    """Abstract base class for a Terraform action."""

    #: attrs class describing the action's configuration block.
    config_class: type[ConfigType] | None = None

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema:
        """Return the schema of the action's configuration."""

    async def validate(self, config: ConfigType | None) -> list[str]:
        """Validate the action's configuration.

        Returns human-readable error messages; empty means valid. The default
        accepts anything the schema itself accepted, which is right for an
        action with no cross-field rules.
        """
        return []

    async def lint(self, ctx: LintContext[ConfigType]) -> Sequence[LintFinding]:
        """Return opt-in advisory findings for a semantically valid configuration."""
        return ()

    async def plan(self, ctx: ActionContext[ConfigType]) -> ActionPlan:
        """Decide whether the action can run now.

        The default plan runs the action unconditionally. Override to emit
        warnings, or to defer when a prerequisite is not yet known.
        """
        return ActionPlan()

    @abstractmethod
    def invoke(self, ctx: ActionContext[ConfigType]) -> AsyncIterator[ActionProgress]:
        """Run the action, yielding progress as it goes.

        Implemented as an async generator. Terraform renders each yielded
        message while the action is still running, so yielding as work
        completes is what makes a long action legible rather than silent.
        Raising aborts the action and is reported to Terraform as an error.
        """


# 🐍🏗️🔚
