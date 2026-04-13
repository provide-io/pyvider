#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.conversion import cty_to_native
from pyvider.cty import CtyList, CtyMap, CtyNumber, CtyObject, CtyString


class TestCtyToNativeConversion:
    """
    TDD: These tests target the `cty_to_native` conversion function, which is
    the suspected root cause of the string and JQ function failures.
    """

    def test_cty_to_native_on_list_of_primitives(self) -> None:
        """
        TDD 1: Verifies that a CtyValue containing a list of CtyStrings is
        correctly unwrapped to a native Python list[str].
        """
        list_type = CtyList(element_type=CtyString())
        cty_value = list_type.validate(["hello", "world"])

        native_result = cty_to_native(cty_value)

        # The result must be a list of plain Python strings.
        assert native_result == ["hello", "world"]
        assert isinstance(native_result, list)
        assert all(isinstance(item, str) for item in native_result)

    def test_cty_to_native_on_map_of_primitives(self) -> None:
        """
        TDD 2: Verifies that a CtyValue containing a map of CtyNumbers is
        correctly unwrapped to a native Python dict[str, int | float].
        """
        map_type = CtyMap(element_type=CtyNumber())
        cty_value = map_type.validate({"a": 10, "b": 20.5})

        native_result = cty_to_native(cty_value)

        # The result must be a dict of plain Python numbers.
        assert native_result == {"a": 10, "b": 20.5}
        assert isinstance(native_result, dict)
        assert isinstance(native_result["a"], int)
        assert isinstance(native_result["b"], float)

    def test_cty_to_native_on_complex_nested_object(self) -> None:
        """
        TDD 3: Verifies that `cty_to_native` works recursively on a complex,
        deeply nested data structure.
        """
        complex_type = CtyObject(
            attribute_types={
                "name": CtyString(),
                "config": CtyMap(element_type=CtyNumber()),
                "tags": CtyList(element_type=CtyString()),
                "sub_items": CtyList(element_type=CtyObject(attribute_types={"id": CtyString()})),
            }
        )

        data = {
            "name": "complex-item",
            "config": {"timeout": 30, "retries": 5},
            "tags": ["prod", "api"],
            "sub_items": [{"id": "sub1"}, {"id": "sub2"}],
        }

        cty_value = complex_type.validate(data)
        native_result = cty_to_native(cty_value)

        # The entire structure should be native Python types.
        assert native_result == data
        assert isinstance(native_result["config"], dict)
        assert isinstance(native_result["tags"], list)
        assert isinstance(native_result["sub_items"][0], dict)
        assert isinstance(native_result["sub_items"][0]["id"], str)


# 🐍🏗️🔚
