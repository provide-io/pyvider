#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for s_function schema factory."""

from typing import Any

import pytest

from pyvider.cty.types import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.schema.factory import (
    a_bool,
    a_dyn,
    a_list,
    a_map,
    a_num,
    a_obj,
    a_str,
    s_function,
)
from pyvider.schema.types import PvsSchema


class TestSFunctionBasic:
    """Basic creation and structure tests for s_function."""

    def test_s_function_with_no_parameters(self) -> None:
        """Test creating a function schema with no parameters."""
        schema = s_function(
            parameters=None,
            return_type=a_str(description="Returns a constant"),
        )
        assert isinstance(schema, PvsSchema)
        assert schema.version == 1
        assert schema.block is not None
        # Should have return_type attribute
        assert "return_type" in schema.block.attributes

    def test_s_function_with_single_string_parameter(self) -> None:
        """Test creating a function with a single string parameter."""
        schema = s_function(
            parameters=[a_str(description="Input string")],
            return_type=a_str(description="Output string"),
        )
        assert isinstance(schema, PvsSchema)
        assert "param_0" in schema.block.attributes
        assert "return_type" in schema.block.attributes
        assert isinstance(schema.block.attributes["param_0"].type, CtyString)
        assert isinstance(schema.block.attributes["return_type"].type, CtyString)

    def test_s_function_with_multiple_parameters(self) -> None:
        """Test creating a function with multiple parameters of different types."""
        schema = s_function(
            parameters=[
                a_str(description="String parameter"),
                a_num(description="Number parameter"),
                a_bool(description="Boolean parameter"),
            ],
            return_type=a_str(description="Result"),
        )
        assert isinstance(schema, PvsSchema)
        assert "param_0" in schema.block.attributes
        assert "param_1" in schema.block.attributes
        assert "param_2" in schema.block.attributes
        assert isinstance(schema.block.attributes["param_0"].type, CtyString)
        assert isinstance(schema.block.attributes["param_1"].type, CtyNumber)
        assert isinstance(schema.block.attributes["param_2"].type, CtyBool)

    def test_s_function_with_variadic_parameter(self) -> None:
        """Test creating a function with a variadic parameter."""
        schema = s_function(
            parameters=[a_str(description="Base parameter")],
            return_type=a_str(description="Result"),
            variadic_parameter=a_num(description="Variable number arguments"),
        )
        assert isinstance(schema, PvsSchema)
        assert "param_0" in schema.block.attributes
        assert "variadic_param" in schema.block.attributes
        assert isinstance(schema.block.attributes["variadic_param"].type, CtyNumber)

    def test_s_function_empty_parameters_list(self) -> None:
        """Test creating a function with an empty parameters list."""
        schema = s_function(
            parameters=[],
            return_type=a_bool(description="Always returns true"),
        )
        assert isinstance(schema, PvsSchema)
        assert "return_type" in schema.block.attributes
        # No param_0 since parameters list is empty
        assert "param_0" not in schema.block.attributes


class TestSFunctionParameterTypes:
    """Tests for different parameter types in s_function."""

    @pytest.mark.parametrize(
        "param_factory, expected_type",
        [
            (a_str, CtyString),
            (a_num, CtyNumber),
            (a_bool, CtyBool),
            (a_dyn, CtyDynamic),
        ],
        ids=["string", "number", "boolean", "dynamic"],
    )
    def test_s_function_with_primitive_types(self, param_factory: Any, expected_type: type) -> None:
        """Test s_function with different primitive parameter types."""
        schema = s_function(
            parameters=[param_factory(description="Test parameter")],
            return_type=a_str(),
        )
        assert isinstance(schema.block.attributes["param_0"].type, expected_type)

    def test_s_function_with_list_parameter(self) -> None:
        """Test s_function with a list parameter."""
        schema = s_function(
            parameters=[a_list(a_str(), description="List of strings")],
            return_type=a_str(),
        )
        param_type = schema.block.attributes["param_0"].type
        assert isinstance(param_type, CtyList)
        assert isinstance(param_type.element_type, CtyString)

    def test_s_function_with_map_parameter(self) -> None:
        """Test s_function with a map parameter."""
        schema = s_function(
            parameters=[a_map(a_num(), description="Map of numbers")],
            return_type=a_num(),
        )
        param_type = schema.block.attributes["param_0"].type
        assert isinstance(param_type, CtyMap)
        assert isinstance(param_type.element_type, CtyNumber)

    def test_s_function_with_object_parameter(self) -> None:
        """Test s_function with an object parameter."""
        schema = s_function(
            parameters=[
                a_obj(
                    attributes={
                        "name": a_str(description="Name field"),
                        "age": a_num(description="Age field"),
                    },
                    description="Person object",
                )
            ],
            return_type=a_bool(),
        )
        assert "param_0" in schema.block.attributes
        # Object type should have the nested attributes
        param = schema.block.attributes["param_0"]
        assert param.object_type is not None
        assert "name" in param.object_type.attributes
        assert "age" in param.object_type.attributes

    def test_s_function_with_complex_nested_types(self) -> None:
        """Test s_function with complex nested type combinations."""
        schema = s_function(
            parameters=[
                a_list(
                    a_map(a_str(), description="Map element"),
                    description="List of maps",
                )
            ],
            return_type=a_num(),
        )
        param_type = schema.block.attributes["param_0"].type
        assert isinstance(param_type, CtyList)
        assert isinstance(param_type.element_type, CtyMap)
        assert isinstance(param_type.element_type.element_type, CtyString)


