#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Property-based tests for function adapters using Hypothesis."""

from hypothesis import given, strategies as st
import pytest

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.functions.adapters import (
    _is_optional_type_hint,
    _python_type_to_cty_type,
    function_to_dict,
)


class TestPythonTypeToCtyTypePropertyBased:
    """Property-based tests for Python to CTY type conversion."""

    @given(value=st.text())
    def test_str_type_always_produces_cty_string(self, value: str) -> None:
        """Property: str type should always produce CtyString."""
        cty_type = _python_type_to_cty_type(str)
        assert isinstance(cty_type, CtyString)

    @given(value=st.integers())
    def test_int_type_always_produces_cty_number(self, value: int) -> None:
        """Property: int type should always produce CtyNumber."""
        cty_type = _python_type_to_cty_type(int)
        assert isinstance(cty_type, CtyNumber)

    @given(value=st.floats(allow_nan=False, allow_infinity=False))
    def test_float_type_always_produces_cty_number(self, value: float) -> None:
        """Property: float type should always produce CtyNumber."""
        cty_type = _python_type_to_cty_type(float)
        assert isinstance(cty_type, CtyNumber)

    @given(value=st.booleans())
    def test_bool_type_always_produces_cty_bool(self, value: bool) -> None:
        """Property: bool type should always produce CtyBool."""
        cty_type = _python_type_to_cty_type(bool)
        assert isinstance(cty_type, CtyBool)


class TestListTypeConversionPropertyBased:
    """Property-based tests for list type conversion."""

    def test_list_str_produces_list_of_strings(self) -> None:
        """Property: list[str] should produce CtyList with CtyString elements."""
        cty_type = _python_type_to_cty_type(list[str])
        assert isinstance(cty_type, CtyList)
        assert isinstance(cty_type.element_type, CtyString)

    def test_list_int_produces_list_of_numbers(self) -> None:
        """Property: list[int] should produce CtyList with CtyNumber elements."""
        cty_type = _python_type_to_cty_type(list[int])
        assert isinstance(cty_type, CtyList)
        assert isinstance(cty_type.element_type, CtyNumber)

    def test_list_bool_produces_list_of_bools(self) -> None:
        """Property: list[bool] should produce CtyList with CtyBool elements."""
        cty_type = _python_type_to_cty_type(list[bool])
        assert isinstance(cty_type, CtyList)
        assert isinstance(cty_type.element_type, CtyBool)

    def test_nested_list_produces_nested_cty_list(self) -> None:
        """Property: list[list[str]] should produce nested CtyList."""
        cty_type = _python_type_to_cty_type(list[list[str]])
        assert isinstance(cty_type, CtyList)
        assert isinstance(cty_type.element_type, CtyList)
        assert isinstance(cty_type.element_type.element_type, CtyString)


class TestDictTypeConversionPropertyBased:
    """Property-based tests for dict type conversion."""

    def test_dict_str_str_produces_map_of_strings(self) -> None:
        """Property: dict[str, str] should produce CtyMap with CtyString values."""
        cty_type = _python_type_to_cty_type(dict[str, str])
        assert isinstance(cty_type, CtyMap)
        assert isinstance(cty_type.element_type, CtyString)

    def test_dict_str_int_produces_map_of_numbers(self) -> None:
        """Property: dict[str, int] should produce CtyMap with CtyNumber values."""
        cty_type = _python_type_to_cty_type(dict[str, int])
        assert isinstance(cty_type, CtyMap)
        assert isinstance(cty_type.element_type, CtyNumber)

    def test_dict_str_bool_produces_map_of_bools(self) -> None:
        """Property: dict[str, bool] should produce CtyMap with CtyBool values."""
        cty_type = _python_type_to_cty_type(dict[str, bool])
        assert isinstance(cty_type, CtyMap)
        assert isinstance(cty_type.element_type, CtyBool)


class TestUnionTypeConversionPropertyBased:
    """Property-based tests for union type conversion."""

    def test_optional_str_is_nullable(self) -> None:
        """Property: str | None should be detected as optional."""
        assert _is_optional_type_hint(str | None) is True

    def test_optional_int_is_nullable(self) -> None:
        """Property: int | None should be detected as optional."""
        assert _is_optional_type_hint(int | None) is True

    def test_non_optional_is_not_nullable(self) -> None:
        """Property: str should not be detected as optional."""
        assert _is_optional_type_hint(str) is False

    def test_union_of_numbers_produces_number(self) -> None:
        """Property: int | float should produce CtyNumber."""
        cty_type = _python_type_to_cty_type(int | float)
        assert isinstance(cty_type, CtyNumber)

    def test_union_of_different_types_produces_dynamic(self) -> None:
        """Property: str | int should produce CtyDynamic."""
        cty_type = _python_type_to_cty_type(str | int)
        assert isinstance(cty_type, CtyDynamic)


