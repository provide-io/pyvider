from collections.abc import Callable

from provide.foundation import logger


def register_data_source(
    name: str, component_of: str | None = None, test_only: bool = False
) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        cls._is_test_only = test_only  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(
            f"📊 Marked data source '{name}' for discovery",
            capability=component_of,
            test_only=test_only,
        )
        return cls

    return decorator
