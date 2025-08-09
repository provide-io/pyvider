#
# pyvider/hub/components.py
#
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pyvider.exceptions import ComponentRegistryError
from pyvider.telemetry import logger


@dataclass
class ComponentRegistry:
    """
    Multi-dimensional registry for managing components by type and name.
    """

    registry: dict[str, dict[str, Callable]] = field(default_factory=dict)

    def register(self, component_type: str, name: str, component: Callable) -> None:
        """Registers a component under a specific type and name."""
        if component_type not in self.registry:
            self.registry[component_type] = {}

        if name in self.registry[component_type]:
            existing_component = self.registry[component_type][name]
            if existing_component is component:
                logger.debug(
                    f"Skipping redundant registration: {component_type}.{name}"
                )
                return
            else:
                logger.warning(
                    f"Component '{name}' under type '{component_type}' is being replaced."
                )

        self.registry[component_type][name] = component
        logger.debug(f"Registered component: type='{component_type}', name='{name}'")

    def unregister(self, component_type: str, name: str) -> None:
        """Unregisters a component by type and name."""
        if (
            component_type not in self.registry
            or name not in self.registry[component_type]
        ):
            raise ComponentRegistryError(
                f"Component '{name}' under type '{component_type}' does not exist."
            )

        del self.registry[component_type][name]
        if not self.registry[component_type]:
            del self.registry[component_type]
        logger.debug(f"Unregistered component: type='{component_type}', name='{name}'")

    def get_component(self, component_type: str, name: str) -> Callable | None:
        """Retrieves a component by type and name."""
        return self.registry.get(component_type, {}).get(name)

    def get_components(self, component_type: str) -> dict[str, Callable]:
        """Get all components of a specific type."""
        return self.registry.get(component_type, {})

    def list_components(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """Lists all registered components."""
        return self.registry


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
        "component_breakdown": {
            comp_type: len(comp_dict) for comp_type, comp_dict in components.items()
        },
    }


# 🐍🏗️📄🪄
