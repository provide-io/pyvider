#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from provide.foundation.errors import (
    NotFoundError as FoundationNotFoundError,
    RuntimeError as FoundationRuntimeError,
    StateError as FoundationStateError,
)

from pyvider.exceptions.base import PluginError, PyviderValueError


class ResourceError(PluginError):
    """Base class for resource-related errors."""

    pass


class DataSourceError(ResourceError):
    """Errors specific to data source operations."""

    pass


class CapabilityError(PluginError):  # Or could be ResourceError if capabilities are tied to resources
    """Errors related to component capabilities."""

    pass


class ResourceValidationError(ResourceError, PyviderValueError):
    """Raised when resource configuration or state validation fails."""

    pass


class ResourceNotFoundError(FoundationNotFoundError):
    """Raised when a resource cannot be found."""

    def _default_code(self) -> str:
        return "RESOURCE_NOT_FOUND"


class ResourceOperationError(FoundationRuntimeError):
    """Raised for errors during resource lifecycle operations (plan, apply, etc.)."""

    def _default_code(self) -> str:
        return "RESOURCE_OPERATION_ERROR"


class ResourceLifecycleContractError(FoundationStateError):
    """
    Raised when the state returned by apply() differs from the planned state.
    This indicates a bug in the resource implementation where the outcome of an
    apply operation did not match its proposed plan.
    """

    def __init__(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "RESOURCE_LIFECYCLE_CONTRACT_ERROR"


# 🐍🏗️🔚
