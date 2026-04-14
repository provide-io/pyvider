#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for functions/adapters.py module (comprehensive coverage)."""

from decimal import Decimal
from typing import Any
from unittest.mock import MagicMock

from provide.testkit import mocking as mock

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString, CtyValue
from pyvider.functions.adapters import (
    _get_cty_type_for_dict,
    _get_cty_type_for_list,
    _get_cty_type_for_primitive,
    _get_cty_type_for_union,
    _is_dict_type,
    _is_list_type,
    _is_optional_type_hint,
    _is_union_type,
    _python_type_to_cty_type,
)


class TestGetCtyTypeForPrimitive:
    """Tests for _get_cty_type_for_primitive function."""

    def test_str_returns_cty_string(self) -> None:
        """Test that str type returns CtyString."""
        result = _get_cty_type_for_primitive(str)
        assert isinstance(result, CtyString)

    def test_bool_returns_cty_bool(self) -> None:
        """Test that bool type returns CtyBool."""
        result = _get_cty_type_for_primitive(bool)
        assert isinstance(result, CtyBool)

    def test_int_returns_cty_number(self) -> None:
        """Test that int type returns CtyNumber."""
        result = _get_cty_type_for_primitive(int)
        assert isinstance(result, CtyNumber)

    def test_float_returns_cty_number(self) -> None:
        """Test that float type returns CtyNumber."""
        result = _get_cty_type_for_primitive(float)
        assert isinstance(result, CtyNumber)

    def test_decimal_returns_cty_number(self) -> None:
        """Test that Decimal type returns CtyNumber."""
        result = _get_cty_type_for_primitive(Decimal)
        assert isinstance(result, CtyNumber)

    def test_unsupported_type_returns_none(self) -> None:
        """Test that unsupported types return None."""
        result = _get_cty_type_for_primitive(bytes)
        assert result is None


class TestGetCtyTypeForList:
    """Tests for _get_cty_type_for_list function."""

    def test_list_with_str_element_type(self) -> None:
        """Test list with string element type."""
        result = _get_cty_type_for_list(list[str], (str,))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyString)

    def test_list_with_int_element_type(self) -> None:
        """Test list with int element type."""
        result = _get_cty_type_for_list(list[int], (int,))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyNumber)

    def test_list_without_element_type_uses_dynamic(self) -> None:
        """Test that list without element type uses CtyDynamic."""
        result = _get_cty_type_for_list(list, ())
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyDynamic)

    def test_nested_list(self) -> None:
        """Test nested list type."""
        result = _get_cty_type_for_list(list[list[str]], (list[str],))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyList)


class TestGetCtyTypeForDict:
    """Tests for _get_cty_type_for_dict function."""

    def test_dict_with_str_value_type(self) -> None:
        """Test dict with string value type."""
        result = _get_cty_type_for_dict(dict[str, str], (str, str))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyString)

    def test_dict_with_int_value_type(self) -> None:
        """Test dict with int value type."""
        result = _get_cty_type_for_dict(dict[str, int], (str, int))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyNumber)

    def test_dict_without_args_uses_dynamic(self) -> None:
        """Test that dict without args uses CtyDynamic."""
        result = _get_cty_type_for_dict(dict, ())
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyDynamic)

    def test_dict_with_only_key_type_uses_dynamic(self) -> None:
        """Test dict with only key type uses CtyDynamic for value."""
        result = _get_cty_type_for_dict(dict[str], (str,))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyDynamic)


class TestGetCtyTypeForUnion:
    """Tests for _get_cty_type_for_union function."""

    def test_union_of_numeric_types_returns_number(self) -> None:
        """Test that union of numeric types returns CtyNumber."""
        result = _get_cty_type_for_union(int | float, (int, float))
        assert isinstance(result, CtyNumber)

    def test_union_with_int_float_decimal_returns_number(self) -> None:
        """Test that union with int, float, Decimal returns CtyNumber."""
        result = _get_cty_type_for_union(int | float | Decimal, (int, float, Decimal))
        assert isinstance(result, CtyNumber)

    def test_union_with_none_and_single_type(self) -> None:
        """Test union with None and single type (Optional)."""
        result = _get_cty_type_for_union(str | None, (str, type(None)))
        assert isinstance(result, CtyString)

    def test_union_with_none_and_int(self) -> None:
        """Test union with None and int (Optional[int])."""
        result = _get_cty_type_for_union(int | None, (int, type(None)))
        assert isinstance(result, CtyNumber)

    def test_union_of_different_types_returns_dynamic(self) -> None:
        """Test that union of different types returns CtyDynamic."""
        result = _get_cty_type_for_union(str | int, (str, int))
        assert isinstance(result, CtyDynamic)

    def test_union_of_multiple_different_types_returns_dynamic(self) -> None:
        """Test union of multiple different types returns CtyDynamic."""
        result = _get_cty_type_for_union(str | int | bool, (str, int, bool))
        assert isinstance(result, CtyDynamic)


