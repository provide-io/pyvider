#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    RuntimeError as FoundationRuntimeError,
)

from pyvider.exceptions.base import ComponentConfigurationError


class ProviderError(FoundationConfigurationError):
    """Base class for provider-specific errors."""

    def _default_code(self) -> str:
        return "PROVIDER_ERROR"


class ProviderConfigurationError(ProviderError, ComponentConfigurationError):
    """Raised when provider configuration is invalid."""

    pass


class ProviderInitializationError(FoundationRuntimeError):
    """Raised when provider initialization fails."""

    def _default_code(self) -> str:
        return "PROVIDER_INITIALIZATION_ERROR"


# 🐍🏗️🔚
