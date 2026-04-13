#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for conversion/marshaler.py."""

import attrs
import pytest

from pyvider.conversion.marshaler import marshal, marshal_value, unmarshal, unmarshal_value
from pyvider.cty import CtyNumber, CtyObject, CtyString, CtyValue
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.types import PvsAttribute, PvsObjectType


class TestMarshal:
    """Tests for marshal function."""

    def test_marshal_simple_string(self) -> None:
        """Test marshaling a simple string value."""
        schema = CtyString()
        value = CtyValue(vtype=CtyString(), value="test")

        result = marshal(value, schema=schema)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_simple_number(self) -> None:
        """Test marshaling a number value."""
        schema = CtyNumber()
        value = CtyValue(vtype=CtyNumber(), value=42)

        result = marshal(value, schema=schema)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_raw_dict_value(self) -> None:
        """Test marshaling a raw dict (not CtyValue)."""
        schema = CtyObject(attribute_types={"name": CtyString()})
        value = {"name": "test"}

        result = marshal(value, schema=schema)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_attrs_instance(self) -> None:
        """Test marshaling an attrs instance."""

        @attrs.define
        class TestConfig:
            name: str

        schema = CtyObject(attribute_types={"name": CtyString()})
        value = TestConfig(name="test")

        result = marshal(value, schema=schema)

        assert isinstance(result, pb.DynamicValue)

    def test_marshal_with_sensitive_marks(self) -> None:
        """Test that sensitive attributes are marked."""
        schema = PvsObjectType(attributes={"password": PvsAttribute(type=CtyString(), sensitive=True)})
        value = CtyValue(
            vtype=CtyObject(attribute_types={"password": CtyString()}),
            value={"password": CtyValue(vtype=CtyString(), value="secret")},
        )

        result = marshal(value, schema=schema)

        assert isinstance(result, pb.DynamicValue)

    def test_marshal_invalid_schema_type_raises_error(self) -> None:
        """Test that invalid schema type raises TypeError."""
        with pytest.raises(TypeError, match="Schema must be a CtyType or PvsType"):
            marshal("value", schema="not_a_schema")  # type: ignore


class TestUnmarshal:
    """Tests for unmarshal function."""

    def test_unmarshal_from_msgpack(self) -> None:
        """Test unmarshaling from msgpack data."""
        schema = CtyString()
        # First marshal to get valid msgpack
        value = CtyValue(vtype=CtyString(), value="test")
        dv = marshal(value, schema=schema)

        # Now unmarshal
        result = unmarshal(dv, schema=schema)

        assert isinstance(result, CtyValue)
        assert result.value == "test"

    def test_unmarshal_number_from_msgpack(self) -> None:
        """Test unmarshaling a number."""
        schema = CtyNumber()
        value = CtyValue(vtype=CtyNumber(), value=42)
        dv = marshal(value, schema=schema)

        result = unmarshal(dv, schema=schema)

        assert isinstance(result, CtyValue)
        assert result.value == 42

    def test_unmarshal_empty_dynamic_value_returns_null(self) -> None:
        """Test that empty DynamicValue returns null CtyValue."""
        schema = CtyString()
        dv = pb.DynamicValue()  # Empty

        result = unmarshal(dv, schema=schema)

        assert isinstance(result, CtyValue)
        assert result.is_null

    def test_unmarshal_json_raises_not_implemented(self) -> None:
        """Test that JSON unmarshaling raises NotImplementedError."""
        schema = CtyString()
        dv = pb.DynamicValue(json=b'{"value": "test"}')

        with pytest.raises(NotImplementedError, match="JSON unmarshalling"):
            unmarshal(dv, schema=schema)

    def test_unmarshal_invalid_schema_type_raises_error(self) -> None:
        """Test that invalid schema type raises TypeError."""
        dv = pb.DynamicValue(msgpack=b"\x00")

        with pytest.raises(TypeError, match="Schema must be a CtyType or PvsType"):
            unmarshal(dv, schema="not_a_schema")  # type: ignore


class TestMarshalValue:
    """Tests for marshal_value convenience function."""

    def test_marshal_value_delegates_to_marshal(self) -> None:
        """Test that marshal_value calls marshal with correct parameters."""
        value = CtyValue(vtype=CtyString(), value="test")
        cty_type = CtyString()

        result = marshal_value(value, cty_type)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None


class TestUnmarshalValue:
    """Tests for unmarshal_value convenience function."""

    def test_unmarshal_value_delegates_to_unmarshal(self) -> None:
        """Test that unmarshal_value calls unmarshal with correct parameters."""
        value = CtyValue(vtype=CtyString(), value="test")
        cty_type = CtyString()
        dv = marshal_value(value, cty_type)

        result = unmarshal_value(dv, cty_type)

        assert isinstance(result, CtyValue)
        assert result.value == "test"


class TestRoundTrip:
    """Round-trip tests for marshal/unmarshal."""

    def test_roundtrip_string(self) -> None:
        """Test marshal -> unmarshal roundtrip for string."""
        schema = CtyString()
        original = CtyValue(vtype=CtyString(), value="test string")

        marshaled = marshal(original, schema=schema)
        result = unmarshal(marshaled, schema=schema)

        assert result.value == original.value

    def test_roundtrip_number(self) -> None:
        """Test marshal -> unmarshal roundtrip for number."""
        schema = CtyNumber()
        original = CtyValue(vtype=CtyNumber(), value=12345.67)

        marshaled = marshal(original, schema=schema)
        result = unmarshal(marshaled, schema=schema)

        assert result.value == original.value

    def test_roundtrip_object(self) -> None:
        """Test marshal -> unmarshal roundtrip for object."""
        schema = CtyObject(attribute_types={"name": CtyString(), "age": CtyNumber()})
        original = CtyValue(
            vtype=schema,
            value={
                "name": CtyValue(vtype=CtyString(), value="Alice"),
                "age": CtyValue(vtype=CtyNumber(), value=30),
            },
        )

        marshaled = marshal(original, schema=schema)
        result = unmarshal(marshaled, schema=schema)

        assert result.value["name"].value == "Alice"
        assert result.value["age"].value == 30


# 🐍🏗️🔚