class TestIsUnionType:
    """Tests for _is_union_type function."""

    def test_detects_union_type(self) -> None:
        """Test that it detects union types."""
        assert _is_union_type(str | int) is True

    def test_detects_typing_union(self) -> None:
        """Test that it detects typing.Union."""

        assert _is_union_type(str | int) is True

    def test_non_union_returns_false(self) -> None:
        """Test that non-union types return False."""
        assert _is_union_type(str) is False
        assert _is_union_type(int) is False
        assert _is_union_type(list) is False


class TestIsListType:
    """Tests for _is_list_type function."""

    def test_detects_list_type(self) -> None:
        """Test that it detects list type."""
        assert _is_list_type(list) is True

    def test_detects_parameterized_list(self) -> None:
        """Test that it detects parameterized list."""
        assert _is_list_type(list[str]) is True

    def test_non_list_returns_false(self) -> None:
        """Test that non-list types return False."""
        assert _is_list_type(dict) is False
        assert _is_list_type(str) is False


class TestIsDictType:
    """Tests for _is_dict_type function."""

    def test_detects_dict_type(self) -> None:
        """Test that it detects dict type."""
        assert _is_dict_type(dict) is True

    def test_detects_parameterized_dict(self) -> None:
        """Test that it detects parameterized dict."""
        assert _is_dict_type(dict[str, int]) is True

    def test_non_dict_returns_false(self) -> None:
        """Test that non-dict types return False."""
        assert _is_dict_type(list) is False
        assert _is_dict_type(str) is False


class TestPythonTypeToCtyType:
    """Tests for _python_type_to_cty_type function."""

    def test_any_type_returns_dynamic(self) -> None:
        """Test that Any type returns CtyDynamic."""
        result = _python_type_to_cty_type(Any)
        assert isinstance(result, CtyDynamic)

    def test_cty_value_returns_dynamic(self) -> None:
        """Test that CtyValue type returns CtyDynamic."""
        result = _python_type_to_cty_type(CtyValue)
        assert isinstance(result, CtyDynamic)

    def test_str_type_returns_cty_string(self) -> None:
        """Test that str type returns CtyString."""
        result = _python_type_to_cty_type(str)
        assert isinstance(result, CtyString)

    def test_int_type_returns_cty_number(self) -> None:
        """Test that int type returns CtyNumber."""
        result = _python_type_to_cty_type(int)
        assert isinstance(result, CtyNumber)

    def test_bool_type_returns_cty_bool(self) -> None:
        """Test that bool type returns CtyBool."""
        result = _python_type_to_cty_type(bool)
        assert isinstance(result, CtyBool)

    def test_list_str_returns_cty_list(self) -> None:
        """Test that list[str] returns CtyList."""
        result = _python_type_to_cty_type(list[str])
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyString)

    def test_dict_str_int_returns_cty_map(self) -> None:
        """Test that dict[str, int] returns CtyMap."""
        result = _python_type_to_cty_type(dict[str, int])
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyNumber)

    def test_optional_str_returns_cty_string(self) -> None:
        """Test that Optional[str] returns CtyString."""
        result = _python_type_to_cty_type(str | None)
        assert isinstance(result, CtyString)

    @mock.patch("pyvider.functions.adapters.logger")
    def test_unknown_type_logs_warning(self, mock_logger: MagicMock) -> None:
        """Test that unknown types log a warning."""

        class CustomType:
            pass

        result = _python_type_to_cty_type(CustomType)
        assert isinstance(result, CtyDynamic)
        assert mock_logger.warning.called


class TestIsOptionalTypeHint:
    """Tests for _is_optional_type_hint function."""

    def test_detects_optional_type(self) -> None:
        """Test that it detects Optional types."""
        assert _is_optional_type_hint(str | None) is True

    def test_non_optional_returns_false(self) -> None:
        """Test that non-Optional types return False."""
        assert _is_optional_type_hint(str) is False
        assert _is_optional_type_hint(int) is False

    def test_union_without_none_returns_false(self) -> None:
        """Test that union without None returns False."""
        assert _is_optional_type_hint(str | int) is False


# 🐍🏗️🔚
