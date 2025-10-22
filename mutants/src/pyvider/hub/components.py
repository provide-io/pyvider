from collections.abc import Callable
from typing import Any

from provide.foundation import Registry, logger

from pyvider.exceptions import ComponentRegistryError
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


class ComponentRegistry:
    """
    Multi-dimensional registry for managing components by type and name.

    Uses provide.foundation's Registry for thread-safe operations.
    """

    def xǁComponentRegistryǁ__init____mutmut_orig(self) -> None:
        """Initialize with foundation's Registry."""
        self._registry = Registry()

    def xǁComponentRegistryǁ__init____mutmut_1(self) -> None:
        """Initialize with foundation's Registry."""
        self._registry = None
    
    xǁComponentRegistryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁ__init____mutmut_1': xǁComponentRegistryǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁComponentRegistryǁ__init____mutmut_orig)
    xǁComponentRegistryǁ__init____mutmut_orig.__name__ = 'xǁComponentRegistryǁ__init__'

    def xǁComponentRegistryǁregister__mutmut_orig(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_1(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = None
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_2(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(None, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_3(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=None)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_4(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_5(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, )
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_6(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is not component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_7(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(None)
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_8(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_9(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(None)

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_10(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=None, value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_11(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=None, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_12(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=None, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_13(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=None)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_14(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(value=component, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_15(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, dimension=component_type, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_16(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, replace=True)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_17(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, )
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_18(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=False)
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁregister__mutmut_19(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug(f"Skipping redundant registration: {component_type}.{name}")
            return
        elif existing is not None:
            logger.warning(f"Component '{name}' under type '{component_type}' is being replaced.")

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug(None)
    
    xǁComponentRegistryǁregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁregister__mutmut_1': xǁComponentRegistryǁregister__mutmut_1, 
        'xǁComponentRegistryǁregister__mutmut_2': xǁComponentRegistryǁregister__mutmut_2, 
        'xǁComponentRegistryǁregister__mutmut_3': xǁComponentRegistryǁregister__mutmut_3, 
        'xǁComponentRegistryǁregister__mutmut_4': xǁComponentRegistryǁregister__mutmut_4, 
        'xǁComponentRegistryǁregister__mutmut_5': xǁComponentRegistryǁregister__mutmut_5, 
        'xǁComponentRegistryǁregister__mutmut_6': xǁComponentRegistryǁregister__mutmut_6, 
        'xǁComponentRegistryǁregister__mutmut_7': xǁComponentRegistryǁregister__mutmut_7, 
        'xǁComponentRegistryǁregister__mutmut_8': xǁComponentRegistryǁregister__mutmut_8, 
        'xǁComponentRegistryǁregister__mutmut_9': xǁComponentRegistryǁregister__mutmut_9, 
        'xǁComponentRegistryǁregister__mutmut_10': xǁComponentRegistryǁregister__mutmut_10, 
        'xǁComponentRegistryǁregister__mutmut_11': xǁComponentRegistryǁregister__mutmut_11, 
        'xǁComponentRegistryǁregister__mutmut_12': xǁComponentRegistryǁregister__mutmut_12, 
        'xǁComponentRegistryǁregister__mutmut_13': xǁComponentRegistryǁregister__mutmut_13, 
        'xǁComponentRegistryǁregister__mutmut_14': xǁComponentRegistryǁregister__mutmut_14, 
        'xǁComponentRegistryǁregister__mutmut_15': xǁComponentRegistryǁregister__mutmut_15, 
        'xǁComponentRegistryǁregister__mutmut_16': xǁComponentRegistryǁregister__mutmut_16, 
        'xǁComponentRegistryǁregister__mutmut_17': xǁComponentRegistryǁregister__mutmut_17, 
        'xǁComponentRegistryǁregister__mutmut_18': xǁComponentRegistryǁregister__mutmut_18, 
        'xǁComponentRegistryǁregister__mutmut_19': xǁComponentRegistryǁregister__mutmut_19
    }
    
    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁregister__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register.__signature__ = _mutmut_signature(xǁComponentRegistryǁregister__mutmut_orig)
    xǁComponentRegistryǁregister__mutmut_orig.__name__ = 'xǁComponentRegistryǁregister'

    def xǁComponentRegistryǁunregister__mutmut_orig(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_1(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_2(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(None, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_3(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=None):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_4(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_5(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, ):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_6(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(None)
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def xǁComponentRegistryǁunregister__mutmut_7(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(None)
    
    xǁComponentRegistryǁunregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁunregister__mutmut_1': xǁComponentRegistryǁunregister__mutmut_1, 
        'xǁComponentRegistryǁunregister__mutmut_2': xǁComponentRegistryǁunregister__mutmut_2, 
        'xǁComponentRegistryǁunregister__mutmut_3': xǁComponentRegistryǁunregister__mutmut_3, 
        'xǁComponentRegistryǁunregister__mutmut_4': xǁComponentRegistryǁunregister__mutmut_4, 
        'xǁComponentRegistryǁunregister__mutmut_5': xǁComponentRegistryǁunregister__mutmut_5, 
        'xǁComponentRegistryǁunregister__mutmut_6': xǁComponentRegistryǁunregister__mutmut_6, 
        'xǁComponentRegistryǁunregister__mutmut_7': xǁComponentRegistryǁunregister__mutmut_7
    }
    
    def unregister(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁunregister__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁunregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    unregister.__signature__ = _mutmut_signature(xǁComponentRegistryǁunregister__mutmut_orig)
    xǁComponentRegistryǁunregister__mutmut_orig.__name__ = 'xǁComponentRegistryǁunregister'

    def xǁComponentRegistryǁget_component__mutmut_orig(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self._registry.get(name, dimension=component_type)

    def xǁComponentRegistryǁget_component__mutmut_1(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self._registry.get(None, dimension=component_type)

    def xǁComponentRegistryǁget_component__mutmut_2(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self._registry.get(name, dimension=None)

    def xǁComponentRegistryǁget_component__mutmut_3(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self._registry.get(dimension=component_type)

    def xǁComponentRegistryǁget_component__mutmut_4(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self._registry.get(name, )
    
    xǁComponentRegistryǁget_component__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁget_component__mutmut_1': xǁComponentRegistryǁget_component__mutmut_1, 
        'xǁComponentRegistryǁget_component__mutmut_2': xǁComponentRegistryǁget_component__mutmut_2, 
        'xǁComponentRegistryǁget_component__mutmut_3': xǁComponentRegistryǁget_component__mutmut_3, 
        'xǁComponentRegistryǁget_component__mutmut_4': xǁComponentRegistryǁget_component__mutmut_4
    }
    
    def get_component(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁget_component__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁget_component__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_component.__signature__ = _mutmut_signature(xǁComponentRegistryǁget_component__mutmut_orig)
    xǁComponentRegistryǁget_component__mutmut_orig.__name__ = 'xǁComponentRegistryǁget_component'

    def xǁComponentRegistryǁget_components__mutmut_orig(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(name, dimension=component_type) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_1(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = None
        return {name: self._registry.get(name, dimension=component_type) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_2(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(None)
        return {name: self._registry.get(name, dimension=component_type) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_3(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(None, dimension=component_type) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_4(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(name, dimension=None) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_5(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(dimension=component_type) for name in component_names}

    def xǁComponentRegistryǁget_components__mutmut_6(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(name, ) for name in component_names}
    
    xǁComponentRegistryǁget_components__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁget_components__mutmut_1': xǁComponentRegistryǁget_components__mutmut_1, 
        'xǁComponentRegistryǁget_components__mutmut_2': xǁComponentRegistryǁget_components__mutmut_2, 
        'xǁComponentRegistryǁget_components__mutmut_3': xǁComponentRegistryǁget_components__mutmut_3, 
        'xǁComponentRegistryǁget_components__mutmut_4': xǁComponentRegistryǁget_components__mutmut_4, 
        'xǁComponentRegistryǁget_components__mutmut_5': xǁComponentRegistryǁget_components__mutmut_5, 
        'xǁComponentRegistryǁget_components__mutmut_6': xǁComponentRegistryǁget_components__mutmut_6
    }
    
    def get_components(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁget_components__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁget_components__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_components.__signature__ = _mutmut_signature(xǁComponentRegistryǁget_components__mutmut_orig)
    xǁComponentRegistryǁget_components__mutmut_orig.__name__ = 'xǁComponentRegistryǁget_components'

    def xǁComponentRegistryǁlist_components__mutmut_orig(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=dimension) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_1(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = None
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=dimension) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_2(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = None
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=dimension) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_3(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = None
        return result

    def xǁComponentRegistryǁlist_components__mutmut_4(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(None, dimension=dimension) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_5(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=None) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_6(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(dimension=dimension) for name in names}
        return result

    def xǁComponentRegistryǁlist_components__mutmut_7(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, ) for name in names}
        return result
    
    xǁComponentRegistryǁlist_components__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryǁlist_components__mutmut_1': xǁComponentRegistryǁlist_components__mutmut_1, 
        'xǁComponentRegistryǁlist_components__mutmut_2': xǁComponentRegistryǁlist_components__mutmut_2, 
        'xǁComponentRegistryǁlist_components__mutmut_3': xǁComponentRegistryǁlist_components__mutmut_3, 
        'xǁComponentRegistryǁlist_components__mutmut_4': xǁComponentRegistryǁlist_components__mutmut_4, 
        'xǁComponentRegistryǁlist_components__mutmut_5': xǁComponentRegistryǁlist_components__mutmut_5, 
        'xǁComponentRegistryǁlist_components__mutmut_6': xǁComponentRegistryǁlist_components__mutmut_6, 
        'xǁComponentRegistryǁlist_components__mutmut_7': xǁComponentRegistryǁlist_components__mutmut_7
    }
    
    def list_components(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryǁlist_components__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryǁlist_components__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_components.__signature__ = _mutmut_signature(xǁComponentRegistryǁlist_components__mutmut_orig)
    xǁComponentRegistryǁlist_components__mutmut_orig.__name__ = 'xǁComponentRegistryǁlist_components'


# Singleton instance
registry = ComponentRegistry()


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_orig() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_1() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = None

    return {
        "total_component_types": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_2() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "XXtotal_component_typesXX": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_3() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "TOTAL_COMPONENT_TYPES": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_4() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "XXtotal_componentsXX": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_5() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "TOTAL_COMPONENTS": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_6() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "total_components": sum(None),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_7() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "XXcomponent_breakdownXX": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# New diagnostics function, living with the data it reports on.
def x_get_hub_diagnostics__mutmut_8() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "COMPONENT_BREAKDOWN": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }

x_get_hub_diagnostics__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_hub_diagnostics__mutmut_1': x_get_hub_diagnostics__mutmut_1, 
    'x_get_hub_diagnostics__mutmut_2': x_get_hub_diagnostics__mutmut_2, 
    'x_get_hub_diagnostics__mutmut_3': x_get_hub_diagnostics__mutmut_3, 
    'x_get_hub_diagnostics__mutmut_4': x_get_hub_diagnostics__mutmut_4, 
    'x_get_hub_diagnostics__mutmut_5': x_get_hub_diagnostics__mutmut_5, 
    'x_get_hub_diagnostics__mutmut_6': x_get_hub_diagnostics__mutmut_6, 
    'x_get_hub_diagnostics__mutmut_7': x_get_hub_diagnostics__mutmut_7, 
    'x_get_hub_diagnostics__mutmut_8': x_get_hub_diagnostics__mutmut_8
}

def get_hub_diagnostics(*args, **kwargs):
    result = _mutmut_trampoline(x_get_hub_diagnostics__mutmut_orig, x_get_hub_diagnostics__mutmut_mutants, args, kwargs)
    return result 

get_hub_diagnostics.__signature__ = _mutmut_signature(x_get_hub_diagnostics__mutmut_orig)
x_get_hub_diagnostics__mutmut_orig.__name__ = 'x_get_hub_diagnostics'
