# pyvider/exceptions/provider.py
from provide.foundation.errors import ConfigurationError as FoundationConfigurationError
from provide.foundation.errors import InitializationError as FoundationInitializationError
from pyvider.exceptions.base import ComponentConfigurationError, PluginError


class ProviderError(FoundationConfigurationError):
    """Base class for provider-specific errors."""

    def _default_code(self) -> str:
        return "PROVIDER_ERROR"


class ProviderConfigurationError(ProviderError, ComponentConfigurationError):
    """Raised when provider configuration is invalid."""

    pass


class ProviderInitializationError(FoundationInitializationError):
    """Raised when provider initialization fails."""

    def _default_code(self) -> str:
        return "PROVIDER_INITIALIZATION_ERROR"
