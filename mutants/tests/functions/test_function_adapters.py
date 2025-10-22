"""Tests for functions/adapters.py module (comprehensive coverage)."""

from decimal import Decimal
from typing import Any
from provide.testkit import mocking as mock

import pytest

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString, CtyValue
from pyvider.functions.adapters import (
    _extract_docstring_meta,
    _extract_parameters_meta,
    _extract_return_type_meta,
    _get_cty_type_for_dict,
    _get_cty_type_for_list,
    _get_cty_type_for_primitive,
    _get_cty_type_for_union,
    _is_dict_type,
    _is_list_type,
    _is_optional_type_hint,
    _is_union_type,
    _python_type_to_cty_type,
    function_to_dict,
)


class TestGetCtyTypeForPrimitive:
    """Tests for _get_cty_type_for_primitive function."""

    def test_str_returns_cty_string(self):
        """Test that str type returns CtyString."""
        result = _get_cty_type_for_primitive(str)
        assert isinstance(result, CtyString)

    def test_bool_returns_cty_bool(self):
        """Test that bool type returns CtyBool."""
        result = _get_cty_type_for_primitive(bool)
        assert isinstance(result, CtyBool)

    def test_int_returns_cty_number(self):
        """Test that int type returns CtyNumber."""
        result = _get_cty_type_for_primitive(int)
        assert isinstance(result, CtyNumber)

    def test_float_returns_cty_number(self):
        """Test that float type returns CtyNumber."""
        result = _get_cty_type_for_primitive(float)
        assert isinstance(result, CtyNumber)

    def test_decimal_returns_cty_number(self):
        """Test that Decimal type returns CtyNumber."""
        result = _get_cty_type_for_primitive(Decimal)
        assert isinstance(result, CtyNumber)

    def test_unsupported_type_returns_none(self):
        """Test that unsupported types return None."""
        result = _get_cty_type_for_primitive(bytes)
        assert result is None


class TestGetCtyTypeForList:
    """Tests for _get_cty_type_for_list function."""

    def test_list_with_str_element_type(self):
        """Test list with string element type."""
        result = _get_cty_type_for_list(list[str], (str,))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyString)

    def test_list_with_int_element_type(self):
        """Test list with int element type."""
        result = _get_cty_type_for_list(list[int], (int,))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyNumber)

    def test_list_without_element_type_uses_dynamic(self):
        """Test that list without element type uses CtyDynamic."""
        result = _get_cty_type_for_list(list, ())
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyDynamic)

    def test_nested_list(self):
        """Test nested list type."""
        result = _get_cty_type_for_list(list[list[str]], (list[str],))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyList)


class TestGetCtyTypeForDict:
    """Tests for _get_cty_type_for_dict function."""

    def test_dict_with_str_value_type(self):
        """Test dict with string value type."""
        result = _get_cty_type_for_dict(dict[str, str], (str, str))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyString)

    def test_dict_with_int_value_type(self):
        """Test dict with int value type."""
        result = _get_cty_type_for_dict(dict[str, int], (str, int))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyNumber)

    def test_dict_without_args_uses_dynamic(self):
        """Test that dict without args uses CtyDynamic."""
        result = _get_cty_type_for_dict(dict, ())
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyDynamic)

    def test_dict_with_only_key_type_uses_dynamic(self):
        """Test dict with only key type uses CtyDynamic for value."""
        result = _get_cty_type_for_dict(dict[str], (str,))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyDynamic)


class TestGetCtyTypeForUnion:
    """Tests for _get_cty_type_for_union function."""

    def test_union_of_numeric_types_returns_number(self):
        """Test that union of numeric types returns CtyNumber."""
        result = _get_cty_type_for_union(int | float, (int, float))
        assert isinstance(result, CtyNumber)

    def test_union_with_int_float_decimal_returns_number(self):
        """Test that union with int, float, Decimal returns CtyNumber."""
        result = _get_cty_type_for_union(int | float | Decimal, (int, float, Decimal))
        assert isinstance(result, CtyNumber)

    def test_union_with_none_and_single_type(self):
        """Test union with None and single type (Optional)."""
        result = _get_cty_type_for_union(str | None, (str, type(None)))
        assert isinstance(result, CtyString)

    def test_union_with_none_and_int(self):
        """Test union with None and int (Optional[int])."""
        result = _get_cty_type_for_union(int | None, (int, type(None)))
        assert isinstance(result, CtyNumber)

    def test_union_of_different_types_returns_dynamic(self):
        """Test that union of different types returns CtyDynamic."""
        result = _get_cty_type_for_union(str | int, (str, int))
        assert isinstance(result, CtyDynamic)

    def test_union_of_multiple_different_types_returns_dynamic(self):
        """Test union of multiple different types returns CtyDynamic."""
        result = _get_cty_type_for_union(str | int | bool, (str, int, bool))
        assert isinstance(result, CtyDynamic)


