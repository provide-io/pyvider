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
