#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyNumber, CtyString
from pyvider.hub import hub, register_function
from pyvider.protocols.tfprotov6.handlers import CallFunctionHandler
import pyvider.protocols.tfprotov6.protobuf as pb

# --- Test Functions ---


@register_function(name="add_numbers")
def add_numbers_func(a: int, b: int) -> int:
    return a + b


@register_function(name="greet")
def greet_func(name: str, suffix: str = "!") -> str:
    # Note: The type hint is no longer Optional, the default value handles it.
    return f"Hello, {name}{suffix}"


@pytest.fixture(autouse=True)
def register_test_functions() -> None:
    """Ensures test functions are registered for each test run."""
    hub.register("function", "add_numbers", add_numbers_func)
    hub.register("function", "greet", greet_func)
    yield
    hub.unregister("function", "add_numbers")
    hub.unregister("function", "greet")


@pytest.mark.asyncio
class TestFunctionDispatch:
    """
    TDD: Verifies the CallFunctionHandler correctly dispatches calls,
    validates argument counts and types, and handles errors gracefully.
    """

    async def test_dispatch_success_with_valid_args(self) -> None:
        """TDD: Handler succeeds with correct argument types."""
        arg1 = marshal(10, schema=CtyNumber())
        arg2 = marshal(20, schema=CtyNumber())
        request = pb.CallFunction.Request(name="add_numbers", arguments=[arg1, arg2])

        response = await CallFunctionHandler(request, context=None)

        assert not response.error.text, f"Function call failed unexpectedly: {response.error.text}"
        result_cty = unmarshal(response.result, schema=CtyNumber())
        assert result_cty.value == 30

    async def test_dispatch_fails_with_wrong_arg_count(self) -> None:
        """TDD: Handler returns an error for incorrect number of arguments."""
        arg1 = marshal(10, schema=CtyNumber())
        request = pb.CallFunction.Request(name="add_numbers", arguments=[arg1])

        response = await CallFunctionHandler(request, context=None)

        assert response.error.text
        assert "Incorrect number of arguments" in response.error.text
        assert "Expected: 2 arguments" in response.error.text
        assert "Received: 1 arguments" in response.error.text

    async def test_dispatch_fails_with_wrong_arg_type(self) -> None:
        """TDD: Handler returns a type validation error for mismatched types."""
        arg1 = marshal(10, schema=CtyNumber())
        arg2 = marshal("twenty", schema=CtyString())  # This is the wrong type
        request = pb.CallFunction.Request(name="add_numbers", arguments=[arg1, arg2])

        response = await CallFunctionHandler(request, context=None)

        assert response.error.text
        # FIX: Update assertion to match the improved, more specific error message.
        assert "Number validation error" in response.error.text
        assert "Cannot represent str value 'twenty' as Decimal" in response.error.text

    async def test_dispatch_handles_optional_null_arg(self) -> None:
        """TDD: Handler correctly uses default value when a null is passed for an optional argument."""
        arg1 = marshal("World", schema=CtyString())
        arg2 = marshal(None, schema=CtyString())  # Pass null for the optional arg
        request = pb.CallFunction.Request(name="greet", arguments=[arg1, arg2])

        response = await CallFunctionHandler(request, context=None)

        assert not response.error.text, f"Function call failed unexpectedly: {response.error.text}"
        result_cty = unmarshal(response.result, schema=CtyString())
        assert result_cty.value == "Hello, World!"


# 🐍🏗️🔚
