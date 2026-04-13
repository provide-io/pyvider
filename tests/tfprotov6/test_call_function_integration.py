#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import pytest

from pyvider.conversion import marshal
from pyvider.cty import CtyDynamic
from pyvider.hub import hub, register_function
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
import pyvider.protocols.tfprotov6.protobuf as pb


@register_function(name="test_identity")
def identity_func(input_data: Any) -> Any:
    return input_data


@pytest.mark.asyncio
async def test_call_function_with_complex_object_avoids_recursion() -> None:
    hub.register("function", "test_identity", identity_func)
    try:
        complex_input = {
            "level1": {
                "name": "L1",
                "items": [{"tag": "A", "value": 1}, {"tag": "B", "value": 2}],
            },
            "enabled": True,
        }
        cty_val = CtyDynamic().validate(complex_input)
        # THE FIX: Provide the schema to the marshaller.
        dynamic_value_in = marshal(cty_val, schema=CtyDynamic())
        request = pb.CallFunction.Request(name="test_identity", arguments=[dynamic_value_in])
        response = await CallFunctionHandler(request, None)
        assert not response.error.text, f"Function call failed with error: {response.error.text}"
    finally:
        hub.unregister("function", "test_identity")


# 🐍🏗️🔚
