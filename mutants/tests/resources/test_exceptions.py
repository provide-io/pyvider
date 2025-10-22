import pytest

from pyvider.resources.exceptions import (
    ResourceError,
    ResourceNotFoundError,
    ResourceOperationError,
    ResourceStateError,
    ResourceValidationError,
)


def test_resource_error():
    with pytest.raises(ResourceError):
        raise ResourceError("test error")


def test_resource_not_found_error():
    with pytest.raises(ResourceNotFoundError):
        raise ResourceNotFoundError("test not found error")


def test_resource_validation_error():
    with pytest.raises(ResourceValidationError):
        raise ResourceValidationError("test validation error")


def test_resource_operation_error():
    with pytest.raises(ResourceOperationError):
        raise ResourceOperationError("test operation error")


def test_resource_state_error():
    with pytest.raises(ResourceStateError):
        raise ResourceStateError("test state error")
