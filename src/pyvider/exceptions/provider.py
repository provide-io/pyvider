# pyvider/exceptions/provider.py
from .base import ComponentConfigurationError, PluginError


class ProviderError(PluginError):
    """Base class for provider-specific errors."""

    pass


class ProviderConfigurationError(ProviderError, ComponentConfigurationError):
    """Raised when provider configuration is invalid."""

    pass


class ProviderInitializationError(ProviderError):
    """Raised when provider initialization fails."""

    pass
