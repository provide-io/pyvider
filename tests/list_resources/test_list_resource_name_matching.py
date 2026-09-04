#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A list resource must share its name with a managed resource.

Terraform resolves a list resource's results against the managed resource type
of the *same name*, and refuses to list at all if there is no such type or it has
no identity schema:

    resourceSchema, ok := schema.ResourceTypes[r.TypeName]
    if !ok || resourceSchema.Identity == nil {
        ... "Identity schema not found for resource type %s; this is a bug in
        the provider - please report it there"

(internal/plugin6/grpc_provider.go:1341-1345). `ResourceTypes` is built only from
`resource_schemas` merged with the identity schemas by name (:183-186), so
publishing an identity schema under the list resource's own name does not
satisfy it -- a managed resource of that name has to exist.

Nothing checked this, so a provider could register `acme_widget_list` alongside a
managed `acme_widget`, pass every test here, and fail on the first
`terraform query` with an error that says the provider is at fault without
saying how. The framework says so itself now, at schema time, where every
component is known.
"""

from __future__ import annotations

from typing import Any

import attrs
import pytest

from pyvider.hub import hub
from pyvider.list_resources import BaseListResource, ListResourceContext, ListResult
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_identity, s_resource


@attrs.define(frozen=True)
class WidgetConfig:
    name: str | None = None


@attrs.define(frozen=True)
class WidgetState:
    name: str | None = None


class Widget(BaseResource[WidgetState, WidgetState, WidgetConfig]):
    config_class = WidgetConfig
    state_class = WidgetState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(required=True)})

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return s_identity({"name": a_str(required=True)})

    async def _validate_config(self, config: WidgetConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> WidgetState | None:
        state: WidgetState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


class WidgetList(BaseListResource[WidgetConfig]):
    config_class = WidgetConfig
    resource_type = "matched_widget"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str()})

    async def list(self, ctx: ListResourceContext) -> Any:
        yield ListResult(identity={"name": "one"}, display_name="one")


@pytest.fixture(autouse=True)
def _provider() -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    yield
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


async def _collect(list_name: str, *, managed: str | None) -> str:
    """Collect list resource schemas and return the diagnostics as one string."""
    from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
        _collect_list_resource_schemas,
    )

    if managed is not None:
        hub.register("resource", managed, Widget)
    hub.register("list_resource", list_name, WidgetList)
    diagnostics: list[pb.Diagnostic] = []
    try:
        await _collect_list_resource_schemas(diagnostics)
    finally:
        if managed is not None:
            hub.unregister("resource", managed)
        hub.unregister("list_resource", list_name)

    return " ".join(d.summary + " " + d.detail for d in diagnostics)


@pytest.mark.asyncio
async def test_a_list_resource_without_a_matching_resource_is_reported() -> None:
    detail = await _collect("matched_widget_list", managed="matched_widget")

    assert "matched_widget_list" in detail, (
        "a list resource with no managed resource of the same name was not "
        f"reported; Terraform will refuse to list it. Diagnostics: {detail}"
    )


@pytest.mark.asyncio
async def test_the_diagnostic_explains_what_to_do() -> None:
    detail = await _collect("matched_widget_list", managed="matched_widget")

    assert "Identity schema not found" in detail, "the diagnostic does not quote what Terraform will say"
    assert "Suggestion:" in detail, "the diagnostic does not say what to do about it"


@pytest.mark.asyncio
async def test_a_matching_pair_is_not_reported() -> None:
    detail = await _collect("matched_widget", managed="matched_widget")

    assert not detail, f"a correctly named pair was reported: {detail}"


@pytest.mark.asyncio
async def test_a_list_resource_with_no_managed_resources_at_all_is_reported() -> None:
    detail = await _collect("orphan_list", managed=None)

    assert "orphan_list" in detail


# 🐍🏗️🔚
