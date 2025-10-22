import inspect
import re
from typing import Any

import attrs
from provide.foundation import logger
from provide.foundation.errors import FoundationError

from pyvider.cty import CtyList, CtyObject, CtyTuple, CtyValue
from pyvider.cty.exceptions import (
    CtyAttributeValidationError,
    CtyBoolValidationError,
    CtyListValidationError,
    CtyMapValidationError,
    CtyNumberValidationError,
    CtySetValidationError,
    CtyStringValidationError,
    CtyTupleValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
from pyvider.exceptions import (
    DataSourceError,
    FunctionError,
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource

# Regex to parse attribute paths like `attr`, `attr[0]`, `attr["key"]`
PATH_STEP_REGEX = re.compile(r"(\.?)(\w+)|\[(\d+)\]|\[['\"]([^'\"]+)['\"]\]")
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


def x__process_instance__mutmut_orig(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_1(instance: Any, _visited: set[int]) -> Any:
    obj_id = None
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_2(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(None)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_3(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id not in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_4(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(None):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_5(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(None)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_6(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"XX__circular_ref__XX": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_7(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__CIRCULAR_REF__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_8(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(None).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_9(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(None).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_10(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_11(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(None)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_12(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(None):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_13(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(None)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_14(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = None
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_15(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(None):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_16(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(None)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_17(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = None
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_18(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(None, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_19(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, None)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_20(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_21(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, )
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_22(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = None
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_23(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(None, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_24(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, None)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_25(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(_visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_26(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, )
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_27(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(None)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_28(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(None, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_29(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, None) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_30(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(_visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_31(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, ) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_32(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(None, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_33(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, None) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_34(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(_visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_35(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, ) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_36(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(None, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_37(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, None) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_38(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(_visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_39(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, ) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_40(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) or obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_41(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_42(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id not in _visited:
            _visited.remove(obj_id)


def x__process_instance__mutmut_43(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(None)

x__process_instance__mutmut_mutants : ClassVar[MutantDict] = {
'x__process_instance__mutmut_1': x__process_instance__mutmut_1, 
    'x__process_instance__mutmut_2': x__process_instance__mutmut_2, 
    'x__process_instance__mutmut_3': x__process_instance__mutmut_3, 
    'x__process_instance__mutmut_4': x__process_instance__mutmut_4, 
    'x__process_instance__mutmut_5': x__process_instance__mutmut_5, 
    'x__process_instance__mutmut_6': x__process_instance__mutmut_6, 
    'x__process_instance__mutmut_7': x__process_instance__mutmut_7, 
    'x__process_instance__mutmut_8': x__process_instance__mutmut_8, 
    'x__process_instance__mutmut_9': x__process_instance__mutmut_9, 
    'x__process_instance__mutmut_10': x__process_instance__mutmut_10, 
    'x__process_instance__mutmut_11': x__process_instance__mutmut_11, 
    'x__process_instance__mutmut_12': x__process_instance__mutmut_12, 
    'x__process_instance__mutmut_13': x__process_instance__mutmut_13, 
    'x__process_instance__mutmut_14': x__process_instance__mutmut_14, 
    'x__process_instance__mutmut_15': x__process_instance__mutmut_15, 
    'x__process_instance__mutmut_16': x__process_instance__mutmut_16, 
    'x__process_instance__mutmut_17': x__process_instance__mutmut_17, 
    'x__process_instance__mutmut_18': x__process_instance__mutmut_18, 
    'x__process_instance__mutmut_19': x__process_instance__mutmut_19, 
    'x__process_instance__mutmut_20': x__process_instance__mutmut_20, 
    'x__process_instance__mutmut_21': x__process_instance__mutmut_21, 
    'x__process_instance__mutmut_22': x__process_instance__mutmut_22, 
    'x__process_instance__mutmut_23': x__process_instance__mutmut_23, 
    'x__process_instance__mutmut_24': x__process_instance__mutmut_24, 
    'x__process_instance__mutmut_25': x__process_instance__mutmut_25, 
    'x__process_instance__mutmut_26': x__process_instance__mutmut_26, 
    'x__process_instance__mutmut_27': x__process_instance__mutmut_27, 
    'x__process_instance__mutmut_28': x__process_instance__mutmut_28, 
    'x__process_instance__mutmut_29': x__process_instance__mutmut_29, 
    'x__process_instance__mutmut_30': x__process_instance__mutmut_30, 
    'x__process_instance__mutmut_31': x__process_instance__mutmut_31, 
    'x__process_instance__mutmut_32': x__process_instance__mutmut_32, 
    'x__process_instance__mutmut_33': x__process_instance__mutmut_33, 
    'x__process_instance__mutmut_34': x__process_instance__mutmut_34, 
    'x__process_instance__mutmut_35': x__process_instance__mutmut_35, 
    'x__process_instance__mutmut_36': x__process_instance__mutmut_36, 
    'x__process_instance__mutmut_37': x__process_instance__mutmut_37, 
    'x__process_instance__mutmut_38': x__process_instance__mutmut_38, 
    'x__process_instance__mutmut_39': x__process_instance__mutmut_39, 
    'x__process_instance__mutmut_40': x__process_instance__mutmut_40, 
    'x__process_instance__mutmut_41': x__process_instance__mutmut_41, 
    'x__process_instance__mutmut_42': x__process_instance__mutmut_42, 
    'x__process_instance__mutmut_43': x__process_instance__mutmut_43
}

def _process_instance(*args, **kwargs):
    result = _mutmut_trampoline(x__process_instance__mutmut_orig, x__process_instance__mutmut_mutants, args, kwargs)
    return result 

_process_instance.__signature__ = _mutmut_signature(x__process_instance__mutmut_orig)
x__process_instance__mutmut_orig.__name__ = 'x__process_instance'


def x_attrs_to_dict_for_cty__mutmut_orig(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, _visited)


def x_attrs_to_dict_for_cty__mutmut_1(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is not None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, _visited)


def x_attrs_to_dict_for_cty__mutmut_2(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = None

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, _visited)


def x_attrs_to_dict_for_cty__mutmut_3(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(None, _visited)


def x_attrs_to_dict_for_cty__mutmut_4(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, None)


def x_attrs_to_dict_for_cty__mutmut_5(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(_visited)


def x_attrs_to_dict_for_cty__mutmut_6(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, )

x_attrs_to_dict_for_cty__mutmut_mutants : ClassVar[MutantDict] = {
'x_attrs_to_dict_for_cty__mutmut_1': x_attrs_to_dict_for_cty__mutmut_1, 
    'x_attrs_to_dict_for_cty__mutmut_2': x_attrs_to_dict_for_cty__mutmut_2, 
    'x_attrs_to_dict_for_cty__mutmut_3': x_attrs_to_dict_for_cty__mutmut_3, 
    'x_attrs_to_dict_for_cty__mutmut_4': x_attrs_to_dict_for_cty__mutmut_4, 
    'x_attrs_to_dict_for_cty__mutmut_5': x_attrs_to_dict_for_cty__mutmut_5, 
    'x_attrs_to_dict_for_cty__mutmut_6': x_attrs_to_dict_for_cty__mutmut_6
}

def attrs_to_dict_for_cty(*args, **kwargs):
    result = _mutmut_trampoline(x_attrs_to_dict_for_cty__mutmut_orig, x_attrs_to_dict_for_cty__mutmut_mutants, args, kwargs)
    return result 

attrs_to_dict_for_cty.__signature__ = _mutmut_signature(x_attrs_to_dict_for_cty__mutmut_orig)
x_attrs_to_dict_for_cty__mutmut_orig.__name__ = 'x_attrs_to_dict_for_cty'


def x__check_type_and_unknown__mutmut_orig(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_1(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_2(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(None):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_3(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            True,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_4(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is not UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_5(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return False, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_6(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, "XXXX"

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_7(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return False, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_8(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, "XXXX"

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_9(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return True, "Value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_10(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "XXValue was known in plan but became unknown in result.XX"

    return True, ""


def x__check_type_and_unknown__mutmut_11(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "value was known in plan but became unknown in result."

    return True, ""


def x__check_type_and_unknown__mutmut_12(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "VALUE WAS KNOWN IN PLAN BUT BECAME UNKNOWN IN RESULT."

    return True, ""


def x__check_type_and_unknown__mutmut_13(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return False, ""


def x__check_type_and_unknown__mutmut_14(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, "XXXX"

x__check_type_and_unknown__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_type_and_unknown__mutmut_1': x__check_type_and_unknown__mutmut_1, 
    'x__check_type_and_unknown__mutmut_2': x__check_type_and_unknown__mutmut_2, 
    'x__check_type_and_unknown__mutmut_3': x__check_type_and_unknown__mutmut_3, 
    'x__check_type_and_unknown__mutmut_4': x__check_type_and_unknown__mutmut_4, 
    'x__check_type_and_unknown__mutmut_5': x__check_type_and_unknown__mutmut_5, 
    'x__check_type_and_unknown__mutmut_6': x__check_type_and_unknown__mutmut_6, 
    'x__check_type_and_unknown__mutmut_7': x__check_type_and_unknown__mutmut_7, 
    'x__check_type_and_unknown__mutmut_8': x__check_type_and_unknown__mutmut_8, 
    'x__check_type_and_unknown__mutmut_9': x__check_type_and_unknown__mutmut_9, 
    'x__check_type_and_unknown__mutmut_10': x__check_type_and_unknown__mutmut_10, 
    'x__check_type_and_unknown__mutmut_11': x__check_type_and_unknown__mutmut_11, 
    'x__check_type_and_unknown__mutmut_12': x__check_type_and_unknown__mutmut_12, 
    'x__check_type_and_unknown__mutmut_13': x__check_type_and_unknown__mutmut_13, 
    'x__check_type_and_unknown__mutmut_14': x__check_type_and_unknown__mutmut_14
}

def _check_type_and_unknown(*args, **kwargs):
    result = _mutmut_trampoline(x__check_type_and_unknown__mutmut_orig, x__check_type_and_unknown__mutmut_mutants, args, kwargs)
    return result 

_check_type_and_unknown.__signature__ = _mutmut_signature(x__check_type_and_unknown__mutmut_orig)
x__check_type_and_unknown__mutmut_orig.__name__ = 'x__check_type_and_unknown'


def x__check_null_refinement__mutmut_orig(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, ""


def x__check_null_refinement__mutmut_1(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return False, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, ""


def x__check_null_refinement__mutmut_2(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, "XXXX"

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, ""


def x__check_null_refinement__mutmut_3(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return True, "Value was non-null in plan but became null in result."

    return True, ""


def x__check_null_refinement__mutmut_4(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "XXValue was non-null in plan but became null in result.XX"

    return True, ""


def x__check_null_refinement__mutmut_5(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "value was non-null in plan but became null in result."

    return True, ""


def x__check_null_refinement__mutmut_6(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "VALUE WAS NON-NULL IN PLAN BUT BECAME NULL IN RESULT."

    return True, ""


def x__check_null_refinement__mutmut_7(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return False, ""


def x__check_null_refinement__mutmut_8(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, "XXXX"

x__check_null_refinement__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_null_refinement__mutmut_1': x__check_null_refinement__mutmut_1, 
    'x__check_null_refinement__mutmut_2': x__check_null_refinement__mutmut_2, 
    'x__check_null_refinement__mutmut_3': x__check_null_refinement__mutmut_3, 
    'x__check_null_refinement__mutmut_4': x__check_null_refinement__mutmut_4, 
    'x__check_null_refinement__mutmut_5': x__check_null_refinement__mutmut_5, 
    'x__check_null_refinement__mutmut_6': x__check_null_refinement__mutmut_6, 
    'x__check_null_refinement__mutmut_7': x__check_null_refinement__mutmut_7, 
    'x__check_null_refinement__mutmut_8': x__check_null_refinement__mutmut_8
}

def _check_null_refinement(*args, **kwargs):
    result = _mutmut_trampoline(x__check_null_refinement__mutmut_orig, x__check_null_refinement__mutmut_mutants, args, kwargs)
    return result 

_check_null_refinement.__signature__ = _mutmut_signature(x__check_null_refinement__mutmut_orig)
x__check_null_refinement__mutmut_orig.__name__ = 'x__check_null_refinement'


def x__check_object_refinement__mutmut_orig(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_1(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() == result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_2(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            True,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_3(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = None
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_4(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(None, result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_5(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], None)
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_6(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_7(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], )
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_8(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_9(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return True, f"Attribute '{attr_name}': {reason}"
    return True, ""


def x__check_object_refinement__mutmut_10(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return False, ""


def x__check_object_refinement__mutmut_11(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, "XXXX"

x__check_object_refinement__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_object_refinement__mutmut_1': x__check_object_refinement__mutmut_1, 
    'x__check_object_refinement__mutmut_2': x__check_object_refinement__mutmut_2, 
    'x__check_object_refinement__mutmut_3': x__check_object_refinement__mutmut_3, 
    'x__check_object_refinement__mutmut_4': x__check_object_refinement__mutmut_4, 
    'x__check_object_refinement__mutmut_5': x__check_object_refinement__mutmut_5, 
    'x__check_object_refinement__mutmut_6': x__check_object_refinement__mutmut_6, 
    'x__check_object_refinement__mutmut_7': x__check_object_refinement__mutmut_7, 
    'x__check_object_refinement__mutmut_8': x__check_object_refinement__mutmut_8, 
    'x__check_object_refinement__mutmut_9': x__check_object_refinement__mutmut_9, 
    'x__check_object_refinement__mutmut_10': x__check_object_refinement__mutmut_10, 
    'x__check_object_refinement__mutmut_11': x__check_object_refinement__mutmut_11
}

def _check_object_refinement(*args, **kwargs):
    result = _mutmut_trampoline(x__check_object_refinement__mutmut_orig, x__check_object_refinement__mutmut_mutants, args, kwargs)
    return result 

_check_object_refinement.__signature__ = _mutmut_signature(x__check_object_refinement__mutmut_orig)
x__check_object_refinement__mutmut_orig.__name__ = 'x__check_object_refinement'


def x__check_collection_refinement__mutmut_orig(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_1(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) == len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_2(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            True,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_3(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(None):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_4(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = None
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_5(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(None, result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_6(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], None)
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_7(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_8(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], )
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_9(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_10(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return True, f"Index [{i}]: {reason}"
    return True, ""


def x__check_collection_refinement__mutmut_11(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return False, ""


def x__check_collection_refinement__mutmut_12(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, "XXXX"

x__check_collection_refinement__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_collection_refinement__mutmut_1': x__check_collection_refinement__mutmut_1, 
    'x__check_collection_refinement__mutmut_2': x__check_collection_refinement__mutmut_2, 
    'x__check_collection_refinement__mutmut_3': x__check_collection_refinement__mutmut_3, 
    'x__check_collection_refinement__mutmut_4': x__check_collection_refinement__mutmut_4, 
    'x__check_collection_refinement__mutmut_5': x__check_collection_refinement__mutmut_5, 
    'x__check_collection_refinement__mutmut_6': x__check_collection_refinement__mutmut_6, 
    'x__check_collection_refinement__mutmut_7': x__check_collection_refinement__mutmut_7, 
    'x__check_collection_refinement__mutmut_8': x__check_collection_refinement__mutmut_8, 
    'x__check_collection_refinement__mutmut_9': x__check_collection_refinement__mutmut_9, 
    'x__check_collection_refinement__mutmut_10': x__check_collection_refinement__mutmut_10, 
    'x__check_collection_refinement__mutmut_11': x__check_collection_refinement__mutmut_11, 
    'x__check_collection_refinement__mutmut_12': x__check_collection_refinement__mutmut_12
}

def _check_collection_refinement(*args, **kwargs):
    result = _mutmut_trampoline(x__check_collection_refinement__mutmut_orig, x__check_collection_refinement__mutmut_mutants, args, kwargs)
    return result 

_check_collection_refinement.__signature__ = _mutmut_signature(x__check_collection_refinement__mutmut_orig)
x__check_collection_refinement__mutmut_orig.__name__ = 'x__check_collection_refinement'


def x_is_valid_refinement__mutmut_orig(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_1(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = None
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_2(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(None, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_3(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, None)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_4(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_5(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, )
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_6(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_7(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return True, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_8(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = None
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_9(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(None, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_10(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, None)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_11(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_12(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, )
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_13(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_14(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return True, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_15(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(None, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_16(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, None)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_17(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_18(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, )

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_19(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(None, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_20(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, None)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_21(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_22(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, )

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_23(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return False, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_24(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, "XXXX"

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_25(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value == result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_26(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            True,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def x_is_valid_refinement__mutmut_27(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return False, ""


def x_is_valid_refinement__mutmut_28(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, "XXXX"

x_is_valid_refinement__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_valid_refinement__mutmut_1': x_is_valid_refinement__mutmut_1, 
    'x_is_valid_refinement__mutmut_2': x_is_valid_refinement__mutmut_2, 
    'x_is_valid_refinement__mutmut_3': x_is_valid_refinement__mutmut_3, 
    'x_is_valid_refinement__mutmut_4': x_is_valid_refinement__mutmut_4, 
    'x_is_valid_refinement__mutmut_5': x_is_valid_refinement__mutmut_5, 
    'x_is_valid_refinement__mutmut_6': x_is_valid_refinement__mutmut_6, 
    'x_is_valid_refinement__mutmut_7': x_is_valid_refinement__mutmut_7, 
    'x_is_valid_refinement__mutmut_8': x_is_valid_refinement__mutmut_8, 
    'x_is_valid_refinement__mutmut_9': x_is_valid_refinement__mutmut_9, 
    'x_is_valid_refinement__mutmut_10': x_is_valid_refinement__mutmut_10, 
    'x_is_valid_refinement__mutmut_11': x_is_valid_refinement__mutmut_11, 
    'x_is_valid_refinement__mutmut_12': x_is_valid_refinement__mutmut_12, 
    'x_is_valid_refinement__mutmut_13': x_is_valid_refinement__mutmut_13, 
    'x_is_valid_refinement__mutmut_14': x_is_valid_refinement__mutmut_14, 
    'x_is_valid_refinement__mutmut_15': x_is_valid_refinement__mutmut_15, 
    'x_is_valid_refinement__mutmut_16': x_is_valid_refinement__mutmut_16, 
    'x_is_valid_refinement__mutmut_17': x_is_valid_refinement__mutmut_17, 
    'x_is_valid_refinement__mutmut_18': x_is_valid_refinement__mutmut_18, 
    'x_is_valid_refinement__mutmut_19': x_is_valid_refinement__mutmut_19, 
    'x_is_valid_refinement__mutmut_20': x_is_valid_refinement__mutmut_20, 
    'x_is_valid_refinement__mutmut_21': x_is_valid_refinement__mutmut_21, 
    'x_is_valid_refinement__mutmut_22': x_is_valid_refinement__mutmut_22, 
    'x_is_valid_refinement__mutmut_23': x_is_valid_refinement__mutmut_23, 
    'x_is_valid_refinement__mutmut_24': x_is_valid_refinement__mutmut_24, 
    'x_is_valid_refinement__mutmut_25': x_is_valid_refinement__mutmut_25, 
    'x_is_valid_refinement__mutmut_26': x_is_valid_refinement__mutmut_26, 
    'x_is_valid_refinement__mutmut_27': x_is_valid_refinement__mutmut_27, 
    'x_is_valid_refinement__mutmut_28': x_is_valid_refinement__mutmut_28
}

def is_valid_refinement(*args, **kwargs):
    result = _mutmut_trampoline(x_is_valid_refinement__mutmut_orig, x_is_valid_refinement__mutmut_mutants, args, kwargs)
    return result 

is_valid_refinement.__signature__ = _mutmut_signature(x_is_valid_refinement__mutmut_orig)
x_is_valid_refinement__mutmut_orig.__name__ = 'x_is_valid_refinement'


def x_str_path_to_proto_path__mutmut_orig(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_1(path_str: str | None) -> pb.AttributePath | None:
    if path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_2(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = None
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_3(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = None

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_4(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace(None, "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_5(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", None)

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_6(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_7(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", )

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_8(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("XX].XX", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_9(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "XX][XX")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_10(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(None):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_11(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = None
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_12(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(None)
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_13(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=None))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_14(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(None)
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_15(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=None))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_16(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(None)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_17(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(None)

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_18(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=None))

    return pb.AttributePath(steps=proto_steps)


def x_str_path_to_proto_path__mutmut_19(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=None)

x_str_path_to_proto_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_str_path_to_proto_path__mutmut_1': x_str_path_to_proto_path__mutmut_1, 
    'x_str_path_to_proto_path__mutmut_2': x_str_path_to_proto_path__mutmut_2, 
    'x_str_path_to_proto_path__mutmut_3': x_str_path_to_proto_path__mutmut_3, 
    'x_str_path_to_proto_path__mutmut_4': x_str_path_to_proto_path__mutmut_4, 
    'x_str_path_to_proto_path__mutmut_5': x_str_path_to_proto_path__mutmut_5, 
    'x_str_path_to_proto_path__mutmut_6': x_str_path_to_proto_path__mutmut_6, 
    'x_str_path_to_proto_path__mutmut_7': x_str_path_to_proto_path__mutmut_7, 
    'x_str_path_to_proto_path__mutmut_8': x_str_path_to_proto_path__mutmut_8, 
    'x_str_path_to_proto_path__mutmut_9': x_str_path_to_proto_path__mutmut_9, 
    'x_str_path_to_proto_path__mutmut_10': x_str_path_to_proto_path__mutmut_10, 
    'x_str_path_to_proto_path__mutmut_11': x_str_path_to_proto_path__mutmut_11, 
    'x_str_path_to_proto_path__mutmut_12': x_str_path_to_proto_path__mutmut_12, 
    'x_str_path_to_proto_path__mutmut_13': x_str_path_to_proto_path__mutmut_13, 
    'x_str_path_to_proto_path__mutmut_14': x_str_path_to_proto_path__mutmut_14, 
    'x_str_path_to_proto_path__mutmut_15': x_str_path_to_proto_path__mutmut_15, 
    'x_str_path_to_proto_path__mutmut_16': x_str_path_to_proto_path__mutmut_16, 
    'x_str_path_to_proto_path__mutmut_17': x_str_path_to_proto_path__mutmut_17, 
    'x_str_path_to_proto_path__mutmut_18': x_str_path_to_proto_path__mutmut_18, 
    'x_str_path_to_proto_path__mutmut_19': x_str_path_to_proto_path__mutmut_19
}

def str_path_to_proto_path(*args, **kwargs):
    result = _mutmut_trampoline(x_str_path_to_proto_path__mutmut_orig, x_str_path_to_proto_path__mutmut_mutants, args, kwargs)
    return result 

str_path_to_proto_path.__signature__ = _mutmut_signature(x_str_path_to_proto_path__mutmut_orig)
x_str_path_to_proto_path__mutmut_orig.__name__ = 'x_str_path_to_proto_path'


def x_cty_path_to_proto_path__mutmut_orig(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_1(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path and not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_2(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_3(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_4(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = None
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_5(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_6(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_7(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_8(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(None)
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_9(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=None))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_10(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(None)
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_11(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=None))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_12(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(None)
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_13(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=None))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_14(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(None)))
    return pb.AttributePath(steps=proto_steps)


def x_cty_path_to_proto_path__mutmut_15(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=None)

x_cty_path_to_proto_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_cty_path_to_proto_path__mutmut_1': x_cty_path_to_proto_path__mutmut_1, 
    'x_cty_path_to_proto_path__mutmut_2': x_cty_path_to_proto_path__mutmut_2, 
    'x_cty_path_to_proto_path__mutmut_3': x_cty_path_to_proto_path__mutmut_3, 
    'x_cty_path_to_proto_path__mutmut_4': x_cty_path_to_proto_path__mutmut_4, 
    'x_cty_path_to_proto_path__mutmut_5': x_cty_path_to_proto_path__mutmut_5, 
    'x_cty_path_to_proto_path__mutmut_6': x_cty_path_to_proto_path__mutmut_6, 
    'x_cty_path_to_proto_path__mutmut_7': x_cty_path_to_proto_path__mutmut_7, 
    'x_cty_path_to_proto_path__mutmut_8': x_cty_path_to_proto_path__mutmut_8, 
    'x_cty_path_to_proto_path__mutmut_9': x_cty_path_to_proto_path__mutmut_9, 
    'x_cty_path_to_proto_path__mutmut_10': x_cty_path_to_proto_path__mutmut_10, 
    'x_cty_path_to_proto_path__mutmut_11': x_cty_path_to_proto_path__mutmut_11, 
    'x_cty_path_to_proto_path__mutmut_12': x_cty_path_to_proto_path__mutmut_12, 
    'x_cty_path_to_proto_path__mutmut_13': x_cty_path_to_proto_path__mutmut_13, 
    'x_cty_path_to_proto_path__mutmut_14': x_cty_path_to_proto_path__mutmut_14, 
    'x_cty_path_to_proto_path__mutmut_15': x_cty_path_to_proto_path__mutmut_15
}

def cty_path_to_proto_path(*args, **kwargs):
    result = _mutmut_trampoline(x_cty_path_to_proto_path__mutmut_orig, x_cty_path_to_proto_path__mutmut_mutants, args, kwargs)
    return result 

cty_path_to_proto_path.__signature__ = _mutmut_signature(x_cty_path_to_proto_path__mutmut_orig)
x_cty_path_to_proto_path__mutmut_orig.__name__ = 'x_cty_path_to_proto_path'


async def x_create_diagnostic_from_exception__mutmut_orig(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_1(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = None
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_2(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "XXAn unexpected error occurredXX"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_3(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "an unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_4(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "AN UNEXPECTED ERROR OCCURRED"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_5(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = None
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_6(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(None)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_7(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = ""
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_8(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = None

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_9(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = None

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_10(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = None
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_11(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = None
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_12(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") or exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_13(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(None, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_14(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, None) and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_15(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr("value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_16(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, ) and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_17(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "XXvalueXX") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_18(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "VALUE") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_19(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_20(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = None
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_21(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(None)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_22(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) >= 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_23(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 101:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_24(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = None
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_25(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] - "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_26(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:98] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_27(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "XX...XX"
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_28(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail = f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_29(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail -= f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_30(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = None
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_31(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = None
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_32(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = None
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_33(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "XXA configuration validation error occurred.XX"
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_34(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "a configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_35(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A CONFIGURATION VALIDATION ERROR OCCURRED."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_36(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = None
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_37(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) or hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_38(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(None, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_39(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, None):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_40(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr("context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_41(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, ):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_42(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "XXcontextXX"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_43(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "CONTEXT"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_44(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = None

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_45(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = None

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_46(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "XXterraform.summaryXX" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_47(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "TERRAFORM.SUMMARY" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_48(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" not in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_49(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = None

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_50(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["XXterraform.summaryXX"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_51(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["TERRAFORM.SUMMARY"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_52(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = None
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_53(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(None)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_54(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "XXterraform.detailXX" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_55(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "TERRAFORM.DETAIL" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_56(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" not in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_57(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(None)

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_58(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["XXterraform.detailXX"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_59(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["TERRAFORM.DETAIL"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_60(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" or value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_61(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") or key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_62(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_63(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith(None) and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_64(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("XXterraform.XX") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_65(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("TERRAFORM.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_66(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key == "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_67(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "XXprivate_state.errorXX" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_68(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "PRIVATE_STATE.ERROR" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_69(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(None)

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_70(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = None
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_71(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(None) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_72(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "XX\nXX".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_73(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(None)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_74(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = None
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_75(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "XX🐍🏗️ ⚠️ Resource Lifecycle Contract ViolationXX"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_76(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ resource lifecycle contract violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_77(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ RESOURCE LIFECYCLE CONTRACT VIOLATION"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_78(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = None
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_79(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(None)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_80(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") or exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_81(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(None, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_82(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, None) and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_83(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr("detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_84(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, ) and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_85(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "XXdetailXX") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_86(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "DETAIL") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_87(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail = f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_88(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail -= f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_89(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = None
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_90(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "XX🐍🏗️ ❌ Function Execution ErrorXX"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_91(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ function execution error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_92(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ FUNCTION EXECUTION ERROR"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_93(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = None
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_94(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(None)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_95(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = None
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_96(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "XX🐍🏗️ ❌ Provider Operation ErrorXX"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_97(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ provider operation error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_98(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ PROVIDER OPERATION ERROR"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_99(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = None
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_100(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(None)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_101(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = None
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_102(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "XX🐍🏗️ ❌ Provider Framework ErrorXX"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_103(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ provider framework error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_104(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ PROVIDER FRAMEWORK ERROR"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_105(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = None
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_106(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(None)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_107(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = None
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_108(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(None).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_109(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = None
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_110(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "XXThe provider encountered an unexpected error. This is likely a bug in the provider.XX"
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_111(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "the provider encountered an unexpected error. this is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_112(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "THE PROVIDER ENCOUNTERED AN UNEXPECTED ERROR. THIS IS LIKELY A BUG IN THE PROVIDER."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_113(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "XX\nPlease report this issue to the provider developers.XX"
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_114(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nplease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_115(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPLEASE REPORT THIS ISSUE TO THE PROVIDER DEVELOPERS."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_116(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                None,
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_117(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=None,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_118(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_119(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_120(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(None).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_121(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=False,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_122(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=None,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_123(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=None,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_124(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=None,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_125(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=None,
    )


async def x_create_diagnostic_from_exception__mutmut_126(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_127(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_128(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        attribute=cty_path_to_proto_path(attribute_path),
    )


async def x_create_diagnostic_from_exception__mutmut_129(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        )


async def x_create_diagnostic_from_exception__mutmut_130(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(None),
    )

x_create_diagnostic_from_exception__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_diagnostic_from_exception__mutmut_1': x_create_diagnostic_from_exception__mutmut_1, 
    'x_create_diagnostic_from_exception__mutmut_2': x_create_diagnostic_from_exception__mutmut_2, 
    'x_create_diagnostic_from_exception__mutmut_3': x_create_diagnostic_from_exception__mutmut_3, 
    'x_create_diagnostic_from_exception__mutmut_4': x_create_diagnostic_from_exception__mutmut_4, 
    'x_create_diagnostic_from_exception__mutmut_5': x_create_diagnostic_from_exception__mutmut_5, 
    'x_create_diagnostic_from_exception__mutmut_6': x_create_diagnostic_from_exception__mutmut_6, 
    'x_create_diagnostic_from_exception__mutmut_7': x_create_diagnostic_from_exception__mutmut_7, 
    'x_create_diagnostic_from_exception__mutmut_8': x_create_diagnostic_from_exception__mutmut_8, 
    'x_create_diagnostic_from_exception__mutmut_9': x_create_diagnostic_from_exception__mutmut_9, 
    'x_create_diagnostic_from_exception__mutmut_10': x_create_diagnostic_from_exception__mutmut_10, 
    'x_create_diagnostic_from_exception__mutmut_11': x_create_diagnostic_from_exception__mutmut_11, 
    'x_create_diagnostic_from_exception__mutmut_12': x_create_diagnostic_from_exception__mutmut_12, 
    'x_create_diagnostic_from_exception__mutmut_13': x_create_diagnostic_from_exception__mutmut_13, 
    'x_create_diagnostic_from_exception__mutmut_14': x_create_diagnostic_from_exception__mutmut_14, 
    'x_create_diagnostic_from_exception__mutmut_15': x_create_diagnostic_from_exception__mutmut_15, 
    'x_create_diagnostic_from_exception__mutmut_16': x_create_diagnostic_from_exception__mutmut_16, 
    'x_create_diagnostic_from_exception__mutmut_17': x_create_diagnostic_from_exception__mutmut_17, 
    'x_create_diagnostic_from_exception__mutmut_18': x_create_diagnostic_from_exception__mutmut_18, 
    'x_create_diagnostic_from_exception__mutmut_19': x_create_diagnostic_from_exception__mutmut_19, 
    'x_create_diagnostic_from_exception__mutmut_20': x_create_diagnostic_from_exception__mutmut_20, 
    'x_create_diagnostic_from_exception__mutmut_21': x_create_diagnostic_from_exception__mutmut_21, 
    'x_create_diagnostic_from_exception__mutmut_22': x_create_diagnostic_from_exception__mutmut_22, 
    'x_create_diagnostic_from_exception__mutmut_23': x_create_diagnostic_from_exception__mutmut_23, 
    'x_create_diagnostic_from_exception__mutmut_24': x_create_diagnostic_from_exception__mutmut_24, 
    'x_create_diagnostic_from_exception__mutmut_25': x_create_diagnostic_from_exception__mutmut_25, 
    'x_create_diagnostic_from_exception__mutmut_26': x_create_diagnostic_from_exception__mutmut_26, 
    'x_create_diagnostic_from_exception__mutmut_27': x_create_diagnostic_from_exception__mutmut_27, 
    'x_create_diagnostic_from_exception__mutmut_28': x_create_diagnostic_from_exception__mutmut_28, 
    'x_create_diagnostic_from_exception__mutmut_29': x_create_diagnostic_from_exception__mutmut_29, 
    'x_create_diagnostic_from_exception__mutmut_30': x_create_diagnostic_from_exception__mutmut_30, 
    'x_create_diagnostic_from_exception__mutmut_31': x_create_diagnostic_from_exception__mutmut_31, 
    'x_create_diagnostic_from_exception__mutmut_32': x_create_diagnostic_from_exception__mutmut_32, 
    'x_create_diagnostic_from_exception__mutmut_33': x_create_diagnostic_from_exception__mutmut_33, 
    'x_create_diagnostic_from_exception__mutmut_34': x_create_diagnostic_from_exception__mutmut_34, 
    'x_create_diagnostic_from_exception__mutmut_35': x_create_diagnostic_from_exception__mutmut_35, 
    'x_create_diagnostic_from_exception__mutmut_36': x_create_diagnostic_from_exception__mutmut_36, 
    'x_create_diagnostic_from_exception__mutmut_37': x_create_diagnostic_from_exception__mutmut_37, 
    'x_create_diagnostic_from_exception__mutmut_38': x_create_diagnostic_from_exception__mutmut_38, 
    'x_create_diagnostic_from_exception__mutmut_39': x_create_diagnostic_from_exception__mutmut_39, 
    'x_create_diagnostic_from_exception__mutmut_40': x_create_diagnostic_from_exception__mutmut_40, 
    'x_create_diagnostic_from_exception__mutmut_41': x_create_diagnostic_from_exception__mutmut_41, 
    'x_create_diagnostic_from_exception__mutmut_42': x_create_diagnostic_from_exception__mutmut_42, 
    'x_create_diagnostic_from_exception__mutmut_43': x_create_diagnostic_from_exception__mutmut_43, 
    'x_create_diagnostic_from_exception__mutmut_44': x_create_diagnostic_from_exception__mutmut_44, 
    'x_create_diagnostic_from_exception__mutmut_45': x_create_diagnostic_from_exception__mutmut_45, 
    'x_create_diagnostic_from_exception__mutmut_46': x_create_diagnostic_from_exception__mutmut_46, 
    'x_create_diagnostic_from_exception__mutmut_47': x_create_diagnostic_from_exception__mutmut_47, 
    'x_create_diagnostic_from_exception__mutmut_48': x_create_diagnostic_from_exception__mutmut_48, 
    'x_create_diagnostic_from_exception__mutmut_49': x_create_diagnostic_from_exception__mutmut_49, 
    'x_create_diagnostic_from_exception__mutmut_50': x_create_diagnostic_from_exception__mutmut_50, 
    'x_create_diagnostic_from_exception__mutmut_51': x_create_diagnostic_from_exception__mutmut_51, 
    'x_create_diagnostic_from_exception__mutmut_52': x_create_diagnostic_from_exception__mutmut_52, 
    'x_create_diagnostic_from_exception__mutmut_53': x_create_diagnostic_from_exception__mutmut_53, 
    'x_create_diagnostic_from_exception__mutmut_54': x_create_diagnostic_from_exception__mutmut_54, 
    'x_create_diagnostic_from_exception__mutmut_55': x_create_diagnostic_from_exception__mutmut_55, 
    'x_create_diagnostic_from_exception__mutmut_56': x_create_diagnostic_from_exception__mutmut_56, 
    'x_create_diagnostic_from_exception__mutmut_57': x_create_diagnostic_from_exception__mutmut_57, 
    'x_create_diagnostic_from_exception__mutmut_58': x_create_diagnostic_from_exception__mutmut_58, 
    'x_create_diagnostic_from_exception__mutmut_59': x_create_diagnostic_from_exception__mutmut_59, 
    'x_create_diagnostic_from_exception__mutmut_60': x_create_diagnostic_from_exception__mutmut_60, 
    'x_create_diagnostic_from_exception__mutmut_61': x_create_diagnostic_from_exception__mutmut_61, 
    'x_create_diagnostic_from_exception__mutmut_62': x_create_diagnostic_from_exception__mutmut_62, 
    'x_create_diagnostic_from_exception__mutmut_63': x_create_diagnostic_from_exception__mutmut_63, 
    'x_create_diagnostic_from_exception__mutmut_64': x_create_diagnostic_from_exception__mutmut_64, 
    'x_create_diagnostic_from_exception__mutmut_65': x_create_diagnostic_from_exception__mutmut_65, 
    'x_create_diagnostic_from_exception__mutmut_66': x_create_diagnostic_from_exception__mutmut_66, 
    'x_create_diagnostic_from_exception__mutmut_67': x_create_diagnostic_from_exception__mutmut_67, 
    'x_create_diagnostic_from_exception__mutmut_68': x_create_diagnostic_from_exception__mutmut_68, 
    'x_create_diagnostic_from_exception__mutmut_69': x_create_diagnostic_from_exception__mutmut_69, 
    'x_create_diagnostic_from_exception__mutmut_70': x_create_diagnostic_from_exception__mutmut_70, 
    'x_create_diagnostic_from_exception__mutmut_71': x_create_diagnostic_from_exception__mutmut_71, 
    'x_create_diagnostic_from_exception__mutmut_72': x_create_diagnostic_from_exception__mutmut_72, 
    'x_create_diagnostic_from_exception__mutmut_73': x_create_diagnostic_from_exception__mutmut_73, 
    'x_create_diagnostic_from_exception__mutmut_74': x_create_diagnostic_from_exception__mutmut_74, 
    'x_create_diagnostic_from_exception__mutmut_75': x_create_diagnostic_from_exception__mutmut_75, 
    'x_create_diagnostic_from_exception__mutmut_76': x_create_diagnostic_from_exception__mutmut_76, 
    'x_create_diagnostic_from_exception__mutmut_77': x_create_diagnostic_from_exception__mutmut_77, 
    'x_create_diagnostic_from_exception__mutmut_78': x_create_diagnostic_from_exception__mutmut_78, 
    'x_create_diagnostic_from_exception__mutmut_79': x_create_diagnostic_from_exception__mutmut_79, 
    'x_create_diagnostic_from_exception__mutmut_80': x_create_diagnostic_from_exception__mutmut_80, 
    'x_create_diagnostic_from_exception__mutmut_81': x_create_diagnostic_from_exception__mutmut_81, 
    'x_create_diagnostic_from_exception__mutmut_82': x_create_diagnostic_from_exception__mutmut_82, 
    'x_create_diagnostic_from_exception__mutmut_83': x_create_diagnostic_from_exception__mutmut_83, 
    'x_create_diagnostic_from_exception__mutmut_84': x_create_diagnostic_from_exception__mutmut_84, 
    'x_create_diagnostic_from_exception__mutmut_85': x_create_diagnostic_from_exception__mutmut_85, 
    'x_create_diagnostic_from_exception__mutmut_86': x_create_diagnostic_from_exception__mutmut_86, 
    'x_create_diagnostic_from_exception__mutmut_87': x_create_diagnostic_from_exception__mutmut_87, 
    'x_create_diagnostic_from_exception__mutmut_88': x_create_diagnostic_from_exception__mutmut_88, 
    'x_create_diagnostic_from_exception__mutmut_89': x_create_diagnostic_from_exception__mutmut_89, 
    'x_create_diagnostic_from_exception__mutmut_90': x_create_diagnostic_from_exception__mutmut_90, 
    'x_create_diagnostic_from_exception__mutmut_91': x_create_diagnostic_from_exception__mutmut_91, 
    'x_create_diagnostic_from_exception__mutmut_92': x_create_diagnostic_from_exception__mutmut_92, 
    'x_create_diagnostic_from_exception__mutmut_93': x_create_diagnostic_from_exception__mutmut_93, 
    'x_create_diagnostic_from_exception__mutmut_94': x_create_diagnostic_from_exception__mutmut_94, 
    'x_create_diagnostic_from_exception__mutmut_95': x_create_diagnostic_from_exception__mutmut_95, 
    'x_create_diagnostic_from_exception__mutmut_96': x_create_diagnostic_from_exception__mutmut_96, 
    'x_create_diagnostic_from_exception__mutmut_97': x_create_diagnostic_from_exception__mutmut_97, 
    'x_create_diagnostic_from_exception__mutmut_98': x_create_diagnostic_from_exception__mutmut_98, 
    'x_create_diagnostic_from_exception__mutmut_99': x_create_diagnostic_from_exception__mutmut_99, 
    'x_create_diagnostic_from_exception__mutmut_100': x_create_diagnostic_from_exception__mutmut_100, 
    'x_create_diagnostic_from_exception__mutmut_101': x_create_diagnostic_from_exception__mutmut_101, 
    'x_create_diagnostic_from_exception__mutmut_102': x_create_diagnostic_from_exception__mutmut_102, 
    'x_create_diagnostic_from_exception__mutmut_103': x_create_diagnostic_from_exception__mutmut_103, 
    'x_create_diagnostic_from_exception__mutmut_104': x_create_diagnostic_from_exception__mutmut_104, 
    'x_create_diagnostic_from_exception__mutmut_105': x_create_diagnostic_from_exception__mutmut_105, 
    'x_create_diagnostic_from_exception__mutmut_106': x_create_diagnostic_from_exception__mutmut_106, 
    'x_create_diagnostic_from_exception__mutmut_107': x_create_diagnostic_from_exception__mutmut_107, 
    'x_create_diagnostic_from_exception__mutmut_108': x_create_diagnostic_from_exception__mutmut_108, 
    'x_create_diagnostic_from_exception__mutmut_109': x_create_diagnostic_from_exception__mutmut_109, 
    'x_create_diagnostic_from_exception__mutmut_110': x_create_diagnostic_from_exception__mutmut_110, 
    'x_create_diagnostic_from_exception__mutmut_111': x_create_diagnostic_from_exception__mutmut_111, 
    'x_create_diagnostic_from_exception__mutmut_112': x_create_diagnostic_from_exception__mutmut_112, 
    'x_create_diagnostic_from_exception__mutmut_113': x_create_diagnostic_from_exception__mutmut_113, 
    'x_create_diagnostic_from_exception__mutmut_114': x_create_diagnostic_from_exception__mutmut_114, 
    'x_create_diagnostic_from_exception__mutmut_115': x_create_diagnostic_from_exception__mutmut_115, 
    'x_create_diagnostic_from_exception__mutmut_116': x_create_diagnostic_from_exception__mutmut_116, 
    'x_create_diagnostic_from_exception__mutmut_117': x_create_diagnostic_from_exception__mutmut_117, 
    'x_create_diagnostic_from_exception__mutmut_118': x_create_diagnostic_from_exception__mutmut_118, 
    'x_create_diagnostic_from_exception__mutmut_119': x_create_diagnostic_from_exception__mutmut_119, 
    'x_create_diagnostic_from_exception__mutmut_120': x_create_diagnostic_from_exception__mutmut_120, 
    'x_create_diagnostic_from_exception__mutmut_121': x_create_diagnostic_from_exception__mutmut_121, 
    'x_create_diagnostic_from_exception__mutmut_122': x_create_diagnostic_from_exception__mutmut_122, 
    'x_create_diagnostic_from_exception__mutmut_123': x_create_diagnostic_from_exception__mutmut_123, 
    'x_create_diagnostic_from_exception__mutmut_124': x_create_diagnostic_from_exception__mutmut_124, 
    'x_create_diagnostic_from_exception__mutmut_125': x_create_diagnostic_from_exception__mutmut_125, 
    'x_create_diagnostic_from_exception__mutmut_126': x_create_diagnostic_from_exception__mutmut_126, 
    'x_create_diagnostic_from_exception__mutmut_127': x_create_diagnostic_from_exception__mutmut_127, 
    'x_create_diagnostic_from_exception__mutmut_128': x_create_diagnostic_from_exception__mutmut_128, 
    'x_create_diagnostic_from_exception__mutmut_129': x_create_diagnostic_from_exception__mutmut_129, 
    'x_create_diagnostic_from_exception__mutmut_130': x_create_diagnostic_from_exception__mutmut_130
}

def create_diagnostic_from_exception(*args, **kwargs):
    result = _mutmut_trampoline(x_create_diagnostic_from_exception__mutmut_orig, x_create_diagnostic_from_exception__mutmut_mutants, args, kwargs)
    return result 

create_diagnostic_from_exception.__signature__ = _mutmut_signature(x_create_diagnostic_from_exception__mutmut_orig)
x_create_diagnostic_from_exception__mutmut_orig.__name__ = 'x_create_diagnostic_from_exception'


def x_cty_to_attrs_instance__mutmut_orig(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_1(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is not None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_2(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_3(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(None):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_4(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError(None)

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_5(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("XXInternal validation error: Passed object must be a class.XX")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_6(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("internal validation error: passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_7(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("INTERNAL VALIDATION ERROR: PASSED OBJECT MUST BE A CLASS.")

    return BaseResource.from_cty(cty_val, attrs_cls)


def x_cty_to_attrs_instance__mutmut_8(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(None, attrs_cls)


def x_cty_to_attrs_instance__mutmut_9(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, None)


def x_cty_to_attrs_instance__mutmut_10(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(attrs_cls)


def x_cty_to_attrs_instance__mutmut_11(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, )

x_cty_to_attrs_instance__mutmut_mutants : ClassVar[MutantDict] = {
'x_cty_to_attrs_instance__mutmut_1': x_cty_to_attrs_instance__mutmut_1, 
    'x_cty_to_attrs_instance__mutmut_2': x_cty_to_attrs_instance__mutmut_2, 
    'x_cty_to_attrs_instance__mutmut_3': x_cty_to_attrs_instance__mutmut_3, 
    'x_cty_to_attrs_instance__mutmut_4': x_cty_to_attrs_instance__mutmut_4, 
    'x_cty_to_attrs_instance__mutmut_5': x_cty_to_attrs_instance__mutmut_5, 
    'x_cty_to_attrs_instance__mutmut_6': x_cty_to_attrs_instance__mutmut_6, 
    'x_cty_to_attrs_instance__mutmut_7': x_cty_to_attrs_instance__mutmut_7, 
    'x_cty_to_attrs_instance__mutmut_8': x_cty_to_attrs_instance__mutmut_8, 
    'x_cty_to_attrs_instance__mutmut_9': x_cty_to_attrs_instance__mutmut_9, 
    'x_cty_to_attrs_instance__mutmut_10': x_cty_to_attrs_instance__mutmut_10, 
    'x_cty_to_attrs_instance__mutmut_11': x_cty_to_attrs_instance__mutmut_11
}

def cty_to_attrs_instance(*args, **kwargs):
    result = _mutmut_trampoline(x_cty_to_attrs_instance__mutmut_orig, x_cty_to_attrs_instance__mutmut_mutants, args, kwargs)
    return result 

cty_to_attrs_instance.__signature__ = _mutmut_signature(x_cty_to_attrs_instance__mutmut_orig)
x_cty_to_attrs_instance__mutmut_orig.__name__ = 'x_cty_to_attrs_instance'
