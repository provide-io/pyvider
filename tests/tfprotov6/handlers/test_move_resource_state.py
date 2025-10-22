"""Tests for MoveResourceState handler."""

import pytest

from pyvider.protocols.tfprotov6.handlers.move_resource_state import (
    MoveResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_move_resource_state_returns_empty_response():
    """
    Verifies that MoveResourceState returns an empty response.
    This handler is currently unimplemented.
    """
    request = pb.MoveResourceState.Request(
        source_type_name="source_resource",
        target_type_name="target_resource",
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 0


@pytest.mark.asyncio
async def test_move_resource_state_handles_same_type():
    """
    Verifies that MoveResourceState handles same source and target types.
    """
    request = pb.MoveResourceState.Request(
        source_type_name="test_resource",
        target_type_name="test_resource",
    )

    response = await MoveResourceStateHandler(request, context=None)

    assert isinstance(response, pb.MoveResourceState.Response)
    assert len(response.diagnostics) == 0
