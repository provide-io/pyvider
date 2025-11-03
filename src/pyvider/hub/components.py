#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable
from typing import Any

from provide.foundation import Registry, logger

from pyvider.exceptions import ComponentRegistryError


class ComponentRegistry:
    """
    Multi-dimensional registry for managing components by type and name.

    Uses provide.foundation's Registry for thread-safe operations.
    """

    def __init__(self) -> None:
        """Initialize with foundation's Registry."""
        self._registry = Registry()

    def register(self, component_type: str, name: str, component: Callable[..., Any]) -> None:
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

    def unregister(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if not self._registry.remove(name, dimension=component_type):
            raise ComponentRegistryError(f"Component '{name}' under type '{component_type}' does not exist.")
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def get_component(self, component_type: str, name: str) -> Callable[..., Any] | None:
        """Retrieves a component by type and name."""
        return self._registry.get(name, dimension=component_type)

    def get_components(self, component_type: str) -> dict[str, Callable[..., Any]]:
        """Get all components of a specific type."""
        component_names = self._registry.list_dimension(component_type)
        return {name: self._registry.get(name, dimension=component_type) for name in component_names}  # type: ignore[misc]

    def list_components(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        all_dimensions = self._registry.list_all()
        result = {}
        for dimension, names in all_dimensions.items():
            result[dimension] = {name: self._registry.get(name, dimension=dimension) for name in names}
        return result  # type: ignore[return-value]


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
