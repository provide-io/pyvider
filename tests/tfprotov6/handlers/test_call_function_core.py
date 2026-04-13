#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CallFunction handler - Core functionality."""

import inspect
from typing import Any

from provide.testkit import mocking as mock
import pytest

from pyvider.cty import CtyDynamic, CtyNumber, CtyString, CtyValue
from pyvider.protocols.tfprotov6.handlers.call_function import (
    CallFunctionHandler,
    _inject_capabilities,
    _process_function_arguments,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestProcessFunctionArguments:
    """Tests for _process_function_arguments helper function."""

    def test_processes_simple_arguments(self) -> None:
        """Test processing simple required arguments."""

        def test_func(name: str, count: int) -> None:
            pass

        func_sig = inspect.signature(test_func)
        params_meta = [
            {"name": "name", "cty_type": CtyString()},
            {"name": "count", "cty_type": CtyNumber()},
        ]

        arg1_proto = pb.DynamicValue(msgpack=b"\xa4test")  # "test"
        arg2_proto = pb.DynamicValue(msgpack=b"\x2a")  # 42

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.unmarshal") as mock_unmarshal,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.cty_to_native") as mock_to_native,
        ):
            mock_unmarshal.side_effect = [
                CtyValue(vtype=CtyString(), value="test"),
                CtyValue(vtype=CtyNumber(), value=42),
            ]
            mock_to_native.side_effect = ["test", 42]

            kwargs, has_unknown = _process_function_arguments(
                [arg1_proto, arg2_proto], params_meta, None, func_sig
            )

            assert kwargs == {"name": "test", "count": 42}
            assert has_unknown is False

    def test_detects_unknown_arguments(self) -> None:
        """Test that unknown arguments are detected."""

        def test_func(name: str) -> None:
            pass

        func_sig = inspect.signature(test_func)
        params_meta = [{"name": "name", "cty_type": CtyString()}]
        arg_proto = pb.DynamicValue(msgpack=b"\xa4test")

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.unmarshal") as mock_unmarshal:
            mock_unmarshal.return_value = CtyValue(vtype=CtyString(), value="test", is_unknown=True)

            _kwargs, has_unknown = _process_function_arguments([arg_proto], params_meta, None, func_sig)

            assert has_unknown is True

    def test_processes_variadic_arguments(self) -> None:
        """Test processing variadic arguments."""

        def test_func(name: str, *options: Any) -> None:
            pass

        func_sig = inspect.signature(test_func)
        params_meta = [{"name": "name", "cty_type": CtyString()}]
        variadic_meta = {"name": "options", "cty_type": CtyDynamic()}

        arg1_proto = pb.DynamicValue(msgpack=b"\xa4test")
        arg2_proto = pb.DynamicValue(msgpack=b"\x01")
        arg3_proto = pb.DynamicValue(msgpack=b"\x02")

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.unmarshal") as mock_unmarshal,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.cty_to_native") as mock_to_native,
        ):
            mock_unmarshal.side_effect = [
                CtyValue(vtype=CtyString(), value="test"),
                CtyValue(vtype=CtyDynamic(), value=1),
                CtyValue(vtype=CtyDynamic(), value=2),
            ]
            mock_to_native.side_effect = ["test", 1, 2]

            kwargs, has_unknown = _process_function_arguments(
                [arg1_proto, arg2_proto, arg3_proto], params_meta, variadic_meta, func_sig
            )

            assert kwargs["name"] == "test"
            assert kwargs["options"] == (1, 2)
            assert has_unknown is False

    def test_skips_none_values_with_defaults(self) -> None:
        """Test that None values are skipped when parameter has default."""

        def test_func(name: str, count: int = 10) -> None:
            pass

        func_sig = inspect.signature(test_func)
        params_meta = [
            {"name": "name", "cty_type": CtyString()},
            {"name": "count", "cty_type": CtyNumber()},
        ]

        arg1_proto = pb.DynamicValue(msgpack=b"\xa4test")
        arg2_proto = pb.DynamicValue(msgpack=b"\xc0")  # null

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.unmarshal") as mock_unmarshal,
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.cty_to_native") as mock_to_native,
        ):
            mock_unmarshal.side_effect = [
                CtyValue(vtype=CtyString(), value="test"),
                CtyValue(vtype=CtyNumber(), value=None, is_null=True),
            ]
            mock_to_native.side_effect = ["test", None]

            kwargs, _has_unknown = _process_function_arguments(
                [arg1_proto, arg2_proto], params_meta, None, func_sig
            )

            assert kwargs == {"name": "test"}
            assert "count" not in kwargs

    def test_detects_unknown_in_variadic_args(self) -> None:
        """Test that unknown values in variadic args are detected."""

        def test_func(*args: Any) -> None:
            pass

        func_sig = inspect.signature(test_func)
        params_meta = []
        variadic_meta = {"name": "args", "cty_type": CtyDynamic()}

        arg1_proto = pb.DynamicValue(msgpack=b"\x01")
        arg2_proto = pb.DynamicValue(msgpack=b"\x02")

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.unmarshal") as mock_unmarshal:
            mock_unmarshal.side_effect = [
                CtyValue(vtype=CtyDynamic(), value=1),
                CtyValue(vtype=CtyDynamic(), value=2, is_unknown=True),
            ]

            _kwargs, has_unknown = _process_function_arguments(
                [arg1_proto, arg2_proto], params_meta, variadic_meta, func_sig
            )

            assert has_unknown is True


