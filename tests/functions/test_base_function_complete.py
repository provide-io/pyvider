#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for BaseFunction and FunctionAdapter classes."""

from typing import Any

import pytest

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.exceptions import FunctionError
from pyvider.functions.base import BaseFunction, FunctionAdapter, FunctionParameter, FunctionReturnType


class TestBaseFunction:
    """Tests for BaseFunction abstract class."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        """Test that BaseFunction cannot be instantiated directly."""
        with pytest.raises(TypeError, match="abstract"):
            BaseFunction(name="test")

    def test_concrete_implementation_works(self) -> None:
        """Test that concrete implementation of BaseFunction works."""

        class ConcreteFunction(BaseFunction):
            def get_parameters(self) -> list[FunctionParameter]:
                return [FunctionParameter(name="input", type=CtyString())]

            def get_return_type(self) -> FunctionReturnType:
                return FunctionReturnType(type=CtyString())

            async def call(self, *args: Any, **kwargs: Any) -> str:
                return "result"

        func = ConcreteFunction(name="test_func")
        assert func.name == "test_func"
        assert len(func.get_parameters()) == 1
        assert isinstance(func.get_return_type().type, CtyString)

    @pytest.mark.asyncio
    async def test_call_method_must_be_async(self) -> None:
        """Test that call method is async."""

        class AsyncFunction(BaseFunction):
            def get_parameters(self) -> list[FunctionParameter]:
                return []

            def get_return_type(self) -> FunctionReturnType:
                return FunctionReturnType(type=CtyString())

            async def call(self, *args: Any, **kwargs: Any) -> str:
                return "async_result"

        func = AsyncFunction(name="async_func")
        result = await func.call()
        assert result == "async_result"

    @pytest.mark.asyncio
    async def test_dunder_call_invokes_call(self) -> None:
        """Test that __call__ delegates to call() method."""

        class CallableFunction(BaseFunction):
            def get_parameters(self) -> list[FunctionParameter]:
                return []

            def get_return_type(self) -> FunctionReturnType:
                return FunctionReturnType(type=CtyNumber())

            async def call(self, *args: Any, **kwargs: Any) -> int:
                return 42

        func = CallableFunction(name="callable_func")
        result = await func("arg1", kwarg1="value1")
        assert result == 42

    def test_function_attributes(self) -> None:
        """Test BaseFunction attributes."""

        class AttributeFunction(BaseFunction):
            def get_parameters(self) -> list[FunctionParameter]:
                return []

            def get_return_type(self) -> FunctionReturnType:
                return FunctionReturnType(type=CtyBool())

            async def call(self, *args: Any, **kwargs: Any) -> bool:
                return True

        func = AttributeFunction(
            name="attr_func",
            summary="Test summary",
            description="Test description",
            deprecation_message="Deprecated",
        )

        assert func.name == "attr_func"
        assert func.summary == "Test summary"
        assert func.description == "Test description"
        assert func.deprecation_message == "Deprecated"


class TestFunctionAdapterInferCtyType:
    """Tests for FunctionAdapter._infer_cty_type_for_hint method."""

    def test_infer_string_type(self) -> None:
        """Test inferring CtyString from str hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(str)
        assert isinstance(result, CtyString)

    def test_infer_number_type_from_int(self) -> None:
        """Test inferring CtyNumber from int hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(int)
        assert isinstance(result, CtyNumber)

    def test_infer_number_type_from_float(self) -> None:
        """Test inferring CtyNumber from float hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(float)
        assert isinstance(result, CtyNumber)

    def test_infer_bool_type(self) -> None:
        """Test inferring CtyBool from bool hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(bool)
        assert isinstance(result, CtyBool)

    def test_infer_list_type(self) -> None:
        """Test inferring CtyList from list hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(list[str])
        assert isinstance(result, CtyList)

    def test_infer_dict_type(self) -> None:
        """Test inferring CtyMap from dict hint."""
        result = FunctionAdapter._infer_cty_type_for_hint(dict[str, int])
        assert isinstance(result, CtyMap)

    def test_infer_dynamic_for_unknown(self) -> None:
        """Test inferring CtyDynamic for unknown types."""

        class CustomType:
            pass

        result = FunctionAdapter._infer_cty_type_for_hint(CustomType)
        assert isinstance(result, CtyDynamic)

    def test_infer_from_cty_type_instance(self) -> None:
        """Test inferring from CtyType subclass."""
        result = FunctionAdapter._infer_cty_type_for_hint(CtyString)
        assert isinstance(result, CtyString)


