from typing import Any

import attrs

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtySet,
    CtyString,
    CtyTuple,
    CtyType,
    CtyValue,
)
from pyvider.schema.types import NestingMode, PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema
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


def x__get_cty_type__mutmut_orig(type_def: Any) -> CtyType:
    """Gets the CtyType from a PvsAttribute or a raw CtyType."""
    if isinstance(type_def, PvsAttribute):
        return type_def.type
    if isinstance(type_def, CtyType):
        return type_def
    raise TypeError(f"Invalid type definition for attribute element: got {type(type_def).__name__}")


def x__get_cty_type__mutmut_1(type_def: Any) -> CtyType:
    """Gets the CtyType from a PvsAttribute or a raw CtyType."""
    if isinstance(type_def, PvsAttribute):
        return type_def.type
    if isinstance(type_def, CtyType):
        return type_def
    raise TypeError(None)


def x__get_cty_type__mutmut_2(type_def: Any) -> CtyType:
    """Gets the CtyType from a PvsAttribute or a raw CtyType."""
    if isinstance(type_def, PvsAttribute):
        return type_def.type
    if isinstance(type_def, CtyType):
        return type_def
    raise TypeError(f"Invalid type definition for attribute element: got {type(None).__name__}")

x__get_cty_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_cty_type__mutmut_1': x__get_cty_type__mutmut_1, 
    'x__get_cty_type__mutmut_2': x__get_cty_type__mutmut_2
}

def _get_cty_type(*args, **kwargs):
    result = _mutmut_trampoline(x__get_cty_type__mutmut_orig, x__get_cty_type__mutmut_mutants, args, kwargs)
    return result 

