#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Generated configuration is configuration, not a copy of state.

`terraform plan -generate-config-out` and `terraform query -generate-config-out`
ask the provider to turn a discovered object into configuration a practitioner
can keep. A provider answers only if it advertises
`server_capabilities.generate_resource_config`; without it Terraform falls back
to `genconfig.ExtractLegacyConfigFromState`, which drops the attributes that
cannot appear in configuration (node_resource_plan_instance.go:1192-1208).

pyvider advertises the capability unconditionally, so Terraform never uses its
fallback -- and when a resource does not override `generate_config`, the handler
forwarded the state bytes verbatim. The generated file then contained
computed-only attributes like `id`, which Terraform rejects on the next plan
because a configuration cannot set them.

Forwarding state was right in one narrow sense: it avoids a round trip. It is
wrong about what was being forwarded.
"""

from __future__ import annotations

from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.config_handlers import GenerateResourceConfigHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_resource

RESOURCE = "generated_widget"


@attrs.define(frozen=True)
class WidgetConfig:
    name: str | None = None


@attrs.define(frozen=True)
class WidgetState:
    name: str | None = None
    id: str | None = None
    region: str | None = None
    secret: str | None = None


class PlainWidget(BaseResource[WidgetState, WidgetState, WidgetConfig]):
    """Does not override `generate_config`, which is the ordinary case."""

    config_class = WidgetConfig
    state_class = WidgetState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True),
                # Computed-only: Terraform assigns it, a configuration cannot.
                "id": a_str(computed=True),
                # Optional+computed: a configuration may set it.
                "region": a_str(optional=True, computed=True),
                "secret": a_str(optional=True, write_only=True),
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
    hub.register("resource", RESOURCE, PlainWidget)

    yield PlainWidget

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


async def _generate(state: dict[str, Any]) -> Any:
    block = PlainWidget.get_schema().block
    response = await GenerateResourceConfigHandler(
        pb.GenerateResourceConfig.Request(type_name=RESOURCE, state=marshal(state, schema=block)),
        context=None,
    )
    assert not response.diagnostics, f"generation failed: {response.diagnostics}"
    return unmarshal(response.config, schema=block)


@pytest.mark.asyncio
async def test_a_computed_only_attribute_is_not_generated(widget: Any) -> None:
    config = await _generate({"name": "alpha", "id": "i-123", "region": "eu", "secret": None})

    assert config["id"].is_null, (
        "the generated configuration sets a computed-only attribute, which Terraform rejects on the next plan"
    )


@pytest.mark.asyncio
async def test_a_configurable_attribute_is_kept(widget: Any) -> None:
    """Dropping too much would lose the practitioner's settings."""
    config = await _generate({"name": "alpha", "id": "i-123", "region": "eu", "secret": None})

    assert config["name"].value == "alpha"
    assert config["region"].value == "eu", "an optional+computed attribute may be configured"


@pytest.mark.asyncio
async def test_a_write_only_attribute_is_not_generated(widget: Any) -> None:
    """It is null in state anyway, and emitting it would suggest otherwise."""
    config = await _generate({"name": "alpha", "id": "i-123", "region": "eu", "secret": None})

    assert config["secret"].is_null


# 🐍🏗️🔚
