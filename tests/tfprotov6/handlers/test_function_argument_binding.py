#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A null argument with a default must not shift the arguments after it.

`_process_function_arguments` drops a parameter from the collected keywords when
Terraform sent null and the Python parameter carries a default, so that the
default applies. `_build_function_arguments` then rebuilt every
positional-or-keyword parameter into an ordered list, and a gap in the middle of
that list silently moved every later argument one place to the left.

    def pad(text, width=10, fill=" ")
    provider::x::pad("x", null, "-")   ->   text="x", width="-", fill=" "

No error, no diagnostic, just the wrong answer. Python lets a
positional-or-keyword parameter be passed by name, so gaps stop mattering once
they are bound that way.

Also covered here: a function that fails on one argument can say which one.
`FunctionError.function_argument` is what Terraform uses to point at the
offending expression (internal/plugin6/grpc_provider.go:1303-1312); it was never
populated, so every function error pointed at the call as a whole.
"""

from typing import Any

from provide.testkit import mocking as mock
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyString, CtyValue
from pyvider.exceptions import FunctionError
from pyvider.functions.decorators import register_function
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
import pyvider.protocols.tfprotov6.protobuf as pb


def _arg(value: Any, vtype: Any) -> pb.DynamicValue:
    return marshal(CtyValue(vtype=vtype, value=value), schema=vtype)


async def _call(func: Any, name: str, *args: pb.DynamicValue) -> pb.CallFunction.Response:
    request = pb.CallFunction.Request(name=name, arguments=list(args))
    with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as get:
        get.return_value = func
        return await CallFunctionHandler(request, context=None)


@register_function(name="pad_text")
def pad_text(text: str, width: str = "10", fill: str = " ") -> str:
    """Return the three arguments as received, so binding is observable."""
    return f"{text}|{width}|{fill}"


@register_function(name="explode_on_second")
def explode_on_second(first: str, second: str) -> str:
    """Rejects its second argument, and says so."""
    if second == "bad":
        raise FunctionError("second argument is not acceptable", argument_index=1)
    return first + second


@pytest.mark.asyncio
async def test_a_null_middle_argument_does_not_shift_the_later_ones() -> None:
    response = await _call(
        pad_text,
        "pad_text",
        _arg("x", CtyString()),
        _arg(None, CtyString()),
        _arg("-", CtyString()),
    )

    assert not response.HasField("error"), response.error.text
    assert unmarshal(response.result, schema=CtyString()).value == "x|10|-", (
        "the null middle argument was dropped from a positional list, so `fill` "
        "was bound to `width` and every later argument moved left"
    )


@pytest.mark.asyncio
async def test_all_arguments_supplied_still_bind_in_order() -> None:
    response = await _call(
        pad_text,
        "pad_text",
        _arg("x", CtyString()),
        _arg("7", CtyString()),
        _arg("-", CtyString()),
    )

    assert not response.HasField("error"), response.error.text
    assert unmarshal(response.result, schema=CtyString()).value == "x|7|-"


@pytest.mark.asyncio
async def test_a_trailing_null_still_takes_its_default() -> None:
    response = await _call(
        pad_text,
        "pad_text",
        _arg("x", CtyString()),
        _arg("7", CtyString()),
        _arg(None, CtyString()),
    )

    assert not response.HasField("error"), response.error.text
    assert unmarshal(response.result, schema=CtyString()).value == "x|7| "


@pytest.mark.asyncio
async def test_a_function_error_names_the_argument_it_rejected() -> None:
    response = await _call(
        explode_on_second,
        "explode_on_second",
        _arg("ok", CtyString()),
        _arg("bad", CtyString()),
    )

    assert response.HasField("error"), "the function's rejection was not reported"
    assert response.error.HasField("function_argument"), (
        "the error does not say which argument was rejected, so Terraform points "
        "at the whole call instead of the offending expression"
    )
    assert response.error.function_argument == 1


@pytest.mark.asyncio
async def test_an_error_without_an_index_omits_the_field() -> None:
    """Only an error that knows the argument should claim to."""
    response = await _call(
        explode_on_second,
        "explode_on_second",
        _arg("ok", CtyString()),
        _arg("fine", CtyString()),
    )

    assert not response.HasField("error"), response.error.text


# 🐍🏗️🔚