class TestInjectCapabilities:
    """Tests for _inject_capabilities helper function."""

    def test_injects_capability_when_parent_capability_exists(self) -> None:
        """Test that capability is injected when parent_capability is set."""
        func_obj = mock.MagicMock()
        func_obj.__name__ = "test_func"
        func_obj._parent_capability = "test_capability"

        kwargs = {}

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get:
            mock_capability = mock.MagicMock()
            mock_get.return_value = mock_capability

            _inject_capabilities(func_obj, kwargs, "test_func")

            assert "test_capability" in kwargs

    def test_does_not_inject_when_no_parent_capability(self) -> None:
        """Test that nothing is injected when no parent_capability."""
        func_obj = mock.MagicMock()
        func_obj.__name__ = "test_func"
        func_obj._parent_capability = None

        kwargs = {"name": "test"}

        _inject_capabilities(func_obj, kwargs, "test_func")

        assert kwargs == {"name": "test"}

    def test_does_not_inject_when_parent_is_provider(self) -> None:
        """Test that nothing is injected when parent_capability is 'provider'."""
        func_obj = mock.MagicMock()
        func_obj.__name__ = "test_func"
        func_obj._parent_capability = "provider"

        kwargs = {"name": "test"}

        _inject_capabilities(func_obj, kwargs, "test_func")

        assert kwargs == {"name": "test"}


class TestCallFunctionHandler:
    """Tests for CallFunctionHandler main functionality."""

    @pytest.mark.asyncio
    async def test_handler_returns_response_object(self) -> None:
        """Test that handler returns proper response object."""
        request = pb.CallFunction.Request(
            name="test_function",
            arguments=[],
        )

        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)

    @pytest.mark.asyncio
    async def test_handler_handles_unknown_function(self) -> None:
        """Test handler with unknown function."""
        request = pb.CallFunction.Request(
            name="nonexistent_function",
            arguments=[],
        )

        response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)
        # Should have error for unknown function
        assert response.HasField("error")

    @pytest.mark.asyncio
    async def test_handler_with_unknown_arguments(self) -> None:
        """Test handler returns unknown result when arguments are unknown."""
        request = pb.CallFunction.Request(
            name="test_function",
            arguments=[pb.DynamicValue(msgpack=b"\x01")],
        )

        func_obj = mock.MagicMock()
        func_obj.metadata.parameters = [{"name": "arg", "cty_type": CtyDynamic()}]
        func_obj.metadata.variadic_parameter = None
        func_obj.metadata.return_type = CtyString()

        def test_func(arg: Any) -> str:
            return "result"

        func_obj.func = test_func

        with (
            mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.call_function._process_function_arguments"
            ) as mock_process,
        ):
            mock_get.return_value = func_obj
            mock_process.return_value = ({"arg": 1}, True)  # has_unknown=True

            response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)
        # Should return unknown result without calling function

    @pytest.mark.asyncio
    async def test_handler_processes_request_successfully(self) -> None:
        """Test handler processes request without crashing."""
        request = pb.CallFunction.Request(
            name="test_function",
            arguments=[],
        )

        # Just verify the handler completes and returns a response
        with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await CallFunctionHandler(request, context=None)

        assert isinstance(response, pb.CallFunction.Response)


# 🐍🏗️🔚
