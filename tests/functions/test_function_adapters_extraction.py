#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for function adapters - Parameter and metadata extraction."""

from typing import Any
from unittest.mock import MagicMock

from provide.testkit import mocking as mock

from pyvider.cty import CtyDynamic, CtyNumber, CtyString
from pyvider.functions.adapters import (
    _extract_docstring_meta,
    _extract_parameters_meta,
    _extract_return_type_meta,
    function_to_dict,
)


class TestExtractParametersMeta:
    """Tests for _extract_parameters_meta function."""

    def test_extracts_required_parameter(self) -> None:
        """Test extracting required parameter."""
        import inspect

        def test_func(name: str) -> None:
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"
        assert isinstance(result["parameters"][0]["cty_type"], CtyString)
        assert result["parameters"][0]["allow_null"] is False

    def test_extracts_optional_parameter(self) -> None:
        """Test extracting optional parameter."""
        import inspect

        def test_func(name: str | None) -> None:
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str | None}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["allow_null"] is True

    def test_extracts_parameter_with_default_as_variadic(self) -> None:
        """Test that parameter with default becomes variadic."""
        import inspect

        def test_func(name: str, count: int = 10) -> None:
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

    def test_extracts_var_positional_as_variadic(self) -> None:
        """Test extracting *args as variadic parameter."""
        import inspect

        def test_func(name: str, *values: int) -> None:
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "values": int}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert len(result["parameters"]) == 1
        assert result["variadic_parameter"] is not None
        assert result["variadic_parameter"]["name"] == "values"

    def test_skips_keyword_only_parameters(self) -> None:
        """Test that keyword-only parameters are skipped."""
        import inspect

        def test_func(name: str, *, internal: str = "test") -> None:
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "internal": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        # Only name should be extracted
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

    def test_skips_self_parameter(self) -> None:
        """Test that self parameter is skipped."""
        import inspect

        class TestClass:
            def test_method(self, name: str) -> None:
                pass

        method = TestClass().test_method
        sig = inspect.signature(method)
        type_hints = {"name": str}
        result = _extract_parameters_meta(method, sig, type_hints)

        # self should be skipped, only name
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"

    @mock.patch("pyvider.functions.adapters.logger")
    def test_warns_on_multiple_defaults(self, mock_logger: MagicMock) -> None:
        """Test warning on multiple default parameters."""
        import inspect

        def test_func(name: str = "default1", count: int = 10) -> None:
            pass

        sig = inspect.signature(test_func)
        type_hints = {"name": str, "count": int}
        _extract_parameters_meta(test_func, sig, type_hints)

        # Should log a warning
        assert mock_logger.warning.called

    def test_uses_parameter_descriptions_from_metadata(self) -> None:
        """Test that parameter descriptions come from metadata."""
        import inspect

        def test_func(name: str) -> None:
            pass

        test_func._function_metadata = {"param_descriptions": {"name": "The name parameter"}}

        sig = inspect.signature(test_func)
        type_hints = {"name": str}
        result = _extract_parameters_meta(test_func, sig, type_hints)

        assert result["parameters"][0]["description"] == "The name parameter"


class TestExtractReturnTypeMeta:
    """Tests for _extract_return_type_meta function."""

    def test_extracts_str_return_type(self) -> None:
        """Test extracting str return type."""
        type_hints = {"return": str}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyString)

    def test_extracts_int_return_type(self) -> None:
        """Test extracting int return type."""
        type_hints = {"return": int}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyNumber)

    def test_defaults_to_dynamic_when_no_return_type(self) -> None:
        """Test that missing return type defaults to CtyDynamic."""
        type_hints = {}
        result = _extract_return_type_meta(type_hints)

        assert isinstance(result["cty_type"], CtyDynamic)


class TestExtractDocstringMeta:
    """Tests for _extract_docstring_meta function."""

    def test_extracts_summary_from_docstring(self) -> None:
        """Test extracting summary from docstring."""

        def test_func() -> None:
            """This is the summary line.

            This is more detail.
            """

        base_meta = {}
        _extract_docstring_meta(test_func, base_meta)

        assert base_meta["summary"] == "This is the summary line."
        assert "This is more detail" in base_meta["description"]

    def test_preserves_existing_summary(self) -> None:
        """Test that existing summary is preserved."""

        def test_func() -> None:
            """Docstring summary."""

        base_meta = {"summary": "Existing summary"}
        _extract_docstring_meta(test_func, base_meta)

        assert base_meta["summary"] == "Existing summary"

    def test_handles_missing_docstring(self) -> None:
        """Test handling functions without docstring."""

        def test_func() -> None:
            pass

        base_meta = {}
        _extract_docstring_meta(test_func, base_meta)

        # Should not crash, may not add summary/description
        assert "summary" not in base_meta or base_meta["summary"] == ""


class TestFunctionToDict:
    """Tests for function_to_dict function."""

    def test_converts_simple_function(self) -> None:
        """Test converting a simple function."""

        def test_func(name: str) -> str:
            """Test function."""
            return name

        result = function_to_dict(test_func)

        assert result["name"] == "test_func"
        assert len(result["parameters"]) == 1
        assert result["parameters"][0]["name"] == "name"
        assert isinstance(result["return"]["cty_type"], CtyString)

    def test_uses_existing_metadata(self) -> None:
        """Test that existing metadata is used."""

        def test_func(name: str) -> None:
            pass

        test_func._function_metadata = {"name": "custom_name"}

        result = function_to_dict(test_func)

        assert result["name"] == "custom_name"

    def test_handles_function_with_defaults(self) -> None:
        """Test function with default parameters."""

        def test_func(name: str, count: int = 10) -> int:
            return count

        result = function_to_dict(test_func)

        assert len(result["parameters"]) == 1
        assert result["variadic_parameter"]["name"] == "count"

    @mock.patch("pyvider.functions.adapters.logger")
    def test_handles_type_hint_resolution_errors(self, mock_logger: MagicMock) -> None:
        """Test handling type hint resolution errors."""

        def test_func(name: Any) -> None:  # No type hints
            pass

        result = function_to_dict(test_func)

        # Should still work but with dynamic types
        assert result["name"] == "test_func"

    def test_includes_docstring_in_output(self) -> None:
        """Test that docstring is included in output."""

        def test_func(name: str) -> None:
            """This function does something."""

        result = function_to_dict(test_func)

        assert "description" in result
        assert "This function does something" in result["description"]


# 🐍🏗️🔚
