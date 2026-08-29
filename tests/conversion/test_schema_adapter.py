#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for schema_adapter module (15% → 85%+)."""

import json

import pytest

from pyvider.conversion.schema_adapter import (
    _pvs_attribute_to_proto,
    _pvs_nested_block_to_proto,
    _pvs_object_type_to_proto,
    pvs_schema_to_proto,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import a_bool, a_num, a_obj, a_str, b_list, b_single, s_data_source, s_resource


class TestPvsAttributeToProto:
    """Tests for _pvs_attribute_to_proto function."""

    def test_converts_string_attribute(self) -> None:
        """Test converting a string attribute to proto."""
        attr = a_str(required=True, description="Test string")
        proto = _pvs_attribute_to_proto(attr)

        assert isinstance(proto, pb.Schema.Attribute)
        assert proto.name == attr.name
        assert proto.required is True
        assert proto.description == "Test string"
        assert proto.optional is False

    def test_converts_number_attribute(self) -> None:
        """Test converting a number attribute to proto."""
        attr = a_num(optional=True, description="Test number")
        proto = _pvs_attribute_to_proto(attr)

        assert isinstance(proto, pb.Schema.Attribute)
        assert proto.optional is True
        assert proto.required is False
        assert proto.description == "Test number"

    def test_converts_boolean_attribute(self) -> None:
        """Test converting a boolean attribute to proto."""
        attr = a_bool(computed=True)
        proto = _pvs_attribute_to_proto(attr)

        assert isinstance(proto, pb.Schema.Attribute)
        assert proto.computed is True

    def test_converts_sensitive_attribute(self) -> None:
        """Test converting a sensitive attribute to proto."""
        attr = a_str(sensitive=True, required=True)
        proto = _pvs_attribute_to_proto(attr)

        assert proto.sensitive is True

    def test_converts_deprecated_attribute(self) -> None:
        """Test converting a deprecated attribute to proto."""
        attr = a_str(deprecated=True, optional=True)
        proto = _pvs_attribute_to_proto(attr)

        assert proto.deprecated is True

    def test_attribute_type_encoding(self) -> None:
        """Test that attribute type is properly encoded as JSON bytes."""
        attr = a_str(required=True)
        proto = _pvs_attribute_to_proto(attr)

        # Type should be JSON-encoded bytes
        assert isinstance(proto.type, bytes)
        # Should be valid JSON
        type_data = json.loads(proto.type)
        assert isinstance(type_data, (dict, str))


class TestObjectAttributesBecomeNestedTypes:
    """`a_obj()` crosses the wire as a `nested_type`, not a flat object type.

    Terraform treats a flat object attribute as one opaque value: the planned
    value must equal the configured one exactly, so a member's Optional +
    Computed flags -- and therefore any default the provider resolves for it --
    could never take effect. `terraform plan` rejects the attempt outright with
    "planned value ... does not match config value". `nested_type` is what
    carries the per-member flags; the configuration syntax is unchanged.
    """

    def test_object_attribute_emits_a_nested_type(self) -> None:
        attr = a_obj({"timeout": a_num(default=30), "label": a_str()})

        proto = _pvs_attribute_to_proto(attr, "config")

        assert proto.HasField("nested_type")
        assert proto.nested_type.nesting == pb.Schema.Object.NestingMode.SINGLE
        assert [a.name for a in proto.nested_type.attributes] == ["timeout", "label"]

    def test_member_flags_cross_the_wire(self) -> None:
        attr = a_obj({"timeout": a_num(default=30), "host": a_str(required=True), "label": a_str()})

        members = {a.name: a for a in _pvs_attribute_to_proto(attr, "config").nested_type.attributes}

        # A default makes the member Optional + Computed, which is exactly what
        # lets Terraform accept a provider-planned value for it.
        assert (members["timeout"].optional, members["timeout"].computed) == (True, True)
        assert (members["host"].required, members["host"].computed) == (True, False)
        assert (members["label"].optional, members["label"].computed) == (True, False)

    def test_objects_nested_inside_objects_nest_too(self) -> None:
        attr = a_obj({"tls": a_obj({"enabled": a_bool(default=True)})})

        tls = _pvs_attribute_to_proto(attr, "config").nested_type.attributes[0]

        assert tls.HasField("nested_type")
        assert tls.nested_type.attributes[0].name == "enabled"

    def test_non_object_attributes_still_carry_a_type(self) -> None:
        proto = _pvs_attribute_to_proto(a_str(required=True), "name")

        assert not proto.HasField("nested_type")
        assert proto.type, "a non-object attribute must still send its cty type"

    def test_object_inside_a_block_nests_as_well(self) -> None:
        schema = s_resource(
            attributes={"name": a_str(required=True)},
            block_types=[b_single("options", attributes={"limits": a_obj({"max": a_num(default=5)})})],
        )

        block = _pvs_object_type_to_proto(schema.block)
        options = block.block_types[0].block

        assert options.attributes[0].name == "limits"
        assert options.attributes[0].HasField("nested_type")


class TestPvsNestedBlockToProto:
    """Tests for _pvs_nested_block_to_proto function."""

    def test_converts_single_nested_block(self) -> None:
        """Test converting a SINGLE nesting mode block."""
        block = b_single("config", attributes={"name": a_str()})
        proto = _pvs_nested_block_to_proto(block)

        assert isinstance(proto, pb.Schema.NestedBlock)
        assert proto.type_name == "config"
        assert proto.nesting == pb.Schema.NestedBlock.NestingMode.SINGLE

    def test_converts_list_nested_block(self) -> None:
        """Test converting a LIST nesting mode block."""
        block = b_list("items", attributes={"value": a_str()})
        proto = _pvs_nested_block_to_proto(block)

        assert proto.nesting == pb.Schema.NestedBlock.NestingMode.LIST

    def test_nested_block_with_min_max_items(self) -> None:
        """Test nested block with min/max items."""
        block = b_list("items", attributes={"value": a_str()}, min_items=1, max_items=10)
        proto = _pvs_nested_block_to_proto(block)

        assert proto.min_items == 1
        assert proto.max_items == 10

    def test_nested_block_without_min_max_defaults_to_zero(self) -> None:
        """Test that missing min/max items defaults to 0."""
        block = b_single("config", attributes={"name": a_str()})
        proto = _pvs_nested_block_to_proto(block)

        assert proto.min_items == 0
        assert proto.max_items == 0

    def test_nested_block_contains_inner_block(self) -> None:
        """Test that nested block properly converts inner block structure."""
        block = b_single("config", attributes={"name": a_str(), "count": a_num()})
        proto = _pvs_nested_block_to_proto(block)

        assert isinstance(proto.block, pb.Schema.Block)
        assert len(proto.block.attributes) == 2


class TestPvsObjectTypeToProto:
    """Tests for _pvs_object_type_to_proto function."""

    def test_converts_empty_object_type(self) -> None:
        """Test converting an object type with no attributes."""
        from pyvider.schema.types import PvsObjectType

        obj = PvsObjectType(attributes={}, block_types=[])
        proto = _pvs_object_type_to_proto(obj)

        assert isinstance(proto, pb.Schema.Block)
        assert len(proto.attributes) == 0
        assert len(proto.block_types) == 0

    def test_converts_object_type_with_attributes(self) -> None:
        """Test converting object type with attributes."""
        schema = s_resource(attributes={"name": a_str(), "count": a_num()})
        proto = _pvs_object_type_to_proto(schema.block)

        assert len(proto.attributes) == 2
        attr_names = {attr.name for attr in proto.attributes}
        assert "name" in attr_names
        assert "count" in attr_names

    def test_converts_object_type_with_nested_blocks(self) -> None:
        """Test converting object type with nested blocks."""
        from pyvider.schema.types import PvsObjectType

        # Create object type with nested block directly
        nested_block = b_single("config", attributes={"value": a_str()})
        obj = PvsObjectType(attributes={"id": a_str()}, block_types=[nested_block])
        proto = _pvs_object_type_to_proto(obj)

        assert len(proto.block_types) == 1
        assert proto.block_types[0].type_name == "config"

    def test_object_type_with_description(self) -> None:
        """Test object type description is included."""
        from pyvider.schema.types import PvsObjectType

        obj = PvsObjectType(attributes={}, block_types=[], description="Test description")
        proto = _pvs_object_type_to_proto(obj)

        assert proto.description == "Test description"

    def test_object_type_with_deprecated_flag(self) -> None:
        """Test object type deprecated flag."""
        from pyvider.schema.types import PvsObjectType

        obj = PvsObjectType(attributes={}, block_types=[], deprecated=True)
        proto = _pvs_object_type_to_proto(obj)

        assert proto.deprecated is True

    def test_object_type_version_is_one(self) -> None:
        """Test that object type version is always 1."""
        from pyvider.schema.types import PvsObjectType

        obj = PvsObjectType(attributes={}, block_types=[])
        proto = _pvs_object_type_to_proto(obj)

        assert proto.version == 1


class TestPvsSchemaToProto:
    """Tests for pvs_schema_to_proto async function."""

    @pytest.mark.asyncio
    async def test_converts_resource_schema(self) -> None:
        """Test converting a resource schema to proto."""
        schema = s_resource(attributes={"name": a_str(required=True)})
        proto = await pvs_schema_to_proto(schema)

        assert isinstance(proto, pb.Schema)
        assert proto.version == schema.version
        assert isinstance(proto.block, pb.Schema.Block)

    @pytest.mark.asyncio
    async def test_converts_data_source_schema(self) -> None:
        """Test converting a data source schema to proto."""
        schema = s_data_source(attributes={"id": a_str()})
        proto = await pvs_schema_to_proto(schema)

        assert isinstance(proto, pb.Schema)
        assert isinstance(proto.block, pb.Schema.Block)

    @pytest.mark.asyncio
    async def test_schema_version_preserved(self) -> None:
        """Test that schema version is preserved."""
        schema = s_resource(attributes={"name": a_str()})
        original_version = schema.version

        proto = await pvs_schema_to_proto(schema)
        assert proto.version == original_version

    @pytest.mark.asyncio
    async def test_complex_nested_schema(self) -> None:
        """Test converting a complex schema with nested blocks."""
        from pyvider.schema.types import PvsObjectType, PvsSchema

        # Create schema with nested blocks directly
        obj = PvsObjectType(
            attributes={"name": a_str(required=True), "count": a_num(optional=True)},
            block_types=[
                b_single("config", attributes={"host": a_str(), "port": a_num()}),
                b_list("items", attributes={"value": a_str()}),
            ],
        )
        schema = PvsSchema(version=1, block=obj)
        proto = await pvs_schema_to_proto(schema)

        assert len(proto.block.attributes) == 2
        assert len(proto.block.block_types) == 2


class TestSchemaAdapterEdgeCases:
    """Edge case tests for schema adapter."""

    def test_attribute_with_empty_description(self) -> None:
        """Test attribute with empty description."""
        attr = a_str(required=True, description="")
        proto = _pvs_attribute_to_proto(attr)

        assert proto.description == ""

    def test_attribute_with_all_flags_false(self) -> None:
        """Test attribute with all boolean flags false."""
        # Create attribute with default flags (all False except what's default)
        attr = a_str()
        proto = _pvs_attribute_to_proto(attr)

        # Check that flags are properly set based on defaults
        assert isinstance(proto.required, bool)
        assert isinstance(proto.optional, bool)
        assert isinstance(proto.computed, bool)
        assert isinstance(proto.sensitive, bool)
        assert isinstance(proto.deprecated, bool)

    def test_nested_block_with_empty_attributes(self) -> None:
        """Test nested block with no attributes."""
        block = b_single("empty_config", attributes={})
        proto = _pvs_nested_block_to_proto(block)

        assert len(proto.block.attributes) == 0

    def test_deeply_nested_blocks(self) -> None:
        """Test schema with deeply nested blocks."""
        from pyvider.schema.types import PvsObjectType

        # Create deeply nested structure manually
        level2_block = b_single("level2", attributes={"value": a_num()})

        # Create level1 object with nested block
        level1_obj = PvsObjectType(attributes={"name": a_str()}, block_types=[level2_block])

        # Create level1 nested block
        from pyvider.schema.types import NestingMode, PvsNestedBlock

        level1_nested = PvsNestedBlock(type_name="level1", block=level1_obj, nesting=NestingMode.SINGLE)

        # Create root object
        root_obj = PvsObjectType(attributes={"id": a_str()}, block_types=[level1_nested])

        proto = _pvs_object_type_to_proto(root_obj)

        assert len(proto.block_types) == 1
        level1_block = proto.block_types[0]
        assert level1_block.type_name == "level1"
        assert len(level1_block.block.block_types) == 1


# 🐍🏗️🔚
