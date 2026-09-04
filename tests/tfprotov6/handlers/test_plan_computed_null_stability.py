#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""An optional+computed attribute must not go unknown again on every update.

Planning a computed attribute unknown is right on a create: the provider does
not know the value yet, and Terraform shows "known after apply". On an update
it is only right if the value is genuinely undetermined. When the remote API
returned null, or returned a value that is already in state, re-planning it
unknown tells Terraform the value may change every single time, which produces:

  - a diff that never converges, so `terraform plan` is never empty; and
  - with `requires_replace`, a destroy and recreate on every plan, because the
    replacement paths are collected from attributes whose planned value differs
    from prior.

Terraform's own `objchange.ProposedNew` carries the prior value forward for an
optional+computed attribute whose configuration is null
(terraform/internal/plans/objchange/objchange.go:328-345), so the prior value is
what the plan should keep when the resource has not said otherwise.

The unconditional fill this replaces was itself a correction: an earlier gate
only filled when some *other* attribute happened to be unknown, which planned
computed attributes null on a wholly known config and broke creates. Both the
create and the update case are pinned here so the next change cannot trade one
for the other.
"""

from __future__ import annotations

from typing import Any, ClassVar

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_resource

RESOURCE = "stable_widget"


@attrs.define(frozen=True)
class WidgetConfig:
    name: str | None = None


@attrs.define(frozen=True)
class WidgetState:
    name: str | None = None
    ext_id: str | None = None


class StableWidget(BaseResource[WidgetState, WidgetState, WidgetConfig]):
    """`ext_id` is optional+computed and the remote API may legitimately leave it null."""

    config_class = WidgetConfig
    state_class = WidgetState

    replaced: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True),
                "ext_id": a_str(optional=True, computed=True),
            }
        )

    async def _validate_config(self, config: WidgetConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> WidgetState | None:
        state: WidgetState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def widget() -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", RESOURCE, StableWidget)

    yield StableWidget

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


async def _plan(config: Any, prior: Any = None, proposed: Any = None) -> Any:
    request = pb.PlanResourceChange.Request(
        type_name=RESOURCE,
        config=config,
        proposed_new_state=proposed if proposed is not None else config,
    )
    if prior is not None:
        request.prior_state.CopyFrom(prior)
    return await PlanResourceChangeHandler(request, context=None)


@pytest.mark.asyncio
async def test_a_create_still_plans_a_computed_attribute_unknown(widget: Any) -> None:
    """The create case the unconditional fill was introduced for."""
    block = widget.get_schema().block
    config = marshal({"name": "alpha", "ext_id": None}, schema=block)

    plan = await _plan(config)

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    planned = unmarshal(plan.planned_state, schema=block)
    assert planned["ext_id"].is_unknown, (
        "a computed attribute with no prior value must plan unknown, or apply "
        "contradicts the null the plan promised"
    )


@pytest.mark.asyncio
async def test_an_update_keeps_a_null_the_api_returned(widget: Any) -> None:
    """The perpetual-diff case: prior null must stay null, not become unknown."""
    block = widget.get_schema().block
    prior = marshal({"name": "alpha", "ext_id": None}, schema=block)
    config = marshal({"name": "beta", "ext_id": None}, schema=block)

    plan = await _plan(config, prior=prior)

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    planned = unmarshal(plan.planned_state, schema=block)
    assert not planned["ext_id"].is_unknown, (
        "an optional+computed attribute the API left null was re-planned unknown "
        "on an update, so `terraform plan` can never come back empty"
    )
    assert planned["ext_id"].is_null


@pytest.mark.asyncio
async def test_an_update_keeps_a_value_already_in_state(widget: Any) -> None:
    """A computed value the provider already knows must be carried forward."""
    block = widget.get_schema().block
    prior = marshal({"name": "alpha", "ext_id": "ext-123"}, schema=block)
    config = marshal({"name": "beta", "ext_id": None}, schema=block)

    plan = await _plan(config, prior=prior)

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    planned = unmarshal(plan.planned_state, schema=block)
    assert not planned["ext_id"].is_unknown, "a known computed value was discarded and re-planned unknown"
    assert planned["ext_id"].value == "ext-123"


@pytest.mark.asyncio
async def test_a_configured_value_still_wins(widget: Any) -> None:
    """Optional+computed means the practitioner may set it, and that must hold."""
    block = widget.get_schema().block
    prior = marshal({"name": "alpha", "ext_id": "ext-123"}, schema=block)
    config = marshal({"name": "alpha", "ext_id": "chosen"}, schema=block)

    plan = await _plan(config, prior=prior)

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    planned = unmarshal(plan.planned_state, schema=block)
    assert planned["ext_id"].value == "chosen"


# 🐍🏗️🔚
