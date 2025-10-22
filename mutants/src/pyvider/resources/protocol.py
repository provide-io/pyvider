#
# pyvider/resources/protocol.py
#

from typing import Protocol, runtime_checkable

from pyvider.common.types import ConfigType, StateType
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.resources.types import ResourceType
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


# 🐍🏗️
