# pyvider/src/pyvider/providers/decorators.py

from collections.abc import Callable

from provide.foundation import logger

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


def x_register_provider__mutmut_orig(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_1(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = None  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_2(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = False  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_3(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = None  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_4(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register(None, name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_5(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", None, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_6(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, None)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_7(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register(name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_8(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_9(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, )
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_10(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("XXproviderXX", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_11(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("PROVIDER", name, cls)
        logger.debug(f"Registered provider '{name}' via decorator.")
        return cls

    return decorator


def x_register_provider__mutmut_12(name: str) -> Callable[[type], type]:
    """Decorator to register a provider with a specific name."""

    def decorator(cls: type) -> type:
        # Attach metadata to the class for discovery purposes
        cls._is_registered_provider = True  # type: ignore
        cls._registered_name = name  # type: ignore

        # Register the provider class immediately
        hub.register("provider", name, cls)
        logger.debug(None)
        return cls

    return decorator

x_register_provider__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_provider__mutmut_1': x_register_provider__mutmut_1, 
    'x_register_provider__mutmut_2': x_register_provider__mutmut_2, 
    'x_register_provider__mutmut_3': x_register_provider__mutmut_3, 
    'x_register_provider__mutmut_4': x_register_provider__mutmut_4, 
    'x_register_provider__mutmut_5': x_register_provider__mutmut_5, 
    'x_register_provider__mutmut_6': x_register_provider__mutmut_6, 
    'x_register_provider__mutmut_7': x_register_provider__mutmut_7, 
    'x_register_provider__mutmut_8': x_register_provider__mutmut_8, 
    'x_register_provider__mutmut_9': x_register_provider__mutmut_9, 
    'x_register_provider__mutmut_10': x_register_provider__mutmut_10, 
    'x_register_provider__mutmut_11': x_register_provider__mutmut_11, 
    'x_register_provider__mutmut_12': x_register_provider__mutmut_12
}

def register_provider(*args, **kwargs):
    result = _mutmut_trampoline(x_register_provider__mutmut_orig, x_register_provider__mutmut_mutants, args, kwargs)
    return result 

register_provider.__signature__ = _mutmut_signature(x_register_provider__mutmut_orig)
x_register_provider__mutmut_orig.__name__ = 'x_register_provider'
