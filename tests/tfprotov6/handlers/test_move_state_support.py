#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A move across resource types is the target resource's decision, not the framework's.

Terraform asks the *target* provider whether it can accept a resource moved from
somewhere else. Answering yes for every pair and copying the source state across
verbatim writes one type's state into another type's slot and reports success --
the practitioner learns about it on the next plan, as an unexplained diff, or on
the next apply, as a failure inside a resource they did not touch.
"""

from collections.abc import Iterator
from typing import Any

import pytest

from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.move_resource_state import (
    MoveResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import PvsSchema, a_str, s_resource


class _NoMoveSupport:
    """The common case: a resource that never considered being moved into."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"id": a_str(computed=True), "name": a_str(required=True)})


class _AcceptsOneSource(_NoMoveSupport):
    """A resource that accepts a move from one named source and refuses the rest."""

    async def move_state(
        self,
        source_provider_address: str,
        source_type_name: str,
        source_state: dict[str, Any],
        source_schema_version: int,
    ) -> dict[str, Any] | None:
        if source_type_name != "old_widget":
            return None
        return {"id": source_state["widget_id"], "name": source_state["label"]}


class _AcceptsWithPrivate(_NoMoveSupport):
    """A resource that also decides what private state the moved resource keeps."""

    async def move_state(
        self,
        source_provider_address: str,
        source_type_name: str,
        source_state: dict[str, Any],
        source_schema_version: int,
    ) -> tuple[dict[str, Any], bytes]:
        return {"id": "moved", "name": source_state["label"]}, b"fresh-private"


@pytest.fixture
def registered(request: pytest.FixtureRequest) -> Iterator[type]:
    """Register a resource class as `target_widget` for the duration of one test."""
    cls = request.param
    hub.register("resource", "target_widget", cls)
    yield cls
    try:
        hub.unregister("resource", "target_widget")
    except Exception:
        pass


def _request(**kwargs: Any) -> pb.MoveResourceState.Request:
    defaults: dict[str, Any] = {
        "source_provider_address": "registry.terraform.io/provide-io/pyvider",
        "source_type_name": "old_widget",
        "target_type_name": "target_widget",
        "source_state": pb.RawState(json=b'{"widget_id":"w-1","label":"first"}'),
    }
    return pb.MoveResourceState.Request(**(defaults | kwargs))


def _errors(response: pb.MoveResourceState.Response) -> list[pb.Diagnostic]:
    return [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]


class TestSameType:
    """Only the provider address changed; the state shape is identical."""

    @pytest.mark.asyncio
    async def test_same_type_name_passes_everything_through(self) -> None:
        request = _request(
            source_type_name="target_widget",
            source_private=b"private-state",
            source_identity=pb.RawState(json=b'{"id":"abc"}'),
        )

        response = await MoveResourceStateHandler(request, context=None)

        assert _errors(response) == []
        assert response.target_state.json == request.source_state.json
        assert response.target_private == b"private-state"
        assert response.target_identity.identity_data.json == b'{"id":"abc"}'


class TestUnsupportedMove:
    """A refusal names the resource, so the practitioner knows whose decision it was."""

    @pytest.mark.asyncio
    async def test_unregistered_target_is_refused(self) -> None:
        response = await MoveResourceStateHandler(
            _request(target_type_name="nonexistent_widget"), context=None
        )

        errors = _errors(response)
        assert len(errors) == 1
        assert "nonexistent_widget" in errors[0].detail
        assert not response.target_state.json

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_NoMoveSupport], indirect=True)
    async def test_target_without_move_state_is_refused(self, registered: type) -> None:
        response = await MoveResourceStateHandler(_request(), context=None)

        errors = _errors(response)
        assert len(errors) == 1
        assert "target_widget" in errors[0].summary
        assert "old_widget" in errors[0].detail
        assert "Suggestion:" in errors[0].detail
        assert not response.target_state.json

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_AcceptsOneSource], indirect=True)
    async def test_a_source_the_resource_declines_is_refused(self, registered: type) -> None:
        response = await MoveResourceStateHandler(_request(source_type_name="some_other_widget"), context=None)

        errors = _errors(response)
        assert len(errors) == 1
        assert "some_other_widget" in errors[0].detail
        assert not response.target_state.json

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_NoMoveSupport], indirect=True)
    async def test_a_refused_move_carries_no_private_state(self, registered: type) -> None:
        """Nothing of the source may leak into a slot the target did not accept."""
        response = await MoveResourceStateHandler(_request(source_private=b"private-state"), context=None)

        assert _errors(response)
        assert response.target_private == b""


class TestSupportedMove:
    """The resource that accepted the move decides what the target state is."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_AcceptsOneSource], indirect=True)
    async def test_the_hook_result_becomes_the_target_state(self, registered: type) -> None:
        import json

        response = await MoveResourceStateHandler(_request(), context=None)

        assert _errors(response) == []
        assert json.loads(response.target_state.json) == {"id": "w-1", "name": "first"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_AcceptsOneSource], indirect=True)
    async def test_source_private_is_not_carried_across_a_type_change(self, registered: type) -> None:
        """The source's private state belongs to the source's type, not the target's."""
        response = await MoveResourceStateHandler(_request(source_private=b"source-private"), context=None)

        assert _errors(response) == []
        assert response.target_private == b""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("registered", [_AcceptsWithPrivate], indirect=True)
    async def test_the_hook_may_supply_the_target_private_state(self, registered: type) -> None:
        response = await MoveResourceStateHandler(_request(source_private=b"source-private"), context=None)

        assert _errors(response) == []
        assert response.target_private == b"fresh-private"


# 🐍🏗️🔚
