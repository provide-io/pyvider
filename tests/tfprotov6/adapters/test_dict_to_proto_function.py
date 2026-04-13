#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for protobuf function_adapter.py module."""

import json

from provide.testkit.mocking import patch

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.protocols.tfprotov6.adapters.function_adapter import dict_to_proto_function
import pyvider.protocols.tfprotov6.protobuf as pb


class TestDictToProtoFunctionBasics:
    """Test basic function conversion from dict to protobuf."""

    def test_converts_simple_function(self) -> None:
        """Test converting a simple function with basic parameters."""
        func_dict = {
            "name": "test_func",
            "summary": "Test function",
            "description": "A test function",
            "parameters": [
                {
                    "name": "param1",
                    "cty_type": CtyString(),
                    "description": "First parameter",
                    "allow_null": False,
                }
            ],
            "return": {"cty_type": CtyBool()},
        }

        result = dict_to_proto_function(func_dict)

        assert isinstance(result, pb.Function)
        assert result.summary == "Test function"
        assert result.description == "A test function"
        assert len(result.parameters) == 1
        assert result.parameters[0].name == "param1"
        assert result.parameters[0].description == "First parameter"
        assert result.parameters[0].allow_null_value is False

    def test_converts_function_with_multiple_parameters(self) -> None:
        """Test function with multiple required parameters."""
        func_dict = {
            "name": "multi_param_func",
            "parameters": [
                {"name": "a", "cty_type": CtyString(), "description": "Param A", "allow_null": False},
                {"name": "b", "cty_type": CtyNumber(), "description": "Param B", "allow_null": False},
                {"name": "c", "cty_type": CtyBool(), "description": "Param C", "allow_null": True},
            ],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert len(result.parameters) == 3
        assert result.parameters[0].name == "a"
        assert result.parameters[1].name == "b"
        assert result.parameters[2].name == "c"
        assert result.parameters[2].allow_null_value is True


class TestDictToProtoFunctionVariadic:
    """Test variadic parameter handling."""

    def test_converts_function_with_variadic_parameter(self) -> None:
        """Test function with variadic (optional) parameter."""
        func_dict = {
            "name": "variadic_func",
            "parameters": [
                {
                    "name": "required",
                    "cty_type": CtyString(),
                    "description": "Required param",
                    "allow_null": False,
                }
            ],
            "variadic_parameter": {
                "name": "options",
                "cty_type": CtyMap(element_type=CtyString()),
                "description": "Optional parameters",
                "allow_null": True,
            },
            "return": {"cty_type": CtyString()},
        }

        result = dict_to_proto_function(func_dict)

        assert len(result.parameters) == 1
        assert result.variadic_parameter is not None
        assert result.variadic_parameter.name == "options"
        assert result.variadic_parameter.description == "Optional parameters"
        assert result.variadic_parameter.allow_null_value is True

    def test_handles_function_without_variadic(self) -> None:
        """Test function without variadic parameter."""
        func_dict = {
            "name": "no_variadic",
            "parameters": [{"name": "x", "cty_type": CtyNumber(), "description": "", "allow_null": False}],
            "return": {"cty_type": CtyNumber()},
        }

        result = dict_to_proto_function(func_dict)

        # Should not have variadic_parameter field set
        assert not result.HasField("variadic_parameter")


class TestDictToProtoFunctionReturnTypes:
    """Test return type handling."""

    def test_converts_function_with_return_type(self) -> None:
        """Test function with explicit return type."""
        func_dict = {
            "name": "return_func",
            "parameters": [],
            "return": {"cty_type": CtyList(element_type=CtyString())},
        }

        result = dict_to_proto_function(func_dict)

        assert getattr(result, "return") is not None
        # Verify it's JSON-encoded type bytes
        type_dict = json.loads(getattr(result, "return").type.decode("utf-8"))
        assert isinstance(type_dict, list)  # CtyList is encoded as ["list", element_type]

    def test_handles_function_without_explicit_return(self) -> None:
        """Test function without explicit return data defaults to CtyDynamic."""
        func_dict = {
            "name": "no_return",
            "parameters": [],
        }

        result = dict_to_proto_function(func_dict)

        # Should default to CtyDynamic
        assert getattr(result, "return") is not None
        type_dict = json.loads(getattr(result, "return").type.decode("utf-8"))
        assert type_dict == "dynamic"


class TestDictToProtoFunctionMissingCtyTypes:
    """Test handling of missing CtyType in parameters."""

    def test_handles_missing_parameter_cty_type(self) -> None:
        """Test warning when parameter CtyType is missing."""
        func_dict = {
            "name": "missing_type",
            "parameters": [
                {"name": "bad_param", "description": "Missing type", "allow_null": False}
                # Note: missing "cty_type" key
            ],
            "return": {"cty_type": CtyString()},
        }

        with patch("pyvider.protocols.tfprotov6.adapters.function_adapter.logger") as mock_logger:
            result = dict_to_proto_function(func_dict)

            # Should log warning
            assert mock_logger.warning.called
            assert "Missing CtyType" in str(mock_logger.warning.call_args)

            # Should default to CtyDynamic
            assert result is not None
            assert len(result.parameters) == 1

    def test_handles_missing_variadic_cty_type(self) -> None:
        """Test warning when variadic parameter CtyType is missing."""
        func_dict = {
            "name": "missing_variadic_type",
            "parameters": [],
            "variadic_parameter": {"name": "opts", "description": "Options", "allow_null": True},
            # Note: missing "cty_type" key
            "return": {"cty_type": CtyString()},
        }

        with patch("pyvider.protocols.tfprotov6.adapters.function_adapter.logger") as mock_logger:
            result = dict_to_proto_function(func_dict)

            # Should log warning
            assert mock_logger.warning.called
            assert "Missing CtyType" in str(mock_logger.warning.call_args)

            # Should still create variadic with CtyDynamic
            assert result.variadic_parameter is not None

    def test_handles_missing_return_cty_type(self) -> None:
        """Test warning when return CtyType is missing."""
        func_dict = {
            "name": "missing_return_type",
            "parameters": [],
            "return": {},  # Empty return dict, no cty_type
        }

        with patch("pyvider.protocols.tfprotov6.adapters.function_adapter.logger") as mock_logger:
            result = dict_to_proto_function(func_dict)

            # Should log warning (different message than missing parameter)
            assert mock_logger.warning.called
            assert "No explicit 'return'" in str(mock_logger.warning.call_args) or "Missing CtyType" in str(
                mock_logger.warning.call_args
            )

            # Should default return to CtyDynamic
            assert getattr(result, "return") is not None


class TestDictToProtoFunctionErrorHandling:
    """Test error handling during conversion."""

    def test_handles_conversion_exception(self) -> None:
        """Test that exceptions are caught and logged."""
        func_dict = {
            "name": "error_func",
            "parameters": [{"name": "x", "cty_type": CtyString(), "description": "", "allow_null": False}],
            "return": {"cty_type": CtyString()},
        }

        with (
            patch("pyvider.protocols.tfprotov6.adapters.function_adapter.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.adapters.function_adapter.json.dumps") as mock_dumps,
        ):
            # Make json.dumps raise an exception during type encoding
            mock_dumps.side_effect = RuntimeError("JSON encoding failed")

            result = dict_to_proto_function(func_dict)

            # Should return None on error
            assert result is None

            # Should log error
            mock_logger.error.assert_called_once()
            assert "error_func" in str(mock_logger.error.call_args)
            assert "JSON encoding failed" in str(mock_logger.error.call_args)

    def test_returns_none_on_construction_error(self) -> None:
        """Test that None is returned when protobuf construction fails."""
        # This is a bit tricky to test, but we can simulate by patching pb.Function
        func_dict = {
            "name": "constructor_error",
            "parameters": [],
            "return": {"cty_type": CtyString()},
        }

        with (
            patch("pyvider.protocols.tfprotov6.adapters.function_adapter.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.adapters.function_adapter.pb.Function") as mock_pb,
        ):
            mock_pb.side_effect = RuntimeError("Construction failed")

            result = dict_to_proto_function(func_dict)

            assert result is None
            mock_logger.error.assert_called_once()


class TestDictToProtoFunctionComplexTypes:
    """Test conversion of complex CtyTypes."""

    def test_converts_list_type_parameter(self) -> None:
        """Test parameter with CtyList type."""
        func_dict = {
            "name": "list_func",
            "parameters": [
                {
                    "name": "items",
                    "cty_type": CtyList(element_type=CtyNumber()),
                    "description": "List of numbers",
                    "allow_null": False,
                }
            ],
            "return": {"cty_type": CtyNumber()},
        }

        result = dict_to_proto_function(func_dict)

        assert result is not None
        assert len(result.parameters) == 1
        # Verify type encoding
        type_dict = json.loads(result.parameters[0].type.decode("utf-8"))
        assert isinstance(type_dict, list)
        assert type_dict[0] == "list"

    def test_converts_map_type_parameter(self) -> None:
        """Test parameter with CtyMap type."""
        func_dict = {
            "name": "map_func",
            "parameters": [
                {
                    "name": "config",
                    "cty_type": CtyMap(element_type=CtyString()),
                    "description": "Configuration map",
                    "allow_null": False,
                }
            ],
            "return": {"cty_type": CtyBool()},
        }

        result = dict_to_proto_function(func_dict)

        assert result is not None
        assert len(result.parameters) == 1
        # Verify type encoding
        type_dict = json.loads(result.parameters[0].type.decode("utf-8"))
        assert isinstance(type_dict, list)
        assert type_dict[0] == "map"

    def test_converts_nested_collection_types(self) -> None:
        """Test parameter with nested collection types."""
        func_dict = {
            "name": "nested_func",
            "parameters": [
                {
                    "name": "data",
                    "cty_type": CtyList(element_type=CtyList(element_type=CtyString())),
                    "description": "Nested list",
                    "allow_null": False,
                }
            ],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert result is not None
        assert len(result.parameters) == 1


class TestDictToProtoFunctionMetadata:
    """Test metadata handling (summary, description, deprecation)."""

    def test_includes_summary_and_description(self) -> None:
        """Test that summary and description are included."""
        func_dict = {
            "name": "documented_func",
            "summary": "Short summary",
            "description": "Longer description with details",
            "parameters": [],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert result.summary == "Short summary"
        assert result.description == "Longer description with details"

    def test_includes_deprecation_message(self) -> None:
        """Test that deprecation message is included."""
        func_dict = {
            "name": "deprecated_func",
            "summary": "Old function",
            "deprecation_message": "Use new_func instead",
            "parameters": [],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert result.deprecation_message == "Use new_func instead"

    def test_handles_missing_optional_metadata(self) -> None:
        """Test that missing optional metadata doesn't cause issues."""
        func_dict = {
            "name": "minimal_func",
            # No summary, description, or deprecation_message
            "parameters": [],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert result is not None
        assert result.summary == ""
        assert result.description == ""
        assert result.deprecation_message == ""


class TestDictToProtoFunctionAllowUnknownValues:
    """Test that allow_unknown_values is always set to True."""

    def test_parameters_allow_unknown_values(self) -> None:
        """Test that parameters have allow_unknown_values=True."""
        func_dict = {
            "name": "test_func",
            "parameters": [
                {"name": "a", "cty_type": CtyString(), "description": "", "allow_null": False},
                {"name": "b", "cty_type": CtyNumber(), "description": "", "allow_null": True},
            ],
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        for param in result.parameters:
            assert param.allow_unknown_values is True

    def test_variadic_parameter_allows_unknown_values(self) -> None:
        """Test that variadic parameter has allow_unknown_values=True."""
        func_dict = {
            "name": "test_func",
            "parameters": [],
            "variadic_parameter": {
                "name": "opts",
                "cty_type": CtyDynamic(),
                "description": "Options",
                "allow_null": True,
            },
            "return": {"cty_type": CtyDynamic()},
        }

        result = dict_to_proto_function(func_dict)

        assert result.variadic_parameter.allow_unknown_values is True


# 🐍🏗️🔚
