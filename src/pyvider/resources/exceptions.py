#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


# 🐍🏗️🔚
