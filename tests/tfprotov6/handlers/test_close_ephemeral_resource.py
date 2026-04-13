#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CloseEphemeralResource handler."""

import msgpack
from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.exceptions import ResourceError
from pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource import (
    CloseEphemeralResourceHandler,
    _close_ephemeral_resource_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.CloseEphemeralResource.Request:
    """Create a sample CloseEphemeralResource request."""
    private_data = {"token": "test_token", "resource_id": "res_123"}
    request = pb.CloseEphemeralResource.Request()
    request.type_name = "test_ephemeral"
    request.private = msgpack.packb(private_data)
    return request


@pytest.fixture
def mock_ephemeral_class() -> MagicMock:
    """Create a mock ephemeral resource class."""
    mock_class = MagicMock()
    mock_class.private_state_class = MagicMock
    mock_instance = AsyncMock()
    mock_instance.close = AsyncMock()
    mock_class.return_value = mock_instance
    return mock_class


class TestCloseEphemeralResourceStructure:
    """Test handler structure and response types."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.CloseEphemeralResource.Request) -> None:
        """Test that handler returns proper response object."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await CloseEphemeralResourceHandler(sample_request, context=None)

            assert isinstance(response, pb.CloseEphemeralResource.Response)

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(
        self, sample_request: pb.CloseEphemeralResource.Request
    ) -> None:
        """Test that handler increments request counter."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await CloseEphemeralResourceHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="CloseEphemeralResource")


class TestCloseEphemeralResourceImpl:
    """Test implementation logic."""

    @pytest.mark.asyncio
    async def test_impl_closes_ephemeral_successfully(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test successful ephemeral resource close."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _close_ephemeral_resource_impl(sample_request, context=None)

            assert isinstance(response, pb.CloseEphemeralResource.Response)
            assert len(response.diagnostics) == 0
            # close() should have been called
            mock_instance = mock_ephemeral_class.return_value
            mock_instance.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_resource_type(
        self, sample_request: pb.CloseEphemeralResource.Request
    ) -> None:
        """Test handling of unknown ephemeral resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await _close_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0
            # ValueError is converted to generic "Internal Provider Error"
            assert (
                "Internal Provider Error" in response.diagnostics[0].summary
                or "not found" in response.diagnostics[0].detail.lower()
            )

    @pytest.mark.asyncio
    async def test_impl_handles_missing_private_state_class(
        self, sample_request: pb.CloseEphemeralResource.Request
    ) -> None:
        """Test handling when resource doesn't define private_state_class."""
        mock_class = MagicMock()
        mock_class.private_state_class = None  # No private state class!

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_class

            response = await _close_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0
            assert "private_state_class" in response.diagnostics[0].detail

    @pytest.mark.asyncio
    async def test_impl_unpacks_private_data_correctly(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that private data is unpacked from msgpack."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.msgpack.unpackb"
            ) as mock_unpack,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_unpack.return_value = {"token": "test_token"}

            await _close_ephemeral_resource_impl(sample_request, context=None)

            # msgpack.unpackb should have been called with private data
            mock_unpack.assert_called_once()
            assert mock_unpack.call_args[0][0] == sample_request.private

    @pytest.mark.asyncio
    async def test_impl_creates_ephemeral_context(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that EphemeralResourceContext is created."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.EphemeralResourceContext"
            ) as mock_ctx,
        ):
            mock_get.return_value = mock_ephemeral_class

            await _close_ephemeral_resource_impl(sample_request, context=None)

            # EphemeralResourceContext should be created with private_state
            mock_ctx.assert_called_once()
            assert "private_state" in mock_ctx.call_args[1]

    @pytest.mark.asyncio
    async def test_impl_handles_pyvider_errors(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that PyviderError exceptions are converted to diagnostics."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.close.side_effect = ResourceError("Close failed")

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _close_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0
            assert "Close failed" in response.diagnostics[0].detail

    @pytest.mark.asyncio
    async def test_impl_handles_generic_exceptions(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that generic exceptions are converted to diagnostics."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.close.side_effect = RuntimeError("Unexpected error")

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _close_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0
            # Should log error
            # Diagnostic should be created

    @pytest.mark.asyncio
    async def test_impl_logs_debug_info(
        self, sample_request: pb.CloseEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that debug logging occurs."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.logger") as mock_logger,
        ):
            mock_get.return_value = mock_ephemeral_class

            await _close_ephemeral_resource_impl(sample_request, context=None)

            # Should log at start with debug and completion with info
            assert mock_logger.debug.call_count >= 1
            assert mock_logger.info.call_count >= 1


class TestCloseEphemeralResourceMetrics:
    """Test metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_duration(self, sample_request: pb.CloseEphemeralResource.Request) -> None:
        """Test that handler records duration metric."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await CloseEphemeralResourceHandler(sample_request, context=None)

            # Duration should be observed
            mock_duration.observe.assert_called_once()
            assert mock_duration.observe.call_args[1]["handler"] == "CloseEphemeralResource"

    @pytest.mark.asyncio
    async def test_handler_records_error_on_exception(
        self, sample_request: pb.CloseEphemeralResource.Request
    ) -> None:
        """Test that handler increments error counter on exceptions."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch(
                "pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource._close_ephemeral_resource_impl"
            ) as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await CloseEphemeralResourceHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="CloseEphemeralResource")


# 🐍🏗️🔚
