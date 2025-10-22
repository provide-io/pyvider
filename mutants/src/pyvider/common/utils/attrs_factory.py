from typing import Any

import attrs

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtySet,
    CtyString,
    CtyTuple,
)
from pyvider.schema.types import PvsAttribute
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


def x__pvs_type_to_python_type__mutmut_orig(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_1(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = None
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_2(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str & None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_3(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float & None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_4(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int & float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_5(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool & None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_6(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list & None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_7(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict & None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_8(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set & None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_9(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple & None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_10(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any & None
    return Any | None


def x__pvs_type_to_python_type__mutmut_11(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict & Any | None
    return Any | None


def x__pvs_type_to_python_type__mutmut_12(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any & None

x__pvs_type_to_python_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__pvs_type_to_python_type__mutmut_1': x__pvs_type_to_python_type__mutmut_1, 
    'x__pvs_type_to_python_type__mutmut_2': x__pvs_type_to_python_type__mutmut_2, 
    'x__pvs_type_to_python_type__mutmut_3': x__pvs_type_to_python_type__mutmut_3, 
    'x__pvs_type_to_python_type__mutmut_4': x__pvs_type_to_python_type__mutmut_4, 
    'x__pvs_type_to_python_type__mutmut_5': x__pvs_type_to_python_type__mutmut_5, 
    'x__pvs_type_to_python_type__mutmut_6': x__pvs_type_to_python_type__mutmut_6, 
    'x__pvs_type_to_python_type__mutmut_7': x__pvs_type_to_python_type__mutmut_7, 
    'x__pvs_type_to_python_type__mutmut_8': x__pvs_type_to_python_type__mutmut_8, 
    'x__pvs_type_to_python_type__mutmut_9': x__pvs_type_to_python_type__mutmut_9, 
    'x__pvs_type_to_python_type__mutmut_10': x__pvs_type_to_python_type__mutmut_10, 
    'x__pvs_type_to_python_type__mutmut_11': x__pvs_type_to_python_type__mutmut_11, 
    'x__pvs_type_to_python_type__mutmut_12': x__pvs_type_to_python_type__mutmut_12
}

def _pvs_type_to_python_type(*args, **kwargs):
    result = _mutmut_trampoline(x__pvs_type_to_python_type__mutmut_orig, x__pvs_type_to_python_type__mutmut_mutants, args, kwargs)
    return result 

_pvs_type_to_python_type.__signature__ = _mutmut_signature(x__pvs_type_to_python_type__mutmut_orig)
x__pvs_type_to_python_type__mutmut_orig.__name__ = 'x__pvs_type_to_python_type'


def x_create_attrs_class_from_schema__mutmut_orig(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_1(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = None
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_2(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_3(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_4(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = None
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_5(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=None, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_6(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=None)
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_7(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_8(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, )
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_9(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(None))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_10(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = None
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_11(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = None
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_12(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=None, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_13(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=None)
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_14(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_15(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, )
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_16(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(None))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_17(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = ""
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_18(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = None

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_19(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=None, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_20(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=None)

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_21(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_22(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, )

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_23(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(None))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_24(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = None

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_25(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(None, attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_26(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, None, frozen=True)


def x_create_attrs_class_from_schema__mutmut_27(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=None)


def x_create_attrs_class_from_schema__mutmut_28(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(attrs_fields, frozen=True)


def x_create_attrs_class_from_schema__mutmut_29(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, frozen=True)


def x_create_attrs_class_from_schema__mutmut_30(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, )


def x_create_attrs_class_from_schema__mutmut_31(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=False)

x_create_attrs_class_from_schema__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_attrs_class_from_schema__mutmut_1': x_create_attrs_class_from_schema__mutmut_1, 
    'x_create_attrs_class_from_schema__mutmut_2': x_create_attrs_class_from_schema__mutmut_2, 
    'x_create_attrs_class_from_schema__mutmut_3': x_create_attrs_class_from_schema__mutmut_3, 
    'x_create_attrs_class_from_schema__mutmut_4': x_create_attrs_class_from_schema__mutmut_4, 
    'x_create_attrs_class_from_schema__mutmut_5': x_create_attrs_class_from_schema__mutmut_5, 
    'x_create_attrs_class_from_schema__mutmut_6': x_create_attrs_class_from_schema__mutmut_6, 
    'x_create_attrs_class_from_schema__mutmut_7': x_create_attrs_class_from_schema__mutmut_7, 
    'x_create_attrs_class_from_schema__mutmut_8': x_create_attrs_class_from_schema__mutmut_8, 
    'x_create_attrs_class_from_schema__mutmut_9': x_create_attrs_class_from_schema__mutmut_9, 
    'x_create_attrs_class_from_schema__mutmut_10': x_create_attrs_class_from_schema__mutmut_10, 
    'x_create_attrs_class_from_schema__mutmut_11': x_create_attrs_class_from_schema__mutmut_11, 
    'x_create_attrs_class_from_schema__mutmut_12': x_create_attrs_class_from_schema__mutmut_12, 
    'x_create_attrs_class_from_schema__mutmut_13': x_create_attrs_class_from_schema__mutmut_13, 
    'x_create_attrs_class_from_schema__mutmut_14': x_create_attrs_class_from_schema__mutmut_14, 
    'x_create_attrs_class_from_schema__mutmut_15': x_create_attrs_class_from_schema__mutmut_15, 
    'x_create_attrs_class_from_schema__mutmut_16': x_create_attrs_class_from_schema__mutmut_16, 
    'x_create_attrs_class_from_schema__mutmut_17': x_create_attrs_class_from_schema__mutmut_17, 
    'x_create_attrs_class_from_schema__mutmut_18': x_create_attrs_class_from_schema__mutmut_18, 
    'x_create_attrs_class_from_schema__mutmut_19': x_create_attrs_class_from_schema__mutmut_19, 
    'x_create_attrs_class_from_schema__mutmut_20': x_create_attrs_class_from_schema__mutmut_20, 
    'x_create_attrs_class_from_schema__mutmut_21': x_create_attrs_class_from_schema__mutmut_21, 
    'x_create_attrs_class_from_schema__mutmut_22': x_create_attrs_class_from_schema__mutmut_22, 
    'x_create_attrs_class_from_schema__mutmut_23': x_create_attrs_class_from_schema__mutmut_23, 
    'x_create_attrs_class_from_schema__mutmut_24': x_create_attrs_class_from_schema__mutmut_24, 
    'x_create_attrs_class_from_schema__mutmut_25': x_create_attrs_class_from_schema__mutmut_25, 
    'x_create_attrs_class_from_schema__mutmut_26': x_create_attrs_class_from_schema__mutmut_26, 
    'x_create_attrs_class_from_schema__mutmut_27': x_create_attrs_class_from_schema__mutmut_27, 
    'x_create_attrs_class_from_schema__mutmut_28': x_create_attrs_class_from_schema__mutmut_28, 
    'x_create_attrs_class_from_schema__mutmut_29': x_create_attrs_class_from_schema__mutmut_29, 
    'x_create_attrs_class_from_schema__mutmut_30': x_create_attrs_class_from_schema__mutmut_30, 
    'x_create_attrs_class_from_schema__mutmut_31': x_create_attrs_class_from_schema__mutmut_31
}

def create_attrs_class_from_schema(*args, **kwargs):
    result = _mutmut_trampoline(x_create_attrs_class_from_schema__mutmut_orig, x_create_attrs_class_from_schema__mutmut_mutants, args, kwargs)
    return result 

create_attrs_class_from_schema.__signature__ = _mutmut_signature(x_create_attrs_class_from_schema__mutmut_orig)
x_create_attrs_class_from_schema__mutmut_orig.__name__ = 'x_create_attrs_class_from_schema'
