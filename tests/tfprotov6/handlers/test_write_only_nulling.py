#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A write-only attribute is null in everything the provider sends back.

Terraform rejects a non-null write-only attribute in every value a provider
returns -- refresh (node_resource_abstract_instance.go:775-790), plan
(:1080-1095, :1313-1328, and objchange/plan_valid.go:323-330), apply
(:2789-2804), import (node_resource_import.go:106-124), upgrade
(upgrade_resource_state.go:129-141) and move
(refactoring/cross_provider_move.go:159-176). On a Terraform old enough not to
check, the value is written to the state file in plain text instead, which is
worse.

The nulling was done in two places, and neither covered the contract:

  - `BaseResource._merge_config_into_plan` handled the plan, so a resource that
    overrides `plan()` -- a documented extension point -- sent the secret to
    Terraform.
  - `complete_state_dict` handled apply and read, and iterated only
    `block.attributes`, so a write-only attribute inside a nested block or an
    `a_obj` was never touched. Import, upgrade and move called neither.

It is now done once, recursively, at the protocol boundary, so overriding a hook
cannot skip it.
"""

from __future__ import annotations

from typing import Any, ClassVar

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import ApplyResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.utils import null_write_only_attributes
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_obj, a_str, b_list, b_single, s_resource

SECRET = "s3cr3t"


# --- The recursive walk itself ---


def test_a_top_level_write_only_attribute_is_nulled() -> None:
    block = s_resource({"name": a_str(required=True), "token": a_str(write_only=True)}).block
    values: dict[str, Any] = {"name": "alpha", "token": SECRET}

    null_write_only_attributes(values, block)

    assert values == {"name": "alpha", "token": None}


def test_a_write_only_attribute_inside_a_nested_object_is_nulled() -> None:
    block = s_resource(
        {
            "creds": a_obj({"user": a_str(), "password": a_str(write_only=True)}),
        }
    ).block
    values: dict[str, Any] = {"creds": {"user": "root", "password": SECRET}}

    null_write_only_attributes(values, block)

    assert values["creds"]["password"] is None
    assert values["creds"]["user"] == "root"


def test_a_write_only_attribute_inside_a_single_block_is_nulled() -> None:
    block = s_resource(
        attributes={"name": a_str(required=True)},
        block_types=[b_single("auth", attributes={"token": a_str(write_only=True)})],
    ).block
    values: dict[str, Any] = {"name": "alpha", "auth": {"token": SECRET}}

    null_write_only_attributes(values, block)

    assert values["auth"]["token"] is None


def test_a_write_only_attribute_inside_a_list_block_is_nulled_in_every_element() -> None:
    block = s_resource(
        attributes={"name": a_str(required=True)},
        block_types=[b_list("cred", attributes={"user": a_str(), "token": a_str(write_only=True)})],
    ).block
    values: dict[str, Any] = {
        "name": "alpha",
        "cred": [{"user": "a", "token": SECRET}, {"user": "b", "token": SECRET}],
    }

    null_write_only_attributes(values, block)

    assert [element["token"] for element in values["cred"]] == [None, None]
    assert [element["user"] for element in values["cred"]] == ["a", "b"]


def test_a_missing_write_only_attribute_is_written_as_null() -> None:
    """Absent is not a state a cty object can be in; null is how it is spelled."""
    block = s_resource({"name": a_str(required=True), "token": a_str(write_only=True)}).block
    values: dict[str, Any] = {"name": "alpha"}

    null_write_only_attributes(values, block)

    assert values["token"] is None


def test_a_null_block_is_left_alone() -> None:
    """An absent block has nothing inside it to null."""
    block = s_resource(
        attributes={"name": a_str(required=True)},
        block_types=[b_single("auth", attributes={"token": a_str(write_only=True)})],
    ).block
    values: dict[str, Any] = {"name": "alpha", "auth": None}

    null_write_only_attributes(values, block)

    assert values["auth"] is None


# --- The handler paths ---

RESOURCE = "secret_widget"


@attrs.define(frozen=True)
class WidgetConfig:
    name: str | None = None
    token: str | None = None


@attrs.define(frozen=True)
class WidgetState:
    name: str | None = None
    token: str | None = None


class OverridingWidget(BaseResource[WidgetState, WidgetState, WidgetConfig]):
    """Overrides `plan()` outright, which is a documented extension point."""

    config_class = WidgetConfig
    state_class = WidgetState

    imported: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True),
                "token": a_str(required=True, write_only=True),
            }
        )

    async def _validate_config(self, config: WidgetConfig) -> list[str]:
        return []

    async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, Any]:
        # Echoes the secret straight back, which the framework must not pass on.
        return {"name": getattr(ctx.config, "name", None), "token": SECRET}, None

    async def _create_apply(self, ctx: ResourceContext) -> tuple[WidgetState | None, Any]:
        return WidgetState(name="alpha", token=SECRET), None

    async def import_state(self, ctx: ResourceContext, import_id: str) -> WidgetState:
        return WidgetState(name=import_id, token=SECRET)

    async def read(self, ctx: ResourceContext) -> WidgetState | None:
        return WidgetState(name="alpha", token=SECRET)

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def widget() -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", RESOURCE, OverridingWidget)

    yield OverridingWidget

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_an_overridden_plan_cannot_leak_a_write_only_value(widget: Any) -> None:
    block = widget.get_schema().block
    config = marshal({"name": "alpha", "token": SECRET}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    planned = unmarshal(plan.planned_state, schema=block)
    assert planned["token"].is_null, (
        "a resource that overrides plan() returned a write-only value and the framework passed it to Terraform"
    )


@pytest.mark.asyncio
async def test_apply_does_not_return_a_write_only_value(widget: Any) -> None:
    block = widget.get_schema().block
    config = marshal({"name": "alpha", "token": SECRET}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            planned_state=plan.planned_state,
        ),
        context=None,
    )

    assert not applied.diagnostics, f"apply failed: {applied.diagnostics}"
    assert unmarshal(applied.new_state, schema=block)["token"].is_null


@pytest.mark.asyncio
async def test_import_does_not_return_a_write_only_value(widget: Any) -> None:
    from pyvider.protocols.tfprotov6.handlers.import_resource_state import ImportResourceStateHandler

    block = widget.get_schema().block

    imported = await ImportResourceStateHandler(
        pb.ImportResourceState.Request(type_name=RESOURCE, id="alpha"),
        context=None,
    )

    assert not imported.diagnostics, f"import failed: {imported.diagnostics}"
    assert imported.imported_resources, "nothing was imported"
    state = unmarshal(imported.imported_resources[0].state, schema=block)
    assert state["token"].is_null, "import returned the write-only value to Terraform"


# 🐍🏗️🔚
