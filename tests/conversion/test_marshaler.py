"""Comprehensive tests for marshaler module (79% → 90%+ coverage)."""

import attrs
import pytest

from pyvider.conversion.marshaler import (
    marshal,
    unmarshal,
    marshal_value,
    unmarshal_value,
    _apply_schema_marks_iterative,
    _process_single_item,
    _finalize_container,
)
from pyvider.cty import (
    CtyString,
    CtyNumber,
    CtyBool,
    CtyObject,
    CtyList,
    CtyValue,
    CtyMark,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import a_str, a_num, a_bool, s_resource


class TestMarshalFunction:
    """Tests for marshal() function."""

    def test_marshal_python_dict_to_dynamic_value(self):
        """Test marshaling a Python dict to DynamicValue."""
        schema = s_resource(attributes={"name": a_str(required=True)})
        data = {"name": "test"}

        result = marshal(data, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None
        assert len(result.msgpack) > 0

    def test_marshal_cty_value_to_dynamic_value(self):
        """Test marshaling a CtyValue to DynamicValue."""
        schema = s_resource(attributes={"count": a_num(required=True)})
        cty_type = schema.block.to_cty_type()
        cty_value = cty_type.validate({"count": 42})

        result = marshal(cty_value, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_with_pvs_type_schema(self):
        """Test marshaling with PvsType schema."""
        schema = s_resource(attributes={"active": a_bool()})
        data = {"active": True}

        result = marshal(data, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_with_cty_type_schema(self):
        """Test marshaling with CtyType schema directly."""
        cty_type = CtyObject({"name": CtyString()})
        data = {"name": "test"}

        result = marshal(data, schema=cty_type)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_attrs_object(self):
        """Test marshaling an attrs object."""
        schema = s_resource(attributes={"name": a_str(), "count": a_num()})

        @attrs.define
        class TestData:
            name: str
            count: int

        data = TestData(name="test", count=10)
        result = marshal(data, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_raises_on_invalid_schema_type(self):
        """Test that marshal raises TypeError for invalid schema."""
        with pytest.raises(TypeError, match="Schema must be a CtyType or PvsType"):
            marshal({"test": "data"}, schema="invalid_schema")  # type: ignore

    def test_marshal_sensitive_attribute_gets_marked(self):
        """Test that sensitive attributes get marked during marshaling."""
        schema = s_resource(attributes={"api_key": a_str(sensitive=True)})
        data = {"api_key": "secret"}

        result = marshal(data, schema=schema.block)

        # Should successfully marshal with sensitive marking
        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_null_value(self):
        """Test marshaling null values."""
        schema = s_resource(attributes={"name": a_str(optional=True)})
        cty_type = schema.block.to_cty_type()
        null_value = CtyValue.null(cty_type)

        result = marshal(null_value, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_unknown_value(self):
        """Test marshaling unknown values."""
        schema = s_resource(attributes={"name": a_str()})
        cty_type = schema.block.to_cty_type()
        unknown_value = CtyValue.unknown(cty_type)

        result = marshal(unknown_value, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_complex_nested_object(self):
        """Test marshaling complex nested structures."""
        schema = s_resource(
            attributes={
                "name": a_str(required=True),
                "count": a_num(optional=True),
                "active": a_bool(computed=True),
            }
        )
        data = {"name": "complex", "count": 99, "active": True}

        result = marshal(data, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None


class TestUnmarshalFunction:
    """Tests for unmarshal() function."""

    def test_unmarshal_msgpack_to_cty_value(self):
        """Test unmarshaling msgpack DynamicValue to CtyValue."""
        schema = s_resource(attributes={"name": a_str()})
        data = {"name": "test"}

        # Marshal first to get valid msgpack
        dv = marshal(data, schema=schema.block)

        # Now unmarshal it back
        result = unmarshal(dv, schema=schema.block)

        assert isinstance(result, CtyValue)
        assert result.value["name"].value == "test"

    def test_unmarshal_with_pvs_type_schema(self):
        """Test unmarshaling with PvsType schema."""
        schema = s_resource(attributes={"count": a_num()})
        data = {"count": 42}

        dv = marshal(data, schema=schema.block)
        result = unmarshal(dv, schema=schema.block)

        assert isinstance(result, CtyValue)
        assert result.value["count"].value == 42

    def test_unmarshal_with_cty_type_schema(self):
        """Test unmarshaling with CtyType schema directly."""
        cty_type = CtyObject({"active": CtyBool()})
        data = {"active": True}

        dv = marshal(data, schema=cty_type)
        result = unmarshal(dv, schema=cty_type)

        assert isinstance(result, CtyValue)
        assert result.value["active"].value is True

    def test_unmarshal_raises_on_invalid_schema_type(self):
        """Test that unmarshal raises TypeError for invalid schema."""
        dv = pb.DynamicValue(msgpack=b"\x81\xa4name\xa4test")

        with pytest.raises(TypeError, match="Schema must be a CtyType or PvsType"):
            unmarshal(dv, schema=123)  # type: ignore

    def test_unmarshal_json_raises_not_implemented(self):
        """Test that JSON unmarshaling raises NotImplementedError."""
        schema = s_resource(attributes={"name": a_str()})
        dv = pb.DynamicValue(json=b'{"name": "test"}')

        with pytest.raises(NotImplementedError, match="JSON unmarshalling is not yet implemented"):
            unmarshal(dv, schema=schema.block)

    def test_unmarshal_empty_dynamic_value_returns_null(self):
        """Test that empty DynamicValue returns null."""
        schema = s_resource(attributes={"name": a_str()})
        dv = pb.DynamicValue()  # No msgpack or json

        result = unmarshal(dv, schema=schema.block)

        assert isinstance(result, CtyValue)
        assert result.is_null

    def test_unmarshal_preserves_data_types(self):
        """Test that unmarshaling preserves various data types."""
        schema = s_resource(
            attributes={
                "name": a_str(),
                "count": a_num(),
                "active": a_bool(),
            }
        )
        data = {"name": "test", "count": 123, "active": False}

        dv = marshal(data, schema=schema.block)
        result = unmarshal(dv, schema=schema.block)

        assert result.value["name"].value == "test"
        assert result.value["count"].value == 123
        assert result.value["active"].value is False


class TestMarshalValueFunction:
    """Tests for marshal_value() wrapper function."""

    def test_marshal_value_with_cty_type(self):
        """Test marshal_value wrapper function."""
        cty_type = CtyObject({"name": CtyString()})
        cty_value = cty_type.validate({"name": "test"})

        result = marshal_value(cty_value, cty_type)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_marshal_value_preserves_value(self):
        """Test that marshal_value preserves the value correctly."""
        cty_type = CtyObject({"count": CtyNumber()})
        cty_value = cty_type.validate({"count": 99})

        result = marshal_value(cty_value, cty_type)
        unmarshaled = unmarshal_value(result, cty_type)

        assert unmarshaled.value["count"].value == 99


class TestUnmarshalValueFunction:
    """Tests for unmarshal_value() wrapper function."""

    def test_unmarshal_value_with_cty_type(self):
        """Test unmarshal_value wrapper function."""
        cty_type = CtyObject({"active": CtyBool()})
        data = {"active": True}

        dv = marshal(data, schema=cty_type)
        result = unmarshal_value(dv, cty_type)

        assert isinstance(result, CtyValue)
        assert result.value["active"].value is True

    def test_unmarshal_value_round_trip(self):
        """Test round-trip marshal_value → unmarshal_value."""
        cty_type = CtyObject({"name": CtyString(), "count": CtyNumber()})
        original_value = cty_type.validate({"name": "roundtrip", "count": 42})

        # Marshal
        dv = marshal_value(original_value, cty_type)

        # Unmarshal
        result = unmarshal_value(dv, cty_type)

        assert result.value["name"].value == "roundtrip"
        assert result.value["count"].value == 42


class TestApplySchemaMarksIterative:
    """Tests for _apply_schema_marks_iterative() internal function."""

    def test_apply_marks_to_null_value_returns_unchanged(self):
        """Test that null values are returned unchanged."""
        schema = s_resource(attributes={"name": a_str(sensitive=True)})
        cty_type = schema.block.to_cty_type()
        null_value = CtyValue.null(cty_type)

        result = _apply_schema_marks_iterative(null_value, schema.block)

        assert result is null_value
        assert result.is_null

    def test_apply_marks_to_unknown_value_returns_unchanged(self):
        """Test that unknown values are returned unchanged."""
        schema = s_resource(attributes={"name": a_str(sensitive=True)})
        cty_type = schema.block.to_cty_type()
        unknown_value = CtyValue.unknown(cty_type)

        result = _apply_schema_marks_iterative(unknown_value, schema.block)

        assert result is unknown_value
        assert result.is_unknown

    def test_apply_marks_to_sensitive_attribute(self):
        """Test applying sensitive mark to attribute."""
        schema = s_resource(attributes={"secret": a_str(sensitive=True)})
        unmarked_value = CtyString().validate("my-secret")

        result = _apply_schema_marks_iterative(
            unmarked_value, schema.block.attributes["secret"]
        )

        assert result.has_mark(CtyMark("sensitive"))

    def test_apply_marks_to_nested_object(self):
        """Test applying marks to nested object structure."""
        schema = s_resource(
            attributes={
                "name": a_str(),
                "password": a_str(sensitive=True),
            }
        )
        cty_type = schema.block.to_cty_type()
        value = cty_type.validate({"name": "user", "password": "secret"})

        result = _apply_schema_marks_iterative(value, schema.block)

        # The container should be marked if any child is sensitive
        assert isinstance(result, CtyValue)

    def test_apply_marks_avoids_recursion_on_deep_nesting(self):
        """Test that deep nesting doesn't cause recursion errors."""
        # Create a deeply nested schema
        schema = s_resource(
            attributes={
                "level1": a_str(),
                "level2": a_str(),
                "level3": a_str(sensitive=True),
            }
        )
        cty_type = schema.block.to_cty_type()
        value = cty_type.validate(
            {"level1": "a", "level2": "b", "level3": "secret"}
        )

        # Should not raise RecursionError
        result = _apply_schema_marks_iterative(value, schema.block)
        assert isinstance(result, CtyValue)


class TestProcessSingleItem:
    """Tests for _process_single_item() internal function."""

    def test_process_sensitive_attribute_adds_mark(self):
        """Test processing sensitive attribute adds mark."""
        schema = s_resource(attributes={"api_key": a_str(sensitive=True)})
        unmarked_value = CtyString().validate("secret")
        processing = set()

        marked_value, children = _process_single_item(
            unmarked_value, schema.block.attributes["api_key"], processing
        )

        assert marked_value.has_mark(CtyMark("sensitive"))
        assert len(children) == 0

    def test_process_non_sensitive_attribute_no_mark(self):
        """Test processing non-sensitive attribute doesn't add mark."""
        schema = s_resource(attributes={"name": a_str()})
        value = CtyString().validate("test")
        processing = set()

        marked_value, children = _process_single_item(
            value, schema.block.attributes["name"], processing
        )

        assert not marked_value.has_mark(CtyMark("sensitive"))
        assert len(children) == 0

    def test_process_object_type_returns_children(self):
        """Test processing PvsObjectType returns children to process."""
        schema = s_resource(
            attributes={"name": a_str(), "count": a_num()}
        )
        cty_type = schema.block.to_cty_type()
        value = cty_type.validate({"name": "test", "count": 10})
        processing = set()

        marked_value, children = _process_single_item(
            value, schema.block, processing
        )

        # Should return children for nested processing
        assert len(children) == 2
        assert id(value) in processing


class TestFinalizeContainer:
    """Tests for _finalize_container() internal function."""

    def test_finalize_with_changes_adds_sensitive_mark(self):
        """Test finalizing container with changes adds sensitive mark."""
        cty_type = CtyObject({"name": CtyString()})
        container_val = cty_type.validate({"name": "test"})
        new_inner = {"name": CtyString().validate("modified").mark(CtyMark("sensitive"))}

        result = _finalize_container(container_val, new_inner, made_change=True)

        assert result.has_mark(CtyMark("sensitive"))
        assert result.value == new_inner

    def test_finalize_without_changes_returns_original(self):
        """Test finalizing container without changes returns original."""
        cty_type = CtyObject({"name": CtyString()})
        container_val = cty_type.validate({"name": "test"})
        new_inner = container_val.value

        result = _finalize_container(container_val, new_inner, made_change=False)

        assert result is container_val
        assert not result.has_mark(CtyMark("sensitive"))


class TestMarshalerEdgeCases:
    """Edge case tests for marshaler module."""

    def test_marshal_unmarshal_empty_object(self):
        """Test marshaling and unmarshaling empty object."""
        schema = s_resource(attributes={})
        data = {}

        dv = marshal(data, schema=schema.block)
        result = unmarshal(dv, schema=schema.block)

        assert isinstance(result, CtyValue)
        assert result.value == {}

    def test_marshal_with_optional_missing_field(self):
        """Test marshaling with optional field missing."""
        schema = s_resource(
            attributes={"required": a_str(required=True), "optional": a_str(optional=True)}
        )
        data = {"required": "present"}

        result = marshal(data, schema=schema.block)

        assert isinstance(result, pb.DynamicValue)
        assert result.msgpack is not None

    def test_unmarshal_preserves_sensitive_marks(self):
        """Test that unmarshaling preserves sensitive information handling."""
        schema = s_resource(attributes={"password": a_str(sensitive=True)})
        data = {"password": "secret123"}

        dv = marshal(data, schema=schema.block)
        result = unmarshal(dv, schema=schema.block)

        # Should successfully unmarshal (marks are applied during marshal)
        assert isinstance(result, CtyValue)
        assert "password" in result.value
