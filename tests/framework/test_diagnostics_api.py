#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal
from pyvider.hub import hub, register_resource
from pyvider.protocols.tfprotov6.handlers import PlanResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_resource


@attrs.define(frozen=True)
class WarningState:
    name: str | None = None
    old_name: str | None = None


@register_resource("warning_test_resource")
class WarningResource(BaseResource):
    state_class = WarningState
    config_class = WarningState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(optional=True),
                "old_name": a_str(optional=True, description="This attribute is deprecated."),
            }
        )

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]) -> tuple[dict[str, Any], None]:
        config = ctx.config
        if config.old_name is not None:
            ctx.add_attribute_warning(
                attribute_path="old_name",
                summary="Attribute 'old_name' is deprecated",
                detail="The 'old_name' attribute is deprecated and will be removed in a future version. Please use the 'name' attribute instead.",
            )
        base_plan["name"] = config.name or config.old_name
        return base_plan, None

    async def read(self, ctx: ResourceContext) -> None:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@pytest.mark.asyncio
async def test_plan_handler_collects_attribute_warnings(provider_in_hub: Any) -> None:
    resource_name = "warning_test_resource"
    hub.register("resource", resource_name, WarningResource)
    try:
        schema = WarningResource.get_schema()
        raw_config = {"old_name": "deprecated-name"}
        config_dv = marshal(raw_config, schema=schema.block)
        null_dv = marshal(None, schema=schema.block)
        request = pb.PlanResourceChange.Request(
            type_name=resource_name, config=config_dv, prior_state=null_dv, proposed_new_state=config_dv
        )
        response = await PlanResourceChangeHandler(request, context=None)
        assert len(response.diagnostics) == 1
        diag = response.diagnostics[0]
        assert diag.severity == pb.Diagnostic.WARNING
        assert diag.summary == "Attribute 'old_name' is deprecated"
        assert diag.attribute.steps[0].attribute_name == "old_name"
    finally:
        hub.unregister("resource", resource_name)


# 🐍🏗️🔚
