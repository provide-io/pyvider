#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal
from pyvider.cty import CtyDynamic
from pyvider.data_sources.base import BaseDataSource
from pyvider.hub import hub, register_data_source, register_function
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
from pyvider.protocols.tfprotov6.handlers.read_data_source import ReadDataSourceHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.schema import a_dyn, s_data_source


@register_function(name="test_identity")
def identity_func(input_data: Any) -> Any:
    return input_data


@attrs.define(frozen=True)
class DynamicState:
    data: Any


@register_data_source("test_dynamic_ds")
class DynamicDataSource(BaseDataSource["test_dynamic_ds", DynamicState, None]):
    state_class = DynamicState
    config_class = None

    @classmethod
    def get_schema(cls) -> s_data_source:
        return s_data_source({"data": a_dyn(computed=True)})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> DynamicState:
        return DynamicState(data={"nested": True, "items": [1, "b"]})


@pytest.mark.asyncio
async def test_call_function_integration_avoids_recursion() -> None:
    hub.register("function", "test_identity", identity_func)
    try:
        complex_input = {"level1": {"items": [{"tag": "A"}]}}
        dynamic_value_in = marshal(complex_input, schema=CtyDynamic())
        request = pb.CallFunction.Request(name="test_identity", arguments=[dynamic_value_in])
        response = await CallFunctionHandler(request, None)
        assert not response.error.text
    finally:
        hub.unregister("function", "test_identity")


@pytest.mark.asyncio
async def test_read_data_source_integration_avoids_recursion() -> None:
    hub.register("data_source", "test_dynamic_ds", DynamicDataSource)
    try:
        request = pb.ReadDataSource.Request(type_name="test_dynamic_ds")
        response = await ReadDataSourceHandler(request, None)
        assert not response.diagnostics
    finally:
        hub.unregister("data_source", "test_dynamic_ds")


# 🐍🏗️🔚
