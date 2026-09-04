#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for conversion/marshaler.py."""

import attrs
import pytest

from pyvider.conversion.marshaler import (
    _apply_schema_marks_iterative,
    marshal,
    marshal_value,
    unmarshal,
    unmarshal_value,
)
from pyvider.cty import CtyList, CtyNumber, CtyObject, CtyString, CtyValue
from pyvider.cty.marks import CtyMark
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

    def test_unmarshal_decodes_a_json_dynamic_value(self) -> None:
        """Both encodings are read, as Terraform reads both.

        Core decodes whichever of msgpack or json is present
        (internal/plugin6/grpc_provider.go:2078-2093). This used to raise
        NotImplementedError, which made a differently-built client -- and raw
        state, which arrives as JSON -- unreadable.
        """
        value = unmarshal(pb.DynamicValue(json=b'"hello"'), schema=CtyString())

        assert value.value == "hello"

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


class TestMarshalUnmarksAtTheWireBoundary:
    """A marked value must reach the wire, not an exception.

    The inbound path deliberately marks config so a resource can see which
    attributes are sensitive. That means resource code is handed marked values
    and may build its planned or new state out of them, so marked values arrive
    here in normal operation.

    pyvider-cty (0.5+) refuses to serialize a marked value rather than dropping
    the marks silently, matching go-cty. Without unmarking here that refusal
    would surface as a provider crash at plan or apply, on precisely the
    resources that handle secrets.

    Marks are safe to drop at this one point because sensitivity reaches
    Terraform through the schema -- Schema.Attribute.sensitive -- and never
    through the value.
    """

    def _schema_and_value(self):
        schema = PvsObjectType(attributes={"password": PvsAttribute(type=CtyString(), sensitive=True)})
        cty_type = CtyObject(attribute_types={"password": CtyString()})
        return schema, cty_type.validate({"password": "secret"})

    def test_a_value_marked_by_the_inbound_path_still_marshals(self) -> None:
        schema, value = self._schema_and_value()
        marked = _apply_schema_marks_iterative(value, schema)

        result = marshal(marked, schema=schema)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack

    def test_a_top_level_marked_value_still_marshals(self) -> None:
        schema, value = self._schema_and_value()

        result = marshal(value.mark(CtyMark("sensitive")), schema=schema)

        assert isinstance(result, pb.DynamicValue)

    def test_the_marshalled_bytes_match_the_unmarked_value(self) -> None:
        """Unmarking must not disturb what goes on the wire."""
        schema, value = self._schema_and_value()
        marked = _apply_schema_marks_iterative(value, schema)

        assert marshal(marked, schema=schema).msgpack == marshal(value, schema=schema).msgpack

    def test_unmarking_reaches_nested_values(self) -> None:
        schema = PvsObjectType(
            attributes={"creds": PvsAttribute(type=CtyList(element_type=CtyString()), sensitive=True)}
        )
        cty_type = CtyObject(attribute_types={"creds": CtyList(element_type=CtyString())})
        value = cty_type.validate({"creds": ["a", "b"]})
        marked = _apply_schema_marks_iterative(value, schema)

        assert isinstance(marshal(marked, schema=schema), pb.DynamicValue)