class TestSFunctionReturnTypes:
    """Tests for different return types in s_function."""

    @pytest.mark.parametrize(
        "return_factory, expected_type",
        [
            (a_str, CtyString),
            (a_num, CtyNumber),
            (a_bool, CtyBool),
            (a_dyn, CtyDynamic),
        ],
        ids=["string", "number", "boolean", "dynamic"],
    )
    def test_s_function_with_primitive_return_types(self, return_factory: Any, expected_type: type) -> None:
        """Test s_function with different primitive return types."""
        schema = s_function(
            parameters=[a_str()],
            return_type=return_factory(description="Return value"),
        )
        assert isinstance(schema.block.attributes["return_type"].type, expected_type)

    def test_s_function_with_list_return_type(self) -> None:
        """Test s_function returning a list."""
        schema = s_function(
            parameters=[a_str()],
            return_type=a_list(a_num(), description="List of numbers"),
        )
        return_type = schema.block.attributes["return_type"].type
        assert isinstance(return_type, CtyList)
        assert isinstance(return_type.element_type, CtyNumber)

    def test_s_function_with_object_return_type(self) -> None:
        """Test s_function returning an object."""
        schema = s_function(
            parameters=[a_str()],
            return_type=a_obj(
                attributes={
                    "result": a_str(description="Result value"),
                    "success": a_bool(description="Success flag"),
                },
                description="Result object",
            ),
        )
        return_attr = schema.block.attributes["return_type"]
        assert return_attr.object_type is not None
        assert "result" in return_attr.object_type.attributes
        assert "success" in return_attr.object_type.attributes

    def test_s_function_with_no_return_type(self) -> None:
        """Test s_function with None as return type."""
        schema = s_function(
            parameters=[a_str()],
            return_type=None,
        )
        assert isinstance(schema, PvsSchema)
        # If return_type is None, it shouldn't be in attributes
        assert "return_type" not in schema.block.attributes


class TestSFunctionDescriptions:
    """Tests for description handling in s_function."""

    def test_s_function_parameters_preserve_descriptions(self) -> None:
        """Test that parameter descriptions are preserved."""
        param_desc = "This is a test parameter"
        schema = s_function(
            parameters=[a_str(description=param_desc)],
            return_type=a_str(),
        )
        assert schema.block.attributes["param_0"].description == param_desc

    def test_s_function_return_type_preserves_description(self) -> None:
        """Test that return type description is preserved."""
        return_desc = "This is the return value"
        schema = s_function(
            parameters=[a_str()],
            return_type=a_num(description=return_desc),
        )
        assert schema.block.attributes["return_type"].description == return_desc

    def test_s_function_variadic_parameter_preserves_description(self) -> None:
        """Test that variadic parameter description is preserved."""
        variadic_desc = "Variable number of arguments"
        schema = s_function(
            parameters=[],
            return_type=a_str(),
            variadic_parameter=a_str(description=variadic_desc),
        )
        assert schema.block.attributes["variadic_param"].description == variadic_desc


class TestSFunctionEdgeCases:
    """Edge cases and error scenarios for s_function."""

    def test_s_function_all_none_parameters(self) -> None:
        """Test s_function with all None parameters."""
        schema = s_function(
            parameters=None,
            return_type=None,
            variadic_parameter=None,
        )
        assert isinstance(schema, PvsSchema)
        assert schema.version == 1
        # Should have an empty attributes dict or only structural attributes
        assert len(schema.block.attributes) == 0

    def test_s_function_preserves_attribute_metadata(self) -> None:
        """Test that attribute metadata like required/optional is preserved."""
        schema = s_function(
            parameters=[a_str(description="Test", required=True)],
            return_type=a_str(required=False),
        )
        assert schema.block.attributes["param_0"].required is True
        assert schema.block.attributes["return_type"].required is False

    def test_s_function_with_many_parameters(self) -> None:
        """Test s_function with a large number of parameters."""
        many_params = [a_num(description=f"Param {i}") for i in range(20)]
        schema = s_function(
            parameters=many_params,
            return_type=a_num(),
        )
        # Verify all parameters are stored
        for i in range(20):
            assert f"param_{i}" in schema.block.attributes

    def test_s_function_schema_version(self) -> None:
        """Test that s_function creates schemas with correct version."""
        schema = s_function(
            parameters=[a_str()],
            return_type=a_str(),
        )
        assert schema.version == 1

    def test_s_function_returns_frozen_schema(self) -> None:
        """Test that s_function returns a frozen (immutable) PvsSchema."""
        schema = s_function(
            parameters=[a_str()],
            return_type=a_str(),
        )
        # PvsSchema is frozen, so this should raise an error
        with pytest.raises(AttributeError):
            schema.version = 2  # type: ignore[misc]


class TestSFunctionIntegration:
    """Integration tests combining s_function with other schema builders."""

    def test_s_function_matches_documented_api(self) -> None:
        """Test that s_function matches the API shown in documentation."""
        # This is the exact example from the docs
        schema = s_function(
            parameters=[
                a_str(description="Input string to convert"),
            ],
            return_type=a_str(description="Uppercase string"),
        )
        assert isinstance(schema, PvsSchema)
        assert "param_0" in schema.block.attributes
        assert "return_type" in schema.block.attributes

    def test_s_function_with_join_example(self) -> None:
        """Test s_function with the join function example from docs."""
        schema = s_function(
            parameters=[
                a_list(a_str(), description="Strings to join"),
                a_str(description="Separator"),
            ],
            return_type=a_str(description="Joined string"),
        )
        assert isinstance(schema, PvsSchema)
        assert "param_0" in schema.block.attributes
        assert "param_1" in schema.block.attributes
        assert isinstance(schema.block.attributes["param_0"].type, CtyList)
        assert isinstance(schema.block.attributes["param_1"].type, CtyString)


# 🐍🏗️🔚
