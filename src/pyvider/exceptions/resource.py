#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation.errors import (
    NotFoundError as FoundationNotFoundError,
    RuntimeError as FoundationRuntimeError,
    StateError as FoundationStateError,
)

from pyvider.exceptions.base import PluginError, PyviderValueError


class ResourceError(PluginError):
    """Base class for resource-related errors."""


class DataSourceError(ResourceError):
    """Errors specific to data source operations."""


class CapabilityError(PluginError):  # Or could be ResourceError if capabilities are tied to resources
    """Errors related to component capabilities."""


class ResourceValidationError(ResourceError, PyviderValueError):
    """Raised when resource configuration or state validation fails."""


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


class IncompleteResourceStateError(ResourceError):
    """
    Raised when a resource's returned state is missing an attribute its schema
    declares. Every non-write-only schema attribute must have a corresponding
    entry in the state a resource returns; a missing one means the resource's
    state class doesn't carry a field the schema promises, which is a bug in
    the resource implementation rather than something the caller did wrong.
    """

    def _default_code(self) -> str:
        return "INCOMPLETE_RESOURCE_STATE"


class StateClassMismatchError(ResourceError):
    """
    Raised when a resource's state or config class requires a field that its
    schema does not declare. Nothing on the wire can supply such a field, so
    every conversion of an incoming value into the class fails.

    This is the mirror of `IncompleteResourceStateError`: that one catches a
    schema attribute the class does not carry, this one catches a class field
    the schema does not promise. Both are bugs in the component rather than
    something the practitioner did wrong, and `assert_schema_state_parity`
    catches both in the component author's own test suite.

    It is raised rather than reported as a missing value because the converted
    instance is used as a control signal: `BaseResource.apply` reads a missing
    planned state as "Terraform asked for a destroy", so answering a mismatch
    with None once destroyed live resources during an update.
    """

    def _default_code(self) -> str:
        return "STATE_CLASS_MISMATCH"


# 🐍🏗️🔚
