#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration test for s_function with provider framework."""

import pytest

from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType
from pyvider.hub import register_function
from pyvider.schema import PvsSchema, a_list, a_num, a_str, s_function


@register_function("upper_func", test_only=True)
class UpperFunction(BaseFunction):
    """Test function using s_function schema builder."""

    name: str = "upper_func"
    summary: str = "Converts string to uppercase"
    description: str = "Takes a string and returns it in uppercase"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema using s_function."""
        return s_function(
            parameters=[
                a_str(description="Input string to convert"),
            ],
            return_type=a_str(description="Uppercase string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method - extract from schema."""
        # For now, return empty list as this is transitional
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method - extract from schema."""
        from pyvider.cty import CtyString

        return FunctionReturnType(type=CtyString())

    async def call(self, input_str: str) -> str:
        """Execute the function."""
        return input_str.upper()


@register_function("join_func", test_only=True)
class JoinFunction(BaseFunction):
    """Test function with multiple parameters using s_function."""

    name: str = "join_func"
    summary: str = "Joins strings with separator"
    description: str = "Takes a list of strings and a separator, returns joined string"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema using s_function."""
        return s_function(
            parameters=[
                a_list(a_str(), description="Strings to join"),
                a_str(description="Separator"),
            ],
            return_type=a_str(description="Joined string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method."""
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method."""
        from pyvider.cty import CtyString

        return FunctionReturnType(type=CtyString())

    async def call(self, strings: list[str], separator: str) -> str:
        """Execute the function."""
        return separator.join(strings)


@register_function("add_numbers", test_only=True)
class AddNumbersFunction(BaseFunction):
    """Test function with numeric parameters."""

    name: str = "add_numbers"
    summary: str = "Adds two numbers"
    description: str = "Takes two numbers and returns their sum"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema using s_function."""
        return s_function(
            parameters=[
                a_num(description="First number"),
                a_num(description="Second number"),
            ],
            return_type=a_num(description="Sum of the numbers"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method."""
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method."""
        from pyvider.cty import CtyNumber

        return FunctionReturnType(type=CtyNumber())

    async def call(self, a: float, b: float) -> int | float:
        """Execute the function."""
        return a + b


class TestSFunctionProviderIntegration:
    """Integration tests for s_function with provider framework."""

    def test_function_can_be_registered_with_s_function_schema(self) -> None:
        """Test that functions using s_function can be registered."""
        func = UpperFunction(name="upper_func")
        assert func.name == "upper_func"
        assert hasattr(func, "get_schema")

    def test_get_schema_returns_pvsschema(self) -> None:
        """Test that get_schema returns a valid PvsSchema."""
        func = UpperFunction(name="upper_func")
        schema = func.get_schema()
        assert isinstance(schema, PvsSchema)
        assert schema.version == 1

    def test_schema_contains_parameters(self) -> None:
        """Test that schema contains function parameters."""
        func = UpperFunction(name="upper_func")
        schema = func.get_schema()
        # Parameters are stored as param_0, param_1, etc.
        assert "param_0" in schema.block.attributes
        assert "return_type" in schema.block.attributes

    def test_multiple_parameters_in_schema(self) -> None:
        """Test function with multiple parameters."""
        func = JoinFunction(name="join_func")
        schema = func.get_schema()
        assert "param_0" in schema.block.attributes  # strings list
        assert "param_1" in schema.block.attributes  # separator
        assert "return_type" in schema.block.attributes

    def test_numeric_parameters_in_schema(self) -> None:
        """Test function with numeric parameters."""
        func = AddNumbersFunction(name="add_numbers")
        schema = func.get_schema()
        assert "param_0" in schema.block.attributes
        assert "param_1" in schema.block.attributes
        assert "return_type" in schema.block.attributes

    @pytest.mark.asyncio
    async def test_function_call_works(self) -> None:
        """Test that the function can actually be called."""
        func = UpperFunction(name="upper_func")
        result = await func.call("hello")
        assert result == "HELLO"

    @pytest.mark.asyncio
    async def test_join_function_call_works(self) -> None:
        """Test that join function works."""
        func = JoinFunction(name="join_func")
        result = await func.call(["hello", "world"], " ")
        assert result == "hello world"

    @pytest.mark.asyncio
    async def test_add_numbers_function_call_works(self) -> None:
        """Test that add function works."""
        func = AddNumbersFunction(name="add_numbers")
        result = await func.call(5, 3)
        assert result == 8

    def test_schema_has_correct_structure(self) -> None:
        """Test that schema structure matches expected format."""
        func = UpperFunction(name="upper_func")
        schema = func.get_schema()

        # Should have PvsObjectType block
        assert hasattr(schema, "block")
        assert hasattr(schema.block, "attributes")

        # Should have parameter and return type
        from pyvider.cty import CtyString

        assert isinstance(schema.block.attributes["param_0"].type, CtyString)
        assert isinstance(schema.block.attributes["return_type"].type, CtyString)

    def test_schema_descriptions_preserved(self) -> None:
        """Test that parameter descriptions are preserved in schema."""
        func = UpperFunction(name="upper_func")
        schema = func.get_schema()

        # Check that descriptions are preserved
        param_desc = schema.block.attributes["param_0"].description
        assert param_desc == "Input string to convert"

        return_desc = schema.block.attributes["return_type"].description
        assert return_desc == "Uppercase string"

    def test_complex_types_work(self) -> None:
        """Test that complex types (lists) work in s_function."""
        func = JoinFunction(name="join_func")
        schema = func.get_schema()

        # param_0 should be a list of strings
        from pyvider.cty import CtyList

        param0_type = schema.block.attributes["param_0"].type
        assert isinstance(param0_type, CtyList)


# 🐍🏗️🔚
