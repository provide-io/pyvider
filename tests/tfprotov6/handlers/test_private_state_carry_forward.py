#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Private state survives a plan or apply that does not re-emit it.

Terraform stores whatever the provider returns as the instance's private state
and hands it back as `prior_private` next time
(terraform/internal/terraform/node_resource_abstract_instance.go:549,1396).
Returning nothing therefore does not mean "unchanged", it means "erase it".

Both handlers set the field only when the resource's hook produced a private
state object. The default `_update` returns `(base_plan, None)`, and most
resources keep private state only at create, so the first plan after a create
erased it -- and with it any lease, token or bookkeeping the resource had put
there. terraform-plugin-sdk defaults the other way, assigning
`resp.PlannedPrivate = req.PriorPrivate` before the hook runs
(helper/schema/grpc_provider.go:1040,1065,1164).

The bytes are carried across as they arrive, still encrypted: they are opaque
to the framework, and re-encrypting them would only add a way to fail.
"""

from __future__ import annotations

from typing import Any

import attrs
import msgpack
import pytest

from pyvider.common.encryption import decrypt, encrypt
from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import ApplyResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource

RESOURCE = "leaseholder"


@attrs.define(frozen=True)
class LeasePrivate(PrivateState):
    lease_id: str


@attrs.define(frozen=True)
class LeaseConfig:
    name: str | None = None


@attrs.define(frozen=True)
class LeaseState:
    name: str | None = None


class Leaseholder(BaseResource[LeaseState, LeaseState, LeaseConfig]):
    """Keeps a lease id in private state at create and never mentions it again.

    This is the ordinary shape: the value is established once, and the update
    and apply hooks have no reason to restate it.
    """

    config_class = LeaseConfig
    state_class = LeaseState
    private_state_class = LeasePrivate

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str(required=True)})

    async def _validate_config(self, config: LeaseConfig) -> list[str]:
        return []

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, Any]:
        return base_plan, LeasePrivate(lease_id="lease-abc123")

    async def read(self, ctx: ResourceContext) -> LeaseState | None:
        state: LeaseState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


@pytest.fixture
def leaseholder(encryption_key_env: None) -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", RESOURCE, Leaseholder)

    yield Leaseholder

    hub.unregister("resource", RESOURCE)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_a_create_plan_stores_the_private_state_it_produced(leaseholder: Any) -> None:
    """Baseline: the hook's private state does reach the response."""
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )

    assert not plan.diagnostics, f"plan failed: {plan.diagnostics}"
    assert plan.planned_private, "the private state the create hook produced was not stored"


@pytest.mark.asyncio
async def test_a_later_plan_keeps_private_state_the_hook_did_not_restate(leaseholder: Any) -> None:
    """The update hook returns no private state, which must not erase it."""
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    created = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    stored = created.planned_private
    assert stored, "fixture failure: nothing was stored at create"

    prior = marshal({"name": "alpha"}, schema=block)
    updated = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=marshal({"name": "beta"}, schema=block),
            prior_state=prior,
            proposed_new_state=marshal({"name": "beta"}, schema=block),
            prior_private=stored,
        ),
        context=None,
    )

    assert not updated.diagnostics, f"plan failed: {updated.diagnostics}"
    assert updated.planned_private == stored, (
        "the plan erased private state the resource never asked to change; "
        "Terraform stores what the plan returns, so the lease is gone"
    )


def _lease_id(private_bytes: bytes) -> str | None:
    """Read the lease back out of an encrypted private state blob.

    Encryption draws a fresh salt and nonce per call, so two encryptions of the
    same value differ; the contents are what matter, not the bytes.
    """
    if not private_bytes:
        return None
    unpacked = msgpack.unpackb(decrypt(private_bytes), raw=False)
    return str(unpacked["lease_id"])


@pytest.mark.asyncio
async def test_apply_keeps_private_state_the_hook_did_not_restate(leaseholder: Any) -> None:
    """The same at apply: silence means unchanged, not erased."""
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    planned = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    assert planned.planned_private, "fixture failure: nothing was planned"

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            planned_state=planned.planned_state,
            planned_private=planned.planned_private,
        ),
        context=None,
    )

    assert not applied.diagnostics, f"apply failed: {applied.diagnostics}"
    assert _lease_id(applied.private) == "lease-abc123", (
        "apply returned no private state, so Terraform recorded an empty one and "
        "the value the resource stored at create is lost"
    )


