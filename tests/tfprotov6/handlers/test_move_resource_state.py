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
async def test_move_resource_state_returns_empty_response() -> None:
    """
    Verifies that MoveResourceState returns a response with warning diagnostic.
    This handler is currently unimplemented.
    """
    request = pb.MoveResourceState.Request(
        source_type_name="source_resource",
        target_type_name="target_resource",
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 1
    assert response.diagnostics[0].severity == pb.Diagnostic.WARNING
    assert "Resource move not yet implemented" in response.diagnostics[0].summary


@pytest.mark.asyncio
async def test_move_resource_state_handles_same_type() -> None:
    """
    Verifies that MoveResourceState handles same source and target types.
    """
    request = pb.MoveResourceState.Request(
        source_type_name="test_resource",
        target_type_name="test_resource",
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 1  # Now returns warning diagnostic
    assert response.diagnostics[0].severity == pb.Diagnostic.WARNING


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


# 🐍🏗️🔚
