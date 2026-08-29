#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The plan a set block produces must agree with the configuration apply reads.

Regression for #30. `_set_elements_match` skipped every attribute carrying a
default, so two elements sharing all their non-defaulted attributes matched both
configurations, nothing paired, and neither received its default. On a create
the plan then promised null for an attribute `ctx.config` reported as "local",
and returning the configured value from apply is a result Terraform did not
plan.
"""

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
from pyvider.schema import PvsSchema, a_str, b_set, s_resource

RESOURCE = "set_defaults_regression"


@attrs.define
class Tag:
    name: str | None = None
    scope: str | None = None


@attrs.define
class Config:
    name: str
    tag: list[Tag] | None = None


@attrs.define
class State:
    name: str
    tag: list[Tag] | None = None


class SetResource(BaseResource[Any, State, Config]):
    """Records the configuration its plan hook was handed, to compare with the plan."""

    config_class = Config
    state_class = State
    seen_config: dict[str, Any] | None = None

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={"name": a_str(required=True)},
            block_types=[
                b_set(
                    "tag",
                    attributes={"name": a_str(required=True), "scope": a_str(default="local")},
                )
            ],
        )

    async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, Any]:
        type(self).seen_config = attrs.asdict(ctx.config) if ctx.config else None
        assert ctx.planned_state is not None
        return attrs.asdict(ctx.planned_state), None

    async def _validate_config(self, config: Config) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> State | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def set_resource() -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register(
        "singleton",
        "provider",
        BaseProvider(metadata=ProviderMetadata(name="test", version="0")),
    )
    hub.register("resource", RESOURCE, SetResource)
    yield SetResource
    SetResource.seen_config = None
    hub.unregister("resource", RESOURCE)
    if previous is not None:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_ambiguous_set_elements_are_planned_with_their_defaults(
    set_resource: Any,
) -> None:
    """Two elements sharing every non-defaulted attribute still take their defaults.

    `scope` is the only thing telling these elements apart, so a matcher that
    skips defaulted attributes has nothing left to pair on.
    """
    block = set_resource.get_schema().block
    config = marshal(
        {
            "name": "example",
            "tag": [
                {"name": "x", "scope": CtyValue.null(CtyString())},
                {"name": "x", "scope": "shared"},
            ],
        },
        schema=block,
    )

    response = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            # A create: no prior state, so nothing fills the omitted `scope`.
            prior_state=marshal(CtyValue.null(block.to_cty_type()), schema=block),
            proposed_new_state=config,
        ),
        context=None,
    )

    assert not response.diagnostics, f"plan failed: {response.diagnostics}"
    planned = unmarshal(response.planned_state, schema=block)

    config_scopes = sorted(str(tag["scope"]) for tag in set_resource.seen_config["tag"])
    planned_scopes = sorted(str(element["scope"].value) for element in planned["tag"].value)

    assert config_scopes == ["local", "shared"]
    assert planned_scopes == config_scopes, "the plan must promise what the apply hook reads"


# 🐍🏗️🔚
