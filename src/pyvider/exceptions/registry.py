#
# pyvider/exceptions/registry.py
#
from .base import FrameworkConfigurationError


class ComponentRegistryError(FrameworkConfigurationError):
    """Raised for errors during component registration or retrieval."""

    pass


class ValidatorRegistrationError(ComponentRegistryError):
    """Raised when a non-callable is registered as a validator, or other validator issues."""

    pass


# 🐍🏗️📄🪄
