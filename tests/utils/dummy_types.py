#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Callable
from typing import Any

from attrs import define, field

from pyvider.cty import (
    CtyList,
    CtyMap,
    CtyNumber,
    CtyString,
    CtyType,
    TypeMetadata,
)
from pyvider.exceptions import (
    AttributeValidationError,
    ValidationError,
)

################################################################################
################################################################################
################################################################################


@define
class DummyType(CtyType[CtyString]):
    metadata: dict[str, Any] = field(factory=dict)

    def __init__(self, children: Any = None) -> None:
        self._children = children or {}
        super().__init__(metadata={"type": "dummy"})

    """Mock Terraform type for testing."""

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError("DummyType", f"Value must be a string, got {type(value).__name__}.")

    def serialize(self, value: str) -> str:
        return f'"{value}"'

    def equal(self, other: "CtyType") -> bool:
        return isinstance(other, DummyType)

    def usable_as(self, other: "CtyType") -> bool:
        return isinstance(other, DummyType)

    def __str__(self) -> str:
        return "DummyType"


@define
class DummyStringType(CtyType[CtyString]):
    metadata: TypeMetadata = field(factory=lambda: TypeMetadata(description="dummy string"))
    validators: list[Callable[[str], None]] = field(factory=list)
    min_length: int = field(default=0)
    max_length: int | None = field(default=None)

    def __init__(self, min_length: int = 0, max_length: int | None = None) -> None:
        # Set metadata directly using object.__setattr__ to avoid AttributeError
        object.__setattr__(self, "metadata", TypeMetadata(description="dummy string"))

        # Initialize validators early to avoid '_CountingAttr' errors
        object.__setattr__(self, "validators", [self.validate])

        # Pass metadata to the superclass
        super().__init__(
            metadata=self.metadata,
            validators=self.validators,
        )

        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        if len(value) < self.min_length:
            raise ValidationError(f"String is shorter than minimum length {self.min_length}.")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"String exceeds maximum length {self.max_length}.")

    def serialize(self, value: str) -> str:
        self.validate(value)
        return f'"{value}"'

    def deserialize(self, value: str) -> str:
        try:
            if not value.startswith('"') or not value.endswith('"'):
                raise ValidationError("Deserialized value is not a valid quoted string.")
            deserialized = value[1:-1]  # Strip the surrounding quotes
            self.validate(deserialized)
            return deserialized
        except Exception as e:
            raise ValidationError(f"Failed to deserialize string: {e}") from e

    def equal(self, other: "CtyType") -> bool:
        return (
            isinstance(other, DummyStringType)
            and self.min_length == other.min_length
            and self.max_length == other.max_length
        )

    def usable_as(self, other: "CtyType") -> bool:
        return isinstance(other, DummyStringType)

    def __str__(self) -> str:
        return f"DummyStringType(min_length={self.min_length}, max_length={self.max_length})"


################################################################################
################################################################################
################################################################################


