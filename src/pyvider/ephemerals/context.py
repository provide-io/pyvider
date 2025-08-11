from typing import Generic, TypeVar

from attrs import define

from pyvider.common.context import BaseContext
from pyvider.resources.private_state import PrivateState

ConfigType = TypeVar("ConfigType")
PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)


@define(frozen=True)
class EphemeralResourceContext(BaseContext, Generic[ConfigType, PrivateStateType]):
    """
    Context for ephemeral resource operations. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: ConfigType | None = None
    private_state: PrivateStateType | None = None
