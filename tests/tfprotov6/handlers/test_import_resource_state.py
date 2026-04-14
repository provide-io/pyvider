#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ImportResourceState handler."""

from provide.testkit.mocking import patch
import pytest

from pyvider.protocols.tfprotov6.handlers.import_resource_state import (
    ImportResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_import_resource_state_returns_empty_response() -> None:
    """
    Verifies that ImportResourceState returns a response with warning diagnostic.
    This handler is currently unimplemented.
    """
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="test-id",
    )

    response = await ImportResourceStateHandler(request, context=None)

    assert isinstance(response, pb.ImportResourceState.Response)
    assert len(response.diagnostics) == 1
    assert response.diagnostics[0].severity == pb.Diagnostic.WARNING
    assert "Import not yet implemented" in response.diagnostics[0].summary
    assert len(response.imported_resources) == 0


@pytest.mark.asyncio
async def test_import_resource_state_handles_empty_id() -> None:
    """
    Verifies that ImportResourceState handles empty ID.
    """
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="",
    )

    response = await ImportResourceStateHandler(request, context=None)

    assert isinstance(response, pb.ImportResourceState.Response)
    assert len(response.diagnostics) == 1  # Now returns warning diagnostic
    assert response.diagnostics[0].severity == pb.Diagnostic.WARNING


@pytest.mark.asyncio
async def test_import_resource_state_records_error_metric_on_exception() -> None:
    """Test that handler increments error counter on exception."""
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="test-id",
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
        patch(
            "pyvider.protocols.tfprotov6.handlers.import_resource_state._import_resource_state_impl"
        ) as mock_impl,
    ):
        mock_impl.side_effect = RuntimeError("Test error")

        with pytest.raises(RuntimeError):
            await ImportResourceStateHandler(request, context=None)

        mock_errors.inc.assert_called_once_with(handler="ImportResourceState")


@pytest.mark.asyncio
async def test_import_resource_state_records_metrics() -> None:
    """Test that handler records request and duration metrics."""
    request = pb.ImportResourceState.Request(
        type_name="test_resource",
        id="test-id",
    )

    with (
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
        patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
    ):
        await ImportResourceStateHandler(request, context=None)

        mock_requests.inc.assert_called_once_with(handler="ImportResourceState")
        assert mock_duration.observe.call_count == 1


# 🐍🏗️🔚
