#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.cty import CtyList, CtyMap, CtyObject, CtySet
from pyvider.schema import a_str, b_list, b_map, b_set, s_resource


def test_pvs_object_type_conversion_handles_nested_blocks() -> None:
    """
    TDD Contract: Verifies that PvsObjectType.to_cty_type correctly converts
    nested block definitions (b_list, b_set, b_map) into the appropriate
    collection attributes on the resulting CtyObject.
    """
    # GIVEN a schema with various nested block types
    schema = s_resource(
        attributes={"id": a_str(required=True)},
        block_types=[
            b_list("users", attributes={"name": a_str()}),
            b_set("tags", attributes={"value": a_str()}),
            b_map("headers", attributes={"value": a_str()}),
        ],
    )

    # WHEN we convert the schema's block to a CtyType
    cty_type = schema.block.to_cty_type()

    # THEN the CtyType must be a CtyObject
    assert isinstance(cty_type, CtyObject)

    # AND it must have attributes corresponding to the nested blocks
    assert "users" in cty_type.attribute_types
    assert "tags" in cty_type.attribute_types
    assert "headers" in cty_type.attribute_types

    # AND the types of those attributes must be correct Cty collection types
    assert isinstance(cty_type.attribute_types["users"], CtyList)
    assert isinstance(cty_type.attribute_types["tags"], CtySet)
    assert isinstance(cty_type.attribute_types["headers"], CtyMap)

    # AND the element types of those collections must be CtyObjects
    assert isinstance(cty_type.attribute_types["users"].element_type, CtyObject)


# 🐍🏗️🔚