class TestIsUnionType:
    """Tests for _is_union_type function."""

    def test_detects_union_type(self):
        """Test that it detects union types."""
        assert _is_union_type(str | int) is True

    def test_detects_typing_union(self):
        """Test that it detects typing.Union."""
        from typing import Union
        assert _is_union_type(Union[str, int]) is True

    def test_non_union_returns_false(self):
        """Test that non-union types return False."""
        assert _is_union_type(str) is False
        assert _is_union_type(int) is False
        assert _is_union_type(list) is False


class TestIsListType:
    """Tests for _is_list_type function."""

    def test_detects_list_type(self):
        """Test that it detects list type."""
        assert _is_list_type(list) is True

    def test_detects_parameterized_list(self):
        """Test that it detects parameterized list."""
        assert _is_list_type(list[str]) is True

    def test_non_list_returns_false(self):
        """Test that non-list types return False."""
        assert _is_list_type(dict) is False
        assert _is_list_type(str) is False


class TestIsDictType:
    """Tests for _is_dict_type function."""

    def test_detects_dict_type(self):
        """Test that it detects dict type."""
        assert _is_dict_type(dict) is True

    def test_detects_parameterized_dict(self):
        """Test that it detects parameterized dict."""
        assert _is_dict_type(dict[str, int]) is True

    def test_non_dict_returns_false(self):
        """Test that non-dict types return False."""
        assert _is_dict_type(list) is False
        assert _is_dict_type(str) is False


class TestPythonTypeToCtyType:
    """Tests for _python_type_to_cty_type function."""

    def test_any_type_returns_dynamic(self):
        """Test that Any type returns CtyDynamic."""
        result = _python_type_to_cty_type(Any)
        assert isinstance(result, CtyDynamic)

    def test_cty_value_returns_dynamic(self):
        """Test that CtyValue type returns CtyDynamic."""
        result = _python_type_to_cty_type(CtyValue)
        assert isinstance(result, CtyDynamic)

    def test_str_type_returns_cty_string(self):
        """Test that str type returns CtyString."""
        result = _python_type_to_cty_type(str)
        assert isinstance(result, CtyString)

    def test_int_type_returns_cty_number(self):
        """Test that int type returns CtyNumber."""
        result = _python_type_to_cty_type(int)
        assert isinstance(result, CtyNumber)

    def test_bool_type_returns_cty_bool(self):
        """Test that bool type returns CtyBool."""
        result = _python_type_to_cty_type(bool)
        assert isinstance(result, CtyBool)

    def test_list_str_returns_cty_list(self):
        """Test that list[str] returns CtyList."""
        result = _python_type_to_cty_type(list[str])
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyString)

    def test_dict_str_int_returns_cty_map(self):
        """Test that dict[str, int] returns CtyMap."""
        result = _python_type_to_cty_type(dict[str, int])
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyNumber)

    def test_optional_str_returns_cty_string(self):
        """Test that Optional[str] returns CtyString."""
        result = _python_type_to_cty_type(str | None)
        assert isinstance(result, CtyString)

    @mock.patch("pyvider.functions.adapters.logger")
    def test_unknown_type_logs_warning(self, mock_logger):
        """Test that unknown types log a warning."""
        class CustomType:
            pass

        result = _python_type_to_cty_type(CustomType)
        assert isinstance(result, CtyDynamic)
        assert mock_logger.warning.called


class TestIsOptionalTypeHint:
    """Tests for _is_optional_type_hint function."""

    def test_detects_optional_type(self):
        """Test that it detects Optional types."""
        assert _is_optional_type_hint(str | None) is True

    def test_non_optional_returns_false(self):
        """Test that non-Optional types return False."""
        assert _is_optional_type_hint(str) is False
        assert _is_optional_type_hint(int) is False

    def test_union_without_none_returns_false(self):
        """Test that union without None returns False."""
        assert _is_optional_type_hint(str | int) is False


