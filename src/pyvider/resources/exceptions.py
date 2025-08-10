#
# pyvider/resources/exceptions.py
#

from pyvider.exceptions import PyviderError


class ResourceError(PyviderError):
    """Base class for resource-related errors."""


class ResourceNotFoundError(ResourceError):
    """Raised when a resource cannot be found."""


class ResourceValidationError(ResourceError):
    """Raised when resource validation fails."""


class ResourceOperationError(ResourceError):
    """Raised when a resource operation fails."""


class ResourceStateError(ResourceError):
    """Raised when resource state is invalid."""


# 🐍🏗️
