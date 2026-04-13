#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.cty import CtyDynamic, CtyObject, CtyString, CtyValue
from pyvider.schema.factory import a_str, a_unknown


class TestCtyValidationRecursion:
    def test_cty_dynamic_validation_avoids_recursion_with_ctyvalue(self) -> None:
        """
        TDD Contract: Verifies that CtyDynamic.validate() does not enter an
        infinite recursion loop when it encounters a raw value that is
        already a CtyValue instance (e.g., an 'unknown' sentinel).
        """
        # Arrange: A schema with a dynamic attribute and input containing a CtyValue.
        schema = CtyObject({"data": CtyDynamic()})
        raw_input_with_sentinel = {"data": a_unknown(a_str())}

        try:
            # Act: Validate the raw input against the schema.
            result = schema.validate(raw_input_with_sentinel)

            # Assert: The validation must succeed and produce a correctly typed value.
            # The value for 'data' should be a CtyValue of type CtyDynamic.
            dynamic_value = result.value["data"]
            assert isinstance(dynamic_value, CtyValue)
            assert isinstance(dynamic_value.type, CtyDynamic)

            # The dynamic value itself should correctly report that it contains an unknown value.
            assert dynamic_value.is_unknown

            # We can inspect the inner concrete value for more detail.
            concrete_value = dynamic_value.value
            assert isinstance(concrete_value, CtyValue)
            assert concrete_value.is_unknown
            assert concrete_value.type.equal(CtyString())

        except RecursionError:
            pytest.fail("CtyDynamic.validate() caused a RecursionError.")


# 🐍🏗️🔚
