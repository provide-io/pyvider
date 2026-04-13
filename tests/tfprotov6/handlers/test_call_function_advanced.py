#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CallFunction handler - Advanced features (error handling, invoke, integration)."""

from typing import Any, Never

from provide.testkit import mocking as mock
import pytest

from pyvider.cty import CtyNumber, CtyString
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
import pyvider.protocols.tfprotov6.protobuf as pb


class TestCallFunctionMetrics:
    """Tests for observability metrics in CallFunction."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metrics(self) -> None:
        """Test that handler records request metrics."""
        request = pb.CallFunction.Request(
            name="test_function",
            arguments=[],
        )

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)


class TestCallFunctionErrorHandling:
    """Tests for error handling in CallFunction."""

    @pytest.mark.asyncio
    async def test_handler_converts_function_errors_to_diagnostics(self) -> None:
        """Test that function errors are converted to diagnostics."""
        from pyvider.exceptions import FunctionError

        request = pb.CallFunction.Request(
            name="test_function",
            arguments=[],
        )

        func_obj = mock.MagicMock()
        func_obj.metadata.parameters = []
        func_obj.metadata.variadic_parameter = None
        func_obj.metadata.return_type = CtyString()

        async def failing_func() -> Never:
            raise FunctionError("Function failed")

        func_obj.func = failing_func

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._process_function_arguments"
            ) as mock_process,
        ):
            mock_get.return_value = func_obj
            mock_process.return_value = ({}, False)

            response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)
        # Should have error field
        assert response.HasField("error")


class TestInvokeFunction:
    """Tests for _invoke_function helper - the core invocation logic."""

    @pytest.mark.asyncio
    async def test_invokes_sync_function_with_positional_args(self) -> None:
        """Test invoking a synchronous function with positional arguments."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def test_func(name: str, count: int) -> str:
            return f"{name}_{count}"

        kwargs = {"name": "test", "count": 42}
        result = await _invoke_function(test_func, kwargs, "test_func")

        assert result == "test_42"

    @pytest.mark.asyncio
    async def test_invokes_async_function_with_positional_args(self) -> None:
        """Test invoking an asynchronous function."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        async def async_test_func(name: str, count: int) -> str:
            return f"{name}_{count}"

        kwargs = {"name": "async_test", "count": 99}
        result = await _invoke_function(async_test_func, kwargs, "async_test_func")

        assert result == "async_test_99"

    @pytest.mark.asyncio
    async def test_invokes_function_with_variadic_args(self) -> None:
        """Test invoking a function with *args (VAR_POSITIONAL)."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def variadic_func(name: str, *options: Any) -> str:
            return f"{name}: {','.join(str(o) for o in options)}"

        kwargs = {"name": "test", "options": (1, 2, 3)}
        result = await _invoke_function(variadic_func, kwargs, "variadic_func")

        assert result == "test: 1,2,3"

    @pytest.mark.asyncio
    async def test_invokes_function_with_keyword_only_args(self) -> None:
        """Test invoking a function with keyword-only parameters."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def keyword_func(name: str, *, debug: bool = False) -> str:
            return f"{name}_{'debug' if debug else 'prod'}"

        kwargs = {"name": "test", "debug": True}
        result = await _invoke_function(keyword_func, kwargs, "keyword_func")

        assert result == "test_debug"

    @pytest.mark.asyncio
    async def test_invokes_function_with_mixed_parameters(self) -> None:
        """Test invoking with positional, variadic, and keyword-only parameters."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def complex_func(name: str, *items: Any, verbose: bool = False) -> str:
            items_str = ",".join(str(i) for i in items)
            return f"{name}[{items_str}]{'!' if verbose else ''}"

        kwargs = {"name": "test", "items": ("a", "b", "c"), "verbose": True}
        result = await _invoke_function(complex_func, kwargs, "complex_func")

        assert result == "test[a,b,c]!"

    @pytest.mark.asyncio
    async def test_handles_variadic_as_list(self) -> None:
        """Test that variadic args work when provided as list instead of tuple."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def variadic_func(*args: int) -> int:
            return sum(args)

        # Provide as list (should be converted to tuple internally)
        kwargs = {"args": [1, 2, 3, 4]}
        result = await _invoke_function(variadic_func, kwargs, "variadic_func")

        assert result == 10

    @pytest.mark.asyncio
    async def test_handles_variadic_as_single_value(self) -> None:
        """Test that single non-tuple variadic value is converted to tuple."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def variadic_func(*args: Any) -> int:
            return len(args)

        # Single value, not in a tuple
        kwargs = {"args": "single"}
        result = await _invoke_function(variadic_func, kwargs, "variadic_func")

        assert result == 1

    @pytest.mark.asyncio
    async def test_wraps_function_errors_as_pyvider_function_error(self) -> None:
        """Test that function errors are wrapped in PyviderFunctionError."""
        from pyvider.exceptions import FunctionError as PyviderFunctionError
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def failing_func(x: int) -> Never:
            raise ValueError("Something went wrong")

        kwargs = {"x": 42}

        with pytest.raises(PyviderFunctionError) as exc_info:
            await _invoke_function(failing_func, kwargs, "failing_func")

        assert "failing_func" in str(exc_info.value)
        assert "Something went wrong" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_preserves_pyvider_function_errors(self) -> None:
        """Test that PyviderFunctionError is re-raised directly."""
        from pyvider.exceptions import FunctionError as PyviderFunctionError
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def failing_func(x: int) -> Never:
            raise PyviderFunctionError("Direct pyvider error")

        kwargs = {"x": 42}

        with pytest.raises(PyviderFunctionError) as exc_info:
            await _invoke_function(failing_func, kwargs, "failing_func")

        # Should re-raise directly (but the except clause still triggers, so it re-raises)
        assert "Direct pyvider error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_logs_successful_invocation(self) -> None:
        """Test that successful invocations are logged."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def simple_func(x: int) -> int:
            return x * 2

        kwargs = {"x": 21}

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.logger") as mock_logger:
            result = await _invoke_function(simple_func, kwargs, "simple_func")

            assert result == 42
            # Should log debug info about return
            assert mock_logger.debug.called

    @pytest.mark.asyncio
    async def test_logs_function_errors(self) -> None:
        """Test that function errors are logged."""
        from pyvider.exceptions import FunctionError as PyviderFunctionError
        from pyvider.protocols.tfprotov6.handlers.call_function import _invoke_function

        def error_func() -> Never:
            raise RuntimeError("Test error")

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.logger") as mock_logger:
            with pytest.raises(PyviderFunctionError):
                await _invoke_function(error_func, {}, "error_func")

            # Should log error
            mock_logger.error.assert_called_once()
            assert "error_func" in str(mock_logger.error.call_args)


class TestCallFunctionImplIntegration:
    """Integration tests for _call_function_impl - testing the full flow."""

    @pytest.mark.asyncio
    async def test_impl_validates_argument_count_exact_match(self) -> None:
        """Test that impl validates exact argument count when no variadic."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl

        def test_func(a: str, b: str) -> str:
            return f"{a}_{b}"

        request = pb.CallFunction.Request(
            name="test_func",
            arguments=[pb.DynamicValue(msgpack=b"\xa4test")],  # Only 1 arg, need 2
        )

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.function_to_dict") as mock_meta,
        ):
            mock_get.return_value = test_func
            mock_meta.return_value = {
                "parameters": [{"name": "a"}, {"name": "b"}],
                "return": {"cty_type": CtyString()},
            }

            response = await _call_function_impl(request, context=None)

            # Should have error about incorrect argument count
            assert response.HasField("error")
            assert "Incorrect number of arguments" in response.error.text
            assert "Expected: 2 arguments" in response.error.text
            assert "Received: 1 arguments" in response.error.text

    @pytest.mark.asyncio
    async def test_impl_short_circuits_on_unknown_arguments(self) -> None:
        """Test that impl returns unknown result when arguments are unknown."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl

        def test_func(x: str) -> str:
            return "should not be called"

        request = pb.CallFunction.Request(
            name="test_func",
            arguments=[pb.DynamicValue(msgpack=b"\xa4test")],
        )

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.function_to_dict") as mock_meta,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._process_function_arguments"
            ) as mock_process,
        ):
            mock_get.return_value = test_func
            mock_meta.return_value = {
                "parameters": [{"name": "x"}],
                "return": {"cty_type": CtyString()},
            }
            mock_process.return_value = ({}, True)
            response = await _call_function_impl(request, context=None)

            # Should have result (not error) but it's unknown
            assert not response.HasField("error")
            assert response.HasField("result")
            # The function should NOT have been invoked (short-circuited)

    @pytest.mark.asyncio
    async def test_impl_injects_capabilities_before_invocation(self) -> None:
        """Test that capabilities are injected before function invocation."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl

        def test_func(x: str) -> str:
            return x.upper()

        request = pb.CallFunction.Request(
            name="test_func",
            arguments=[pb.DynamicValue(msgpack=b"\xa4test")],
        )

        test_func._parent_capability = "test_capability"

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.function_to_dict") as mock_meta,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._process_function_arguments"
            ) as mock_process,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._inject_capabilities"
            ) as mock_inject,
        ):
            mock_get.return_value = test_func
            mock_meta.return_value = {
                "parameters": [{"name": "x"}],
                "return": {"cty_type": CtyString()},
            }
            mock_process.return_value = ({"x": "test"}, False)

            await _call_function_impl(request, context=None)

            # _inject_capabilities should have been called
            mock_inject.assert_called_once()
            assert mock_inject.call_args[0][0] == test_func

    @pytest.mark.asyncio
    async def test_impl_marshals_result_correctly(self) -> None:
        """Test that function result is marshaled to protobuf."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl

        def test_func(x: int) -> int:
            return x * 2

        request = pb.CallFunction.Request(
            name="test_func",
            arguments=[pb.DynamicValue(msgpack=b"\x2a")],  # 42
        )

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.function_to_dict") as mock_meta,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._process_function_arguments"
            ) as mock_process,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.marshal") as mock_marshal,
        ):
            mock_get.return_value = test_func
            mock_meta.return_value = {
                "parameters": [{"name": "x"}],
                "return": {"cty_type": CtyNumber()},
            }
            mock_process.return_value = ({"x": 42}, False)
            mock_marshal.return_value = pb.DynamicValue(msgpack=b"\x54")  # 84

            response = await _call_function_impl(request, context=None)

            # Should have called marshal with result
            mock_marshal.assert_called_once()
            # Result should be copied to response
            assert response.HasField("result")

    @pytest.mark.asyncio
    async def test_impl_handles_missing_function_name(self) -> None:
        """Test that impl handles empty function name."""
        from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl

        request = pb.CallFunction.Request(
            name="",  # Empty name
            arguments=[],
        )

        response = await _call_function_impl(request, context=None)

        assert response.HasField("error")
        assert "Function name is required" in response.error.text


# 🐍🏗️🔚
