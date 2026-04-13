#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider/schema/transforms.py."""

import pytest

from pyvider.schema import a_num, a_str, s_resource
from pyvider.schema.transforms import PvsSchemaTransformer
from pyvider.schema.types.blocks import PvsNestedBlock
from pyvider.schema.types.object import PvsObjectType
from pyvider.schema.types.schema import PvsSchema


class TestPvsSchemaTransformer:
    """Tests for PvsSchemaTransformer class."""

    def test_add_attribute_to_schema(self) -> None:
        """Test adding a new attribute to a schema."""
        schema = s_resource(attributes={"name": a_str()})
        transformer = PvsSchemaTransformer()

        new_attr = a_num(name="count")
        updated_schema = transformer.add_attribute(schema, new_attr)

        assert "name" in updated_schema.block.attributes
        assert "count" in updated_schema.block.attributes

    def test_add_duplicate_attribute_raises_error(self) -> None:
        """Test that adding a duplicate attribute raises ValueError."""
        schema = s_resource(attributes={"name": a_str()})
        transformer = PvsSchemaTransformer()

        # Try to add an attribute with the same name
        duplicate_attr = a_str(name="name")
        with pytest.raises(ValueError, match="already exists"):
            transformer.add_attribute(schema, duplicate_attr)

    def test_remove_attribute_from_schema(self) -> None:
        """Test removing an attribute from a schema."""
        schema = s_resource(attributes={"name": a_str(), "count": a_num()})
        transformer = PvsSchemaTransformer()

        updated_schema = transformer.remove_attribute(schema, "count")

        assert "name" in updated_schema.block.attributes
        assert "count" not in updated_schema.block.attributes

    def test_remove_nonexistent_attribute_raises_error(self) -> None:
        """Test that removing a non-existent attribute raises ValueError."""
        schema = s_resource(attributes={"name": a_str()})
        transformer = PvsSchemaTransformer()

        with pytest.raises(ValueError, match="not found"):
            transformer.remove_attribute(schema, "nonexistent")

    def test_merge_schemas_combines_attributes(self) -> None:
        """Test merging multiple schemas combines their attributes."""
        schema1 = s_resource(attributes={"name": a_str()})
        schema2 = s_resource(attributes={"count": a_num()})
        transformer = PvsSchemaTransformer()

        merged = transformer.merge_schemas([schema1, schema2])

        assert "name" in merged.block.attributes
        assert "count" in merged.block.attributes

    def test_merge_schemas_with_attribute_conflict_raises_error(self) -> None:
        """Test that merging schemas with conflicting attribute names raises ValueError."""
        schema1 = s_resource(attributes={"name": a_str()})
        schema2 = s_resource(attributes={"name": a_num()})
        transformer = PvsSchemaTransformer()

        with pytest.raises(ValueError, match=r"Cannot merge schemas.*attribute name conflict"):
            transformer.merge_schemas([schema1, schema2])

    def test_merge_schemas_with_description(self) -> None:
        """Test merging schemas with a custom description."""
        schema1 = s_resource(attributes={"name": a_str()})
        schema2 = s_resource(attributes={"count": a_num()})
        transformer = PvsSchemaTransformer()

        merged = transformer.merge_schemas([schema1, schema2], description="Merged schema")

        assert merged.block.description == "Merged schema"

    def test_merge_schemas_with_block_type_conflict_raises_error(self) -> None:
        """Test that merging schemas with conflicting block type names raises ValueError."""
        # Create schemas with block types that have the same name
        from pyvider.schema.types.blocks import NestingMode

        block_type1 = PvsNestedBlock(
            type_name="config",
            nesting=NestingMode.SINGLE,
            block=PvsObjectType(attributes={"value1": a_str()}),
        )
        block_type2 = PvsNestedBlock(
            type_name="config",
            nesting=NestingMode.SINGLE,
            block=PvsObjectType(attributes={"value2": a_str()}),
        )

        schema1 = PvsSchema(
            version=1,
            block=PvsObjectType(attributes={}, block_types=(block_type1,)),
        )
        schema2 = PvsSchema(
            version=1,
            block=PvsObjectType(attributes={}, block_types=(block_type2,)),
        )

        transformer = PvsSchemaTransformer()

        with pytest.raises(ValueError, match=r"Cannot merge schemas.*block type name conflict"):
            transformer.merge_schemas([schema1, schema2])

    def test_merge_schemas_preserves_block_types(self) -> None:
        """Test that merging schemas preserves block types when there's no conflict."""
        from pyvider.schema.types.blocks import NestingMode

        block_type1 = PvsNestedBlock(
            type_name="config1",
            nesting=NestingMode.SINGLE,
            block=PvsObjectType(attributes={"value1": a_str()}),
        )
        block_type2 = PvsNestedBlock(
            type_name="config2",
            nesting=NestingMode.SINGLE,
            block=PvsObjectType(attributes={"value2": a_str()}),
        )

        schema1 = PvsSchema(
            version=1,
            block=PvsObjectType(attributes={"name": a_str()}, block_types=(block_type1,)),
        )
        schema2 = PvsSchema(
            version=1,
            block=PvsObjectType(attributes={"count": a_num()}, block_types=(block_type2,)),
        )

        transformer = PvsSchemaTransformer()
        merged = transformer.merge_schemas([schema1, schema2])

        assert len(merged.block.block_types) == 2
        block_type_names = {bt.type_name for bt in merged.block.block_types}
        assert "config1" in block_type_names
        assert "config2" in block_type_names


# 🐍🏗️🔚
