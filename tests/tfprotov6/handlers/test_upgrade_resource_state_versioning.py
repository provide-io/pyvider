#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""State written under an older schema version reaches the resource's upgrade hook.

Regression for #26. `UpgradeResourceState` was a pass-through, and correct only
because `s_resource` accepted no version, so the stored version could never
differ from the advertised one. Either fact changing alone hands old state to a
new schema.
"""

from __future__ import annotations

import json
from typing import Any

import attrs
from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.conversion import unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import (
    UpgradeResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.schema import a_num, a_str, s_resource

MODULE = "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state"
SCHEMA = s_resource(
    attributes={"name": a_str(required=True), "size": a_num(optional=True)},
    version=3,
)


def _resource(schema: Any = SCHEMA, upgraded: Any = None) -> MagicMock:
    cls = MagicMock()
    cls.get_schema.return_value = schema
    cls.upgrade_state = AsyncMock(return_value=upgraded)
    return cls


def _request(version: int, state: dict[str, Any] | None = None) -> pb.UpgradeResourceState.Request:
    payload = {"name": "demo", "size": 4} if state is None else state
    return pb.UpgradeResourceState.Request(
        type_name="demo",
        version=version,
        raw_state=pb.RawState(json=json.dumps(payload).encode("utf-8")),
    )


@pytest.mark.asyncio
async def test_a_resource_declares_its_schema_version() -> None:
    """Without this the stored version can never differ and the hook is dead code."""
    assert s_resource(attributes={"name": a_str(required=True)}).version == 1
    assert SCHEMA.version == 3


@pytest.mark.asyncio
async def test_matching_version_passes_the_stored_bytes_through_untouched() -> None:
    """The pass-through path is what every existing provider is on; it must not change."""
    resource = _resource()
    request = _request(version=3)

    with patch(f"{MODULE}.hub.get_component", return_value=resource):
        response = await UpgradeResourceStateHandler(request, context=None)

    assert not response.diagnostics
    assert response.upgraded_state.json == request.raw_state.json
    resource.upgrade_state.assert_not_awaited()


@pytest.mark.asyncio
async def test_an_older_version_reaches_the_upgrade_hook() -> None:
    resource = _resource(upgraded={"name": "demo", "size": 4})

    with patch(f"{MODULE}.hub.get_component", return_value=resource):
        response = await UpgradeResourceStateHandler(_request(version=1), context=None)

    assert not response.diagnostics, f"upgrade failed: {response.diagnostics}"
    resource.upgrade_state.assert_awaited_once_with(1, {"name": "demo", "size": 4})


@pytest.mark.asyncio
async def test_the_upgraded_state_comes_back_marshalled_against_the_current_schema() -> None:
    """The hook returns native data; Terraform needs it as a value of the current type."""
    resource = _resource(upgraded={"name": "renamed", "size": 9})

    with patch(f"{MODULE}.hub.get_component", return_value=resource):
        response = await UpgradeResourceStateHandler(_request(version=1), context=None)

    assert not response.diagnostics
    upgraded = unmarshal(response.upgraded_state, schema=SCHEMA.block)
    assert str(upgraded["name"].value) == "renamed"


@pytest.mark.asyncio
async def test_an_upgrade_the_current_schema_rejects_is_not_written_to_state() -> None:
    """A hook that returns the wrong shape must fail the RPC, not persist it."""
    resource = _resource(upgraded={"name": "demo", "size": "not-a-number", "gone": 1})

    with patch(f"{MODULE}.hub.get_component", return_value=resource):
        response = await UpgradeResourceStateHandler(_request(version=1), context=None)

    assert response.diagnostics, "an unusable upgrade must be reported"
    assert not response.upgraded_state.msgpack
    assert not response.upgraded_state.json
    detail = response.diagnostics[0].summary + response.diagnostics[0].detail
    assert "demo" in detail
    assert "1" in detail and "3" in detail, "the diagnostic must name both versions"


@pytest.mark.asyncio
async def test_an_unregistered_resource_type_is_reported() -> None:
    """Terraform only asks about advertised types, so this is a provider bug worth naming."""
    with patch(f"{MODULE}.hub.get_component", return_value=None):
        response = await UpgradeResourceStateHandler(_request(version=1), context=None)

    assert response.diagnostics
    assert "demo" in response.diagnostics[0].summary + response.diagnostics[0].detail


@pytest.mark.asyncio
async def test_no_stored_state_stays_the_empty_object() -> None:
    request = pb.UpgradeResourceState.Request(type_name="demo", version=1, raw_state=pb.RawState())

    with patch(f"{MODULE}.hub.get_component", return_value=_resource()):
        response = await UpgradeResourceStateHandler(request, context=None)

    assert not response.diagnostics
    assert response.upgraded_state.json == b"{}"


# --- end to end, through the real hub and a real resource -------------------
#
# The tests above drive the handler with a MagicMock, which proves the handler's
# logic but not that a resource can actually declare a version and have its hook
# reached. This registers a real resource and goes in through the RPC.


@attrs.define
class _State:
    name: str
    size: int | None = None


class _MigratingResource(BaseResource[Any, _State, _State]):
    """Version 2. State written at version 1 called the attribute `title`."""

    config_class = _State
    state_class = _State
    seen: tuple[int, dict[str, Any]] | None = None

    @classmethod
    def get_schema(cls) -> Any:
        return s_resource(
            attributes={"name": a_str(required=True), "size": a_num(optional=True)},
            version=2,
        )

    @classmethod
    async def upgrade_state(cls, version: int, raw_state: dict[str, Any]) -> dict[str, Any]:
        _MigratingResource.seen = (version, dict(raw_state))
        return {"name": raw_state["title"], "size": raw_state.get("size")}

    async def _validate_config(self, config: _State) -> list[str]:
        return []

    async def read(self, ctx: Any) -> _State | None:
        return ctx.state

    async def _delete_apply(self, ctx: Any) -> None:
        return None


@pytest.fixture
def migrating_resource() -> Any:
    hub.register("resource", "migrating", _MigratingResource)
    yield _MigratingResource
    _MigratingResource.seen = None
    hub.unregister("resource", "migrating")


@pytest.mark.asyncio
async def test_a_registered_resource_migrates_its_own_state(migrating_resource: Any) -> None:
    """A rename that would otherwise hand `title` to a schema that only knows `name`."""
    request = pb.UpgradeResourceState.Request(
        type_name="migrating",
        version=1,
        raw_state=pb.RawState(json=json.dumps({"title": "old-name", "size": 7}).encode("utf-8")),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert not response.diagnostics, f"upgrade failed: {response.diagnostics}"
    assert migrating_resource.seen == (1, {"title": "old-name", "size": 7})

    upgraded = unmarshal(response.upgraded_state, schema=_MigratingResource.get_schema().block)
    assert str(upgraded["name"].value) == "old-name"


@pytest.mark.asyncio
async def test_a_registered_resource_at_its_current_version_is_untouched(
    migrating_resource: Any,
) -> None:
    """Version 2 is current, so the hook must not run and the bytes must survive."""
    stored = json.dumps({"name": "current", "size": 1}).encode("utf-8")
    request = pb.UpgradeResourceState.Request(
        type_name="migrating", version=2, raw_state=pb.RawState(json=stored)
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert not response.diagnostics
    assert response.upgraded_state.json == stored
    assert migrating_resource.seen is None, "the hook must not run when versions agree"


# 🐍🏗️🔚
