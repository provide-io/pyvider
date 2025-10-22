"""Tests for ImportResourceState handler."""

import pytest

from pyvider.protocols.tfprotov6.handlers.import_resource_state import (
    ImportResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_import_resource_state_returns_empty_response():
    """
    Verifies that ImportResourceState returns an empty response.
    This handler is currently unimplemented.
    """
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="test-id",
    )

    response = await ImportResourceStateHandler(request, context=None)

    assert isinstance(response, pb.ImportResourceState.Response)
    assert len(response.diagnostics) == 0
    assert len(response.imported_resources) == 0


@pytest.mark.asyncio
async def test_import_resource_state_handles_empty_id():
    """
    Verifies that ImportResourceState handles empty ID.
    """
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="",
    )

    response = await ImportResourceStateHandler(request, context=None)

    assert isinstance(response, pb.ImportResourceState.Response)
    assert len(response.diagnostics) == 0
