import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

from pyvider.exceptions import ResourceError
from pyvider.hub import hub
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


def x_register_capability__mutmut_orig(name: str) -> Callable[[type], type]:
    """Decorator to register a capability class for discovery."""

    def decorator(cls: type) -> type:
        cls._is_registered_capability = True  # type: ignore
        cls._registered_name = name  # type: ignore
        return cls

    return decorator


def x_register_capability__mutmut_1(name: str) -> Callable[[type], type]:
    """Decorator to register a capability class for discovery."""

    def decorator(cls: type) -> type:
        cls._is_registered_capability = None  # type: ignore
        cls._registered_name = name  # type: ignore
        return cls

    return decorator


def x_register_capability__mutmut_2(name: str) -> Callable[[type], type]:
    """Decorator to register a capability class for discovery."""

    def decorator(cls: type) -> type:
        cls._is_registered_capability = False  # type: ignore
        cls._registered_name = name  # type: ignore
        return cls

    return decorator


def x_register_capability__mutmut_3(name: str) -> Callable[[type], type]:
    """Decorator to register a capability class for discovery."""

    def decorator(cls: type) -> type:
        cls._is_registered_capability = True  # type: ignore
        cls._registered_name = None  # type: ignore
        return cls

    return decorator

x_register_capability__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_capability__mutmut_1': x_register_capability__mutmut_1, 
    'x_register_capability__mutmut_2': x_register_capability__mutmut_2, 
    'x_register_capability__mutmut_3': x_register_capability__mutmut_3
}

def register_capability(*args, **kwargs):
    result = _mutmut_trampoline(x_register_capability__mutmut_orig, x_register_capability__mutmut_mutants, args, kwargs)
    return result 

register_capability.__signature__ = _mutmut_signature(x_register_capability__mutmut_orig)
x_register_capability__mutmut_orig.__name__ = 'x_register_capability'


def x_requires_capability__mutmut_orig(func: Callable) -> Callable:
    """
    Decorator that automatically injects a component's parent capability
    instance as a keyword argument into the decorated method.
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        component_instance = args[0]
        parent_capability_name = getattr(component_instance.__class__, "_parent_capability", "provider")

        # ctx = next((arg for arg in args if isinstance(arg, ResourceContext)), None)
        provider = hub.get_component("singleton", "provider")
        if not provider:
            raise ResourceError("Provider not available for capability injection.")

        if parent_capability_name == "provider":
            return await func(*args, **kwargs)

        capability_instance = hub.get_component("capability", parent_capability_name)
        if not capability_instance:
            raise ResourceError(f"Required parent capability '{parent_capability_name}' not found in context.")

        kwargs[parent_capability_name] = capability_instance
        return await func(*args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            parent_cap_name = getattr(func, "_parent_capability", "provider")

            provider = hub.get_component("singleton", "provider")
            if not provider:
                raise ResourceError("Provider not available for capability injection.")

            if parent_cap_name == "provider":
                return func(*args, **kwargs)

            capability_instance = hub.get_component("capability", parent_cap_name)
            if not capability_instance:
                raise ResourceError(f"Required parent capability '{parent_cap_name}' not found in context.")

            kwargs[parent_cap_name] = capability_instance
            return func(*args, **kwargs)

        return sync_wrapper


def x_requires_capability__mutmut_1(func: Callable) -> Callable:
    """
    Decorator that automatically injects a component's parent capability
    instance as a keyword argument into the decorated method.
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        component_instance = args[0]
        parent_capability_name = getattr(component_instance.__class__, "_parent_capability", "provider")

        # ctx = next((arg for arg in args if isinstance(arg, ResourceContext)), None)
        provider = hub.get_component("singleton", "provider")
        if not provider:
            raise ResourceError("Provider not available for capability injection.")

        if parent_capability_name == "provider":
            return await func(*args, **kwargs)

        capability_instance = hub.get_component("capability", parent_capability_name)
        if not capability_instance:
            raise ResourceError(f"Required parent capability '{parent_capability_name}' not found in context.")

        kwargs[parent_capability_name] = capability_instance
        return await func(*args, **kwargs)

    if asyncio.iscoroutinefunction(None):
        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            parent_cap_name = getattr(func, "_parent_capability", "provider")

            provider = hub.get_component("singleton", "provider")
            if not provider:
                raise ResourceError("Provider not available for capability injection.")

            if parent_cap_name == "provider":
                return func(*args, **kwargs)

            capability_instance = hub.get_component("capability", parent_cap_name)
            if not capability_instance:
                raise ResourceError(f"Required parent capability '{parent_cap_name}' not found in context.")

            kwargs[parent_cap_name] = capability_instance
            return func(*args, **kwargs)

        return sync_wrapper

x_requires_capability__mutmut_mutants : ClassVar[MutantDict] = {
'x_requires_capability__mutmut_1': x_requires_capability__mutmut_1
}

def requires_capability(*args, **kwargs):
    result = _mutmut_trampoline(x_requires_capability__mutmut_orig, x_requires_capability__mutmut_mutants, args, kwargs)
    return result 

requires_capability.__signature__ = _mutmut_signature(x_requires_capability__mutmut_orig)
x_requires_capability__mutmut_orig.__name__ = 'x_requires_capability'
