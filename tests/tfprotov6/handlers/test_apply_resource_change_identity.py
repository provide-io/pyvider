#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for identity handling in the ApplyResourceChange handler."""

from typing import Any

from attrs import define
from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.conversion import marshal, marshal_identity, unmarshal_identity
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import (
    _apply_resource_change_impl,
    _handle_apply_result,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_identity, s_resource

MODULE = "pyvider.protocols.tfprotov6.handlers.apply_resource_change"
IDENTITY_SCHEMA = s_identity(attributes={"path": a_str(required=True)})
RESOURCE_SCHEMA = s_resource({"path": a_str(required=True)})
# Declares an attribute that DemoState never has -- exercises the ordinary (non-raising)
# None-return path when the identity schema doesn't resolve against the resource's state.
MISMATCHED_IDENTITY_SCHEMA = s_identity(attributes={"id": a_str(required=True)})


@define(frozen=True)
class DemoState:
    path: str | None = None


def test_omits_identity_when_schema_is_none() -> None:
    response = pb.ApplyResourceChange.Response()

    _handle_apply_result(
        DemoState(path="/tmp/x"),
        None,
        RESOURCE_SCHEMA,
        None,
        response,
        type_name="demo",
        identity_schema=None,
        identity_values=None,
    )

    assert not response.HasField("new_identity")


def test_emits_identity_after_apply() -> None:
    response = pb.ApplyResourceChange.Response()

    _handle_apply_result(
        DemoState(path="/tmp/x"),
        None,
        RESOURCE_SCHEMA,
        None,
        response,
        type_name="demo",
        identity_schema=IDENTITY_SCHEMA,
        identity_values={"path": "/tmp/x"},
    )

    assert unmarshal_identity(response.new_identity, IDENTITY_SCHEMA) == {"path": "/tmp/x"}


def test_omits_identity_when_schema_present_but_values_are_none() -> None:
    """A resource may declare an identity schema yet get_identity() return None. Identity
    is never marshalled partially -- None means emit nothing, since Terraform errors on an
    identity that contains unknown values."""
    response = pb.ApplyResourceChange.Response()

    _handle_apply_result(
        DemoState(path="/tmp/x"),
        None,
        RESOURCE_SCHEMA,
        None,
        response,
        type_name="demo",
        identity_schema=IDENTITY_SCHEMA,
        identity_values=None,
    )

    assert not response.HasField("new_identity")


# --- Integration-level coverage through _apply_resource_change_impl ---
# The helper-level tests above prove _handle_apply_result's own contract, but not that the
# real derivation path (resource_class.get_identity_schema()/get_identity()) actually
# reaches it, nor that inbound planned_identity reaches ResourceContext.identity. These
# exercise the full handler.


@define(frozen=True)
class DemoConfig:
    path: str | None = None


class _Base(BaseResource[Any, DemoState, DemoConfig]):
    config_class = DemoConfig
    state_class = DemoState
    seen_identity: Any = None

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return RESOURCE_SCHEMA

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, None]:
        type(self).seen_identity = ctx.identity
        return ctx.planned_state, None

    async def read(self, ctx: ResourceContext) -> DemoState | None:
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


class NoIdentityResource(_Base):
    seen_identity: Any = None


class IdentityResource(_Base):
    seen_identity: Any = None

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return IDENTITY_SCHEMA


class IdentityResourceRaisingOnDerive(_Base):
    """A resource whose get_identity() override is buggy -- the apply itself must still
    succeed, with identity simply omitted, distinct from the state-contract-violation path."""

    seen_identity: Any = None

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return IDENTITY_SCHEMA

    @classmethod
    def get_identity(cls, state: Any) -> dict[str, Any] | None:
        raise RuntimeError("boom: buggy get_identity() override")


class IdentityResourceRaisingUnconditionally(_Base):
    """A get_identity() override that does not guard for state is None -- unlike the
    framework default, this one raises even on a destroy. Proves the call site skips
    derivation entirely when there is no new state, rather than relying on this override
    to guard itself."""

    seen_identity: Any = None

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return IDENTITY_SCHEMA

    @classmethod
    def get_identity(cls, state: Any) -> dict[str, Any] | None:
        raise RuntimeError("boom: does not guard against state is None")


class IdentityResourceWithMismatchedSchema(_Base):
    """Declares an identity schema whose attributes don't exist on DemoState. Uses the
    framework default get_identity(), which returns None (via getattr(..., None)) rather
    than raising -- the ordinary, non-exceptional None-return path."""

    seen_identity: Any = None

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return MISMATCHED_IDENTITY_SCHEMA


class DuckTypedResource:
    """Registered by marker attribute alone, with no BaseResource and therefore no
    get_identity_schema(). @register_resource stamps markers and discovery registers on the
    marker, so this shape predates identity and must not start raising AttributeError."""

    config_class = DemoConfig
    state_class = DemoState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return RESOURCE_SCHEMA

    async def apply(self, ctx: ResourceContext) -> tuple[Any, None]:
        return DemoState(path="/tmp/x"), None


