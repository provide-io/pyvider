# pyvider/schema/__init__.py
from pyvider.schema.factory import (
    a_bool,
    a_dyn,
    a_list,
    a_map,
    a_null,
    a_num,
    a_obj,
    a_set,
    a_str,
    a_tuple,
    a_unknown,
    b_group,
    b_list,
    b_main,
    b_map,
    b_set,
    b_single,
    s_data_source,
    s_provider,
    s_resource,
)
from pyvider.schema.types import (
    NestingMode,
    PvsAttribute,
    PvsNestedBlock,
    PvsObjectType,
    PvsSchema,
    PvsType,
)

__all__ = [
    "NestingMode",
    "PvsAttribute",
    "PvsNestedBlock",
    "PvsObjectType",
    "PvsSchema",
    "PvsType",
    "a_bool",
    "a_dyn",
    "a_list",
    "a_map",
    "a_null",
    "a_num",
    "a_obj",
    "a_set",
    "a_str",
    "a_tuple",
    "a_unknown",
    "b_group",
    "b_list",
    "b_main",
    "b_map",
    "b_set",
    "b_single",
    "s_data_source",
    "s_provider",
    "s_resource",
]
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
