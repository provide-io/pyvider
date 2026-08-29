#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for MoveResourceState handler."""

from unittest.mock import patch

import pytest

from pyvider.protocols.tfprotov6.handlers.move_resource_state import (
    MoveResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_move_resource_state_carries_state_private_identity() -> None:
    """State, private state and identity survive a move that changed no type.

    This used to assert the same pass-through for `source_resource` ->
    `target_resource`, which is what the handler did for every pair of names.
    That is the defect, not the contract: see test_move_state_support.py. The
    pass-through itself is right when the type did not change.
    """
    request = pb.MoveResourceState.Request(
        source_type_name="same_resource",
        target_type_name="same_resource",
        source_state=pb.RawState(json=b'{"status":"old"}'),
        source_private=b"private-state",
        source_identity=pb.RawState(json=b'{"id":"abc"}'),
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 0
    assert response.target_state.json == request.source_state.json
    assert response.target_private == request.source_private
    assert response.target_identity.identity_data.json == request.source_identity.json


@pytest.mark.asyncio
async def test_move_resource_state_handles_same_type() -> None:
    """Verify same-type moves remain valid no-op operations."""
    request = pb.MoveResourceState.Request(
        source_type_name="test_resource",
        target_type_name="test_resource",
        source_state=pb.RawState(json=b"{}"),
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 0


@pytest.mark.asyncio
async def test_move_resource_state_records_metrics() -> None:
    """Test that handler records request metrics."""
    request = pb.MoveResourceState.Request(
        source_type_name="source_resource",
        target_type_name="target_resource",
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
    ):
        response = await MoveResourceStateHandler(request, context=None)

        # Verify metrics were recorded
        mock_requests.inc.assert_called_once_with(handler="MoveResourceState")
        mock_duration.observe.assert_called_once()
        assert isinstance(response, pb.MoveResourceState.Response)


@pytest.mark.asyncio
async def test_move_resource_state_records_errors_on_exception() -> None:
    """Test that handler records error metrics when exception occurs."""
    request = pb.MoveResourceState.Request(
        source_type_name="source_resource",
        target_type_name="target_resource",
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests"),
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
        patch(
            "pyvider.protocols.tfprotov6.handlers.move_resource_state._move_resource_state_impl"
        ) as mock_impl,
    ):
        # Make implementation raise an exception
        mock_impl.side_effect = RuntimeError("Test error")

        with pytest.raises(RuntimeError, match="Test error"):
            await MoveResourceStateHandler(request, context=None)

        # Verify error metric was recorded
        mock_errors.inc.assert_called_once_with(handler="MoveResourceState")
