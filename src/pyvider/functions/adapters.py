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


def _get_cty_type_for_union(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    non_none_args = [arg for arg in args if arg is not type(None)]
    if set(non_none_args) <= {int, float, Decimal}:
        return CtyNumber()
    if len(non_none_args) == 1:
        return _python_type_to_cty_type(non_none_args[0])
    return CtyDynamic()


def _get_cty_type_for_list(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    element_type = _python_type_to_cty_type(args[0]) if args else CtyDynamic()
    return CtyList(element_type=element_type)


def _get_cty_type_for_dict(python_type: Any, args: tuple[Any, ...]) -> CtyType:
    value_type = _python_type_to_cty_type(args[1]) if len(args) > 1 else CtyDynamic()
    return CtyMap(element_type=value_type)


def _get_cty_type_for_primitive(python_type: type) -> CtyType | None:
    if issubclass(python_type, str):
        return CtyString()
    if issubclass(python_type, bool):
        return CtyBool()
    if issubclass(python_type, int | float | Decimal):
        return CtyNumber()
    return None


def _is_union_type(annotation: Any) -> bool:
    origin = get_origin(annotation)
    is_union = origin is UnionType
    try:
        from typing import Union

        is_union = is_union or origin is Union
    except ImportError:
        pass
    return is_union


def _is_list_type(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (list, list) or annotation is list


def _is_dict_type(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (dict, dict) or annotation is dict


def _python_type_to_cty_type(python_type: Any) -> CtyType:
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


def _is_optional_type_hint(annotation: Any) -> bool:
    return _is_union_type(annotation) and type(None) in get_args(annotation)


def _extract_parameters_meta(
    func_obj: Callable, sig: inspect.Signature, type_hints: dict[str, Any]
) -> list[dict[str, Any]]:
    parameters = []
    param_descriptions = getattr(func_obj, "_function_metadata", {}).get("param_descriptions", {})
    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY or name == "self":
            continue
        param_hint = type_hints.get(name, Any)
        parameters.append(
            {
                "name": name,
                "cty_type": _python_type_to_cty_type(param_hint),
                "description": param_descriptions.get(name, ""),
                "allow_null": _is_optional_type_hint(param_hint)
                or (param.default is not inspect.Parameter.empty),
            }
        )
    return parameters


def _extract_return_type_meta(type_hints: dict[str, Any]) -> dict[str, Any]:
    return_type_hint = type_hints.get("return", Any)
    return {"cty_type": _python_type_to_cty_type(return_type_hint)}


def _extract_docstring_meta(func_obj: Callable, base_meta: dict[str, Any]) -> None:
    docstring = inspect.getdoc(func_obj) or ""
    if not base_meta.get("summary") and docstring:
        base_meta["summary"] = docstring.strip().split("\n", 1)[0]
    if not base_meta.get("description") and docstring:
        base_meta["description"] = docstring


def function_to_dict(func_obj: Callable[..., Any]) -> dict[str, Any]:
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

    base_meta["parameters"] = _extract_parameters_meta(func_obj, sig, type_hints)
    base_meta["return"] = _extract_return_type_meta(type_hints)
    _extract_docstring_meta(func_obj, base_meta)

    return base_meta