_get_cty_type.__signature__ = _mutmut_signature(x__get_cty_type__mutmut_orig)
x__get_cty_type__mutmut_orig.__name__ = 'x__get_cty_type'


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_orig(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=description, **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_1(description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=description, **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_2(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=None, description=description, **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_3(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=None, **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_4(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(description=description, **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_5(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), **kwargs)


# --- Attribute Factories (a_*) ---
def x_a_str__mutmut_6(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=description, )

x_a_str__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_str__mutmut_1': x_a_str__mutmut_1, 
    'x_a_str__mutmut_2': x_a_str__mutmut_2, 
    'x_a_str__mutmut_3': x_a_str__mutmut_3, 
    'x_a_str__mutmut_4': x_a_str__mutmut_4, 
    'x_a_str__mutmut_5': x_a_str__mutmut_5, 
    'x_a_str__mutmut_6': x_a_str__mutmut_6
}

def a_str(*args, **kwargs):
    result = _mutmut_trampoline(x_a_str__mutmut_orig, x_a_str__mutmut_mutants, args, kwargs)
    return result 

a_str.__signature__ = _mutmut_signature(x_a_str__mutmut_orig)
x_a_str__mutmut_orig.__name__ = 'x_a_str'


def x_a_num__mutmut_orig(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=description, **kwargs)


def x_a_num__mutmut_1(description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=description, **kwargs)


def x_a_num__mutmut_2(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=None, description=description, **kwargs)


def x_a_num__mutmut_3(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=None, **kwargs)


def x_a_num__mutmut_4(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(description=description, **kwargs)


def x_a_num__mutmut_5(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), **kwargs)


def x_a_num__mutmut_6(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=description, )

x_a_num__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_num__mutmut_1': x_a_num__mutmut_1, 
    'x_a_num__mutmut_2': x_a_num__mutmut_2, 
    'x_a_num__mutmut_3': x_a_num__mutmut_3, 
    'x_a_num__mutmut_4': x_a_num__mutmut_4, 
    'x_a_num__mutmut_5': x_a_num__mutmut_5, 
    'x_a_num__mutmut_6': x_a_num__mutmut_6
}

def a_num(*args, **kwargs):
    result = _mutmut_trampoline(x_a_num__mutmut_orig, x_a_num__mutmut_mutants, args, kwargs)
    return result 

a_num.__signature__ = _mutmut_signature(x_a_num__mutmut_orig)
x_a_num__mutmut_orig.__name__ = 'x_a_num'


def x_a_bool__mutmut_orig(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=description, **kwargs)


def x_a_bool__mutmut_1(description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=description, **kwargs)


def x_a_bool__mutmut_2(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=None, description=description, **kwargs)


def x_a_bool__mutmut_3(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=None, **kwargs)


def x_a_bool__mutmut_4(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(description=description, **kwargs)


def x_a_bool__mutmut_5(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), **kwargs)


def x_a_bool__mutmut_6(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=description, )

x_a_bool__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_bool__mutmut_1': x_a_bool__mutmut_1, 
    'x_a_bool__mutmut_2': x_a_bool__mutmut_2, 
    'x_a_bool__mutmut_3': x_a_bool__mutmut_3, 
    'x_a_bool__mutmut_4': x_a_bool__mutmut_4, 
    'x_a_bool__mutmut_5': x_a_bool__mutmut_5, 
    'x_a_bool__mutmut_6': x_a_bool__mutmut_6
}

def a_bool(*args, **kwargs):
    result = _mutmut_trampoline(x_a_bool__mutmut_orig, x_a_bool__mutmut_mutants, args, kwargs)
    return result 

a_bool.__signature__ = _mutmut_signature(x_a_bool__mutmut_orig)
x_a_bool__mutmut_orig.__name__ = 'x_a_bool'


def x_a_dyn__mutmut_orig(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=description, **kwargs)


def x_a_dyn__mutmut_1(description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=description, **kwargs)


def x_a_dyn__mutmut_2(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=None, description=description, **kwargs)


def x_a_dyn__mutmut_3(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=None, **kwargs)


def x_a_dyn__mutmut_4(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(description=description, **kwargs)


def x_a_dyn__mutmut_5(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), **kwargs)


def x_a_dyn__mutmut_6(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=description, )

x_a_dyn__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_dyn__mutmut_1': x_a_dyn__mutmut_1, 
    'x_a_dyn__mutmut_2': x_a_dyn__mutmut_2, 
    'x_a_dyn__mutmut_3': x_a_dyn__mutmut_3, 
    'x_a_dyn__mutmut_4': x_a_dyn__mutmut_4, 
    'x_a_dyn__mutmut_5': x_a_dyn__mutmut_5, 
    'x_a_dyn__mutmut_6': x_a_dyn__mutmut_6
}

def a_dyn(*args, **kwargs):
    result = _mutmut_trampoline(x_a_dyn__mutmut_orig, x_a_dyn__mutmut_mutants, args, kwargs)
    return result 

a_dyn.__signature__ = _mutmut_signature(x_a_dyn__mutmut_orig)
x_a_dyn__mutmut_orig.__name__ = 'x_a_dyn'


def x_a_list__mutmut_orig(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_list__mutmut_1(element_type_def: Any, description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_list__mutmut_2(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=None,
        description=description,
        **kwargs,
    )


def x_a_list__mutmut_3(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=None,
        **kwargs,
    )


def x_a_list__mutmut_4(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        description=description,
        **kwargs,
    )


def x_a_list__mutmut_5(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        **kwargs,
    )


def x_a_list__mutmut_6(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=description,
        )


def x_a_list__mutmut_7(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=None),
        description=description,
        **kwargs,
    )


def x_a_list__mutmut_8(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(None)),
        description=description,
        **kwargs,
    )

x_a_list__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_list__mutmut_1': x_a_list__mutmut_1, 
    'x_a_list__mutmut_2': x_a_list__mutmut_2, 
    'x_a_list__mutmut_3': x_a_list__mutmut_3, 
    'x_a_list__mutmut_4': x_a_list__mutmut_4, 
    'x_a_list__mutmut_5': x_a_list__mutmut_5, 
    'x_a_list__mutmut_6': x_a_list__mutmut_6, 
    'x_a_list__mutmut_7': x_a_list__mutmut_7, 
    'x_a_list__mutmut_8': x_a_list__mutmut_8
}

def a_list(*args, **kwargs):
    result = _mutmut_trampoline(x_a_list__mutmut_orig, x_a_list__mutmut_mutants, args, kwargs)
    return result 

a_list.__signature__ = _mutmut_signature(x_a_list__mutmut_orig)
x_a_list__mutmut_orig.__name__ = 'x_a_list'


def x_a_map__mutmut_orig(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_map__mutmut_1(element_type_def: Any, description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_map__mutmut_2(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=None,
        description=description,
        **kwargs,
    )


def x_a_map__mutmut_3(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=None,
        **kwargs,
    )


def x_a_map__mutmut_4(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        description=description,
        **kwargs,
    )


def x_a_map__mutmut_5(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        **kwargs,
    )


def x_a_map__mutmut_6(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=description,
        )


def x_a_map__mutmut_7(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=None),
        description=description,
        **kwargs,
    )


def x_a_map__mutmut_8(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(None)),
        description=description,
        **kwargs,
    )