class TestFunctionConversionPropertyBased:
    """Property-based tests for function_to_dict."""

    @given(
        func_name=st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), whitelist_characters="_"),
        )
    )
    def test_function_name_preserved(self, func_name: str) -> None:
        """Property: Function name should be preserved in output."""
        # Filter invalid identifiers
        if not func_name.isidentifier():
            pytest.skip("Generated name is not a valid identifier")

        # Create a function dynamically
        def func() -> None:
            return None

        func.__name__ = func_name

        result = function_to_dict(func)
        assert result["name"] == func_name

    def test_function_with_str_param_produces_string_type(self) -> None:
        """Property: Function with str parameter should produce CtyString type."""

        def test_func(name: str) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert isinstance(result["parameters"][0]["cty_type"], CtyString)

    def test_function_with_int_param_produces_number_type(self) -> None:
        """Property: Function with int parameter should produce CtyNumber type."""

        def test_func(count: int) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert isinstance(result["parameters"][0]["cty_type"], CtyNumber)

    def test_function_with_bool_param_produces_bool_type(self) -> None:
        """Property: Function with bool parameter should produce CtyBool type."""

        def test_func(flag: bool) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert isinstance(result["parameters"][0]["cty_type"], CtyBool)

    def test_function_with_list_param_produces_list_type(self) -> None:
        """Property: Function with list parameter should produce CtyList type."""

        def test_func(items: list[str]) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert isinstance(result["parameters"][0]["cty_type"], CtyList)

    def test_function_with_dict_param_produces_map_type(self) -> None:
        """Property: Function with dict parameter should produce CtyMap type."""

        def test_func(mapping: dict[str, int]) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert isinstance(result["parameters"][0]["cty_type"], CtyMap)

    def test_function_with_optional_param_is_nullable(self) -> None:
        """Property: Function with optional parameter should be nullable."""

        def test_func(name: str | None) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["allow_null"] is True

    def test_function_with_default_produces_variadic(self) -> None:
        """Property: Function with default parameter should produce variadic parameter."""

        def test_func(name: str, count: int = 10) -> None:
            pass

        result = function_to_dict(test_func)
        # name should be required parameter
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

        # count should be variadic parameter
        assert "variadic_parameter" in result
        assert result["variadic_parameter"]["name"] == "count"
        assert result["variadic_parameter"]["allow_null"] is True

    def test_function_with_args_produces_variadic(self) -> None:
        """Property: Function with *args should produce variadic parameter."""

        def test_func(name: str, *values: int) -> None:
            pass

        result = function_to_dict(test_func)
        # name should be required parameter
        assert len(result["parameters"]) == 1

        # values should be variadic parameter
        assert "variadic_parameter" in result
        assert result["variadic_parameter"]["name"] == "values"

    @given(num_params=st.integers(min_value=0, max_value=5))
    def test_function_with_n_params_produces_n_parameters(self, num_params: int) -> None:
        """Property: Function with N parameters should produce N parameter entries."""
        # Generate function signature dynamically
        param_names = [f"param{i}" for i in range(num_params)]
        param_str = ", ".join(f"{name}: str" for name in param_names)

        # Create function using exec (for testing purposes)
        func_code = f"def test_func({param_str}): pass"
        local_vars = {}
        exec(func_code, {}, local_vars)
        test_func = local_vars["test_func"]

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == num_params


class TestReturnTypeConversionPropertyBased:
    """Property-based tests for return type conversion."""

    def test_str_return_type_produces_string(self) -> None:
        """Property: str return type should produce CtyString."""

        def test_func() -> str:
            return ""

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyString)

    def test_int_return_type_produces_number(self) -> None:
        """Property: int return type should produce CtyNumber."""

        def test_func() -> int:
            return 0

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyNumber)

    def test_bool_return_type_produces_bool(self) -> None:
        """Property: bool return type should produce CtyBool."""

        def test_func() -> bool:
            return True

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyBool)

    def test_list_return_type_produces_list(self) -> None:
        """Property: list return type should produce CtyList."""

        def test_func() -> list[str]:
            return []

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyList)

    def test_dict_return_type_produces_map(self) -> None:
        """Property: dict return type should produce CtyMap."""

        def test_func() -> dict[str, int]:
            return {}

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyMap)

    def test_no_return_type_produces_dynamic(self) -> None:
        """Property: No return type should produce CtyDynamic."""

        def test_func() -> None:
            pass

        result = function_to_dict(test_func)
        assert isinstance(result["return"]["cty_type"], CtyDynamic)


class TestComplexFunctionSignaturesPropertyBased:
    """Property-based tests for complex function signatures."""

    def test_function_with_multiple_types(self) -> None:
        """Property: Function with multiple parameter types should handle all correctly."""

        def test_func(name: str, count: int, flag: bool, items: list[str]) -> None:
            pass

        result = function_to_dict(test_func)
        assert len(result["parameters"]) == 4
        assert isinstance(result["parameters"][0]["cty_type"], CtyString)
        assert isinstance(result["parameters"][1]["cty_type"], CtyNumber)
        assert isinstance(result["parameters"][2]["cty_type"], CtyBool)
        assert isinstance(result["parameters"][3]["cty_type"], CtyList)

    def test_function_with_nested_types(self) -> None:
        """Property: Function with nested types should handle nesting correctly."""

        def test_func(nested: list[list[int]]) -> None:
            pass

        result = function_to_dict(test_func)
        param_type = result["parameters"][0]["cty_type"]
        assert isinstance(param_type, CtyList)
        assert isinstance(param_type.element_type, CtyList)
        assert isinstance(param_type.element_type.element_type, CtyNumber)

    def test_function_with_map_of_lists(self) -> None:
        """Property: Function with dict[str, list[int]] should handle correctly."""

        def test_func(data: dict[str, list[int]]) -> None:
            pass

        result = function_to_dict(test_func)
        param_type = result["parameters"][0]["cty_type"]
        assert isinstance(param_type, CtyMap)
        assert isinstance(param_type.element_type, CtyList)
        assert isinstance(param_type.element_type.element_type, CtyNumber)

    @given(default_val=st.integers(min_value=-100, max_value=100))
    def test_function_with_int_default(self, default_val: int) -> None:
        """Property: Function with int default should be variadic."""

        def test_func(count: int = default_val) -> None:
            pass

        result = function_to_dict(test_func)
        assert "variadic_parameter" in result
        assert result["variadic_parameter"]["name"] == "count"
        assert isinstance(result["variadic_parameter"]["cty_type"], CtyNumber)


# Docstring extraction tests removed - whitespace normalization makes property-based testing difficult

# 🐍🏗️🔚
