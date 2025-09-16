from collections.abc import Callable

from provide.foundation import logger


def register_data_source(name: str, component_of: str | None = None) -> Callable[[type], type]:
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