x_a_map__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_map__mutmut_1': x_a_map__mutmut_1, 
    'x_a_map__mutmut_2': x_a_map__mutmut_2, 
    'x_a_map__mutmut_3': x_a_map__mutmut_3, 
    'x_a_map__mutmut_4': x_a_map__mutmut_4, 
    'x_a_map__mutmut_5': x_a_map__mutmut_5, 
    'x_a_map__mutmut_6': x_a_map__mutmut_6, 
    'x_a_map__mutmut_7': x_a_map__mutmut_7, 
    'x_a_map__mutmut_8': x_a_map__mutmut_8
}

def a_map(*args, **kwargs):
    result = _mutmut_trampoline(x_a_map__mutmut_orig, x_a_map__mutmut_mutants, args, kwargs)
    return result 

a_map.__signature__ = _mutmut_signature(x_a_map__mutmut_orig)
x_a_map__mutmut_orig.__name__ = 'x_a_map'


def x_a_set__mutmut_orig(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_set__mutmut_1(element_type_def: Any, description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def x_a_set__mutmut_2(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=None,
        description=description,
        **kwargs,
    )


def x_a_set__mutmut_3(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=None,
        **kwargs,
    )


def x_a_set__mutmut_4(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        description=description,
        **kwargs,
    )


def x_a_set__mutmut_5(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        **kwargs,
    )


def x_a_set__mutmut_6(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=description,
        )


def x_a_set__mutmut_7(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=None),
        description=description,
        **kwargs,
    )


def x_a_set__mutmut_8(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(None)),
        description=description,
        **kwargs,
    )

x_a_set__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_set__mutmut_1': x_a_set__mutmut_1, 
    'x_a_set__mutmut_2': x_a_set__mutmut_2, 
    'x_a_set__mutmut_3': x_a_set__mutmut_3, 
    'x_a_set__mutmut_4': x_a_set__mutmut_4, 
    'x_a_set__mutmut_5': x_a_set__mutmut_5, 
    'x_a_set__mutmut_6': x_a_set__mutmut_6, 
    'x_a_set__mutmut_7': x_a_set__mutmut_7, 
    'x_a_set__mutmut_8': x_a_set__mutmut_8
}

def a_set(*args, **kwargs):
    result = _mutmut_trampoline(x_a_set__mutmut_orig, x_a_set__mutmut_mutants, args, kwargs)
    return result 

a_set.__signature__ = _mutmut_signature(x_a_set__mutmut_orig)
x_a_set__mutmut_orig.__name__ = 'x_a_set'


def x_a_tuple__mutmut_orig(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_1(element_type_defs: list[Any], description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_2(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=None,
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_3(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=None,
        **kwargs,
    )


def x_a_tuple__mutmut_4(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_5(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        **kwargs,
    )


def x_a_tuple__mutmut_6(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=description,
        )


def x_a_tuple__mutmut_7(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=None),
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_8(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(None)),
        description=description,
        **kwargs,
    )


def x_a_tuple__mutmut_9(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(None) for v in element_type_defs)),
        description=description,
        **kwargs,
    )

x_a_tuple__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_tuple__mutmut_1': x_a_tuple__mutmut_1, 
    'x_a_tuple__mutmut_2': x_a_tuple__mutmut_2, 
    'x_a_tuple__mutmut_3': x_a_tuple__mutmut_3, 
    'x_a_tuple__mutmut_4': x_a_tuple__mutmut_4, 
    'x_a_tuple__mutmut_5': x_a_tuple__mutmut_5, 
    'x_a_tuple__mutmut_6': x_a_tuple__mutmut_6, 
    'x_a_tuple__mutmut_7': x_a_tuple__mutmut_7, 
    'x_a_tuple__mutmut_8': x_a_tuple__mutmut_8, 
    'x_a_tuple__mutmut_9': x_a_tuple__mutmut_9
}

def a_tuple(*args, **kwargs):
    result = _mutmut_trampoline(x_a_tuple__mutmut_orig, x_a_tuple__mutmut_mutants, args, kwargs)
    return result 

a_tuple.__signature__ = _mutmut_signature(x_a_tuple__mutmut_orig)
x_a_tuple__mutmut_orig.__name__ = 'x_a_tuple'


