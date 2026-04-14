#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import datetime
from typing import Any

import attrs
import msgpack
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.ephemerals import (
    BaseEphemeralResource,
    EphemeralResourceContext,
    register_ephemeral_resource,
)
from pyvider.exceptions import ResourceError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    CloseEphemeralResourceHandler,
    OpenEphemeralResourceHandler,
    RenewEphemeralResourceHandler,
    ValidateEphemeralResourceConfigHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource

# --- Test Resource Definitions ---


@attrs.define(frozen=True)
class MockConnectionConfig:
    """Config for our mock ephemeral resource."""

    host: str


@attrs.define(frozen=True)
class MockConnectionResult:
    """The 'result' data returned to Terraform by OpenEphemeralResource."""

    connection_id: str
    host: str


@attrs.define(frozen=True)
class MockConnectionPrivateState(PrivateState):
    """The private state used to manage the connection."""

    connection_id: str
    session_token: str
    version: int


@register_ephemeral_resource("mock_connection")
class MockConnectionResource(BaseEphemeralResource):
    config_class = MockConnectionConfig
    result_class = MockConnectionResult
    private_state_class = MockConnectionPrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "host": a_str(required=True),
                "connection_id": a_str(computed=True),
            }
        )

    async def validate(self, config: MockConnectionConfig) -> list[str]:
        if "localhost" not in config.host:
            return ["Host must contain 'localhost'."]
        return []

    async def open(self, ctx: EphemeralResourceContext) -> tuple[Any, Any, datetime.datetime]:
        # Simulate opening a connection and getting a result and private state
        result = self.result_class(connection_id="conn-123", host=ctx.config.host)
        private_state = self.private_state_class(
            connection_id="conn-123", session_token="token-abc", version=1
        )
        renew_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
        return result, private_state, renew_at

    async def renew(self, ctx: EphemeralResourceContext) -> tuple[Any, datetime.datetime]:
        # Simulate renewing a session token
        if not isinstance(ctx.private_state, self.private_state_class):
            raise ResourceError("Renew received invalid private state.")

        new_private_state = self.private_state_class(
            connection_id=ctx.private_state.connection_id,
            session_token="token-def-renewed",
            version=ctx.private_state.version + 1,
        )
        new_renew_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10)
        return new_private_state, new_renew_at

    async def close(self, ctx: EphemeralResourceContext) -> None:
        # Simulate closing the connection
        if not ctx.private_state or ctx.private_state.connection_id != "conn-123":
            raise ResourceError("Close called with invalid private state.")
        # In a real implementation, this is where you'd call something like `connection.close()`


@pytest.mark.asyncio
async def test_ephemeral_resource_full_lifecycle() -> None:
    """
    TDD: Verifies the entire ephemeral resource lifecycle from validation to close.
    """
    resource_name = "mock_connection"
    hub.register("ephemeral_resource", resource_name, MockConnectionResource)
    schema = MockConnectionResource.get_schema()

    try:
        # --- 1. Validate ---
        raw_config = {"host": "localhost:8080"}
        config_dv = marshal(raw_config, schema=schema.block)
        validate_req = pb.ValidateEphemeralResourceConfig.Request(type_name=resource_name, config=config_dv)
        validate_resp = await ValidateEphemeralResourceConfigHandler(validate_req, context=None)
        assert not validate_resp.diagnostics

        # --- 2. Open ---
        open_req = pb.OpenEphemeralResource.Request(type_name=resource_name, config=config_dv)
        open_resp = await OpenEphemeralResourceHandler(open_req, context=None)
        assert not open_resp.diagnostics
        assert open_resp.private
        assert open_resp.renew_at.seconds > 0

        # Unmarshal results for inspection
        result_cty = unmarshal(open_resp.result, schema=schema.block)
        assert result_cty.value["connection_id"].value == "conn-123"

        private_data = msgpack.unpackb(open_resp.private, raw=False)
        assert private_data["session_token"] == "token-abc"
        assert private_data["version"] == 1

        # --- 3. Renew ---
        renew_req = pb.RenewEphemeralResource.Request(type_name=resource_name, private=open_resp.private)
        renew_resp = await RenewEphemeralResourceHandler(renew_req, context=None)
        assert not renew_resp.diagnostics
        assert renew_resp.private != open_resp.private  # Private state should be new
        assert renew_resp.renew_at.seconds > open_resp.renew_at.seconds

        # Unmarshal new private state for inspection
        renewed_private_data = msgpack.unpackb(renew_resp.private, raw=False)
        assert renewed_private_data["session_token"] == "token-def-renewed"
        assert renewed_private_data["version"] == 2

        # --- 4. Close ---
        close_req = pb.CloseEphemeralResource.Request(type_name=resource_name, private=renew_resp.private)
        close_resp = await CloseEphemeralResourceHandler(close_req, context=None)
        assert not close_resp.diagnostics

    finally:
        hub.unregister("ephemeral_resource", resource_name)


# 🐍🏗️🔚