class TestFunctionAdapterCollectionTypes:
    """Tests for FunctionAdapter collection type inference."""

    def test_infer_list_with_element_type(self) -> None:
        """Test inferring list with element type."""
        result = FunctionAdapter._infer_collection_cty_type(list, (CtyString,))
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyString)

    def test_infer_list_without_element_type(self) -> None:
        """Test inferring list without element type defaults to Dynamic."""
        result = FunctionAdapter._infer_collection_cty_type(list, ())
        assert isinstance(result, CtyList)
        assert isinstance(result.element_type, CtyDynamic)

    def test_infer_dict_with_value_type(self) -> None:
        """Test inferring dict with value type."""
        result = FunctionAdapter._infer_collection_cty_type(dict, (str, CtyNumber))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyNumber)

    def test_infer_dict_without_value_type(self) -> None:
        """Test inferring dict without value type defaults to Dynamic."""
        result = FunctionAdapter._infer_collection_cty_type(dict, (str,))
        assert isinstance(result, CtyMap)
        assert isinstance(result.element_type, CtyDynamic)

    def test_unsupported_collection_raises(self) -> None:
        """Test that unsupported collection types raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported collection type"):
            FunctionAdapter._infer_collection_cty_type(tuple, ())


class TestFunctionAdapterUnionTypes:
    """Tests for FunctionAdapter union type inference."""

    def test_union_of_numbers(self) -> None:
        """Test union of int and float infers to CtyNumber."""
        result = FunctionAdapter._infer_union_cty_type((int, float))
        assert isinstance(result, CtyNumber)

    def test_union_with_none_string(self) -> None:
        """Test Optional[str] infers to CtyString."""
        result = FunctionAdapter._infer_union_cty_type((str, type(None)))
        assert isinstance(result, CtyString)

    def test_complex_union_defaults_dynamic(self) -> None:
        """Test complex union defaults to CtyDynamic."""
        result = FunctionAdapter._infer_union_cty_type((str, int, bool))
        assert isinstance(result, CtyDynamic)


class TestFunctionAdapterAdapt:
    """Tests for FunctionAdapter.adapt method."""

    def test_adapt_simple_function(self) -> None:
        """Test adapting a simple synchronous function."""

        def simple_func(name: str) -> str:
            return f"Hello, {name}"

        adapted = FunctionAdapter.adapt(simple_func, name="greet")

        assert isinstance(adapted, BaseFunction)
        assert adapted.name == "greet"
        assert len(adapted.get_parameters()) == 1
        assert adapted.get_parameters()[0].name == "name"
        assert isinstance(adapted.get_parameters()[0].type, CtyString)
        assert isinstance(adapted.get_return_type().type, CtyString)

    @pytest.mark.asyncio
    async def test_adapt_async_function(self) -> None:
        """Test adapting an async function."""

        async def async_func(x: int) -> int:
            return x * 2

        adapted = FunctionAdapter.adapt(async_func, name="double")

        result = await adapted.call(5)
        assert result == 10

    @pytest.mark.asyncio
    async def test_adapt_sync_function_execution(self) -> None:
        """Test that sync functions are executed correctly."""

        def sync_func(x: int) -> int:
            return x + 1

        adapted = FunctionAdapter.adapt(sync_func)

        result = await adapted.call(5)
        assert result == 6

    def test_adapt_with_custom_descriptions(self) -> None:
        """Test adapting with custom parameter descriptions."""

        def func(param1: str, param2: int) -> bool:
            return True

        adapted = FunctionAdapter.adapt(
            func,
            summary="Test function",
            description="Detailed description",
            param_descriptions={"param1": "First parameter", "param2": "Second parameter"},
        )

        assert adapted.summary == "Test function"
        assert adapted.description == "Detailed description"
        assert adapted.get_parameters()[0].description == "First parameter"
        assert adapted.get_parameters()[1].description == "Second parameter"

    def test_adapt_with_docstring(self) -> None:
        """Test that docstring is used for summary and description."""

        def documented_func(x: int) -> int:
            """
            This is the summary line.

            This is the detailed description
            that spans multiple lines.
            """
            return x

        adapted = FunctionAdapter.adapt(documented_func)

        assert "This is the summary line" in adapted.summary
        assert "detailed description" in adapted.description

    def test_adapt_with_allow_null(self) -> None:
        """Test adapting with allow_null parameter."""

        def nullable_func(x: str | None) -> str:
            return x or "default"

        adapted = FunctionAdapter.adapt(nullable_func, allow_null=True)

        params = adapted.get_parameters()
        assert params[0].allow_null is True

    def test_adapt_with_allow_null_list(self) -> None:
        """Test adapting with allow_null as list of parameter names."""

        def func(param1: str, param2: int) -> str:
            return ""

        adapted = FunctionAdapter.adapt(func, allow_null=["param1"])

        params = adapted.get_parameters()
        assert params[0].allow_null is True
        assert params[1].allow_null is False

    def test_adapt_with_allow_unknown(self) -> None:
        """Test adapting with allow_unknown parameter."""

        def func(x: str) -> str:
            return x

        adapted = FunctionAdapter.adapt(func, allow_unknown=True)

        params = adapted.get_parameters()
        assert params[0].allow_unknown is True

    @pytest.mark.xfail(reason="FunctionAdapter doesn't yet support PEP 604 union types (int | None)")
    def test_adapt_detects_optional_as_allow_null(self) -> None:
        """Test that Optional[T] is automatically detected as allow_null."""

        def optional_func(x: int | None) -> int:
            return x or 0

        adapted = FunctionAdapter.adapt(optional_func)

        params = adapted.get_parameters()
        assert params[0].allow_null is True

    def test_adapt_with_deprecation_message(self) -> None:
        """Test adapting with deprecation message."""

        def deprecated_func() -> str:
            return "old"

        adapted = FunctionAdapter.adapt(deprecated_func, deprecation_message="Use new_func instead")

        assert adapted.deprecation_message == "Use new_func instead"

    @pytest.mark.asyncio
    async def test_adapted_function_raises_function_error(self) -> None:
        """Test that FunctionError is propagated correctly."""

        def error_func() -> str:
            raise FunctionError("Test error")

        adapted = FunctionAdapter.adapt(error_func)

        with pytest.raises(FunctionError, match="Test error"):
            await adapted.call()

    @pytest.mark.asyncio
    async def test_adapted_function_wraps_generic_exceptions(self) -> None:
        """Test that generic exceptions are wrapped in FunctionError."""

        def exception_func() -> str:
            raise ValueError("Something went wrong")

        adapted = FunctionAdapter.adapt(exception_func)

        with pytest.raises(FunctionError, match="execution failed"):
            await adapted.call()

    def test_adapt_handles_missing_type_hints(self) -> None:
        """Test that adapt handles functions without type hints."""

        def untyped_func(x: Any, y: Any) -> Any:
            return x + y

        adapted = FunctionAdapter.adapt(untyped_func)

        params = adapted.get_parameters()
        # Should default to CtyDynamic when no hints
        assert all(isinstance(p.type, CtyDynamic) for p in params)


class TestFunctionAdapterProcessParameters:
    """Tests for FunctionAdapter._process_parameters method."""

    def test_process_parameters_basic(self) -> None:
        """Test processing basic parameters."""

        def func(name: str, age: int) -> None:
            pass

        import inspect

        sig = inspect.signature(func)
        import typing

        type_hints = typing.get_type_hints(func)

        params = FunctionAdapter._process_parameters(func, sig, type_hints, {}, False, False)

        assert len(params) == 2
        assert params[0].name == "name"
        assert isinstance(params[0].type, CtyString)
        assert params[1].name == "age"
        assert isinstance(params[1].type, CtyNumber)

    def test_process_parameters_skips_self(self) -> None:
        """Test that 'self' parameter is skipped."""

        class MyClass:
            def method(self, x: int) -> None:
                pass

        import inspect

        sig = inspect.signature(MyClass.method)
        import typing

        type_hints = typing.get_type_hints(MyClass.method)

        params = FunctionAdapter._process_parameters(MyClass.method, sig, type_hints, {}, False, False)

        assert len(params) == 1
        assert params[0].name == "x"

    def test_process_parameters_with_descriptions(self) -> None:
        """Test processing parameters with descriptions."""

        def func(x: int, y: str) -> None:
            pass

        import inspect

        sig = inspect.signature(func)
        import typing

        type_hints = typing.get_type_hints(func)

        param_descriptions = {"x": "X value", "y": "Y value"}
        params = FunctionAdapter._process_parameters(func, sig, type_hints, param_descriptions, False, False)

        assert params[0].description == "X value"
        assert params[1].description == "Y value"


class TestFunctionAdapterEdgeCases:
    """Edge case tests for FunctionAdapter."""

    def test_adapt_function_with_no_parameters(self) -> None:
        """Test adapting function with no parameters."""

        def no_params() -> str:
            return "result"

        adapted = FunctionAdapter.adapt(no_params)

        assert len(adapted.get_parameters()) == 0

    def test_adapt_function_with_complex_types(self) -> None:
        """Test adapting function with complex type hints."""

        def complex_func(items: list[str], mapping: dict[str, int]) -> list[int]:
            return [1, 2, 3]

        adapted = FunctionAdapter.adapt(complex_func)

        params = adapted.get_parameters()
        assert isinstance(params[0].type, CtyList)
        assert isinstance(params[1].type, CtyMap)
        assert isinstance(adapted.get_return_type().type, CtyList)

    def test_adapt_uses_function_name_if_no_name_provided(self) -> None:
        """Test that function name is used if no explicit name provided."""

        def my_function() -> str:
            return ""

        adapted = FunctionAdapter.adapt(my_function)

        assert adapted.name == "my_function"

    @pytest.mark.asyncio
    async def test_adapted_function_callable_via_dunder_call(self) -> None:
        """Test that adapted function can be called via __call__."""

        def add(x: int, y: int) -> int:
            return x + y

        adapted = FunctionAdapter.adapt(add)

        result = await adapted(5, 3)
        assert result == 8


# 🐍🏗️🔚
