#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

import attrs
from attrs import define, field

from pyvider.common.context import BaseContext
from pyvider.common.types import ConfigType, StateType
from pyvider.cty import CtyValue
from pyvider.resources.private_state import PrivateState

if TYPE_CHECKING:
    from pyvider.capabilities import BaseCapability

PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)


@define(frozen=True)
class ResourceContext(BaseContext, Generic[ConfigType, StateType, PrivateStateType]):
    config: ConfigType | None = None
    state: StateType | None = None
    planned_state: StateType | None = None
    private_state: PrivateStateType | None = None
    config_cty: CtyValue | None = None
    planned_state_cty: CtyValue | None = None
    capabilities: dict[str, BaseCapability] = field(factory=dict)
    test_mode_enabled: bool = field(default=False, kw_only=True)

    def get_private_state(self, private_state_class: type[PrivateStateType]) -> PrivateStateType | None:
        """
        Get typed private state with automatic casting.

        Args:
            private_state_class: The private state class type to cast to

        Returns:
            Typed private state instance or None if no private state exists

        Example:
            private_data = ctx.get_private_state(MyPrivateState)
            if private_data:
                token = private_data.token
        """
        if self.private_state:
            # If it's already the correct type, return as-is
            if isinstance(self.private_state, private_state_class):
                return self.private_state
            # Otherwise, convert from dict representation
            if hasattr(self.private_state, "__dict__") or isinstance(self.private_state, dict):
                state_dict = (
                    attrs.asdict(self.private_state)
                    if hasattr(self.private_state, "__dict__")
                    else self.private_state
                )
                return private_state_class(**state_dict)
        return None

    def has_private_state(self) -> bool:
        """
        Check if private state exists.

        Returns:
            True if private state is present, False otherwise
        """
        return self.private_state is not None

    def is_field_unknown(self, field_name: str, source: str = "config") -> bool:
        """
        Check if a configuration or state field has an unknown value during planning.

        This is the proper way for resources to handle unknown values - check explicitly
        rather than catching errors or working around None values.

        Args:
            field_name: Name of the field to check
            source: Which CTY value to check - "config" or "planned_state" (default: "config")

        Returns:
            True if the field exists but has an unknown value, False otherwise

        Example:
            async def _create(self, ctx: ResourceContext, base_plan: dict) -> ...:
                if ctx.is_field_unknown("content"):
                    # Content is unknown during planning, can't compute hash
                    base_plan["exists"] = True
                    return base_plan, None

                # Content is known, use typed config
                config = cast(FileContentConfig, ctx.config)
                base_plan["content_hash"] = hashlib.sha256(config.content.encode()).hexdigest()
                return base_plan, None
        """
        cty_value = self.config_cty if source == "config" else self.planned_state_cty

        if not cty_value or cty_value.is_null:
            return False

        if not hasattr(cty_value, "value") or not isinstance(cty_value.value, dict):
            return False

        field_cty = cty_value.value.get(field_name)
        if field_cty is None:
            return False

        # Check if it's a CtyValue with unknown marker
        if isinstance(field_cty, CtyValue):
            return field_cty.is_unknown

        return False


# 🐍🏗️🔚