def x_a_obj__mutmut_orig(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_1(attributes: dict[str, PvsAttribute], description: str = "XXXX", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_2(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = None
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_3(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=None, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_4(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=None)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_5(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_6(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, )
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_7(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=None,
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_8(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=None,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_9(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=None,
        **kwargs,
    )


def x_a_obj__mutmut_10(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_11(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        description=description,
        **kwargs,
    )


def x_a_obj__mutmut_12(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        **kwargs,
    )


def x_a_obj__mutmut_13(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        )

x_a_obj__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_obj__mutmut_1': x_a_obj__mutmut_1, 
    'x_a_obj__mutmut_2': x_a_obj__mutmut_2, 
    'x_a_obj__mutmut_3': x_a_obj__mutmut_3, 
    'x_a_obj__mutmut_4': x_a_obj__mutmut_4, 
    'x_a_obj__mutmut_5': x_a_obj__mutmut_5, 
    'x_a_obj__mutmut_6': x_a_obj__mutmut_6, 
    'x_a_obj__mutmut_7': x_a_obj__mutmut_7, 
    'x_a_obj__mutmut_8': x_a_obj__mutmut_8, 
    'x_a_obj__mutmut_9': x_a_obj__mutmut_9, 
    'x_a_obj__mutmut_10': x_a_obj__mutmut_10, 
    'x_a_obj__mutmut_11': x_a_obj__mutmut_11, 
    'x_a_obj__mutmut_12': x_a_obj__mutmut_12, 
    'x_a_obj__mutmut_13': x_a_obj__mutmut_13
}

def a_obj(*args, **kwargs):
    result = _mutmut_trampoline(x_a_obj__mutmut_orig, x_a_obj__mutmut_mutants, args, kwargs)
    return result 

a_obj.__signature__ = _mutmut_signature(x_a_obj__mutmut_orig)
x_a_obj__mutmut_orig.__name__ = 'x_a_obj'


# --- Block Factories (b_*) ---
def x_b_main__mutmut_orig(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_1(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = None
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_2(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = None
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_3(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(None, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_4(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=None)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_5(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_6(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, )
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_7(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=None,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_8(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=None,
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_9(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_10(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        **kwargs,
    )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_11(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        )


# --- Block Factories (b_*) ---
def x_b_main__mutmut_12(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(None) if block_types else (),
        **kwargs,
    )

x_b_main__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_main__mutmut_1': x_b_main__mutmut_1, 
    'x_b_main__mutmut_2': x_b_main__mutmut_2, 
    'x_b_main__mutmut_3': x_b_main__mutmut_3, 
    'x_b_main__mutmut_4': x_b_main__mutmut_4, 
    'x_b_main__mutmut_5': x_b_main__mutmut_5, 
    'x_b_main__mutmut_6': x_b_main__mutmut_6, 
    'x_b_main__mutmut_7': x_b_main__mutmut_7, 
    'x_b_main__mutmut_8': x_b_main__mutmut_8, 
    'x_b_main__mutmut_9': x_b_main__mutmut_9, 
    'x_b_main__mutmut_10': x_b_main__mutmut_10, 
    'x_b_main__mutmut_11': x_b_main__mutmut_11, 
    'x_b_main__mutmut_12': x_b_main__mutmut_12
}

def b_main(*args, **kwargs):
    result = _mutmut_trampoline(x_b_main__mutmut_orig, x_b_main__mutmut_mutants, args, kwargs)
    return result 

b_main.__signature__ = _mutmut_signature(x_b_main__mutmut_orig)
x_b_main__mutmut_orig.__name__ = 'x_b_main'


def x__nested_block_factory__mutmut_orig(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_1(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = None
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_2(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop(None, {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_3(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", None)
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_4(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop({})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_5(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", )
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_6(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("XXattributesXX", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_7(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("ATTRIBUTES", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_8(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = None
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_9(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop(None, None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_10(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop(None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_11(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", )
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_12(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("XXblock_typesXX", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_13(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("BLOCK_TYPES", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_14(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = None
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_15(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=None,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_16(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=None,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_17(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=None,
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_18(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_19(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_20(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_21(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get(None, ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_22(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", None),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_23(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get(""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_24(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_25(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("XXdescriptionXX", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_26(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("DESCRIPTION", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_27(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", "XXXX"),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_28(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=None, nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_29(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=None, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_30(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=None, **kwargs)


def x__nested_block_factory__mutmut_31(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(nesting=nesting, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_32(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, block=block_content, **kwargs)


def x__nested_block_factory__mutmut_33(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, **kwargs)


def x__nested_block_factory__mutmut_34(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, )

x__nested_block_factory__mutmut_mutants : ClassVar[MutantDict] = {
'x__nested_block_factory__mutmut_1': x__nested_block_factory__mutmut_1, 
    'x__nested_block_factory__mutmut_2': x__nested_block_factory__mutmut_2, 
    'x__nested_block_factory__mutmut_3': x__nested_block_factory__mutmut_3, 
    'x__nested_block_factory__mutmut_4': x__nested_block_factory__mutmut_4, 
    'x__nested_block_factory__mutmut_5': x__nested_block_factory__mutmut_5, 
    'x__nested_block_factory__mutmut_6': x__nested_block_factory__mutmut_6, 
    'x__nested_block_factory__mutmut_7': x__nested_block_factory__mutmut_7, 
    'x__nested_block_factory__mutmut_8': x__nested_block_factory__mutmut_8, 
    'x__nested_block_factory__mutmut_9': x__nested_block_factory__mutmut_9, 
    'x__nested_block_factory__mutmut_10': x__nested_block_factory__mutmut_10, 
    'x__nested_block_factory__mutmut_11': x__nested_block_factory__mutmut_11, 
    'x__nested_block_factory__mutmut_12': x__nested_block_factory__mutmut_12, 
    'x__nested_block_factory__mutmut_13': x__nested_block_factory__mutmut_13, 
    'x__nested_block_factory__mutmut_14': x__nested_block_factory__mutmut_14, 
    'x__nested_block_factory__mutmut_15': x__nested_block_factory__mutmut_15, 
    'x__nested_block_factory__mutmut_16': x__nested_block_factory__mutmut_16, 
    'x__nested_block_factory__mutmut_17': x__nested_block_factory__mutmut_17, 
    'x__nested_block_factory__mutmut_18': x__nested_block_factory__mutmut_18, 
    'x__nested_block_factory__mutmut_19': x__nested_block_factory__mutmut_19, 
    'x__nested_block_factory__mutmut_20': x__nested_block_factory__mutmut_20, 
    'x__nested_block_factory__mutmut_21': x__nested_block_factory__mutmut_21, 
    'x__nested_block_factory__mutmut_22': x__nested_block_factory__mutmut_22, 
    'x__nested_block_factory__mutmut_23': x__nested_block_factory__mutmut_23, 
    'x__nested_block_factory__mutmut_24': x__nested_block_factory__mutmut_24, 
    'x__nested_block_factory__mutmut_25': x__nested_block_factory__mutmut_25, 
    'x__nested_block_factory__mutmut_26': x__nested_block_factory__mutmut_26, 
    'x__nested_block_factory__mutmut_27': x__nested_block_factory__mutmut_27, 
    'x__nested_block_factory__mutmut_28': x__nested_block_factory__mutmut_28, 
    'x__nested_block_factory__mutmut_29': x__nested_block_factory__mutmut_29, 
    'x__nested_block_factory__mutmut_30': x__nested_block_factory__mutmut_30, 
    'x__nested_block_factory__mutmut_31': x__nested_block_factory__mutmut_31, 
    'x__nested_block_factory__mutmut_32': x__nested_block_factory__mutmut_32, 
    'x__nested_block_factory__mutmut_33': x__nested_block_factory__mutmut_33, 
    'x__nested_block_factory__mutmut_34': x__nested_block_factory__mutmut_34
}

def _nested_block_factory(*args, **kwargs):
    result = _mutmut_trampoline(x__nested_block_factory__mutmut_orig, x__nested_block_factory__mutmut_mutants, args, kwargs)
    return result 

_nested_block_factory.__signature__ = _mutmut_signature(x__nested_block_factory__mutmut_orig)
x__nested_block_factory__mutmut_orig.__name__ = 'x__nested_block_factory'


def x_b_list__mutmut_orig(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.LIST, **kwargs)


def x_b_list__mutmut_1(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(None, NestingMode.LIST, **kwargs)


def x_b_list__mutmut_2(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, None, **kwargs)


def x_b_list__mutmut_3(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(NestingMode.LIST, **kwargs)


def x_b_list__mutmut_4(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, **kwargs)


def x_b_list__mutmut_5(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.LIST, )

x_b_list__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_list__mutmut_1': x_b_list__mutmut_1, 
    'x_b_list__mutmut_2': x_b_list__mutmut_2, 
    'x_b_list__mutmut_3': x_b_list__mutmut_3, 
    'x_b_list__mutmut_4': x_b_list__mutmut_4, 
    'x_b_list__mutmut_5': x_b_list__mutmut_5
}

def b_list(*args, **kwargs):
    result = _mutmut_trampoline(x_b_list__mutmut_orig, x_b_list__mutmut_mutants, args, kwargs)
    return result 

b_list.__signature__ = _mutmut_signature(x_b_list__mutmut_orig)
x_b_list__mutmut_orig.__name__ = 'x_b_list'


def x_b_set__mutmut_orig(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SET, **kwargs)


def x_b_set__mutmut_1(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(None, NestingMode.SET, **kwargs)


def x_b_set__mutmut_2(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, None, **kwargs)


def x_b_set__mutmut_3(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(NestingMode.SET, **kwargs)


def x_b_set__mutmut_4(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, **kwargs)


def x_b_set__mutmut_5(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SET, )

x_b_set__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_set__mutmut_1': x_b_set__mutmut_1, 
    'x_b_set__mutmut_2': x_b_set__mutmut_2, 
    'x_b_set__mutmut_3': x_b_set__mutmut_3, 
    'x_b_set__mutmut_4': x_b_set__mutmut_4, 
    'x_b_set__mutmut_5': x_b_set__mutmut_5
}

def b_set(*args, **kwargs):
    result = _mutmut_trampoline(x_b_set__mutmut_orig, x_b_set__mutmut_mutants, args, kwargs)
    return result 

b_set.__signature__ = _mutmut_signature(x_b_set__mutmut_orig)
x_b_set__mutmut_orig.__name__ = 'x_b_set'


def x_b_map__mutmut_orig(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.MAP, **kwargs)


def x_b_map__mutmut_1(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(None, NestingMode.MAP, **kwargs)


def x_b_map__mutmut_2(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, None, **kwargs)


def x_b_map__mutmut_3(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(NestingMode.MAP, **kwargs)


def x_b_map__mutmut_4(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, **kwargs)


def x_b_map__mutmut_5(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.MAP, )

x_b_map__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_map__mutmut_1': x_b_map__mutmut_1, 
    'x_b_map__mutmut_2': x_b_map__mutmut_2, 
    'x_b_map__mutmut_3': x_b_map__mutmut_3, 
    'x_b_map__mutmut_4': x_b_map__mutmut_4, 
    'x_b_map__mutmut_5': x_b_map__mutmut_5
}

def b_map(*args, **kwargs):
    result = _mutmut_trampoline(x_b_map__mutmut_orig, x_b_map__mutmut_mutants, args, kwargs)
    return result 

b_map.__signature__ = _mutmut_signature(x_b_map__mutmut_orig)
x_b_map__mutmut_orig.__name__ = 'x_b_map'


def x_b_single__mutmut_orig(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SINGLE, **kwargs)


def x_b_single__mutmut_1(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(None, NestingMode.SINGLE, **kwargs)


def x_b_single__mutmut_2(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, None, **kwargs)


def x_b_single__mutmut_3(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(NestingMode.SINGLE, **kwargs)


def x_b_single__mutmut_4(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, **kwargs)


def x_b_single__mutmut_5(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SINGLE, )

x_b_single__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_single__mutmut_1': x_b_single__mutmut_1, 
    'x_b_single__mutmut_2': x_b_single__mutmut_2, 
    'x_b_single__mutmut_3': x_b_single__mutmut_3, 
    'x_b_single__mutmut_4': x_b_single__mutmut_4, 
    'x_b_single__mutmut_5': x_b_single__mutmut_5
}

def b_single(*args, **kwargs):
    result = _mutmut_trampoline(x_b_single__mutmut_orig, x_b_single__mutmut_mutants, args, kwargs)
    return result 

b_single.__signature__ = _mutmut_signature(x_b_single__mutmut_orig)
x_b_single__mutmut_orig.__name__ = 'x_b_single'


def x_b_group__mutmut_orig(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.GROUP, **kwargs)


def x_b_group__mutmut_1(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(None, NestingMode.GROUP, **kwargs)


def x_b_group__mutmut_2(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, None, **kwargs)


def x_b_group__mutmut_3(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(NestingMode.GROUP, **kwargs)


def x_b_group__mutmut_4(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, **kwargs)


def x_b_group__mutmut_5(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.GROUP, )

x_b_group__mutmut_mutants : ClassVar[MutantDict] = {
'x_b_group__mutmut_1': x_b_group__mutmut_1, 
    'x_b_group__mutmut_2': x_b_group__mutmut_2, 
    'x_b_group__mutmut_3': x_b_group__mutmut_3, 
    'x_b_group__mutmut_4': x_b_group__mutmut_4, 
    'x_b_group__mutmut_5': x_b_group__mutmut_5
}

def b_group(*args, **kwargs):
    result = _mutmut_trampoline(x_b_group__mutmut_orig, x_b_group__mutmut_mutants, args, kwargs)
    return result 

b_group.__signature__ = _mutmut_signature(x_b_group__mutmut_orig)
x_b_group__mutmut_orig.__name__ = 'x_b_group'


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_orig(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_1(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = None
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_2(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=None, block_types=block_types)
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_3(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=None)
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_4(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(block_types=block_types)
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_5(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, )
    return PvsSchema(version=version, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_6(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=None, block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_7(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=version, block=None)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_8(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(block=block)


# --- Schema Factories (s_*) ---
def x__create_schema__mutmut_9(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=version, )

x__create_schema__mutmut_mutants : ClassVar[MutantDict] = {
'x__create_schema__mutmut_1': x__create_schema__mutmut_1, 
    'x__create_schema__mutmut_2': x__create_schema__mutmut_2, 
    'x__create_schema__mutmut_3': x__create_schema__mutmut_3, 
    'x__create_schema__mutmut_4': x__create_schema__mutmut_4, 
    'x__create_schema__mutmut_5': x__create_schema__mutmut_5, 
    'x__create_schema__mutmut_6': x__create_schema__mutmut_6, 
    'x__create_schema__mutmut_7': x__create_schema__mutmut_7, 
    'x__create_schema__mutmut_8': x__create_schema__mutmut_8, 
    'x__create_schema__mutmut_9': x__create_schema__mutmut_9
}

def _create_schema(*args, **kwargs):
    result = _mutmut_trampoline(x__create_schema__mutmut_orig, x__create_schema__mutmut_mutants, args, kwargs)
    return result 

_create_schema.__signature__ = _mutmut_signature(x__create_schema__mutmut_orig)
x__create_schema__mutmut_orig.__name__ = 'x__create_schema'


def x_s_resource__mutmut_orig(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


def x_s_resource__mutmut_1(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(None, attributes=attributes, block_types=block_types)


def x_s_resource__mutmut_2(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=None, block_types=block_types)


def x_s_resource__mutmut_3(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=None)


def x_s_resource__mutmut_4(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(attributes=attributes, block_types=block_types)


def x_s_resource__mutmut_5(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, block_types=block_types)


def x_s_resource__mutmut_6(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, )


def x_s_resource__mutmut_7(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(2, attributes=attributes, block_types=block_types)

x_s_resource__mutmut_mutants : ClassVar[MutantDict] = {
'x_s_resource__mutmut_1': x_s_resource__mutmut_1, 
    'x_s_resource__mutmut_2': x_s_resource__mutmut_2, 
    'x_s_resource__mutmut_3': x_s_resource__mutmut_3, 
    'x_s_resource__mutmut_4': x_s_resource__mutmut_4, 
    'x_s_resource__mutmut_5': x_s_resource__mutmut_5, 
    'x_s_resource__mutmut_6': x_s_resource__mutmut_6, 
    'x_s_resource__mutmut_7': x_s_resource__mutmut_7
}

def s_resource(*args, **kwargs):
    result = _mutmut_trampoline(x_s_resource__mutmut_orig, x_s_resource__mutmut_mutants, args, kwargs)
    return result 

s_resource.__signature__ = _mutmut_signature(x_s_resource__mutmut_orig)
x_s_resource__mutmut_orig.__name__ = 'x_s_resource'


def x_s_data_source__mutmut_orig(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


def x_s_data_source__mutmut_1(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(None, attributes=attributes, block_types=block_types)


def x_s_data_source__mutmut_2(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=None, block_types=block_types)


def x_s_data_source__mutmut_3(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=None)


def x_s_data_source__mutmut_4(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(attributes=attributes, block_types=block_types)


def x_s_data_source__mutmut_5(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, block_types=block_types)


def x_s_data_source__mutmut_6(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, )


def x_s_data_source__mutmut_7(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(2, attributes=attributes, block_types=block_types)

x_s_data_source__mutmut_mutants : ClassVar[MutantDict] = {
'x_s_data_source__mutmut_1': x_s_data_source__mutmut_1, 
    'x_s_data_source__mutmut_2': x_s_data_source__mutmut_2, 
    'x_s_data_source__mutmut_3': x_s_data_source__mutmut_3, 
    'x_s_data_source__mutmut_4': x_s_data_source__mutmut_4, 
    'x_s_data_source__mutmut_5': x_s_data_source__mutmut_5, 
    'x_s_data_source__mutmut_6': x_s_data_source__mutmut_6, 
    'x_s_data_source__mutmut_7': x_s_data_source__mutmut_7
}

def s_data_source(*args, **kwargs):
    result = _mutmut_trampoline(x_s_data_source__mutmut_orig, x_s_data_source__mutmut_mutants, args, kwargs)
    return result 

s_data_source.__signature__ = _mutmut_signature(x_s_data_source__mutmut_orig)
x_s_data_source__mutmut_orig.__name__ = 'x_s_data_source'


def x_s_provider__mutmut_orig(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


def x_s_provider__mutmut_1(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(None, attributes=attributes, block_types=block_types)


def x_s_provider__mutmut_2(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=None, block_types=block_types)


def x_s_provider__mutmut_3(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=None)


def x_s_provider__mutmut_4(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(attributes=attributes, block_types=block_types)


def x_s_provider__mutmut_5(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, block_types=block_types)


def x_s_provider__mutmut_6(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, )


def x_s_provider__mutmut_7(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(2, attributes=attributes, block_types=block_types)

x_s_provider__mutmut_mutants : ClassVar[MutantDict] = {
'x_s_provider__mutmut_1': x_s_provider__mutmut_1, 
    'x_s_provider__mutmut_2': x_s_provider__mutmut_2, 
    'x_s_provider__mutmut_3': x_s_provider__mutmut_3, 
    'x_s_provider__mutmut_4': x_s_provider__mutmut_4, 
    'x_s_provider__mutmut_5': x_s_provider__mutmut_5, 
    'x_s_provider__mutmut_6': x_s_provider__mutmut_6, 
    'x_s_provider__mutmut_7': x_s_provider__mutmut_7
}

def s_provider(*args, **kwargs):
    result = _mutmut_trampoline(x_s_provider__mutmut_orig, x_s_provider__mutmut_mutants, args, kwargs)
    return result 

s_provider.__signature__ = _mutmut_signature(x_s_provider__mutmut_orig)
x_s_provider__mutmut_orig.__name__ = 'x_s_provider'


# --- Special Value Factories ---


def x_a_unknown__mutmut_orig(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_1(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = ""
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_2(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = None
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_3(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = None

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_4(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is not None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_5(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError(None)
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_6(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("XXa_unknown() expects a schema builder instance like a_str() or s_resource()XX")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_7(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("A_UNKNOWN() EXPECTS A SCHEMA BUILDER INSTANCE LIKE A_STR() OR S_RESOURCE()")
    return CtyValue.unknown(target_type)


# --- Special Value Factories ---


def x_a_unknown__mutmut_8(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(None)

x_a_unknown__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_unknown__mutmut_1': x_a_unknown__mutmut_1, 
    'x_a_unknown__mutmut_2': x_a_unknown__mutmut_2, 
    'x_a_unknown__mutmut_3': x_a_unknown__mutmut_3, 
    'x_a_unknown__mutmut_4': x_a_unknown__mutmut_4, 
    'x_a_unknown__mutmut_5': x_a_unknown__mutmut_5, 
    'x_a_unknown__mutmut_6': x_a_unknown__mutmut_6, 
    'x_a_unknown__mutmut_7': x_a_unknown__mutmut_7, 
    'x_a_unknown__mutmut_8': x_a_unknown__mutmut_8
}

def a_unknown(*args, **kwargs):
    result = _mutmut_trampoline(x_a_unknown__mutmut_orig, x_a_unknown__mutmut_mutants, args, kwargs)
    return result 

a_unknown.__signature__ = _mutmut_signature(x_a_unknown__mutmut_orig)
x_a_unknown__mutmut_orig.__name__ = 'x_a_unknown'


def x_a_null__mutmut_orig(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_1(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = ""
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_2(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = None
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_3(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = None

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_4(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is not None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_5(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError(None)
    return CtyValue.null(target_type)


def x_a_null__mutmut_6(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("XXa_null() expects a schema builder instance like a_str() or s_resource()XX")
    return CtyValue.null(target_type)


def x_a_null__mutmut_7(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("A_NULL() EXPECTS A SCHEMA BUILDER INSTANCE LIKE A_STR() OR S_RESOURCE()")
    return CtyValue.null(target_type)


def x_a_null__mutmut_8(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(None)

x_a_null__mutmut_mutants : ClassVar[MutantDict] = {
'x_a_null__mutmut_1': x_a_null__mutmut_1, 
    'x_a_null__mutmut_2': x_a_null__mutmut_2, 
    'x_a_null__mutmut_3': x_a_null__mutmut_3, 
    'x_a_null__mutmut_4': x_a_null__mutmut_4, 
    'x_a_null__mutmut_5': x_a_null__mutmut_5, 
    'x_a_null__mutmut_6': x_a_null__mutmut_6, 
    'x_a_null__mutmut_7': x_a_null__mutmut_7, 
    'x_a_null__mutmut_8': x_a_null__mutmut_8
}

def a_null(*args, **kwargs):
    result = _mutmut_trampoline(x_a_null__mutmut_orig, x_a_null__mutmut_mutants, args, kwargs)
    return result 

a_null.__signature__ = _mutmut_signature(x_a_null__mutmut_orig)
x_a_null__mutmut_orig.__name__ = 'x_a_null'
