#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for UpgradeResourceState handler."""

import json

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import (
    UpgradeResourceStateHandler,
    _upgrade_resource_state_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import a_str, s_resource

MODULE = "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state"

# These exercise the pass-through, which is what happens when the stored version
# matches the schema's. The resource is registered at version 0 so the requests
# below -- all of which send version 0 -- take that path.
PASSTHROUGH_SCHEMA = s_resource(attributes={"name": a_str(optional=True)}, version=0)


@pytest.fixture(autouse=True)
def _registered_resource():
    """UpgradeResourceState now resolves the resource to learn its schema version."""
    resource = MagicMock()
    resource.get_schema.return_value = PASSTHROUGH_SCHEMA
    with patch(f"{MODULE}.hub.get_component", return_value=resource):
        yield resource


@pytest.mark.asyncio
async def test_upgrade_resource_state_passes_through_json_state() -> None:
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
async def test_upgrade_resource_state_handles_empty_state() -> None:
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
async def test_upgrade_resource_state_handles_no_raw_state() -> None:
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
async def test_upgrade_resource_state_preserves_complex_state() -> None:
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


@pytest.mark.asyncio
async def test_upgrade_resource_state_impl_handles_exception() -> None:
    """Test that implementation handles exceptions gracefully."""
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(json=b'{"test": "data"}'),
    )

    # Patch logger.debug to raise an exception on second call
    with patch("pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.logger") as mock_logger:
        call_count = 0

        def debug_side_effect(*args: list, **kwargs: dict) -> None:
            nonlocal call_count
            call_count += 1
            if call_count == 2:  # Raise on second debug call
                raise RuntimeError("Test error")

        mock_logger.debug.side_effect = debug_side_effect

        response = await _upgrade_resource_state_impl(request, context=None)

        # Should return response with error diagnostic
        assert len(response.diagnostics) == 1
        assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
        assert "State upgrade failed" in response.diagnostics[0].summary
        assert "Test error" in response.diagnostics[0].detail


@pytest.mark.asyncio
async def test_upgrade_resource_state_handler_records_error_metric() -> None:
    """Test that handler increments error counter on exception."""
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
        patch(
            "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state._upgrade_resource_state_impl"
        ) as mock_impl,
    ):
        mock_impl.side_effect = RuntimeError("Test error")

        with pytest.raises(RuntimeError):
            await UpgradeResourceStateHandler(request, context=None)

        mock_errors.inc.assert_called_once_with(handler="UpgradeResourceState")


@pytest.mark.asyncio
async def test_upgrade_resource_state_records_metrics() -> None:
    """Test that handler records request and duration metrics."""
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
    ):
        await UpgradeResourceStateHandler(request, context=None)

        mock_requests.inc.assert_called_once_with(handler="UpgradeResourceState")
        assert mock_duration.observe.call_count == 1


# 🐍🏗️🔚
