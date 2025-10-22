from collections.abc import Callable
from decimal import Decimal
import inspect
from types import UnionType
from typing import Any, get_args, get_origin, get_type_hints

from provide.foundation import logger

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyString,
    CtyType,
    CtyValue,
)
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


def x__get_cty_type_for_union__mutmut_orig(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_1(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = None
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_2(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_3(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(None) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_4(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) < {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_5(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) != 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_6(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 2:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_7(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(None)
    return CtyDynamic()


def x__get_cty_type_for_union__mutmut_8(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[1])
    return CtyDynamic()

x__get_cty_type_for_union__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_cty_type_for_union__mutmut_1': x__get_cty_type_for_union__mutmut_1, 
    'x__get_cty_type_for_union__mutmut_2': x__get_cty_type_for_union__mutmut_2, 
    'x__get_cty_type_for_union__mutmut_3': x__get_cty_type_for_union__mutmut_3, 
    'x__get_cty_type_for_union__mutmut_4': x__get_cty_type_for_union__mutmut_4, 
    'x__get_cty_type_for_union__mutmut_5': x__get_cty_type_for_union__mutmut_5, 
    'x__get_cty_type_for_union__mutmut_6': x__get_cty_type_for_union__mutmut_6, 
    'x__get_cty_type_for_union__mutmut_7': x__get_cty_type_for_union__mutmut_7, 
    'x__get_cty_type_for_union__mutmut_8': x__get_cty_type_for_union__mutmut_8
}

def _get_cty_type_for_union(*args, **kwargs):
    result = _mutmut_trampoline(x__get_cty_type_for_union__mutmut_orig, x__get_cty_type_for_union__mutmut_mutants, args, kwargs)
    return result 

_get_cty_type_for_union.__signature__ = _mutmut_signature(x__get_cty_type_for_union__mutmut_orig)
x__get_cty_type_for_union__mutmut_orig.__name__ = 'x__get_cty_type_for_union'


def x__get_cty_type_for_list__mutmut_orig(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = _python_type_to_cty_type(args[0]) if args else CtyDynamic()
    return CtyList(element_type=element_type)


def x__get_cty_type_for_list__mutmut_1(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = None
    return CtyList(element_type=element_type)


def x__get_cty_type_for_list__mutmut_2(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = _python_type_to_cty_type(None) if args else CtyDynamic()
    return CtyList(element_type=element_type)


def x__get_cty_type_for_list__mutmut_3(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = _python_type_to_cty_type(args[1]) if args else CtyDynamic()
    return CtyList(element_type=element_type)


def x__get_cty_type_for_list__mutmut_4(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = _python_type_to_cty_type(args[0]) if args else CtyDynamic()
    return CtyList(element_type=None)

x__get_cty_type_for_list__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_cty_type_for_list__mutmut_1': x__get_cty_type_for_list__mutmut_1, 
    'x__get_cty_type_for_list__mutmut_2': x__get_cty_type_for_list__mutmut_2, 
    'x__get_cty_type_for_list__mutmut_3': x__get_cty_type_for_list__mutmut_3, 
    'x__get_cty_type_for_list__mutmut_4': x__get_cty_type_for_list__mutmut_4
}

def _get_cty_type_for_list(*args, **kwargs):
    result = _mutmut_trampoline(x__get_cty_type_for_list__mutmut_orig, x__get_cty_type_for_list__mutmut_mutants, args, kwargs)
    return result 

_get_cty_type_for_list.__signature__ = _mutmut_signature(x__get_cty_type_for_list__mutmut_orig)
x__get_cty_type_for_list__mutmut_orig.__name__ = 'x__get_cty_type_for_list'


def x__get_cty_type_for_dict__mutmut_orig(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[1]) if len(args) > 1 else CtyDynamic()
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_1(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = None
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_2(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(None) if len(args) > 1 else CtyDynamic()
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_3(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[2]) if len(args) > 1 else CtyDynamic()
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_4(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[1]) if len(args) >= 1 else CtyDynamic()
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_5(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[1]) if len(args) > 2 else CtyDynamic()
    return CtyMap(element_type=value_type)


def x__get_cty_type_for_dict__mutmut_6(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[1]) if len(args) > 1 else CtyDynamic()
    return CtyMap(element_type=None)

x__get_cty_type_for_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_cty_type_for_dict__mutmut_1': x__get_cty_type_for_dict__mutmut_1, 
    'x__get_cty_type_for_dict__mutmut_2': x__get_cty_type_for_dict__mutmut_2, 
    'x__get_cty_type_for_dict__mutmut_3': x__get_cty_type_for_dict__mutmut_3, 
    'x__get_cty_type_for_dict__mutmut_4': x__get_cty_type_for_dict__mutmut_4, 
    'x__get_cty_type_for_dict__mutmut_5': x__get_cty_type_for_dict__mutmut_5, 
    'x__get_cty_type_for_dict__mutmut_6': x__get_cty_type_for_dict__mutmut_6
}

def _get_cty_type_for_dict(*args, **kwargs):
    result = _mutmut_trampoline(x__get_cty_type_for_dict__mutmut_orig, x__get_cty_type_for_dict__mutmut_mutants, args, kwargs)
    return result 

_get_cty_type_for_dict.__signature__ = _mutmut_signature(x__get_cty_type_for_dict__mutmut_orig)
x__get_cty_type_for_dict__mutmut_orig.__name__ = 'x__get_cty_type_for_dict'


def x__get_cty_type_for_primitive__mutmut_orig(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_1(python_type: type) -> CtyType | None:
    if issubclass(None, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_2(python_type: type) -> CtyType | None:
    if issubclass(python_type, None):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_3(python_type: type) -> CtyType | None:
    if issubclass(str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_4(python_type: type) -> CtyType | None:
    if issubclass(python_type, ):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_5(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(None, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_6(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, None):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_7(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_8(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, ):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_9(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(None, int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_10(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, None):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_11(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(int | float | Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_12(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, ):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_13(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float & Decimal):
        return CtyNumber()
    return None


def x__get_cty_type_for_primitive__mutmut_14(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int & float | Decimal):
        return CtyNumber()
    return None

x__get_cty_type_for_primitive__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_cty_type_for_primitive__mutmut_1': x__get_cty_type_for_primitive__mutmut_1, 
    'x__get_cty_type_for_primitive__mutmut_2': x__get_cty_type_for_primitive__mutmut_2, 
    'x__get_cty_type_for_primitive__mutmut_3': x__get_cty_type_for_primitive__mutmut_3, 
    'x__get_cty_type_for_primitive__mutmut_4': x__get_cty_type_for_primitive__mutmut_4, 
    'x__get_cty_type_for_primitive__mutmut_5': x__get_cty_type_for_primitive__mutmut_5, 
    'x__get_cty_type_for_primitive__mutmut_6': x__get_cty_type_for_primitive__mutmut_6, 
    'x__get_cty_type_for_primitive__mutmut_7': x__get_cty_type_for_primitive__mutmut_7, 
    'x__get_cty_type_for_primitive__mutmut_8': x__get_cty_type_for_primitive__mutmut_8, 
    'x__get_cty_type_for_primitive__mutmut_9': x__get_cty_type_for_primitive__mutmut_9, 
    'x__get_cty_type_for_primitive__mutmut_10': x__get_cty_type_for_primitive__mutmut_10, 
    'x__get_cty_type_for_primitive__mutmut_11': x__get_cty_type_for_primitive__mutmut_11, 
    'x__get_cty_type_for_primitive__mutmut_12': x__get_cty_type_for_primitive__mutmut_12, 
    'x__get_cty_type_for_primitive__mutmut_13': x__get_cty_type_for_primitive__mutmut_13, 
    'x__get_cty_type_for_primitive__mutmut_14': x__get_cty_type_for_primitive__mutmut_14
}

def _get_cty_type_for_primitive(*args, **kwargs):
    result = _mutmut_trampoline(x__get_cty_type_for_primitive__mutmut_orig, x__get_cty_type_for_primitive__mutmut_mutants, args, kwargs)
    return result 

_get_cty_type_for_primitive.__signature__ = _mutmut_signature(x__get_cty_type_for_primitive__mutmut_orig)
x__get_cty_type_for_primitive__mutmut_orig.__name__ = 'x__get_cty_type_for_primitive'


def x__is_union_type__mutmut_orig(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_1(annotation: Any) -> bool:
    origin = None
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_2(annotation: Any) -> bool:
    origin = get_origin(None)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_3(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = None
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_4(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is not UnionType
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_5(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = None
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_6(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union and origin is Union
    except ImportError:
        pass
    return is_union


def x__is_union_type__mutmut_7(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union or origin is not Union
    except ImportError:
        pass
    return is_union

x__is_union_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_union_type__mutmut_1': x__is_union_type__mutmut_1, 
    'x__is_union_type__mutmut_2': x__is_union_type__mutmut_2, 
    'x__is_union_type__mutmut_3': x__is_union_type__mutmut_3, 
    'x__is_union_type__mutmut_4': x__is_union_type__mutmut_4, 
    'x__is_union_type__mutmut_5': x__is_union_type__mutmut_5, 
    'x__is_union_type__mutmut_6': x__is_union_type__mutmut_6, 
    'x__is_union_type__mutmut_7': x__is_union_type__mutmut_7
}

def _is_union_type(*args, **kwargs):
    result = _mutmut_trampoline(x__is_union_type__mutmut_orig, x__is_union_type__mutmut_mutants, args, kwargs)
    return result 

_is_union_type.__signature__ = _mutmut_signature(x__is_union_type__mutmut_orig)
x__is_union_type__mutmut_orig.__name__ = 'x__is_union_type'


def x__is_list_type__mutmut_orig(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (list, list) or annotation is list


def x__is_list_type__mutmut_1(annotation: Any) -> bool:
    origin = None
    return origin in (list, list) or annotation is list


def x__is_list_type__mutmut_2(annotation: Any) -> bool:
    origin = get_origin(None)
    return origin in (list, list) or annotation is list


def x__is_list_type__mutmut_3(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (list, list) and annotation is list


def x__is_list_type__mutmut_4(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin not in (list, list) or annotation is list


def x__is_list_type__mutmut_5(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (list, list) or annotation is not list

x__is_list_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_list_type__mutmut_1': x__is_list_type__mutmut_1, 
    'x__is_list_type__mutmut_2': x__is_list_type__mutmut_2, 
    'x__is_list_type__mutmut_3': x__is_list_type__mutmut_3, 
    'x__is_list_type__mutmut_4': x__is_list_type__mutmut_4, 
    'x__is_list_type__mutmut_5': x__is_list_type__mutmut_5
}

def _is_list_type(*args, **kwargs):
    result = _mutmut_trampoline(x__is_list_type__mutmut_orig, x__is_list_type__mutmut_mutants, args, kwargs)
    return result 

_is_list_type.__signature__ = _mutmut_signature(x__is_list_type__mutmut_orig)
x__is_list_type__mutmut_orig.__name__ = 'x__is_list_type'


def x__is_dict_type__mutmut_orig(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (dict, dict) or annotation is dict


def x__is_dict_type__mutmut_1(annotation: Any) -> bool:
    origin = None
    return origin in (dict, dict) or annotation is dict


def x__is_dict_type__mutmut_2(annotation: Any) -> bool:
    origin = get_origin(None)
    return origin in (dict, dict) or annotation is dict


def x__is_dict_type__mutmut_3(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (dict, dict) and annotation is dict


def x__is_dict_type__mutmut_4(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin not in (dict, dict) or annotation is dict


def x__is_dict_type__mutmut_5(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (dict, dict) or annotation is not dict

x__is_dict_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_dict_type__mutmut_1': x__is_dict_type__mutmut_1, 
    'x__is_dict_type__mutmut_2': x__is_dict_type__mutmut_2, 
    'x__is_dict_type__mutmut_3': x__is_dict_type__mutmut_3, 
    'x__is_dict_type__mutmut_4': x__is_dict_type__mutmut_4, 
    'x__is_dict_type__mutmut_5': x__is_dict_type__mutmut_5
}

def _is_dict_type(*args, **kwargs):
    result = _mutmut_trampoline(x__is_dict_type__mutmut_orig, x__is_dict_type__mutmut_mutants, args, kwargs)
    return result 

_is_dict_type.__signature__ = _mutmut_signature(x__is_dict_type__mutmut_orig)
x__is_dict_type__mutmut_orig.__name__ = 'x__is_dict_type'


def x__python_type_to_cty_type__mutmut_orig(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_1(python_type: Any) -> CtyType:
    if python_type is CtyValue and python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_2(python_type: Any) -> CtyType:
    if python_type is not CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_3(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is not Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_4(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = None

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_5(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(None)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_6(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(None):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_7(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(None, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_8(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, None)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_9(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_10(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, )

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_11(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(None):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_12(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(None, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_13(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, None)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_14(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_15(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, )

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_16(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(None):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_17(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(None, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_18(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, None)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_19(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_20(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, )

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_21(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = None
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_22(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(None)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(f"Could not infer a specific CtyType for hint '{python_type}', defaulting to CtyDynamic.")
    return CtyDynamic()


def x__python_type_to_cty_type__mutmut_23(python_type: Any) -> CtyType:
    if python_type is CtyValue or python_type is Any:
        return CtyDynamic()

    args = get_args(python_type)

    if _is_union_type(python_type):
        return _get_cty_type_for_union(python_type, args)

    if _is_list_type(python_type):
        return _get_cty_type_for_list(python_type, args)

    if _is_dict_type(python_type):
        return _get_cty_type_for_dict(python_type, args)

    if isinstance(python_type, type):
        primitive_cty_type = _get_cty_type_for_primitive(python_type)
        if primitive_cty_type:
            return primitive_cty_type

    logger.warning(None)
    return CtyDynamic()

x__python_type_to_cty_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__python_type_to_cty_type__mutmut_1': x__python_type_to_cty_type__mutmut_1, 
    'x__python_type_to_cty_type__mutmut_2': x__python_type_to_cty_type__mutmut_2, 
    'x__python_type_to_cty_type__mutmut_3': x__python_type_to_cty_type__mutmut_3, 
    'x__python_type_to_cty_type__mutmut_4': x__python_type_to_cty_type__mutmut_4, 
    'x__python_type_to_cty_type__mutmut_5': x__python_type_to_cty_type__mutmut_5, 
    'x__python_type_to_cty_type__mutmut_6': x__python_type_to_cty_type__mutmut_6, 
    'x__python_type_to_cty_type__mutmut_7': x__python_type_to_cty_type__mutmut_7, 
    'x__python_type_to_cty_type__mutmut_8': x__python_type_to_cty_type__mutmut_8, 
    'x__python_type_to_cty_type__mutmut_9': x__python_type_to_cty_type__mutmut_9, 
    'x__python_type_to_cty_type__mutmut_10': x__python_type_to_cty_type__mutmut_10, 
    'x__python_type_to_cty_type__mutmut_11': x__python_type_to_cty_type__mutmut_11, 
    'x__python_type_to_cty_type__mutmut_12': x__python_type_to_cty_type__mutmut_12, 
    'x__python_type_to_cty_type__mutmut_13': x__python_type_to_cty_type__mutmut_13, 
    'x__python_type_to_cty_type__mutmut_14': x__python_type_to_cty_type__mutmut_14, 
    'x__python_type_to_cty_type__mutmut_15': x__python_type_to_cty_type__mutmut_15, 
    'x__python_type_to_cty_type__mutmut_16': x__python_type_to_cty_type__mutmut_16, 
    'x__python_type_to_cty_type__mutmut_17': x__python_type_to_cty_type__mutmut_17, 
    'x__python_type_to_cty_type__mutmut_18': x__python_type_to_cty_type__mutmut_18, 
    'x__python_type_to_cty_type__mutmut_19': x__python_type_to_cty_type__mutmut_19, 
    'x__python_type_to_cty_type__mutmut_20': x__python_type_to_cty_type__mutmut_20, 
    'x__python_type_to_cty_type__mutmut_21': x__python_type_to_cty_type__mutmut_21, 
    'x__python_type_to_cty_type__mutmut_22': x__python_type_to_cty_type__mutmut_22, 
    'x__python_type_to_cty_type__mutmut_23': x__python_type_to_cty_type__mutmut_23
}

def _python_type_to_cty_type(*args, **kwargs):
    result = _mutmut_trampoline(x__python_type_to_cty_type__mutmut_orig, x__python_type_to_cty_type__mutmut_mutants, args, kwargs)
    return result 

_python_type_to_cty_type.__signature__ = _mutmut_signature(x__python_type_to_cty_type__mutmut_orig)
x__python_type_to_cty_type__mutmut_orig.__name__ = 'x__python_type_to_cty_type'


def x__is_optional_type_hint__mutmut_orig(annotation: Any) -> bool:
    return _is_union_type(annotation) and type(None) in get_args(annotation)


def x__is_optional_type_hint__mutmut_1(annotation: Any) -> bool:
    return _is_union_type(annotation) or type(None) in get_args(annotation)


def x__is_optional_type_hint__mutmut_2(annotation: Any) -> bool:
    return _is_union_type(None) and type(None) in get_args(annotation)


def x__is_optional_type_hint__mutmut_3(annotation: Any) -> bool:
    return _is_union_type(annotation) and type(None) not in get_args(annotation)


def x__is_optional_type_hint__mutmut_4(annotation: Any) -> bool:
    return _is_union_type(annotation) and type(None) in get_args(None)

x__is_optional_type_hint__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_optional_type_hint__mutmut_1': x__is_optional_type_hint__mutmut_1, 
    'x__is_optional_type_hint__mutmut_2': x__is_optional_type_hint__mutmut_2, 
    'x__is_optional_type_hint__mutmut_3': x__is_optional_type_hint__mutmut_3, 
    'x__is_optional_type_hint__mutmut_4': x__is_optional_type_hint__mutmut_4
}

def _is_optional_type_hint(*args, **kwargs):
    result = _mutmut_trampoline(x__is_optional_type_hint__mutmut_orig, x__is_optional_type_hint__mutmut_mutants, args, kwargs)
    return result 

_is_optional_type_hint.__signature__ = _mutmut_signature(x__is_optional_type_hint__mutmut_orig)
x__is_optional_type_hint__mutmut_orig.__name__ = 'x__is_optional_type_hint'


def x__extract_parameters_meta__mutmut_orig(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_1(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = None
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_2(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = ""
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_3(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = None

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_4(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get(None, {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_5(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", None)

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_6(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get({})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_7(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", )

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_8(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(None, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_9(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, None, {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_10(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", None).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_11(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr("_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_12(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_13(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", ).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_14(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "XX_function_metadataXX", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_15(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_FUNCTION_METADATA", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_16(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("XXparam_descriptionsXX", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_17(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("PARAM_DESCRIPTIONS", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_18(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_19(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind != inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_20(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name != "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_21(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "XXselfXX":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_22(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "SELF":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_23(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            break

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_24(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind != inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_25(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = None
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_26(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(None, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_27(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, None)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_28(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_29(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, )
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_30(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') or param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_31(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(None, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_32(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, None) and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_33(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr('__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_34(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, ) and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_35(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, 'XX__args__XX') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_36(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__ARGS__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_37(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = None
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_38(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[1]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_39(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = None

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_40(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = None
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_41(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "XXnameXX": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_42(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "NAME": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_43(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "XXcty_typeXX": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_44(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "CTY_TYPE": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_45(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(None),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_46(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "XXdescriptionXX": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_47(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "DESCRIPTION": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_48(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(None, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_49(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, None),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_50(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get("Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_51(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, ),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_52(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "XXOptional parametersXX"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_53(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_54(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "OPTIONAL PARAMETERS"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_55(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "XXallow_nullXX": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_56(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "ALLOW_NULL": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_57(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": False,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_58(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            break

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_59(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = None
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_60(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(None, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_61(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, None)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_62(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_63(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, )
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_64(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = None

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_65(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "XXnameXX": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_66(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "NAME": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_67(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "XXcty_typeXX": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_68(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "CTY_TYPE": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_69(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(None),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_70(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "XXdescriptionXX": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_71(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "DESCRIPTION": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_72(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(None, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_73(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, None),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_74(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_75(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_76(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, "XXXX"),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_77(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "XXallow_nullXX": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_78(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "ALLOW_NULL": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_79(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(None),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_80(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_81(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is not None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_82(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = None
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_83(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["XXallow_nullXX"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_84(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["ALLOW_NULL"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_85(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = False
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_86(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = None
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_87(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    None
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_88(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(None)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_89(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(None)

    return {
        "parameters": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_90(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "XXparametersXX": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_91(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "PARAMETERS": required_params,
        "variadic_parameter": variadic_param,
    }


def x__extract_parameters_meta__mutmut_92(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "XXvariadic_parameterXX": variadic_param,
    }


def x__extract_parameters_meta__mutmut_93(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract parameter metadata, separating required and variadic parameters.

    Parameters with default values become variadic (optional) parameters in Terraform.
    This enables true optional parameters with excellent DX.

    Returns:
        dict with "parameters" (required) and "variadic_parameter" (optional) keys
    """
    required_params = []
    variadic_param = None
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})

    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue

        # Handle *args (VAR_POSITIONAL) - this is a true variadic parameter
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_hint = type_hints.get(name, Any)
            # Extract element type from *args annotation if available
            if hasattr(param_hint, '__args__') and param_hint.__args__:
                element_type = param_hint.__args__[0]
            else:
                element_type = Any

            variadic_param = {
                "name": name,
                "cty_type": _python_type_to_cty_type(element_type),
                "description": param_descriptions.get(name, "Optional parameters"),
                "allow_null": True,  # Variadic params can be omitted
            }
            continue

        param_hint = type_hints.get(name, Any)
        param_meta = {
            "name": name,
            "cty_type": _python_type_to_cty_type(param_hint),
            "description": param_descriptions.get(name, ""),
            "allow_null": _is_optional_type_hint(param_hint),
        }

        # Parameters with defaults become variadic (but we only support ONE variadic param)
        # So if we find a default, convert it to variadic and stop processing params
        if param.default is not inspect.Parameter.empty:
            if variadic_param is None:
                # Parameters with defaults are always nullable (can be omitted)
                param_meta["allow_null"] = True
                variadic_param = param_meta
            else:
                # Multiple defaults - add as required param with a warning
                logger.warning(
                    f"Function {func_obj.__name__} has multiple parameters with defaults. "
                    f"Only the first will be variadic. Parameter '{name}' will be required."
                )
                required_params.append(param_meta)
        else:
            required_params.append(param_meta)

    return {
        "parameters": required_params,
        "VARIADIC_PARAMETER": variadic_param,
    }

x__extract_parameters_meta__mutmut_mutants : ClassVar[MutantDict] = {
'x__extract_parameters_meta__mutmut_1': x__extract_parameters_meta__mutmut_1, 
    'x__extract_parameters_meta__mutmut_2': x__extract_parameters_meta__mutmut_2, 
    'x__extract_parameters_meta__mutmut_3': x__extract_parameters_meta__mutmut_3, 
    'x__extract_parameters_meta__mutmut_4': x__extract_parameters_meta__mutmut_4, 
    'x__extract_parameters_meta__mutmut_5': x__extract_parameters_meta__mutmut_5, 
    'x__extract_parameters_meta__mutmut_6': x__extract_parameters_meta__mutmut_6, 
    'x__extract_parameters_meta__mutmut_7': x__extract_parameters_meta__mutmut_7, 
    'x__extract_parameters_meta__mutmut_8': x__extract_parameters_meta__mutmut_8, 
    'x__extract_parameters_meta__mutmut_9': x__extract_parameters_meta__mutmut_9, 
    'x__extract_parameters_meta__mutmut_10': x__extract_parameters_meta__mutmut_10, 
    'x__extract_parameters_meta__mutmut_11': x__extract_parameters_meta__mutmut_11, 
    'x__extract_parameters_meta__mutmut_12': x__extract_parameters_meta__mutmut_12, 
    'x__extract_parameters_meta__mutmut_13': x__extract_parameters_meta__mutmut_13, 
    'x__extract_parameters_meta__mutmut_14': x__extract_parameters_meta__mutmut_14, 
    'x__extract_parameters_meta__mutmut_15': x__extract_parameters_meta__mutmut_15, 
    'x__extract_parameters_meta__mutmut_16': x__extract_parameters_meta__mutmut_16, 
    'x__extract_parameters_meta__mutmut_17': x__extract_parameters_meta__mutmut_17, 
    'x__extract_parameters_meta__mutmut_18': x__extract_parameters_meta__mutmut_18, 
    'x__extract_parameters_meta__mutmut_19': x__extract_parameters_meta__mutmut_19, 
    'x__extract_parameters_meta__mutmut_20': x__extract_parameters_meta__mutmut_20, 
    'x__extract_parameters_meta__mutmut_21': x__extract_parameters_meta__mutmut_21, 
    'x__extract_parameters_meta__mutmut_22': x__extract_parameters_meta__mutmut_22, 
    'x__extract_parameters_meta__mutmut_23': x__extract_parameters_meta__mutmut_23, 
    'x__extract_parameters_meta__mutmut_24': x__extract_parameters_meta__mutmut_24, 
    'x__extract_parameters_meta__mutmut_25': x__extract_parameters_meta__mutmut_25, 
    'x__extract_parameters_meta__mutmut_26': x__extract_parameters_meta__mutmut_26, 
    'x__extract_parameters_meta__mutmut_27': x__extract_parameters_meta__mutmut_27, 
    'x__extract_parameters_meta__mutmut_28': x__extract_parameters_meta__mutmut_28, 
    'x__extract_parameters_meta__mutmut_29': x__extract_parameters_meta__mutmut_29, 
    'x__extract_parameters_meta__mutmut_30': x__extract_parameters_meta__mutmut_30, 
    'x__extract_parameters_meta__mutmut_31': x__extract_parameters_meta__mutmut_31, 
    'x__extract_parameters_meta__mutmut_32': x__extract_parameters_meta__mutmut_32, 
    'x__extract_parameters_meta__mutmut_33': x__extract_parameters_meta__mutmut_33, 
    'x__extract_parameters_meta__mutmut_34': x__extract_parameters_meta__mutmut_34, 
    'x__extract_parameters_meta__mutmut_35': x__extract_parameters_meta__mutmut_35, 
    'x__extract_parameters_meta__mutmut_36': x__extract_parameters_meta__mutmut_36, 
    'x__extract_parameters_meta__mutmut_37': x__extract_parameters_meta__mutmut_37, 
    'x__extract_parameters_meta__mutmut_38': x__extract_parameters_meta__mutmut_38, 
    'x__extract_parameters_meta__mutmut_39': x__extract_parameters_meta__mutmut_39, 
    'x__extract_parameters_meta__mutmut_40': x__extract_parameters_meta__mutmut_40, 
    'x__extract_parameters_meta__mutmut_41': x__extract_parameters_meta__mutmut_41, 
    'x__extract_parameters_meta__mutmut_42': x__extract_parameters_meta__mutmut_42, 
    'x__extract_parameters_meta__mutmut_43': x__extract_parameters_meta__mutmut_43, 
    'x__extract_parameters_meta__mutmut_44': x__extract_parameters_meta__mutmut_44, 
    'x__extract_parameters_meta__mutmut_45': x__extract_parameters_meta__mutmut_45, 
    'x__extract_parameters_meta__mutmut_46': x__extract_parameters_meta__mutmut_46, 
    'x__extract_parameters_meta__mutmut_47': x__extract_parameters_meta__mutmut_47, 
    'x__extract_parameters_meta__mutmut_48': x__extract_parameters_meta__mutmut_48, 
    'x__extract_parameters_meta__mutmut_49': x__extract_parameters_meta__mutmut_49, 
    'x__extract_parameters_meta__mutmut_50': x__extract_parameters_meta__mutmut_50, 
    'x__extract_parameters_meta__mutmut_51': x__extract_parameters_meta__mutmut_51, 
    'x__extract_parameters_meta__mutmut_52': x__extract_parameters_meta__mutmut_52, 
    'x__extract_parameters_meta__mutmut_53': x__extract_parameters_meta__mutmut_53, 
    'x__extract_parameters_meta__mutmut_54': x__extract_parameters_meta__mutmut_54, 
    'x__extract_parameters_meta__mutmut_55': x__extract_parameters_meta__mutmut_55, 
    'x__extract_parameters_meta__mutmut_56': x__extract_parameters_meta__mutmut_56, 
    'x__extract_parameters_meta__mutmut_57': x__extract_parameters_meta__mutmut_57, 
    'x__extract_parameters_meta__mutmut_58': x__extract_parameters_meta__mutmut_58, 
    'x__extract_parameters_meta__mutmut_59': x__extract_parameters_meta__mutmut_59, 
    'x__extract_parameters_meta__mutmut_60': x__extract_parameters_meta__mutmut_60, 
    'x__extract_parameters_meta__mutmut_61': x__extract_parameters_meta__mutmut_61, 
    'x__extract_parameters_meta__mutmut_62': x__extract_parameters_meta__mutmut_62, 
    'x__extract_parameters_meta__mutmut_63': x__extract_parameters_meta__mutmut_63, 
    'x__extract_parameters_meta__mutmut_64': x__extract_parameters_meta__mutmut_64, 
    'x__extract_parameters_meta__mutmut_65': x__extract_parameters_meta__mutmut_65, 
    'x__extract_parameters_meta__mutmut_66': x__extract_parameters_meta__mutmut_66, 
    'x__extract_parameters_meta__mutmut_67': x__extract_parameters_meta__mutmut_67, 
    'x__extract_parameters_meta__mutmut_68': x__extract_parameters_meta__mutmut_68, 
    'x__extract_parameters_meta__mutmut_69': x__extract_parameters_meta__mutmut_69, 
    'x__extract_parameters_meta__mutmut_70': x__extract_parameters_meta__mutmut_70, 
    'x__extract_parameters_meta__mutmut_71': x__extract_parameters_meta__mutmut_71, 
    'x__extract_parameters_meta__mutmut_72': x__extract_parameters_meta__mutmut_72, 
    'x__extract_parameters_meta__mutmut_73': x__extract_parameters_meta__mutmut_73, 
    'x__extract_parameters_meta__mutmut_74': x__extract_parameters_meta__mutmut_74, 
    'x__extract_parameters_meta__mutmut_75': x__extract_parameters_meta__mutmut_75, 
    'x__extract_parameters_meta__mutmut_76': x__extract_parameters_meta__mutmut_76, 
    'x__extract_parameters_meta__mutmut_77': x__extract_parameters_meta__mutmut_77, 
    'x__extract_parameters_meta__mutmut_78': x__extract_parameters_meta__mutmut_78, 
    'x__extract_parameters_meta__mutmut_79': x__extract_parameters_meta__mutmut_79, 
    'x__extract_parameters_meta__mutmut_80': x__extract_parameters_meta__mutmut_80, 
    'x__extract_parameters_meta__mutmut_81': x__extract_parameters_meta__mutmut_81, 
    'x__extract_parameters_meta__mutmut_82': x__extract_parameters_meta__mutmut_82, 
    'x__extract_parameters_meta__mutmut_83': x__extract_parameters_meta__mutmut_83, 
    'x__extract_parameters_meta__mutmut_84': x__extract_parameters_meta__mutmut_84, 
    'x__extract_parameters_meta__mutmut_85': x__extract_parameters_meta__mutmut_85, 
    'x__extract_parameters_meta__mutmut_86': x__extract_parameters_meta__mutmut_86, 
    'x__extract_parameters_meta__mutmut_87': x__extract_parameters_meta__mutmut_87, 
    'x__extract_parameters_meta__mutmut_88': x__extract_parameters_meta__mutmut_88, 
    'x__extract_parameters_meta__mutmut_89': x__extract_parameters_meta__mutmut_89, 
    'x__extract_parameters_meta__mutmut_90': x__extract_parameters_meta__mutmut_90, 
    'x__extract_parameters_meta__mutmut_91': x__extract_parameters_meta__mutmut_91, 
    'x__extract_parameters_meta__mutmut_92': x__extract_parameters_meta__mutmut_92, 
    'x__extract_parameters_meta__mutmut_93': x__extract_parameters_meta__mutmut_93
}

def _extract_parameters_meta(*args, **kwargs):
    result = _mutmut_trampoline(x__extract_parameters_meta__mutmut_orig, x__extract_parameters_meta__mutmut_mutants, args, kwargs)
    return result 

_extract_parameters_meta.__signature__ = _mutmut_signature(x__extract_parameters_meta__mutmut_orig)
x__extract_parameters_meta__mutmut_orig.__name__ = 'x__extract_parameters_meta'


def x__extract_return_type_meta__mutmut_orig(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_1(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = None
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_2(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get(None, Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_3(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", None)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_4(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get(Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_5(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", )
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_6(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("XXreturnXX", Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_7(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("RETURN", Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_8(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", Any)
    return {"XXcty_typeXX": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_9(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", Any)
    return {"CTY_TYPE": _python_type_to_cty_type(return_type_hint)}


def x__extract_return_type_meta__mutmut_10(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", Any)
    return {"cty_type": _python_type_to_cty_type(None)}

x__extract_return_type_meta__mutmut_mutants : ClassVar[MutantDict] = {
'x__extract_return_type_meta__mutmut_1': x__extract_return_type_meta__mutmut_1, 
    'x__extract_return_type_meta__mutmut_2': x__extract_return_type_meta__mutmut_2, 
    'x__extract_return_type_meta__mutmut_3': x__extract_return_type_meta__mutmut_3, 
    'x__extract_return_type_meta__mutmut_4': x__extract_return_type_meta__mutmut_4, 
    'x__extract_return_type_meta__mutmut_5': x__extract_return_type_meta__mutmut_5, 
    'x__extract_return_type_meta__mutmut_6': x__extract_return_type_meta__mutmut_6, 
    'x__extract_return_type_meta__mutmut_7': x__extract_return_type_meta__mutmut_7, 
    'x__extract_return_type_meta__mutmut_8': x__extract_return_type_meta__mutmut_8, 
    'x__extract_return_type_meta__mutmut_9': x__extract_return_type_meta__mutmut_9, 
    'x__extract_return_type_meta__mutmut_10': x__extract_return_type_meta__mutmut_10
}

def _extract_return_type_meta(*args, **kwargs):
    result = _mutmut_trampoline(x__extract_return_type_meta__mutmut_orig, x__extract_return_type_meta__mutmut_mutants, args, kwargs)
    return result 

_extract_return_type_meta.__signature__ = _mutmut_signature(x__extract_return_type_meta__mutmut_orig)
x__extract_return_type_meta__mutmut_orig.__name__ = 'x__extract_return_type_meta'


def x__extract_docstring_meta__mutmut_orig(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_1(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = None
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_2(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) and ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_3(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(None) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_4(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or "XXXX"
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_5(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") or docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_6(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_7(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get(None) and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_8(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("XXsummaryXX") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_9(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("SUMMARY") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_10(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = None
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_11(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["XXsummaryXX"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_12(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["SUMMARY"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_13(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split(None, 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_14(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", None)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_15(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split(1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_16(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", )[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_17(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().rsplit("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_18(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("XX\nXX", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_19(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 2)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_20(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[1]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_21(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") or docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_22(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_23(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get(None) and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_24(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("XXdescriptionXX") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_25(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("DESCRIPTION") and docstring:
        base_meta["description"] = docstring


def x__extract_docstring_meta__mutmut_26(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = None


def x__extract_docstring_meta__mutmut_27(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["XXdescriptionXX"] = docstring


def x__extract_docstring_meta__mutmut_28(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["DESCRIPTION"] = docstring

x__extract_docstring_meta__mutmut_mutants : ClassVar[MutantDict] = {
'x__extract_docstring_meta__mutmut_1': x__extract_docstring_meta__mutmut_1, 
    'x__extract_docstring_meta__mutmut_2': x__extract_docstring_meta__mutmut_2, 
    'x__extract_docstring_meta__mutmut_3': x__extract_docstring_meta__mutmut_3, 
    'x__extract_docstring_meta__mutmut_4': x__extract_docstring_meta__mutmut_4, 
    'x__extract_docstring_meta__mutmut_5': x__extract_docstring_meta__mutmut_5, 
    'x__extract_docstring_meta__mutmut_6': x__extract_docstring_meta__mutmut_6, 
    'x__extract_docstring_meta__mutmut_7': x__extract_docstring_meta__mutmut_7, 
    'x__extract_docstring_meta__mutmut_8': x__extract_docstring_meta__mutmut_8, 
    'x__extract_docstring_meta__mutmut_9': x__extract_docstring_meta__mutmut_9, 
    'x__extract_docstring_meta__mutmut_10': x__extract_docstring_meta__mutmut_10, 
    'x__extract_docstring_meta__mutmut_11': x__extract_docstring_meta__mutmut_11, 
    'x__extract_docstring_meta__mutmut_12': x__extract_docstring_meta__mutmut_12, 
    'x__extract_docstring_meta__mutmut_13': x__extract_docstring_meta__mutmut_13, 
    'x__extract_docstring_meta__mutmut_14': x__extract_docstring_meta__mutmut_14, 
    'x__extract_docstring_meta__mutmut_15': x__extract_docstring_meta__mutmut_15, 
    'x__extract_docstring_meta__mutmut_16': x__extract_docstring_meta__mutmut_16, 
    'x__extract_docstring_meta__mutmut_17': x__extract_docstring_meta__mutmut_17, 
    'x__extract_docstring_meta__mutmut_18': x__extract_docstring_meta__mutmut_18, 
    'x__extract_docstring_meta__mutmut_19': x__extract_docstring_meta__mutmut_19, 
    'x__extract_docstring_meta__mutmut_20': x__extract_docstring_meta__mutmut_20, 
    'x__extract_docstring_meta__mutmut_21': x__extract_docstring_meta__mutmut_21, 
    'x__extract_docstring_meta__mutmut_22': x__extract_docstring_meta__mutmut_22, 
    'x__extract_docstring_meta__mutmut_23': x__extract_docstring_meta__mutmut_23, 
    'x__extract_docstring_meta__mutmut_24': x__extract_docstring_meta__mutmut_24, 
    'x__extract_docstring_meta__mutmut_25': x__extract_docstring_meta__mutmut_25, 
    'x__extract_docstring_meta__mutmut_26': x__extract_docstring_meta__mutmut_26, 
    'x__extract_docstring_meta__mutmut_27': x__extract_docstring_meta__mutmut_27, 
    'x__extract_docstring_meta__mutmut_28': x__extract_docstring_meta__mutmut_28
}

def _extract_docstring_meta(*args, **kwargs):
    result = _mutmut_trampoline(x__extract_docstring_meta__mutmut_orig, x__extract_docstring_meta__mutmut_mutants, args, kwargs)
    return result 

_extract_docstring_meta.__signature__ = _mutmut_signature(x__extract_docstring_meta__mutmut_orig)
x__extract_docstring_meta__mutmut_orig.__name__ = 'x__extract_docstring_meta'


def x_function_to_dict__mutmut_orig(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_1(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = None
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_2(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(None, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_3(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, None, {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_4(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", None)
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_5(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr("_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_6(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_7(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", )
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_8(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "XX_function_metadataXX", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_9(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_FUNCTION_METADATA", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_10(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault(None, func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_11(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", None)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_12(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault(func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_13(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", )
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_14(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("XXnameXX", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_15(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("NAME", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_16(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = None
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_17(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(None)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_18(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = None
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_19(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(None)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_20(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            None
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_21(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = None

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_22(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = None
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_23(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(None, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_24(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, None, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_25(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, None)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_26(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_27(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_28(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, )
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_29(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = None
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_30(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["XXparametersXX"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_31(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["PARAMETERS"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_32(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["XXparametersXX"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_33(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["PARAMETERS"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_34(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["XXvariadic_parameterXX"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_35(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["VARIADIC_PARAMETER"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_36(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = None

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_37(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["XXvariadic_parameterXX"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_38(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["VARIADIC_PARAMETER"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_39(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["XXvariadic_parameterXX"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_40(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["VARIADIC_PARAMETER"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_41(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = None
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_42(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["XXreturnXX"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_43(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["RETURN"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_44(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(None)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta


def x_function_to_dict__mutmut_45(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(None, base_meta)

    return base_meta


def x_function_to_dict__mutmut_46(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, None)

    return base_meta


def x_function_to_dict__mutmut_47(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(base_meta)

    return base_meta


def x_function_to_dict__mutmut_48(func_obj: Callable[..., Any]) -> dict[str, Any]:
    base_meta = getattr(func_obj, "_function_metadata", {})
    base_meta.setdefault("name", func_obj.__name__)
    sig = inspect.signature(func_obj)
    try:
        type_hints = get_type_hints(func_obj)
    except (NameError, TypeError) as e:
        logger.warning(
            f"Could not resolve type hints for {func_obj.__name__}: {e}. Types will default to CtyDynamic."
        )
        type_hints = {}

    # Extract parameters (returns dict with "parameters" and "variadic_parameter")
    params_meta = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["parameters"] = params_meta["parameters"]
    if params_meta["variadic_parameter"]:
        base_meta["variadic_parameter"] = params_meta["variadic_parameter"]

    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, )

    return base_meta

x_function_to_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x_function_to_dict__mutmut_1': x_function_to_dict__mutmut_1, 
    'x_function_to_dict__mutmut_2': x_function_to_dict__mutmut_2, 
    'x_function_to_dict__mutmut_3': x_function_to_dict__mutmut_3, 
    'x_function_to_dict__mutmut_4': x_function_to_dict__mutmut_4, 
    'x_function_to_dict__mutmut_5': x_function_to_dict__mutmut_5, 
    'x_function_to_dict__mutmut_6': x_function_to_dict__mutmut_6, 
    'x_function_to_dict__mutmut_7': x_function_to_dict__mutmut_7, 
    'x_function_to_dict__mutmut_8': x_function_to_dict__mutmut_8, 
    'x_function_to_dict__mutmut_9': x_function_to_dict__mutmut_9, 
    'x_function_to_dict__mutmut_10': x_function_to_dict__mutmut_10, 
    'x_function_to_dict__mutmut_11': x_function_to_dict__mutmut_11, 
    'x_function_to_dict__mutmut_12': x_function_to_dict__mutmut_12, 
    'x_function_to_dict__mutmut_13': x_function_to_dict__mutmut_13, 
    'x_function_to_dict__mutmut_14': x_function_to_dict__mutmut_14, 
    'x_function_to_dict__mutmut_15': x_function_to_dict__mutmut_15, 
    'x_function_to_dict__mutmut_16': x_function_to_dict__mutmut_16, 
    'x_function_to_dict__mutmut_17': x_function_to_dict__mutmut_17, 
    'x_function_to_dict__mutmut_18': x_function_to_dict__mutmut_18, 
    'x_function_to_dict__mutmut_19': x_function_to_dict__mutmut_19, 
    'x_function_to_dict__mutmut_20': x_function_to_dict__mutmut_20, 
    'x_function_to_dict__mutmut_21': x_function_to_dict__mutmut_21, 
    'x_function_to_dict__mutmut_22': x_function_to_dict__mutmut_22, 
    'x_function_to_dict__mutmut_23': x_function_to_dict__mutmut_23, 
    'x_function_to_dict__mutmut_24': x_function_to_dict__mutmut_24, 
    'x_function_to_dict__mutmut_25': x_function_to_dict__mutmut_25, 
    'x_function_to_dict__mutmut_26': x_function_to_dict__mutmut_26, 
    'x_function_to_dict__mutmut_27': x_function_to_dict__mutmut_27, 
    'x_function_to_dict__mutmut_28': x_function_to_dict__mutmut_28, 
    'x_function_to_dict__mutmut_29': x_function_to_dict__mutmut_29, 
    'x_function_to_dict__mutmut_30': x_function_to_dict__mutmut_30, 
    'x_function_to_dict__mutmut_31': x_function_to_dict__mutmut_31, 
    'x_function_to_dict__mutmut_32': x_function_to_dict__mutmut_32, 
    'x_function_to_dict__mutmut_33': x_function_to_dict__mutmut_33, 
    'x_function_to_dict__mutmut_34': x_function_to_dict__mutmut_34, 
    'x_function_to_dict__mutmut_35': x_function_to_dict__mutmut_35, 
    'x_function_to_dict__mutmut_36': x_function_to_dict__mutmut_36, 
    'x_function_to_dict__mutmut_37': x_function_to_dict__mutmut_37, 
    'x_function_to_dict__mutmut_38': x_function_to_dict__mutmut_38, 
    'x_function_to_dict__mutmut_39': x_function_to_dict__mutmut_39, 
    'x_function_to_dict__mutmut_40': x_function_to_dict__mutmut_40, 
    'x_function_to_dict__mutmut_41': x_function_to_dict__mutmut_41, 
    'x_function_to_dict__mutmut_42': x_function_to_dict__mutmut_42, 
    'x_function_to_dict__mutmut_43': x_function_to_dict__mutmut_43, 
    'x_function_to_dict__mutmut_44': x_function_to_dict__mutmut_44, 
    'x_function_to_dict__mutmut_45': x_function_to_dict__mutmut_45, 
    'x_function_to_dict__mutmut_46': x_function_to_dict__mutmut_46, 
    'x_function_to_dict__mutmut_47': x_function_to_dict__mutmut_47, 
    'x_function_to_dict__mutmut_48': x_function_to_dict__mutmut_48
}

def function_to_dict(*args, **kwargs):
    result = _mutmut_trampoline(x_function_to_dict__mutmut_orig, x_function_to_dict__mutmut_mutants, args, kwargs)
    return result 

function_to_dict.__signature__ = _mutmut_signature(x_function_to_dict__mutmut_orig)
x_function_to_dict__mutmut_orig.__name__ = 'x_function_to_dict'
