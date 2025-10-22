#
# pyvider/resources/lifecycle.py
#

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
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


class ResourceState(Enum):
    """Resource lifecycle states."""

    UNKNOWN = "UNKNOWN"
    PLANNED = "PLANNED"
    CREATING = "CREATING"
    CREATED = "CREATED"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    DELETED = "DELETED"
    FAILED = "FAILED"


@dataclass
class ResourceLifecycle:
    """Tracks resource lifecycle state."""

    state: ResourceState = ResourceState.UNKNOWN
    last_operation: str | None = None
    last_updated: datetime | None = None
    error: str | None = None

    def transition_to(self, state: ResourceState, operation: str) -> None:
        """Transition to a new state."""
        self.state = state
        self.last_operation = operation
        self.last_updated = datetime.now(UTC)


# 🐍🏗️
