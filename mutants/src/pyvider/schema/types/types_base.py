# pyvider-schema/src/pyvider/schema/types/types_base.py
"""Base protocols to prevent circular imports in schema definitions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pyvider.cty import CtyType
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
class PvsType(Protocol):
    """
    A Protocol that all Pyvider Schema type definition classes must implement.
    It ensures that any schema type object can be converted into its
    corresponding CtyType, which is essential for the conversion and
    marshalling layers of the framework.
    """

    def to_cty_type(self) -> CtyType:
        """Converts the Pyvider Schema type to its equivalent CtyType."""
        ...
