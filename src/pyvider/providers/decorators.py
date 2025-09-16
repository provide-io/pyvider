# pyvider/src/pyvider/providers/decorators.py

from collections.abc import Callable

from provide.foundation import logger

from pyvider.hub import hub


def register_provider(name: str) -> Callable[[type], type]:
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
