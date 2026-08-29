#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A Python parameter carrying a default is reachable from Terraform.

`_extract_parameters_meta` promotes such a parameter into the schema's
`variadic_parameter`, because tfproto v6 has no notion of an optional
positional parameter -- `variadic_parameter` is the only trailing thing
Terraform will let a caller omit. These tests run the real handler over real
msgpack so that the value Terraform sends actually reaches the function.
"""

from typing import Any

from provide.testkit import mocking as mock
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyNumber, CtyString, CtyValue
from pyvider.functions.decorators import register_function
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
import pyvider.protocols.tfprotov6.protobuf as pb


def _arg(value: Any, vtype: Any) -> pb.DynamicValue:
    """Marshal a native value the way Terraform sends it."""
    return marshal(CtyValue(vtype=vtype, value=value), schema=vtype)


async def _call(func: Any, name: str, *args: pb.DynamicValue) -> pb.CallFunction.Response:
    request = pb.CallFunction.Request(name=name, arguments=list(args))
    with mock.patch("pyvider.protocols.tfprotov6.handlers.call_function.hub.get_component") as get:
        get.return_value = func
        return await CallFunctionHandler(request, context=None)


def _result(response: pb.CallFunction.Response, vtype: Any) -> Any:
    assert not response.HasField("error"), response.error.text
    return unmarshal(response.result, schema=vtype).value


@register_function(name="repeat_text")
def repeat_text(text: str, count: int = 2) -> str:
    """Repeat `text` `count` times."""
    return text * count


@register_function(name="star_join")
def star_join(sep: str, *parts: str) -> str:
    """Join `parts` with `sep`."""
    return sep.join(parts)


class TestDefaultCarryingParameter:
    """A parameter with a default is bound from the wire, not discarded."""

    @pytest.mark.asyncio
    async def test_supplied_default_parameter_reaches_the_function(self) -> None:
        response = await _call(
            repeat_text,
            "repeat_text",
            _arg("ab", CtyString()),
            _arg(5, CtyNumber()),
        )
        assert _result(response, CtyString()) == "ababababab"

    @pytest.mark.asyncio
    async def test_omitted_default_parameter_uses_the_python_default(self) -> None:
        response = await _call(repeat_text, "repeat_text", _arg("ab", CtyString()))
        assert _result(response, CtyString()) == "abab"

    @pytest.mark.asyncio
    async def test_too_many_arguments_is_an_error_not_a_silent_drop(self) -> None:
        """One slot, three values: refuse rather than bind the first and drop two."""
        response = await _call(
            repeat_text,
            "repeat_text",
            _arg("ab", CtyString()),
            _arg(1, CtyNumber()),
            _arg(2, CtyNumber()),
            _arg(3, CtyNumber()),
        )
        assert response.HasField("error")
        assert "repeat_text" in response.error.text


class TestVarPositionalParameter:
    """A real *args parameter keeps working."""

    @pytest.mark.asyncio
    async def test_var_positional_collects_every_trailing_argument(self) -> None:
        response = await _call(
            star_join,
            "star_join",
            _arg("-", CtyString()),
            _arg("a", CtyString()),
            _arg("b", CtyString()),
            _arg("c", CtyString()),
        )
        assert _result(response, CtyString()) == "a-b-c"

    @pytest.mark.asyncio
    async def test_var_positional_with_no_trailing_arguments(self) -> None:
        response = await _call(star_join, "star_join", _arg("-", CtyString()))
        assert _result(response, CtyString()) == ""


class TestExplicitNull:
    """Terraform sends null for an argument the practitioner left out."""

    @pytest.mark.asyncio
    async def test_null_for_a_defaulted_parameter_means_omitted(self) -> None:
        response = await _call(
            repeat_text,
            "repeat_text",
            _arg("ab", CtyString()),
            marshal(CtyValue.null(CtyNumber()), schema=CtyNumber()),
        )
        assert _result(response, CtyString()) == "abab"

    @pytest.mark.asyncio
    async def test_null_reaching_var_positional_is_a_real_element(self) -> None:
        """*args has no default to fall back to, so a null is an argument."""

        @register_function(name="count_parts")
        def count_parts(sep: str, *parts: str) -> str:
            return f"{len(parts)}:{parts}"

        response = await _call(
            count_parts,
            "count_parts",
            _arg("-", CtyString()),
            marshal(CtyValue.null(CtyString()), schema=CtyString()),
        )
        assert _result(response, CtyString()) == "1:(None,)"


@register_function(name="three_slots")
def three_slots(a: str, b: int = 1, c: int = 2) -> str:
    """Two defaults: more than the one variadic slot tfproto v6 offers."""
    return f"a={a} b={b} c={c}"


class TestMoreDefaultsThanSlots:
    """Two defaulted parameters cannot share one variadic slot without scrambling."""

    def test_no_parameter_is_variadic_when_several_carry_defaults(self) -> None:
        from pyvider.functions.adapters import function_to_dict

        meta = function_to_dict(three_slots)
        assert meta.get("variadic_parameter") is None
        assert [p["name"] for p in meta["parameters"]] == ["a", "b", "c"]

    @pytest.mark.asyncio
    async def test_arguments_arrive_in_the_order_they_were_written(self) -> None:
        response = await _call(
            three_slots,
            "three_slots",
            _arg("x", CtyString()),
            _arg(9, CtyNumber()),
            _arg(7, CtyNumber()),
        )
        assert _result(response, CtyString()) == "a=x b=9 c=7"


# 🐍🏗️🔚
