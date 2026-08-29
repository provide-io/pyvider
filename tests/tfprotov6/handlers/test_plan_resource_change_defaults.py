#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Defaults are a protocol invariant, including for custom plan hooks."""

from __future__ import annotations

from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyString, CtyValue
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_obj, a_str, b_list, b_single, s_resource

RESOURCE = "custom_plan_default"


@attrs.define
class WholeOptions:
    mode: str | None = None


@attrs.define
class Options:
    label: str | None = None
    size: str | None = None


@attrs.define
class Settings:
    label: str | None = None
    size: str | None = None


@attrs.define
class Config:
    name: str
    size: str | None = None
    whole: WholeOptions | None = None
    opts: Options | None = None
    settings: Settings | None = None
    tier: list[Settings] | None = None


@attrs.define
class State:
    name: str
    size: str | None = None
    whole: WholeOptions | None = None
    opts: Options | None = None
    settings: Settings | None = None
    tier: list[Settings] | None = None


class CustomPlanResource(BaseResource[Any, State, Config]):
    """Overrides plan completely, bypassing BaseResource's merge helper."""

    config_class = Config
    state_class = State

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "size": a_str(default="small"),
                "whole": a_obj(
                    {"mode": a_str(optional=True)},
                    optional=True,
                    default={"mode": "fast"},
                ),
                "opts": a_obj({"label": a_str(), "size": a_str(default="small")}),
            },
            block_types=[
                b_single("settings", attributes={"label": a_str(), "size": a_str(default="small")}),
                b_list("tier", attributes={"label": a_str(), "size": a_str(default="small")}),
            ],
        )

    async def plan(self, ctx: ResourceContext):
        assert ctx.planned_state is not None
        return attrs.asdict(ctx.planned_state), None

    async def _validate_config(self, config: Config) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> State | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def custom_plan_resource() -> type[CustomPlanResource]:
    previous = hub.get_component("singleton", "provider")
    hub.register(
        "singleton",
        "provider",
        BaseProvider(metadata=ProviderMetadata(name="test", version="0")),
    )
    hub.register("resource", RESOURCE, CustomPlanResource)
    yield CustomPlanResource
    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_handler_merges_defaults_after_a_custom_plan_hook(
    custom_plan_resource: type[CustomPlanResource],
) -> None:
    block = custom_plan_resource.get_schema().block
    config = marshal(
        {
            "name": "example",
            "size": CtyValue.null(CtyString()),
            "whole": CtyValue.null(block.attributes["whole"].type),
            "opts": {"label": "primary", "size": CtyValue.null(CtyString())},
            "settings": {"label": "primary", "size": CtyValue.null(CtyString())},
            "tier": [{"label": "hot", "size": CtyValue.null(CtyString())}],
        },
        schema=block,
    )
    retained_prior = marshal(
        {
            "name": "example",
            "size": "large",
            "whole": {"mode": "slow"},
            "opts": {"label": "primary", "size": "large"},
            "settings": {"label": "primary", "size": "large"},
            "tier": [{"label": "hot", "size": "large"}],
        },
        schema=block,
    )

    response = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            prior_state=retained_prior,
            proposed_new_state=retained_prior,
        ),
        context=None,
    )

    assert not response.diagnostics, f"plan failed: {response.diagnostics}"
    planned = unmarshal(response.planned_state, schema=block)
    assert planned["size"].value == "small"
    assert planned["whole"]["mode"].value == "fast"
    assert planned["opts"]["size"].value == "small"
    assert planned["settings"]["size"].value == "small"
    assert planned["tier"][0]["size"].value == "small"
