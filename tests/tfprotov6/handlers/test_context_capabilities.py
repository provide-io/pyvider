#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`ctx.capabilities` is the provider's configured capability instances.

`ResourceContext.capabilities` is declared `dict[str, BaseCapability]`, and
`BaseProvider.capabilities` is exactly that -- the instances built during
`setup()`, each one configured from the provider block. But every resource
handler populated the context from `provider_instance.metadata.capabilities`,
which is `ProviderMetadata.capabilities`: a `ProviderCapabilities` flags struct
describing what the provider supports, an unrelated object that happens to share
the name.

So the documented `ctx.capabilities["auth"]` raised `TypeError: 'ProviderCapabilities'
object is not subscriptable`, and there was no way to reach a capability from a
resource at all.
"""

from __future__ import annotations

from typing import Any, ClassVar

import attrs
import pytest

from pyvider.capabilities.base import BaseCapability
from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import ApplyResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.read_resource import ReadResourceHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsAttribute, PvsSchema, a_str, s_resource

RESOURCE = "capability_widget"


class AuthCapability(BaseCapability):
    """A capability carrying a value that only its configured instance knows."""

    def __init__(self, config: Any | None = None) -> None:
        self.token = "configured-token"

    @staticmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        return {}


@attrs.define(frozen=True)
class WidgetConfig:
    name: str | None = None


@attrs.define(frozen=True)
class WidgetState:
    name: str | None = None


class CapabilityWidget(BaseResource[WidgetState, WidgetState, WidgetConfig]):
    """Records what it was handed as `ctx.capabilities` on each hook."""

    config_class = WidgetConfig
    state_class = WidgetState

    seen: ClassVar[list[Any]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(required=True)})

    async def _validate_config(self, config: WidgetConfig) -> list[str]:
        return []

    async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]) -> tuple[Any, Any]:
        type(self).seen.append(ctx.capabilities)
        return base_plan, None

    async def _update(self, ctx: ResourceContext, base_plan: dict[str, Any]) -> tuple[Any, Any]:
        type(self).seen.append(ctx.capabilities)
        return base_plan, None

    async def _create_apply(self, ctx: ResourceContext) -> tuple[WidgetState | None, Any]:
        type(self).seen.append(ctx.capabilities)
        return ctx.planned_state, None

    async def read(self, ctx: ResourceContext) -> WidgetState | None:
        type(self).seen.append(ctx.capabilities)
        state: WidgetState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def widget() -> Any:
    CapabilityWidget.seen = []
    previous = hub.get_component("singleton", "provider")

    provider = BaseProvider(metadata=ProviderMetadata(name="t", version="0"))
    # What setup() publishes: capability name -> configured instance.
    provider.capabilities = {"auth": AuthCapability()}
    hub.register("singleton", "provider", provider)
    hub.register("resource", RESOURCE, CapabilityWidget)

    yield CapabilityWidget

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)
    CapabilityWidget.seen = []


def _assert_usable(capabilities: Any) -> None:
    assert isinstance(capabilities, dict), (
        f"ctx.capabilities is {type(capabilities).__name__}, not the provider's "
        "capability instances; the documented ctx.capabilities['auth'] cannot work"
    )
    assert capabilities["auth"].token == "configured-token", (
        "the capability instance is not the one the provider configured"
    )


@pytest.mark.asyncio
async def test_plan_receives_the_configured_capabilities(widget: Any) -> None:
    block = widget.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    assert widget.seen, "the plan hook never ran"
    _assert_usable(widget.seen[0])


@pytest.mark.asyncio
async def test_apply_receives_the_configured_capabilities(widget: Any) -> None:
    block = widget.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    widget.seen.clear()

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(type_name=RESOURCE, config=config, planned_state=plan.planned_state),
        context=None,
    )

    assert not applied.diagnostics, f"apply failed: {applied.diagnostics}"
    assert widget.seen, "the apply hook never ran"
    _assert_usable(widget.seen[0])


@pytest.mark.asyncio
async def test_read_receives_the_configured_capabilities(widget: Any) -> None:
    block = widget.get_schema().block
    state = marshal({"name": "alpha"}, schema=block)

    read = await ReadResourceHandler(
        pb.ReadResource.Request(type_name=RESOURCE, current_state=state),
        context=None,
    )

    assert not read.diagnostics, f"read failed: {read.diagnostics}"
    assert widget.seen, "the read hook never ran"
    _assert_usable(widget.seen[0])


@pytest.mark.asyncio
async def test_a_provider_with_no_capabilities_gives_an_empty_mapping(widget: Any) -> None:
    """The common case must stay usable, not become None."""
    provider = hub.get_component("singleton", "provider")
    provider.capabilities = {}

    block = widget.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    assert widget.seen[0] == {}


# 🐍🏗️🔚
