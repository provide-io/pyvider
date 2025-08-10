from typing import TypeVar

from attrs import define

from pyvider.common.context import BaseContext
from pyvider.resources.private_state import PrivateState

PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)


@define(frozen=True)
class EphemeralResourceContext[ConfigType, PrivateStateType](BaseContext):
    """
    Context for ephemeral resource operations. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: ConfigType | None = None
    private_state: PrivateStateType | None = None
