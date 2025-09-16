from collections.abc import Callable
from typing import ParamSpec, TypeVar

from provide.foundation import logger

P = ParamSpec("P")
T = TypeVar("T")


def register_resource(name: str, component_of: str | None = None) -> Callable[[type], type]:
    """
    Decorator to register a resource and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_resource = True  # type: ignore
        cls._registered_name = name
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(f"🔧 Marked resource '{name}' for discovery", capability=component_of)
        return cls

    return decorator
