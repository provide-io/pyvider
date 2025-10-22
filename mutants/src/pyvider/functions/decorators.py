from collections.abc import Callable
from typing import Any

from provide.foundation import logger
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


def x_register_function__mutmut_orig(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_1(
    name: str,
    component_of: str | None = None,
    summary: str = "XXXX",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_2(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "XXXX",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_3(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "XXXX",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_4(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = None  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_5(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = False  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_6(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = None  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_7(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = None  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_8(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = None
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_9(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "XXnameXX": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_10(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "NAME": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_11(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "XXtypeXX": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_12(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "TYPE": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_13(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "XXfunctionXX",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_14(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "FUNCTION",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_15(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "XXsummaryXX": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_16(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "SUMMARY": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_17(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "XXdescriptionXX": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_18(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "DESCRIPTION": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_19(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "XXparam_descriptionsXX": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_20(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "PARAM_DESCRIPTIONS": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_21(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions and {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_22(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "XXdeprecation_messageXX": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_23(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "DEPRECATION_MESSAGE": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_24(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "XXfunction_nameXX": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_25(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "FUNCTION_NAME": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_26(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "XXmoduleXX": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_27(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "MODULE": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_28(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "XXdiscovery_methodXX": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_29(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "DISCOVERY_METHOD": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_30(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "XXdecoratorXX",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_31(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "DECORATOR",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_32(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = None  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_33(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(None, capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_34(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", capability=None)
        return func

    return decorator


def x_register_function__mutmut_35(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(capability=component_of)
        return func

    return decorator


def x_register_function__mutmut_36(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(f"🧰 Marked function '{name}' for discovery", )
        return func

    return decorator

x_register_function__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_function__mutmut_1': x_register_function__mutmut_1, 
    'x_register_function__mutmut_2': x_register_function__mutmut_2, 
    'x_register_function__mutmut_3': x_register_function__mutmut_3, 
    'x_register_function__mutmut_4': x_register_function__mutmut_4, 
    'x_register_function__mutmut_5': x_register_function__mutmut_5, 
    'x_register_function__mutmut_6': x_register_function__mutmut_6, 
    'x_register_function__mutmut_7': x_register_function__mutmut_7, 
    'x_register_function__mutmut_8': x_register_function__mutmut_8, 
    'x_register_function__mutmut_9': x_register_function__mutmut_9, 
    'x_register_function__mutmut_10': x_register_function__mutmut_10, 
    'x_register_function__mutmut_11': x_register_function__mutmut_11, 
    'x_register_function__mutmut_12': x_register_function__mutmut_12, 
    'x_register_function__mutmut_13': x_register_function__mutmut_13, 
    'x_register_function__mutmut_14': x_register_function__mutmut_14, 
    'x_register_function__mutmut_15': x_register_function__mutmut_15, 
    'x_register_function__mutmut_16': x_register_function__mutmut_16, 
    'x_register_function__mutmut_17': x_register_function__mutmut_17, 
    'x_register_function__mutmut_18': x_register_function__mutmut_18, 
    'x_register_function__mutmut_19': x_register_function__mutmut_19, 
    'x_register_function__mutmut_20': x_register_function__mutmut_20, 
    'x_register_function__mutmut_21': x_register_function__mutmut_21, 
    'x_register_function__mutmut_22': x_register_function__mutmut_22, 
    'x_register_function__mutmut_23': x_register_function__mutmut_23, 
    'x_register_function__mutmut_24': x_register_function__mutmut_24, 
    'x_register_function__mutmut_25': x_register_function__mutmut_25, 
    'x_register_function__mutmut_26': x_register_function__mutmut_26, 
    'x_register_function__mutmut_27': x_register_function__mutmut_27, 
    'x_register_function__mutmut_28': x_register_function__mutmut_28, 
    'x_register_function__mutmut_29': x_register_function__mutmut_29, 
    'x_register_function__mutmut_30': x_register_function__mutmut_30, 
    'x_register_function__mutmut_31': x_register_function__mutmut_31, 
    'x_register_function__mutmut_32': x_register_function__mutmut_32, 
    'x_register_function__mutmut_33': x_register_function__mutmut_33, 
    'x_register_function__mutmut_34': x_register_function__mutmut_34, 
    'x_register_function__mutmut_35': x_register_function__mutmut_35, 
    'x_register_function__mutmut_36': x_register_function__mutmut_36
}

def register_function(*args, **kwargs):
    result = _mutmut_trampoline(x_register_function__mutmut_orig, x_register_function__mutmut_mutants, args, kwargs)
    return result 

register_function.__signature__ = _mutmut_signature(x_register_function__mutmut_orig)
x_register_function__mutmut_orig.__name__ = 'x_register_function'
