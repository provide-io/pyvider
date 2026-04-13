#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for StopProvider handler."""

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.stop_provider import StopProviderHandler, _stop_provider_impl
import pyvider.protocols.tfprotov6.protobuf as pb


class TestStopProviderHandlerStructure:
    """Tests for StopProvider handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self) -> None:
        """Test that handler returns a StopProvider.Response."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub:
            mock_server = AsyncMock()
            # Return a factory that returns the mock server
            mock_hub.get_component.return_value = lambda: mock_server

            response = await StopProviderHandler(request, context=None)

            assert isinstance(response, pb.StopProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self) -> None:
        """Test that handler delegates to implementation."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider._stop_provider_impl") as mock_impl:
            mock_impl.return_value = pb.StopProvider.Response()

            await StopProviderHandler(request, context=None)

            mock_impl.assert_called_once_with(request, None)


class TestStopProviderImpl:
    """Tests for StopProvider implementation."""

    @pytest.mark.asyncio
    async def test_impl_stops_server_instance(self) -> None:
        """Test that implementation calls server stop() when instance exists."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub:
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            response = await _stop_provider_impl(request, context=None)

            assert isinstance(response, pb.StopProvider.Response)
            mock_hub.get_component.assert_called_once_with("singleton", "rpc_plugin_server")
            mock_server.stop.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_impl_handles_no_server_instance(self) -> None:
        """Test that implementation handles missing server instance gracefully."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub:
            mock_hub.get_component.return_value = None

            response = await _stop_provider_impl(request, context=None)

            assert isinstance(response, pb.StopProvider.Response)

    @pytest.mark.asyncio
    async def test_impl_raises_on_server_stop_error(self) -> None:
        """Test that implementation propagates errors from server.stop()."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub:
            mock_server = AsyncMock()
            mock_server.stop.side_effect = RuntimeError("Server stop failed")
            mock_hub.get_component.return_value = lambda: mock_server

            with pytest.raises(RuntimeError, match="Server stop failed"):
                await _stop_provider_impl(request, context=None)


class TestStopProviderMetrics:
    """Tests for StopProvider metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self) -> None:
        """Test that handler increments request counter."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            await StopProviderHandler(request, context=None)

            mock_requests.inc.assert_called_once_with(handler="StopProvider")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(self) -> None:
        """Test that handler records duration metric."""
        request = pb.StopProvider.Request()
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            await StopProviderHandler(request, context=None)

            # Duration should be recorded
            assert mock_duration.observe.called
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "StopProvider"
            # Duration should be a positive number
            assert call_args[0][0] >= 0

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(self) -> None:
        """Test that handler increments error counter on failure."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_server.stop.side_effect = RuntimeError("Stop failed")
            mock_hub.get_component.return_value = lambda: mock_server

            with pytest.raises(RuntimeError):
                await StopProviderHandler(request, context=None)

            mock_errors.inc.assert_called_once_with(handler="StopProvider")


class TestStopProviderLogging:
    """Tests for StopProvider logging behavior."""

    @pytest.mark.asyncio
    async def test_impl_logs_shutdown_initiation(self) -> None:
        """Test that implementation logs shutdown initiation."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            await _stop_provider_impl(request, context=None)

            # Check that info was called with shutdown message
            assert any("StopProvider RPC received" in str(call) for call in mock_logger.info.call_args_list)

    @pytest.mark.asyncio
    async def test_impl_logs_server_stop_completion(self) -> None:
        """Test that implementation logs when server stop completes."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            await _stop_provider_impl(request, context=None)

            # Check that completion was logged
            assert any("stop completed successfully" in str(call) for call in mock_logger.info.call_args_list)

    @pytest.mark.asyncio
    async def test_impl_logs_warning_when_no_server(self) -> None:
        """Test that implementation logs warning when no server instance."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            await _stop_provider_impl(request, context=None)

            # Check that warning was logged
            mock_logger.warning.assert_called_once()
            assert "No active RPCPluginServer" in str(mock_logger.warning.call_args)

    @pytest.mark.asyncio
    async def test_impl_logs_error_on_exception(self) -> None:
        """Test that implementation logs error when exception occurs."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_server.stop.side_effect = RuntimeError("Test error")
            mock_hub.get_component.return_value = lambda: mock_server

            with pytest.raises(RuntimeError):
                await _stop_provider_impl(request, context=None)

            # Check that error was logged
            mock_logger.error.assert_called_once()
            assert "Unexpected error" in str(mock_logger.error.call_args)


class TestStopProviderEdgeCases:
    """Edge case tests for StopProvider handler."""

    @pytest.mark.asyncio
    async def test_handler_with_context_object(self) -> None:
        """Test handler with non-None context object."""
        request = pb.StopProvider.Request()
        context = MagicMock()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub:
            mock_server = AsyncMock()
            mock_hub.get_component.return_value = lambda: mock_server

            response = await StopProviderHandler(request, context=context)

            assert isinstance(response, pb.StopProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_resilience_decorator(self) -> None:
        """Test that handler uses resilient decorator."""
        # The @resilient() decorator should handle exceptions gracefully
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider._stop_provider_impl") as mock_impl:
            mock_impl.side_effect = Exception("Test exception")

            with pytest.raises(Exception, match="Test exception"):
                await StopProviderHandler(request, context=None)

    @pytest.mark.asyncio
    async def test_metrics_recorded_even_on_error(self) -> None:
        """Test that metrics are recorded even when handler errors."""
        request = pb.StopProvider.Request()

        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.protocols.tfprotov6.handlers.stop_provider.hub") as mock_hub,
        ):
            mock_server = AsyncMock()
            mock_server.stop.side_effect = RuntimeError("Error")
            mock_hub.get_component.return_value = lambda: mock_server

            with pytest.raises(RuntimeError):
                await StopProviderHandler(request, context=None)

            # Duration should still be recorded
            assert mock_duration.observe.called


# 🐍🏗️🔚
