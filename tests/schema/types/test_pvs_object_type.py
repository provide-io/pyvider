#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.cty import CtyNumber, CtyObject, CtyString
from pyvider.schema.factory import a_num, a_str
from pyvider.schema.types import PvsObjectType


class TestPvsObjectType:
    def test_pvs_object_type_creation(self) -> None:
        attrs = {"name": a_str(required=True), "age": a_num(optional=True)}
        obj_type = PvsObjectType(attributes=attrs, description="A person object")
        assert obj_type.description == "A person object"
        assert len(obj_type.attributes) == 2

    def test_to_cty_type_conversion(self) -> None:
        attrs = {"name": a_str(required=True), "age": a_num(optional=True)}
        obj_type = PvsObjectType(attributes=attrs)
        cty_obj = obj_type.to_cty_type()
        assert isinstance(cty_obj, CtyObject)
        assert len(cty_obj.attribute_types) == 2
        assert isinstance(cty_obj.attribute_types["name"], CtyString)
        assert isinstance(cty_obj.attribute_types["age"], CtyNumber)
        assert "age" in cty_obj.optional_attributes
        assert "name" not in cty_obj.optional_attributes

    def test_pvs_object_type_behaves_as_a_validator(self) -> None:
        attrs = {"name": a_str(required=True)}
        obj_type = PvsObjectType(attributes=attrs)
        cty_type = obj_type.to_cty_type()
        # This test now correctly checks that the *converted* CtyType can validate
        validated = cty_type.validate({"name": "test"})
        assert validated["name"].value == "test"


# 🐍🏗️🔚
