from collections.abc import Callable

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


def x_register_data_source__mutmut_orig(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_1(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = None  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_2(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = False  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_3(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = None  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_4(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = None  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_5(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(None, capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_6(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", capability=None)
        return cls

    return decorator


def x_register_data_source__mutmut_7(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(capability=component_of)
        return cls

    return decorator


def x_register_data_source__mutmut_8(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"📊 Marked data source '{name}' for discovery", )
        return cls

    return decorator

x_register_data_source__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_data_source__mutmut_1': x_register_data_source__mutmut_1, 
    'x_register_data_source__mutmut_2': x_register_data_source__mutmut_2, 
    'x_register_data_source__mutmut_3': x_register_data_source__mutmut_3, 
    'x_register_data_source__mutmut_4': x_register_data_source__mutmut_4, 
    'x_register_data_source__mutmut_5': x_register_data_source__mutmut_5, 
    'x_register_data_source__mutmut_6': x_register_data_source__mutmut_6, 
    'x_register_data_source__mutmut_7': x_register_data_source__mutmut_7, 
    'x_register_data_source__mutmut_8': x_register_data_source__mutmut_8
}

def register_data_source(*args, **kwargs):
    result = _mutmut_trampoline(x_register_data_source__mutmut_orig, x_register_data_source__mutmut_mutants, args, kwargs)
    return result 

register_data_source.__signature__ = _mutmut_signature(x_register_data_source__mutmut_orig)
x_register_data_source__mutmut_orig.__name__ = 'x_register_data_source'
