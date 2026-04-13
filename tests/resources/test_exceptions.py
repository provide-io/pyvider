#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Never

import pytest

from pyvider.resources.exceptions import (
    ResourceError,
    ResourceNotFoundError,
    ResourceOperationError,
    ResourceStateError,
    ResourceValidationError,
)


def test_resource_error() -> Never:
    with pytest.raises(ResourceError):
        raise ResourceError("test error")


def test_resource_not_found_error() -> Never:
    with pytest.raises(ResourceNotFoundError):
        raise ResourceNotFoundError("test not found error")


def test_resource_validation_error() -> Never:
    with pytest.raises(ResourceValidationError):
        raise ResourceValidationError("test validation error")


def test_resource_operation_error() -> Never:
    with pytest.raises(ResourceOperationError):
        raise ResourceOperationError("test operation error")


def test_resource_state_error() -> Never:
    with pytest.raises(ResourceStateError):
        raise ResourceStateError("test state error")


# 🐍🏗️🔚
