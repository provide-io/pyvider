#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A state class that does not match its schema must not be applied as a destroy.

``BaseResource.apply`` decided between create, update and destroy by asking
whether ``ctx.planned_state`` is None. That is derived data: the planned state
instance is built by converting the planned state value into the resource's
attrs state class, and the converter returns None when the class cannot be
constructed. So a state class carrying a required field the schema does not
declare -- an ordinary authoring mistake -- collapsed to None and was read as
"Terraform asked for a destroy".

On a create that produced a null state and Terraform's "inconsistent result
after apply"; on an update it ran the resource's own ``_delete_apply`` against
a live object. Terraform says whether it wants a destroy by sending a null
``planned_state``, so that is what the decision has to be taken from.

This is the same failure as ``test_apply_unknown_computed.py`` reached by the
other route: there the planned state was withheld because values were unknown,
here because the class does not fit the schema.
"""

from __future__ import annotations

from typing import Any, ClassVar

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import ApplyResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_resource

RESOURCE = "mismatched_widget"


@attrs.define(frozen=True)
class MismatchConfig:
    name: str | None = None


@attrs.define(frozen=True)
class MismatchState:
    """`bookkeeping` is required here but absent from the schema.

    Nothing on the wire can ever supply it, so every conversion of a planned
    state into this class raises attrs' "missing required argument".
    """

    bookkeeping: str  # required: no default, and no schema attribute supplies it
    name: str | None = None


class MismatchedWidget(BaseResource[MismatchState, MismatchState, MismatchConfig]):
    config_class = MismatchConfig
    state_class = MismatchState

    deleted: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(required=True)})

    async def _validate_config(self, config: MismatchConfig) -> list[str]:
        return []

    async def _create_apply(self, ctx: ResourceContext) -> tuple[MismatchState | None, Any]:
        return ctx.planned_state, None

    async def read(self, ctx: ResourceContext) -> MismatchState | None:
        state: MismatchState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        type(self).deleted.append(getattr(ctx.state, "name", "?"))


@pytest.fixture
def widget() -> Any:
    MismatchedWidget.deleted = []
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", RESOURCE, MismatchedWidget)

    yield MismatchedWidget

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)
    MismatchedWidget.deleted = []


@pytest.mark.asyncio
async def test_a_state_class_missing_a_schema_attribute_does_not_delete(widget: Any) -> None:
    """A create whose state class cannot be built must fail loudly, not destroy."""
    block = widget.get_schema().block
    planned = marshal({"name": "alpha"}, schema=block)

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=planned,
            planned_state=planned,
        ),
        context=None,
    )

    assert widget.deleted == [], (
        "apply ran _delete_apply for a create: a state class that does not match "
        "its schema was read as Terraform asking for a destroy"
    )
    assert applied.diagnostics, (
        "a state class that cannot be constructed produced no diagnostic; the "
        "practitioner is given no way to find the mismatch"
    )
    detail = " ".join(d.summary + " " + d.detail for d in applied.diagnostics)
    assert "bookkeeping" in detail, f"the diagnostic does not name the offending attribute: {detail}"


@pytest.mark.asyncio
async def test_an_update_with_an_unconstructable_state_class_does_not_delete(widget: Any) -> None:
    """The destructive half: an update must never fall through to _delete_apply."""
    block = widget.get_schema().block
    prior = marshal({"name": "alpha"}, schema=block)
    planned = marshal({"name": "beta"}, schema=block)

    await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=planned,
            prior_state=prior,
            planned_state=planned,
        ),
        context=None,
    )

    assert widget.deleted == [], (
        "apply deleted a live resource during an update because its state class could not be constructed"
    )


@pytest.mark.asyncio
async def test_a_mismatched_class_reports_rather_than_destroying_silently(widget: Any) -> None:
    """Even a destroy surfaces the mismatch instead of running on a null state.

    A destroy could be let through -- the practitioner is removing the resource
    anyway -- but `_delete_apply` would be handed `ctx.state = None` and so has
    nothing to identify the remote object with. Reporting the real fault is more
    use than deleting on no information.
    """
    block = widget.get_schema().block
    prior = marshal({"name": "alpha"}, schema=block)

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=pb.DynamicValue(msgpack=b"\xc0"),
            prior_state=prior,
            planned_state=pb.DynamicValue(msgpack=b"\xc0"),
        ),
        context=None,
    )

    assert applied.diagnostics, "the mismatch was not reported"
    detail = " ".join(d.summary + " " + d.detail for d in applied.diagnostics)
    assert "bookkeeping" in detail, f"the diagnostic does not name the offending attribute: {detail}"


# --- A well-formed resource, to prove the destroy signal itself still works ---

WELL_FORMED = "well_formed_widget"


@attrs.define(frozen=True)
class WellFormedState:
    name: str | None = None


class WellFormedWidget(BaseResource[WellFormedState, WellFormedState, MismatchConfig]):
    config_class = MismatchConfig
    state_class = WellFormedState

    deleted: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(required=True)})

    async def _validate_config(self, config: MismatchConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> WellFormedState | None:
        state: WellFormedState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        type(self).deleted.append(getattr(ctx.state, "name", "?"))


@pytest.fixture
def well_formed() -> Any:
    WellFormedWidget.deleted = []
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", WELL_FORMED, WellFormedWidget)

    yield WellFormedWidget

    hub.unregister("resource", WELL_FORMED)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)
    WellFormedWidget.deleted = []


@pytest.mark.asyncio
async def test_a_null_planned_state_is_still_a_destroy(well_formed: Any) -> None:
    """The destroy signal is unchanged: Terraform sends a null planned state."""
    block = well_formed.get_schema().block
    prior = marshal({"name": "alpha"}, schema=block)

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=WELL_FORMED,
            config=pb.DynamicValue(msgpack=b"\xc0"),
            prior_state=prior,
            planned_state=pb.DynamicValue(msgpack=b"\xc0"),
        ),
        context=None,
    )

    assert not applied.diagnostics, f"destroy failed: {applied.diagnostics}"
    assert well_formed.deleted == ["alpha"], "a null planned state must still run the resource's delete"
    assert unmarshal(applied.new_state, schema=block).is_null, "a destroy must return a null state"


@pytest.mark.asyncio
async def test_a_populated_planned_state_is_never_a_destroy(well_formed: Any) -> None:
    """The other half of the decision: a real planned state must not delete."""
    block = well_formed.get_schema().block
    prior = marshal({"name": "alpha"}, schema=block)
    planned = marshal({"name": "beta"}, schema=block)

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=WELL_FORMED,
            config=planned,
            prior_state=prior,
            planned_state=planned,
        ),
        context=None,
    )

    assert not applied.diagnostics, f"update failed: {applied.diagnostics}"
    assert well_formed.deleted == [], "an update ran the resource's delete"
    assert unmarshal(applied.new_state, schema=block)["name"].value == "beta"


# 🐍🏗️🔚
