#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal, overload

from provide.foundation import Registry, logger

from pyvider.exceptions import ComponentRegistryError

if TYPE_CHECKING:
    from pyvider.capabilities.base import BaseCapability
    from pyvider.cli.context import PyviderContext
    from pyvider.data_sources.base import BaseDataSource
    from pyvider.ephemerals.base import BaseEphemeralResource
    from pyvider.providers.base import BaseProvider
    from pyvider.providers.context import ProviderContext
    from pyvider.resources.base import BaseResource


class ComponentRegistry:
    """
    Multi-dimensional registry for managing components by type and name.

    Uses provide.foundation's Registry for thread-safe operations.
    """

    def __init__(self) -> None:
        """Initialize with foundation's Registry."""
        self._registry = Registry()

    def register(self, component_type: str, name: str, component: Any) -> None:
        """Registers a component under a specific type and name."""
        # Check if already registered
        existing = self._registry.get(name, dimension=component_type)
        if existing is component:
            logger.debug("Skipping redundant registration", component_type=component_type, name=name)
            return
        elif existing is not None:
            logger.warning("Component is being replaced", component_type=component_type, name=name)

        # Register with replace=True to allow overwrites
        self._registry.register(name=name, value=component, dimension=component_type, replace=True)
        logger.debug("Registered component", component_type=component_type, name=name)

    def unregister(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug("Unregistered component", component_type=component_type, name=name)

    # Singleton overloads - fixed names with specific return types
    @overload
    def get_component(
        self, component_type: Literal["singleton"], name: Literal["provider"]
    ) -> "BaseProvider | None": ...

    @overload
    def get_component(
        self, component_type: Literal["singleton"], name: Literal["provider_context"]
    ) -> "ProviderContext | PyviderContext | Callable[[], ProviderContext] | None": ...

    @overload
    def get_component(
        self, component_type: Literal["singleton"], name: Literal["rpc_plugin_server"]
    ) -> "Callable[[], Any] | None": ...

    # Generic singleton fallback
    @overload
    def get_component(self, component_type: Literal["singleton"], name: str) -> Any | None: ...

    # Component class lookups - dynamic names, return class types
    @overload
    def get_component(self, component_type: Literal["provider"], name: str) -> "type[BaseProvider] | None": ...

    @overload
    def get_component(
        self, component_type: Literal["resource"], name: str
    ) -> "type[BaseResource[Any, Any, Any, Any]] | None": ...

    @overload
    def get_component(
        self, component_type: Literal["data_source"], name: str
    ) -> "type[BaseDataSource[Any, Any, Any]] | None": ...

    @overload
    def get_component(self, component_type: Literal["function"], name: str) -> Callable[..., Any] | None: ...

    @overload
    def get_component(
        self, component_type: Literal["capability"], name: str
    ) -> "type[BaseCapability] | None": ...

    @overload
    def get_component(
        self, component_type: Literal["ephemeral_resource"], name: str
    ) -> "type[BaseEphemeralResource[Any, Any, Any]] | None": ...

    # Generic fallback for unknown component types
    @overload
    def get_component(self, component_type: str, name: str) -> Any | None: ...

    def get_component(self, component_type: str, name: str) -> Any | None:
        """Retrieves a component by type and name."""
        return self._registry.get(name, dimension=component_type)

    # Overloads for get_components - return proper types for each component type
    @overload
    def get_components(self, component_type: Literal["provider"]) -> "dict[str, type[BaseProvider]]": ...

    @overload
    def get_components(
        self, component_type: Literal["resource"]
    ) -> "dict[str, type[BaseResource[Any, Any, Any, Any]]]": ...

    @overload
    def get_components(
        self, component_type: Literal["data_source"]
    ) -> "dict[str, type[BaseDataSource[Any, Any, Any]]]": ...

    @overload
    def get_components(self, component_type: Literal["function"]) -> dict[str, Callable[..., Any]]: ...

    @overload
    def get_components(self, component_type: Literal["capability"]) -> "dict[str, type[BaseCapability]]": ...

    @overload
    def get_components(
        self, component_type: Literal["ephemeral_resource"]
    ) -> "dict[str, type[BaseEphemeralResource[Any, Any, Any]]]": ...

    # Generic fallback
    @overload
    def get_components(self, component_type: str) -> dict[str, Any]: ...

    def get_components(self, component_type: str) -> dict[str, Any]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(name, dimension=component_type) for name in component_names}

    def list_components(self) -> dict[str, dict[str, Any]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=dimension) for name in names}
        return result


# Singleton instance
registry = ComponentRegistry()


# New diagnostics function, living with the data it reports on.
def get_hub_diagnostics() -> dict[str, Any]:
    """
    Get diagnostic information about the component hub's state.
    """
    components = registry.list_components()

    return {
        "total_component_types": len(components),
        "total_components": sum(len(comp_dict) for comp_dict in components.values()),
        "component_breakdown": {comp_type: len(comp_dict) for comp_type, comp_dict in components.items()},
    }


# 🐍🏗️🔚
