#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for hub validators."""

from typing import Any

from provide.foundation.config import ConfigValidationError
import pytest

from pyvider.hub.validators import Validators


@pytest.fixture(autouse=True)
def reset_validators() -> None:
    """Reset the validator registry before each test."""
    Validators._registry.clear()
    yield
    Validators._registry.clear()


def test_register_validator() -> None:
    """Test registering a validator."""

    @Validators.register("test_validator")
    def my_validator(value: Any, metadata: Any) -> None:
        if not isinstance(value, str):
            raise ValueError("Value must be a string")

    assert "test_validator" in Validators._registry
    assert Validators._registry["test_validator"] == my_validator


def test_register_multiple_validators() -> None:
    """Test registering multiple validators."""

    @Validators.register("validator_1")
    def validator_1(value: Any, metadata: Any) -> None:
        pass

    @Validators.register("validator_2")
    def validator_2(value: Any, metadata: Any) -> None:
        pass

    assert "validator_1" in Validators._registry
    assert "validator_2" in Validators._registry
    assert len(Validators._registry) == 2


def test_attach_validator_to_metadata() -> None:
    """Test attaching validators to metadata."""

    @Validators.register("length_check")
    def length_check(value: Any, metadata: Any) -> None:
        pass

    class MockMetadata:
        def __init__(self) -> None:
            self.validators = []
            self.description = "test attribute"

    metadata = MockMetadata()
    Validators.attach(metadata, "length_check")

    assert len(metadata.validators) == 1
    assert metadata.validators[0] == length_check


def test_attach_multiple_validators_to_metadata() -> None:
    """Test attaching multiple validators to metadata."""

    @Validators.register("validator_a")
    def validator_a(value: Any, metadata: Any) -> None:
        pass

    @Validators.register("validator_b")
    def validator_b(value: Any, metadata: Any) -> None:
        pass

    class MockMetadata:
        def __init__(self) -> None:
            self.validators = []
            self.description = "test attribute"

    metadata = MockMetadata()
    Validators.attach(metadata, "validator_a", "validator_b")

    assert len(metadata.validators) == 2


def test_attach_unregistered_validator_raises_error() -> None:
    """Test that attaching an unregistered validator raises an error."""

    class MockMetadata:
        def __init__(self) -> None:
            self.validators = []
            self.description = "test attribute"

    metadata = MockMetadata()

    with pytest.raises(ConfigValidationError, match="Validator 'nonexistent' not registered"):
        Validators.attach(metadata, "nonexistent")


def test_attach_validator_to_metadata_without_validators_list() -> None:
    """Test attaching validator to metadata without validators list."""

    @Validators.register("test_validator")
    def test_validator(value: Any, metadata: Any) -> None:
        pass

    class MockMetadataNoList:
        def __init__(self) -> None:
            self.description = "test attribute"

    metadata = MockMetadataNoList()
    # Should not raise an error, but logs a warning
    Validators.attach(metadata, "test_validator")
    # Validator should not be attached
    assert not hasattr(metadata, "validators")


def test_validate_with_registered_validator() -> None:
    """Test validating a value with a registered validator."""

    @Validators.register("string_validator")
    def string_validator(value: Any, metadata: Any) -> None:
        if not isinstance(value, str):
            raise ValueError("Must be a string")

    class MockMetadata:
        description = "test"

    # Should not raise for valid input
    Validators.validate("string_validator", "test", MockMetadata())


def test_validate_with_failing_validator() -> None:
    """Test validation failure."""

    @Validators.register("positive_number")
    def positive_number(value: Any, metadata: Any) -> None:
        if value <= 0:
            raise ValueError("Must be positive")

    class MockMetadata:
        description = "test"

    with pytest.raises(ConfigValidationError, match="Validation failed"):
        Validators.validate("positive_number", -5, MockMetadata())


def test_validate_with_unregistered_validator() -> None:
    """Test validation with unregistered validator."""

    class MockMetadata:
        description = "test"

    with pytest.raises(ConfigValidationError, match="Validator 'missing' not registered"):
        Validators.validate("missing", "value", MockMetadata())


def test_validator_receives_metadata() -> None:
    """Test that validators receive metadata correctly."""
    received_metadata = []

    @Validators.register("metadata_checker")
    def metadata_checker(value: Any, metadata: Any) -> None:
        received_metadata.append(metadata)

    class MockMetadata:
        description = "test attribute"

    meta = MockMetadata()
    Validators.validate("metadata_checker", "test", meta)

    assert len(received_metadata) == 1
    assert received_metadata[0] == meta


def test_multiple_attach_calls_accumulate() -> None:
    """Test that multiple attach calls accumulate validators."""

    @Validators.register("validator_1")
    def validator_1(value: Any, metadata: Any) -> None:
        pass

    @Validators.register("validator_2")
    def validator_2(value: Any, metadata: Any) -> None:
        pass

    class MockMetadata:
        def __init__(self) -> None:
            self.validators = []
            self.description = "test"

    metadata = MockMetadata()
    Validators.attach(metadata, "validator_1")
    Validators.attach(metadata, "validator_2")

    assert len(metadata.validators) == 2


# 🐍🏗️🔚
