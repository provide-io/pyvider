# pyvider/src/pyvider/conversion/utils.py
"""
Provides general-purpose, high-level conversion utilities for the framework.
"""

from typing import Any

from pyvider.cty import CtyDynamic, CtyList, CtyObject, CtyType, CtyValue

# FIX: Correctly import from the pyvider-cty library's canonical location.
from pyvider.cty.conversion import infer_cty_type_from_raw
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


def x_unify_and_validate_list_of_objects__mutmut_orig(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_1(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_2(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate(None)

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_3(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=None).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_4(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = None
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_5(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = None

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_6(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(None)
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_7(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = None
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_8(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(None)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_9(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_10(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = None
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_11(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_12(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(None):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_13(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = None

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_14(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = None

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_15(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_16(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(None)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_17(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key not in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_18(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = None

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_19(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=None, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_20(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=None
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_21(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_22(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_23(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(None)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_24(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = None

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_25(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=None)

    return final_list_type.validate(dict_list)


def x_unify_and_validate_list_of_objects__mutmut_26(dict_list: list[dict[str, Any]]) -> CtyValue:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys = {key for key in all_keys if not all(key in item for item in dict_list)}

    unified_object_type = CtyObject(
        attribute_types=attribute_types, optional_attributes=frozenset(optional_keys)
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(None)

x_unify_and_validate_list_of_objects__mutmut_mutants : ClassVar[MutantDict] = {
'x_unify_and_validate_list_of_objects__mutmut_1': x_unify_and_validate_list_of_objects__mutmut_1, 
    'x_unify_and_validate_list_of_objects__mutmut_2': x_unify_and_validate_list_of_objects__mutmut_2, 
    'x_unify_and_validate_list_of_objects__mutmut_3': x_unify_and_validate_list_of_objects__mutmut_3, 
    'x_unify_and_validate_list_of_objects__mutmut_4': x_unify_and_validate_list_of_objects__mutmut_4, 
    'x_unify_and_validate_list_of_objects__mutmut_5': x_unify_and_validate_list_of_objects__mutmut_5, 
    'x_unify_and_validate_list_of_objects__mutmut_6': x_unify_and_validate_list_of_objects__mutmut_6, 
    'x_unify_and_validate_list_of_objects__mutmut_7': x_unify_and_validate_list_of_objects__mutmut_7, 
    'x_unify_and_validate_list_of_objects__mutmut_8': x_unify_and_validate_list_of_objects__mutmut_8, 
    'x_unify_and_validate_list_of_objects__mutmut_9': x_unify_and_validate_list_of_objects__mutmut_9, 
    'x_unify_and_validate_list_of_objects__mutmut_10': x_unify_and_validate_list_of_objects__mutmut_10, 
    'x_unify_and_validate_list_of_objects__mutmut_11': x_unify_and_validate_list_of_objects__mutmut_11, 
    'x_unify_and_validate_list_of_objects__mutmut_12': x_unify_and_validate_list_of_objects__mutmut_12, 
    'x_unify_and_validate_list_of_objects__mutmut_13': x_unify_and_validate_list_of_objects__mutmut_13, 
    'x_unify_and_validate_list_of_objects__mutmut_14': x_unify_and_validate_list_of_objects__mutmut_14, 
    'x_unify_and_validate_list_of_objects__mutmut_15': x_unify_and_validate_list_of_objects__mutmut_15, 
    'x_unify_and_validate_list_of_objects__mutmut_16': x_unify_and_validate_list_of_objects__mutmut_16, 
    'x_unify_and_validate_list_of_objects__mutmut_17': x_unify_and_validate_list_of_objects__mutmut_17, 
    'x_unify_and_validate_list_of_objects__mutmut_18': x_unify_and_validate_list_of_objects__mutmut_18, 
    'x_unify_and_validate_list_of_objects__mutmut_19': x_unify_and_validate_list_of_objects__mutmut_19, 
    'x_unify_and_validate_list_of_objects__mutmut_20': x_unify_and_validate_list_of_objects__mutmut_20, 
    'x_unify_and_validate_list_of_objects__mutmut_21': x_unify_and_validate_list_of_objects__mutmut_21, 
    'x_unify_and_validate_list_of_objects__mutmut_22': x_unify_and_validate_list_of_objects__mutmut_22, 
    'x_unify_and_validate_list_of_objects__mutmut_23': x_unify_and_validate_list_of_objects__mutmut_23, 
    'x_unify_and_validate_list_of_objects__mutmut_24': x_unify_and_validate_list_of_objects__mutmut_24, 
    'x_unify_and_validate_list_of_objects__mutmut_25': x_unify_and_validate_list_of_objects__mutmut_25, 
    'x_unify_and_validate_list_of_objects__mutmut_26': x_unify_and_validate_list_of_objects__mutmut_26
}

def unify_and_validate_list_of_objects(*args, **kwargs):
    result = _mutmut_trampoline(x_unify_and_validate_list_of_objects__mutmut_orig, x_unify_and_validate_list_of_objects__mutmut_mutants, args, kwargs)
    return result 

unify_and_validate_list_of_objects.__signature__ = _mutmut_signature(x_unify_and_validate_list_of_objects__mutmut_orig)
x_unify_and_validate_list_of_objects__mutmut_orig.__name__ = 'x_unify_and_validate_list_of_objects'