def _request(planned_identity: pb.ResourceIdentityData | None = None) -> pb.ApplyResourceChange.Request:
    config = marshal({"path": "/tmp/x"}, schema=RESOURCE_SCHEMA.block)
    planned_state = marshal({"path": "/tmp/x"}, schema=RESOURCE_SCHEMA.block)
    request = pb.ApplyResourceChange.Request(
        type_name="demo",
        config=config,
        planned_state=planned_state,
        planned_private=b"",
    )
    if planned_identity is not None:
        request.planned_identity.CopyFrom(planned_identity)
    return request


def _destroy_request() -> pb.ApplyResourceChange.Request:
    """A destroy request: prior_state is set, planned_state is left unset/null, which
    drives BaseResource.apply()'s is_delete branch and leaves new_state_attrs as None."""
    config = marshal({"path": "/tmp/x"}, schema=RESOURCE_SCHEMA.block)
    prior_state = marshal({"path": "/tmp/x"}, schema=RESOURCE_SCHEMA.block)
    return pb.ApplyResourceChange.Request(
        type_name="demo",
        config=config,
        prior_state=prior_state,
        planned_private=b"",
    )


def _patched(resource_class: Any) -> Any:
    provider = MagicMock()
    provider.metadata.capabilities = {}
    return patch(
        f"{MODULE}.hub.get_component",
        side_effect=lambda kind, name: resource_class if kind == "resource" else provider,
    )


@pytest.mark.asyncio
async def test_impl_omits_new_identity_when_resource_declares_none() -> None:
    with _patched(NoIdentityResource):
        response = await _apply_resource_change_impl(_request(), context=None)

    assert not response.diagnostics
    assert not response.HasField("new_identity")


@pytest.mark.asyncio
async def test_impl_emits_new_identity_when_derivable() -> None:
    with _patched(IdentityResource):
        response = await _apply_resource_change_impl(_request(), context=None)

    assert not response.diagnostics
    assert unmarshal_identity(response.new_identity, IDENTITY_SCHEMA) == {"path": "/tmp/x"}


@pytest.mark.asyncio
async def test_impl_inbound_planned_identity_reaches_the_resource_context() -> None:
    inbound = marshal_identity({"path": "/planned"}, IDENTITY_SCHEMA)

    with _patched(IdentityResource):
        await _apply_resource_change_impl(_request(planned_identity=inbound), context=None)

    assert IdentityResource.seen_identity == {"path": "/planned"}


@pytest.mark.asyncio
async def test_impl_omits_new_identity_when_derivation_raises() -> None:
    """A buggy get_identity() override must not fail the apply or surface as a diagnostic --
    identity is simply omitted. Unlike plan, apply runs after state is fully known, so this
    is logged loudly (WARNING) as it is a genuine defect rather than a "not yet knowable"."""
    with _patched(IdentityResourceRaisingOnDerive):
        response = await _apply_resource_change_impl(_request(), context=None)

    assert not any(d.severity == pb.Diagnostic.ERROR for d in response.diagnostics)
    assert not response.HasField("new_identity")


@pytest.mark.asyncio
async def test_impl_skips_derivation_entirely_on_destroy() -> None:
    """On destroy there is no new state, so identity derivation must not even be attempted
    -- calling get_identity(None) would be misleading regardless of whether it raises or
    returns cleanly. Uses a get_identity() that raises unconditionally (does not guard for
    state is None, unlike the framework default) and asserts the derivation helper itself
    is never called, not merely that the output looks right, since output correctness alone
    would pass even if the (wrong) exception path silently produced the same result."""
    with (
        _patched(IdentityResourceRaisingUnconditionally),
        patch(f"{MODULE}.derive_identity_values") as mock_derive,
    ):
        response = await _apply_resource_change_impl(_destroy_request(), context=None)

    mock_derive.assert_not_called()
    assert not any(d.severity == pb.Diagnostic.ERROR for d in response.diagnostics)
    assert not response.HasField("new_identity")


@pytest.mark.asyncio
async def test_impl_omits_new_identity_on_schema_state_mismatch() -> None:
    """The new state is fully known (a create, not a destroy), yet get_identity() returns
    None through the ordinary framework-default path because the identity schema's
    attribute ("id") does not exist on DemoState. The apply still succeeds and identity is
    simply omitted -- this is the schema/state-mismatch case Finding 2 warns about."""
    with _patched(IdentityResourceWithMismatchedSchema):
        response = await _apply_resource_change_impl(_request(), context=None)

    assert not any(d.severity == pb.Diagnostic.ERROR for d in response.diagnostics)
    assert not response.HasField("new_identity")


@pytest.mark.asyncio
async def test_impl_duck_typed_resource_without_get_identity_schema_still_applies() -> None:
    """A missing get_identity_schema() means the same as one returning None."""
    with _patched(DuckTypedResource):
        response = await _apply_resource_change_impl(_request(), context=None)

    assert not response.diagnostics
    assert not response.HasField("new_identity")
    assert response.new_state.msgpack


# 🐍🏗️🔚