@define
class DummyNumberType(CtyType[CtyNumber]):
    metadata: TypeMetadata = field(factory=lambda: TypeMetadata(description="dummy string"))
    validators: list[Callable[[str], None]] = field(factory=list)
    min_value: float | None = field(default=None)
    max_value: float | None = field(default=None)

    def __init__(self, min_value: int = 0, max_value: int | None = None) -> None:
        # Set metadata directly using object.__setattr__ to avoid AttributeError
        object.__setattr__(self, "metadata", TypeMetadata(description="dummy string"))

        # Initialize validators early to avoid '_CountingAttr' errors
        object.__setattr__(self, "validators", [self.validate])

        # Pass metadata to the superclass
        super().__init__(
            metadata=self.metadata,
            validators=self.validators,
        )

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: float) -> None:
        """
        Validates that the value is a number and within the specified range.

        Args:
            value (float): The value to validate.

        Raises:
            ValidationError: If the value is not valid.
        """
        if not isinstance(value, (int, float)):
            raise ValidationError("Value must be a number.")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value {value} is less than the minimum {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value {value} exceeds the maximum {self.max_value}.")

    def serialize(self, value: float) -> str:
        """
        Serializes the number value into a string.

        Args:
            value (float): The number to serialize.

        Returns:
            str: The serialized string representation.
        """
        self.validate(value)
        return str(value)

    def deserialize(self, value: str) -> float:
        """
        Deserializes a string into a numeric value.

        Args:
            value (str): The string to deserialize.

        Returns:
            float: The deserialized number.

        Raises:
            ValidationError: If the deserialized data is not a valid number.
        """
        try:
            deserialized = float(value)
            self.validate(deserialized)
            return deserialized
        except ValueError:
            raise ValidationError(f"Failed to deserialize number: {value}") from None

    def equal(self, other: "CtyType") -> bool:
        """
        Checks equality with another type.

        Args:
            other (CtyType): Another type to compare.

        Returns:
            bool: True if the types are equal.
        """
        return (
            isinstance(other, DummyNumberType)
            and self.min_value == other.min_value
            and self.max_value == other.max_value
        )

    def usable_as(self, other: "CtyType") -> bool:
        """
        Checks if this type can be used as another type.

        Args:
            other (CtyType): Another type to check compatibility with.

        Returns:
            bool: True if compatible.
        """
        return isinstance(other, DummyNumberType)

    def __str__(self) -> str:
        return f"DummyNumberType(min_value={self.min_value}, max_value={self.max_value})"


################################################################################
################################################################################
################################################################################


@define
class DummyInvalidNumberType(CtyType[Any]):
    """A dummy type that allows invalid values but raises during serialization."""

    def validate(self, value: Any) -> None:
        pass  # Skip validation to allow invalid values for testing serialization

    def serialize(self, value: Any) -> str:
        raise ValidationError("Serialization failed intentionally.")

    def equal(self, other: "CtyType") -> bool:
        return False

    def usable_as(self, other: "CtyType") -> bool:
        return False


################################################################################
################################################################################
################################################################################
@define
class DummyListType(CtyType[CtyList]):
    metadata: TypeMetadata = field(factory=lambda: TypeMetadata(description="dummy list"))
    validators: list[Callable[[list], None]] = field(factory=list)
    element_type: Any = field(default=int)

    def __attrs_post_init__(self) -> None:
        if not isinstance(self.element_type, (type, tuple, CtyType)):
            raise AttributeValidationError(
                "element_type must be a type, a tuple of types, or an instance of CtyType."
            )

        # Initialize validators (if any custom ones are needed)
        object.__setattr__(self, "validators", [self.validate])

    def validate(self, value: list) -> None:
        if not isinstance(value, list):
            raise ValidationError("Value must be a list.")
        for element in value:
            if isinstance(self.element_type, CtyType):
                self.element_type.validate(element)
            elif not isinstance(element, self.element_type):
                raise ValidationError(f"Element {element} is not of type {self.element_type}.")

    def serialize(self, value: list) -> str:
        self.validate(value)
        return str(value)

    def deserialize(self, value: str) -> list:
        try:
            deserialized = eval(value)  # Replace with safer JSON deserialization for real use
            self.validate(deserialized)
            return deserialized
        except Exception as e:
            raise ValidationError(f"Failed to deserialize list: {e}") from e

    def equal(self, other: "CtyType") -> bool:
        return isinstance(other, DummyListType) and self.element_type == other.element_type

    def usable_as(self, other: "CtyType") -> bool:
        return isinstance(other, DummyListType) and self.element_type == other.element_type

    def __str__(self) -> str:
        if isinstance(self.element_type, CtyType):
            element_type_name = self.element_type.__class__.__name__
        else:
            element_type_name = self.element_type.__name__
        return f"DummyListType({element_type_name})"


################################################################################
################################################################################
################################################################################


@define
class DummyMapType(CtyType[CtyMap]):
    metadata: TypeMetadata = field(factory=lambda: TypeMetadata(description="dummy map"))
    validators: list[Callable[[dict], None]] = field(factory=list)
    key_type: Any = field(default=str)
    value_type: Any = field(default=str)

    def __attrs_post_init__(self) -> None:
        if not isinstance(self.key_type, type | CtyType) or not isinstance(self.value_type, type | CtyType):
            raise AttributeValidationError("key_type and value_type must be types or instances of CtyType.")

        # Initialize validators
        object.__setattr__(self, "validators", [self.validate])

    def validate(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise ValidationError("Value must be a dictionary.")
        for key, val in value.items():
            self._validate_key(key)
            self._validate_value(val)

    def _validate_key(self, key: Any) -> None:
        if isinstance(self.key_type, CtyType):
            self.key_type.validate(key)
        elif not isinstance(key, self.key_type):
            raise ValidationError(f"Key {key} is not of type {self.key_type}.")

    def _validate_value(self, value: Any) -> None:
        try:
            if isinstance(self.value_type, CtyType):
                self.value_type.validate(value)
            elif isinstance(self.value_type, tuple):
                if not isinstance(value, self.value_type):
                    raise ValidationError(f"Value {value} is not one of the types {self.value_type}.")
            elif not isinstance(value, self.value_type):
                raise ValidationError(f"Value {value} is not of type {self.value_type}.")
        except ValidationError:
            raise

    def serialize(self, value: dict) -> str:
        self.validate(value)
        return str(value)

    def deserialize(self, value: str) -> dict:
        try:
            deserialized = eval(value)  # Replace with safer JSON deserialization for real use
            self.validate(deserialized)
            return deserialized
        except Exception as e:
            raise ValidationError(f"Failed to deserialize map: {e}") from e

    def equal(self, other: "CtyType") -> bool:
        return (
            isinstance(other, DummyMapType)
            and self.key_type == other.key_type
            and self.value_type == other.value_type
        )

    def usable_as(self, other: "CtyType") -> bool:
        return isinstance(other, DummyMapType) and (
            (
                isinstance(self.key_type, type)
                and isinstance(other.key_type, type)
                and issubclass(self.key_type, other.key_type)
            )
            and (
                isinstance(self.value_type, type)
                and isinstance(other.value_type, type)
                and issubclass(self.value_type, other.value_type)
            )
        )

    def __str__(self) -> str:
        return f"DummyMapType(key_type={self.key_type}, value_type={self.value_type})"


# 🐍🏗️🔚
