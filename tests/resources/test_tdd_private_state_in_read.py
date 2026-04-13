#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import msgpack
import pytest

from pyvider.common.encryption import encrypt
from pyvider.conversion import marshal, unmarshal
from pyvider.exceptions import ResourceError
from pyvider.hub import hub, register_resource
from pyvider.protocols.tfprotov6.handlers import ReadResourceHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_num, a_str, s_resource


@attrs.define(frozen=True)
class ReadPrivateState(PrivateState):
    internal_id: str
    version: int


@attrs.define(frozen=True)
class ReadState:
    name: str
    read_version: int


@register_resource("read_private_state_test_resource")
class ResourceWithPrivateStateInRead(BaseResource):
    state_class = ReadState
    private_state_class = ReadPrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(), "read_version": a_num(computed=True)})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> ReadState | None:
        if not ctx.private_state:
            raise ResourceError("Read operation received no private state.")
        if not isinstance(ctx.private_state, ReadPrivateState):
            raise ResourceError("Private state has incorrect type.")
        return self.state_class(name=ctx.state.name, read_version=ctx.private_state.version)

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> None:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@pytest.mark.asyncio
async def test_read_handler_provides_private_state_to_context(
    encryption_key_env: str, provider_in_hub: Any
) -> None:
    resource_name = "read_private_state_test_resource"
    hub.register("resource", resource_name, ResourceWithPrivateStateInRead)
    try:
        schema = ResourceWithPrivateStateInRead.get_schema()
        prior_state_data = {"name": "existing-resource", "read_version": 1}
        private_state_obj = ReadPrivateState(internal_id="id-123", version=2)
        current_state_dv = marshal(prior_state_data, schema=schema.block)
        raw_private_bytes = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=True)
        encrypted_private_bytes = encrypt(raw_private_bytes)
        request = pb.ReadResource.Request(
            type_name=resource_name, current_state=current_state_dv, private=encrypted_private_bytes
        )
        response = await ReadResourceHandler(request, context=None)
        assert not response.diagnostics, (
            f"Handler returned diagnostics: {[d.summary for d in response.diagnostics]}"
        )
        new_state_cty = unmarshal(response.new_state, schema=schema.block)
        assert new_state_cty.value["read_version"].value == 2
    finally:
        hub.unregister("resource", resource_name)


# 🐍🏗️🔚
