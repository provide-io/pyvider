#
# pyvider/exceptions/resource.py
#
from .base import PluginError, PyviderValueError


class ResourceError(PluginError):
    """Base class for resource-related errors."""

    pass


class DataSourceError(ResourceError):
    """Errors specific to data source operations."""

    pass


class CapabilityError(
    PluginError
):  # Or could be ResourceError if capabilities are tied to resources
    """Errors related to component capabilities."""

    pass


class ResourceValidationError(ResourceError, PyviderValueError):
    """Raised when resource configuration or state validation fails."""

    pass


class ResourceNotFoundError(ResourceError):
    """Raised when a resource cannot be found."""

    pass


class ResourceOperationError(ResourceError):
    """Raised for errors during resource lifecycle operations (plan, apply, etc.)."""

    pass


class ResourceLifecycleContractError(ResourceError):
    """
    Raised when the state returned by apply() differs from the planned state.
    This indicates a bug in the resource implementation where the outcome of an
    apply operation did not match its proposed plan.
    """

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        self.detail = detail
        super().__init__(message)


# 🐍🏗️📄🪄
