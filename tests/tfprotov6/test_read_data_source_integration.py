#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest

from pyvider.data_sources.base import BaseDataSource
from pyvider.hub import hub, register_data_source
from pyvider.protocols.tfprotov6.handlers.read_data_source import ReadDataSourceHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.schema import a_dyn, s_data_source


@attrs.define(frozen=True)
class DynamicOutputState:
    output: Any


@register_data_source("test_dynamic_ds")
class DynamicDataSource(BaseDataSource["test_dynamic_ds", DynamicOutputState, None]):
    state_class = DynamicOutputState
    config_class = None

    @classmethod
    def get_schema(cls) -> s_data_source:
        return s_data_source({"output": a_dyn(computed=True)})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> DynamicOutputState:
        return DynamicOutputState(output={"a": 1, "b": ["x", "y"]})


@pytest.mark.asyncio
async def test_read_data_source_with_dynamic_output() -> None:
    hub.register("data_source", "test_dynamic_ds", DynamicDataSource)
    try:
        request = pb.ReadDataSource.Request(type_name="test_dynamic_ds")
        response = await ReadDataSourceHandler(request, None)
        assert not response.diagnostics, (
            f"ReadDataSource failed: {response.diagnostics[0].detail if response.diagnostics else 'Unknown error'}"
        )
        assert response.state.msgpack is not None
    finally:
        hub.unregister("data_source", "test_dynamic_ds")


# 🐍🏗️🔚