class TestExtractParametersMeta:
    """Tests for _extract_parameters_meta function."""

    def test_extracts_required_parameter(self):
        """Test extracting required parameter."""
        import inspect

        def test_func(name: str):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"
        assert isinstance(result["parameters"][0]["cty_type"], CtyString)
        assert result["parameters"][0]["allow_null"] is False

    def test_extracts_optional_parameter(self):
        """Test extracting optional parameter."""
        import inspect

        def test_func(name: str | None):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str | None}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["allow_null"] is True

    def test_extracts_parameter_with_default_as_variadic(self):
        """Test that parameter with default becomes variadic."""
        import inspect

        def test_func(name: str, count: int = 10):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "count": int}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        # name should be required
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

        # count should be variadic
        assert result["variadic_parameter"] is not None
        assert result["variadic_parameter"]["name"] == "count"
        assert result["variadic_parameter"]["allow_null"] is True

    def test_extracts_var_positional_as_variadic(self):
        """Test extracting *args as variadic parameter."""
        import inspect

        def test_func(name: str, *values: int):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "values": int}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["variadic_parameter"] is not None
        assert result["variadic_parameter"]["name"] == "values"

    def test_skips_keyword_only_parameters(self):
        """Test that keyword-only parameters are skipped."""
        import inspect

        def test_func(name: str, *, internal: str = "test"):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "internal": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        # Only name should be extracted
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

    def test_skips_self_parameter(self):
        """Test that self parameter is skipped."""
        import inspect

        class TestClass:
            def test_method(self, name: str):
                pass

        method = TestClass().test_method
        sig = inspect.signature(method)
        type_hints = {"name": str}
        result = _extract_parameters_meta(method, sig, type_hints)

        # self should be skipped, only name
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

    @mock.patch("pyvider.functions.adapters.logger")
    def test_warns_on_multiple_defaults(self, mock_logger):
        """Test warning on multiple default parameters."""
        import inspect

        def test_func(name: str = "default1", count: int = 10):
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "count": int}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        # Should log a warning
        assert mock_logger.warning.called

    def test_uses_parameter_descriptions_from_metadata(self):
        """Test that parameter descriptions come from metadata."""
        import inspect

        def test_func(name: str):
            pass

        test_func._function_metadata = {
            "param_descriptions": {"name": "The name parameter"}
        }

        sig = inspect.signature(test_func)
        type_hints = {"name": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert result["parameters"][0]["description"] == "The name parameter"


class TestExtractReturnTypeMeta:
    """Tests for _extract_return_type_meta function."""

    def test_extracts_str_return_type(self):
        """Test extracting str return type."""
        type_hints = {"return": str}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyString)

    def test_extracts_int_return_type(self):
        """Test extracting int return type."""
        type_hints = {"return": int}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyNumber)

    def test_defaults_to_dynamic_when_no_return_type(self):
        """Test that missing return type defaults to CtyDynamic."""
        type_hints = {}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyDynamic)


class TestExtractDocstringMeta:
    """Tests for _extract_docstring_meta function."""

    def test_extracts_summary_from_docstring(self):
        """Test extracting summary from docstring."""
        def test_func():
            """This is the summary line.

            This is more detail.
            """
            pass

        base_meta = {}
        _extract_docstring_meta(test_func, base_meta)

        assert base_meta["summary"] == "This is the summary line."
        assert "This is more detail" in base_meta["description"]

    def test_preserves_existing_summary(self):
        """Test that existing summary is preserved."""
        def test_func():
            """Docstring summary."""
            pass

        base_meta = {"summary": "Existing summary"}
        _extract_docstring_meta(test_func, base_meta)

        assert base_meta["summary"] == "Existing summary"

    def test_handles_missing_docstring(self):
        """Test handling functions without docstring."""
        def test_func():
            pass

        base_meta = {}
        _extract_docstring_meta(test_func, base_meta)

        # Should not crash, may not add summary/description
        assert "summary" not in base_meta or base_meta["summary"] == ""


class TestFunctionToDict:
    """Tests for function_to_dict function."""

    def test_converts_simple_function(self):
        """Test converting a simple function."""
        def test_func(name: str) -> str:
            """Test function."""
            return name

        result = function_to_dict(test_func)

        assert result["name"] == "test_func"
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"
        assert isinstance(result["return"]["cty_type"], CtyString)

    def test_uses_existing_metadata(self):
        """Test that existing metadata is used."""
        def test_func(name: str):
            pass

        test_func._function_metadata = {"name": "custom_name"}

        result = function_to_dict(test_func)

        assert result["name"] == "custom_name"

    def test_handles_function_with_defaults(self):
        """Test function with default parameters."""
        def test_func(name: str, count: int = 10) -> int:
            return count

        result = function_to_dict(test_func)

        assert len(result["parameters"]) == 1
        assert result["variadic_parameter"]["name"] == "count"

    @mock.patch("pyvider.functions.adapters.logger")
    def test_handles_type_hint_resolution_errors(self, mock_logger):
        """Test handling type hint resolution errors."""
        def test_func(name):  # No type hints
            pass

        result = function_to_dict(test_func)

        # Should still work but with dynamic types
        assert result["name"] == "test_func"

    def test_includes_docstring_in_output(self):
        """Test that docstring is included in output."""
        def test_func(name: str):
            """This function does something."""
            pass

        result = function_to_dict(test_func)

        assert "description" in result
        assert "This function does something" in result["description"]
