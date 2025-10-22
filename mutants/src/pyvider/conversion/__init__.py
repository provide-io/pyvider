"""
The pyvider.conversion package provides the primary bridge between the wire
protocol (via DynamicValue) and the framework's internal CtyValue representation.
"""

# Import the canonical type inference logic from the cty package.
from pyvider.conversion.adapter import cty_to_native
from pyvider.conversion.marshaler import marshal, marshal_value, unmarshal, unmarshal_value
from pyvider.conversion.schema_adapter import pvs_schema_to_proto
from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty.conversion import infer_cty_type_from_raw

__all__ = [
    "cty_to_native",
    "infer_cty_type_from_raw",  # Export the canonical function
    "marshal",
    "marshal_value",
    "pvs_schema_to_proto",
    "unify_and_validate_list_of_objects",
    "unmarshal",
    "unmarshal_value",
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
