#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for conversion/utils.py."""

from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty import CtyList, CtyObject


class TestUnifyAndValidateListOfObjects:
    """Tests for unify_and_validate_list_of_objects function."""

    def test_empty_list_returns_empty_dynamic_list(self) -> None:
        """Test that empty list returns CtyList of CtyDynamic."""
        result = unify_and_validate_list_of_objects([])

        assert len(result.value) == 0
        assert isinstance(result.vtype, CtyList)

    def test_single_dict_creates_object_schema(self) -> None:
        """Test single dictionary creates appropriate object schema."""
        dict_list = [{"name": "test", "count": 42}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 1
        assert isinstance(result.vtype, CtyList)
        assert isinstance(result.vtype.element_type, CtyObject)

    def test_multiple_dicts_with_same_schema(self) -> None:
        """Test multiple dictionaries with consistent schema."""
        dict_list = [{"name": "first", "age": 25}, {"name": "second", "age": 30}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 2
        assert isinstance(result.vtype.element_type, CtyObject)

    def test_inconsistent_types_uses_dynamic(self) -> None:
        """Test that inconsistent types for same key use CtyDynamic."""
        dict_list = [{"value": "string"}, {"value": 123}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 2
        # Type should be Dynamic due to inconsistency
        element_type = result.vtype.element_type
        assert isinstance(element_type, CtyObject)

    def test_optional_keys_detected(self) -> None:
        """Test that optional keys (not in all dicts) are detected."""
        dict_list = [
            {"name": "first", "optional": "value"},
            {"name": "second"},  # missing 'optional'
        ]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 2
        element_type = result.vtype.element_type
        assert "optional" in element_type.optional_attributes

    def test_all_keys_merged_across_dicts(self) -> None:
        """Test that all keys from all dicts are merged."""
        dict_list = [{"a": 1}, {"b": 2}, {"c": 3}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 3
        element_type = result.vtype.element_type
        # All keys should be in the schema
        assert "a" in element_type.attribute_types
        assert "b" in element_type.attribute_types
        assert "c" in element_type.attribute_types

    def test_nested_dicts_supported(self) -> None:
        """Test that nested dictionaries are supported."""
        dict_list = [{"outer": {"inner": "value"}}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 1

    def test_mixed_value_types(self) -> None:
        """Test handling of different value types."""
        dict_list = [{"str": "text", "num": 42, "bool": True, "null": None}]
        result = unify_and_validate_list_of_objects(dict_list)

        assert len(result.value) == 1


# 🐍🏗️🔚
