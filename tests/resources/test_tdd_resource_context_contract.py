#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyMark, CtyValue
from pyvider.hub import hub, register_resource
from pyvider.protocols.tfprotov6.handlers import PlanResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_bool, a_str, s_resource


@attrs.define(frozen=True)
class ContextAwareConfig:
    api_key: str
    username: str


@attrs.define(frozen=True)
class ContextSnapshotState:
    api_key: str | None = None
    username: str | None = None
    config_cty_was_present: bool | None = None
    api_key_was_sensitive: bool | None = None
    username_was_sensitive: bool | None = None


@attrs.define(frozen=True)
class ContextAwarePrivateState(PrivateState):
    plan_id: str


@register_resource("context_aware_resource")
class ContextAwareResource(BaseResource):
    config_class = ContextAwareConfig
    state_class = ContextSnapshotState
    private_state_class = ContextAwarePrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "api_key": a_str(required=True, sensitive=True),
                "username": a_str(required=True),
                "config_cty_was_present": a_bool(computed=True),
                "api_key_was_sensitive": a_bool(computed=True),
                "username_was_sensitive": a_bool(computed=True),
            }
        )

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any], ContextAwarePrivateState]:
        config_cty: CtyValue | None = ctx.config_cty
        was_present = config_cty is not None
        api_key_marked = False
        username_marked = False
        if was_present and isinstance(config_cty.value, dict):
            api_key_val = config_cty.value.get("api_key")
            if api_key_val:
                api_key_marked = api_key_val.has_mark(CtyMark("sensitive"))
            username_val = config_cty.value.get("username")
            if username_val:
                username_marked = username_val.has_mark(CtyMark("sensitive"))
        base_plan["config_cty_was_present"] = was_present
        base_plan["api_key_was_sensitive"] = api_key_marked
        base_plan["username_was_sensitive"] = username_marked
        private_state = self.private_state_class(plan_id="plan-123")
        return base_plan, private_state

    async def read(self, ctx: ResourceContext) -> None:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@pytest.mark.asyncio
async def test_plan_handler_populates_full_resource_context(
    encryption_key_env: str, provider_in_hub: Any
) -> None:
    resource_name = "context_aware_resource"
    hub.register("resource", resource_name, ContextAwareResource)
    try:
        raw_config = {"api_key": "secret-key", "username": "testuser"}
        resource_schema = ContextAwareResource.get_schema()
        config_dv = marshal(raw_config, schema=resource_schema.block)
        null_dv = marshal(None, schema=resource_schema.block)
        request = pb.PlanResourceChange.Request(
            type_name=resource_name, config=config_dv, prior_state=null_dv, proposed_new_state=config_dv
        )
        response = await PlanResourceChangeHandler(request, context=None)
        assert not response.diagnostics, (
            f"Handler returned diagnostics: {[d.summary for d in response.diagnostics]}"
        )
        planned_state_cty = unmarshal(response.planned_state, schema=resource_schema.block)
        planned_state = ContextAwareResource.from_cty(planned_state_cty, ContextSnapshotState)
        assert planned_state.config_cty_was_present is True
        assert planned_state.api_key_was_sensitive is True
        assert planned_state.username_was_sensitive is False
    finally:
        hub.unregister("resource", resource_name)


# 🐍🏗️🔚
