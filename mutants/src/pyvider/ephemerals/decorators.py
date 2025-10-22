#
# pyvider/ephemerals/decorators.py
#


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


def x_register_ephemeral_resource__mutmut_orig(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_1(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register(None, name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_2(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", None, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_3(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", name, None)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_4(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register(name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_5(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_6(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", name, )
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_7(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("XXephemeral_resourceXX", name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_8(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("EPHEMERAL_RESOURCE", name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


def x_register_ephemeral_resource__mutmut_9(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", name, cls)
        logger.debug(None)
        return cls

    return decorator

x_register_ephemeral_resource__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_ephemeral_resource__mutmut_1': x_register_ephemeral_resource__mutmut_1, 
    'x_register_ephemeral_resource__mutmut_2': x_register_ephemeral_resource__mutmut_2, 
    'x_register_ephemeral_resource__mutmut_3': x_register_ephemeral_resource__mutmut_3, 
    'x_register_ephemeral_resource__mutmut_4': x_register_ephemeral_resource__mutmut_4, 
    'x_register_ephemeral_resource__mutmut_5': x_register_ephemeral_resource__mutmut_5, 
    'x_register_ephemeral_resource__mutmut_6': x_register_ephemeral_resource__mutmut_6, 
    'x_register_ephemeral_resource__mutmut_7': x_register_ephemeral_resource__mutmut_7, 
    'x_register_ephemeral_resource__mutmut_8': x_register_ephemeral_resource__mutmut_8, 
    'x_register_ephemeral_resource__mutmut_9': x_register_ephemeral_resource__mutmut_9
}

def register_ephemeral_resource(*args, **kwargs):
    result = _mutmut_trampoline(x_register_ephemeral_resource__mutmut_orig, x_register_ephemeral_resource__mutmut_mutants, args, kwargs)
    return result 

register_ephemeral_resource.__signature__ = _mutmut_signature(x_register_ephemeral_resource__mutmut_orig)
x_register_ephemeral_resource__mutmut_orig.__name__ = 'x_register_ephemeral_resource'


# 🐍🏗️
