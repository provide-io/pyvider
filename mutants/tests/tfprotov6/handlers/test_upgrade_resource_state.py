"""Tests for UpgradeResourceState handler."""

import json
import pytest

from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import (
    UpgradeResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_upgrade_resource_state_passes_through_json_state():
    """
    Verifies that UpgradeResourceState returns the same state it receives.
    """
    state_data = {"name": "test", "value": 123}
    state_json = json.dumps(state_data).encode("utf-8")

    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(json=state_json),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert isinstance(response, pb.UpgradeResourceState.Response)
    assert len(response.diagnostics) == 0
    assert response.upgraded_state.json == state_json


@pytest.mark.asyncio
async def test_upgrade_resource_state_handles_empty_state():
    """
    Verifies that UpgradeResourceState handles empty state correctly.
    """
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert isinstance(response, pb.UpgradeResourceState.Response)
    assert len(response.diagnostics) == 0
    # Should return empty object
    assert response.upgraded_state.json == b"{}"


@pytest.mark.asyncio
async def test_upgrade_resource_state_handles_no_raw_state():
    """
    Verifies that UpgradeResourceState handles missing raw_state.
    """
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert isinstance(response, pb.UpgradeResourceState.Response)
    assert len(response.diagnostics) == 0
    # Should return empty object
    assert response.upgraded_state.json == b"{}"


@pytest.mark.asyncio
async def test_upgrade_resource_state_preserves_complex_state():
    """
    Verifies that UpgradeResourceState preserves complex nested state.
    """
    state_data = {
        "name": "test",
        "nested": {"key": "value", "count": 42},
        "list": [1, 2, 3],
    }
    state_json = json.dumps(state_data).encode("utf-8")

    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(json=state_json),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert isinstance(response, pb.UpgradeResourceState.Response)
    assert len(response.diagnostics) == 0
    # Should preserve exact state
    assert response.upgraded_state.json == state_json
    # Verify we can parse it back
    parsed = json.loads(response.upgraded_state.json)
    assert parsed == state_data
