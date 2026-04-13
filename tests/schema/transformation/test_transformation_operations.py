#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.schema import (
    PvsAttribute,
    PvsSchema,
    a_bool,
    a_num,
    a_str,
    s_resource,
)
from pyvider.schema.transforms import PvsSchemaTransformer


@pytest.fixture
def base_schema() -> PvsSchema:
    return s_resource(
        {"name": a_str(required=True), "description": a_str(optional=True), "count": a_num(default=0)}
    )


class TestSchemaTransforms:
    def test_add_attribute(self, base_schema: PvsSchema) -> None:
        transformer = PvsSchemaTransformer()
        new_attr = a_bool(name="enabled", description="Whether the resource is enabled")
        new_schema = transformer.add_attribute(base_schema, new_attr)
        assert "enabled" in new_schema.block.attributes
        assert isinstance(new_schema.block.attributes["enabled"], PvsAttribute)

    def test_remove_attribute(self, base_schema: PvsSchema) -> None:
        transformer = PvsSchemaTransformer()
        new_schema = transformer.remove_attribute(base_schema, "description")
        attr_names = new_schema.block.attributes.keys()
        assert "description" not in attr_names
        assert "name" in attr_names

    def test_merge_schemas(self) -> None:
        transformer = PvsSchemaTransformer()
        schema1 = s_resource({"name": a_str(required=True)})
        schema2 = s_resource({"count": a_num(default=0)})
        merged_schema = transformer.merge_schemas([schema1, schema2], description="Merged")
        assert "name" in merged_schema.block.attributes
        assert "count" in merged_schema.block.attributes
        assert merged_schema.block.description == "Merged"


# 🐍🏗️🔚