# --- A resource whose apply hook returns None outright ---

SILENT = "silent_leaseholder"


class SilentLeaseholder(Leaseholder):
    """Returns no private state from apply, which must not erase what was planned."""

    async def _create_apply(self, ctx: ResourceContext) -> tuple[LeaseState | None, Any]:
        return ctx.planned_state, None


@pytest.fixture
def silent(encryption_key_env: None) -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register("singleton", "provider", BaseProvider(metadata=ProviderMetadata(name="t", version="0")))
    hub.register("resource", SILENT, SilentLeaseholder)

    yield SilentLeaseholder

    hub.unregister("resource", SILENT)
    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_apply_returning_none_keeps_the_planned_private_state(silent: Any) -> None:
    """An apply hook that returns None explicitly still must not erase it."""
    block = silent.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    planned = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=SILENT, config=config, proposed_new_state=config),
        context=None,
    )
    assert planned.planned_private, "fixture failure: nothing was planned"

    applied = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=SILENT,
            config=config,
            planned_state=planned.planned_state,
            planned_private=planned.planned_private,
        ),
        context=None,
    )

    assert not applied.diagnostics, f"apply failed: {applied.diagnostics}"
    assert _lease_id(applied.private) == "lease-abc123", (
        "an apply hook returning None erased the private state the plan stored"
    )


@pytest.mark.asyncio
async def test_a_destroy_plan_carries_private_state_forward(leaseholder: Any) -> None:
    """A destroy plan gets prior_private back, which apply then needs to clean up.

    This is what Terraform does itself when a provider does not implement
    plan_destroy (internal/plugin6/grpc_provider.go:648-654), so a provider that
    does implement it should not behave differently.
    """
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    created = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(type_name=RESOURCE, config=config, proposed_new_state=config),
        context=None,
    )
    stored = created.planned_private

    destroyed = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=pb.DynamicValue(msgpack=b"\xc0"),
            prior_state=marshal({"name": "alpha"}, schema=block),
            proposed_new_state=pb.DynamicValue(msgpack=b"\xc0"),
            prior_private=stored,
        ),
        context=None,
    )

    assert not destroyed.diagnostics, f"destroy plan failed: {destroyed.diagnostics}"
    assert destroyed.planned_private == stored


# 🐍🏗️🔚


@pytest.mark.asyncio
async def test_undecryptable_private_state_is_reported_at_plan(leaseholder: Any) -> None:
    """A decrypt failure must be reported, not planned straight past.

    Plan swallowed any failure here with a warning and continued with no private
    state, while apply raises on the very same bytes. So rotating or losing
    PYVIDER_PRIVATE_STATE_SHARED_SECRET produced a clean-looking plan and an
    apply that failed, and a resource whose `_update` does not restate its
    private state planned as though it never had any.
    """
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            prior_state=marshal({"name": "alpha"}, schema=block),
            proposed_new_state=config,
            prior_private=b"\x01this-is-not-a-valid-ciphertext",
        ),
        context=None,
    )

    assert plan.diagnostics, "an undecryptable private state produced no diagnostic"
    detail = " ".join(d.summary + " " + d.detail for d in plan.diagnostics)
    assert "private" in detail.lower(), f"the diagnostic does not mention private state: {detail}"


@pytest.mark.asyncio
async def test_private_state_that_no_longer_fits_its_class_is_tolerated(leaseholder: Any) -> None:
    """The legitimate case the warning was written for stays a warning.

    Private state that decrypts but no longer matches `private_state_class` is a
    resource whose private shape changed between releases. There is nothing to
    recover, and the resource is expected to rebuild it, so the plan continues.
    """
    block = leaseholder.get_schema().block
    config = marshal({"name": "alpha"}, schema=block)
    stale = encrypt(msgpack.packb({"retired_field": "x"}, use_bin_type=True))

    plan = await PlanResourceChangeHandler(
        pb.PlanResourceChange.Request(
            type_name=RESOURCE,
            config=config,
            prior_state=marshal({"name": "alpha"}, schema=block),
            proposed_new_state=config,
            prior_private=stale,
        ),
        context=None,
    )

    assert not plan.diagnostics, (
        f"a recoverable private state shape change failed the plan: {plan.diagnostics}"
    )
