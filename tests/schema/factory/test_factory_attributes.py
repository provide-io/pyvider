#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.cty import CtyObject
from pyvider.schema import a_num, a_obj, a_str
from pyvider.schema.types import PvsAttribute


class TestAttributeFactoriesCoverage:
    def test_a_obj_attribute_type_variations(self) -> None:
        """Test a_obj returns a PvsAttribute whose type is a CtyObject."""
        # a_obj now correctly returns a PvsAttribute instance.
        obj_attr_factory_instance = a_obj({"description": a_str(), "count": a_num(required=True)})

        # The instance itself is a PvsAttribute
        assert isinstance(obj_attr_factory_instance, PvsAttribute)

        # The .type property of that attribute is the CtyObject
        assert isinstance(obj_attr_factory_instance.type, CtyObject)

        # Check that optionality was correctly inferred for the inner attributes
        # of the CtyObject type.
        cty_obj_type = obj_attr_factory_instance.type
        assert "description" in cty_obj_type.optional_attributes
        assert "count" not in cty_obj_type.optional_attributes


# 🐍🏗️🔚
