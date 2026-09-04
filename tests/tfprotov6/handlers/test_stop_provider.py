#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the StopProvider handler.

Terraform's Stop is advisory: it asks the provider to halt what it is doing and
expects an immediate answer, then waits for the calls already in flight to come
back on their own (terraform/internal/providers/provider.go:63-73,
internal/terraform/context.go:340-386). Stopping the process is a separate step,
driven by `Close()` and go-plugin's `Kill()`, which reaches the plugin as
GRPCController.Shutdown (internal/plugin6/grpc_provider.go:1885-1904).

This handler used to schedule `RPCPluginServer.stop()` shortly after replying,
which tore down the gRPC server, unlinked the socket and exited the process. An
`ApplyResourceChange` still running was cut off, so an interrupted apply failed
with UNAVAILABLE and a resource created remotely never reached state; Terraform's
own teardown then found a dead socket and reported "plugin failed to exit
gracefully". terraform-plugin-go implements Stop by cancelling contexts and
carries on serving (tfprotov6/tf6server/server.go:412-454).
"""

from provide.testkit.mocking import AsyncMock, patch
import pytest

from pyvider.common.stop_signal import is_stop_requested, reset_stop_signal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.stop_provider import (
    StopProviderHandler,
    _stop_provider_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture(autouse=True)
def _clean_signal() -> None:
    reset_stop_signal()
    yield
    reset_stop_signal()


class TestStopProviderHandlerStructure:
    """Tests for StopProvider handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self) -> None:
        """Test that handler returns a StopProvider.Response."""
        response = await StopProviderHandler(pb.StopProvider.Request(), context=None)

        assert isinstance(response, pb.StopProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_reports_no_error(self) -> None:
        """Nothing here can fail, so the protocol's Error field stays empty."""
        response = await StopProviderHandler(pb.StopProvider.Request(), context=None)

        assert not response.Error

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self) -> None:
        """Test that handler delegates to implementation."""
        request = pb.StopProvider.Request()

        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider._stop_provider_impl") as mock_impl:
            mock_impl.return_value = pb.StopProvider.Response()

            await StopProviderHandler(request, context=None)

            mock_impl.assert_called_once_with(request, None)


class TestStopProviderSignals:
    """Stop asks in-flight work to wind up."""

    @pytest.mark.asyncio
    async def test_it_raises_the_stop_signal(self) -> None:
        assert is_stop_requested() is False

        await _stop_provider_impl(pb.StopProvider.Request(), context=None)

        assert is_stop_requested() is True

    @pytest.mark.asyncio
    async def test_a_context_sees_the_request(self) -> None:
        """A resource reaches the signal through the context it already has."""
        from pyvider.resources.context import ResourceContext

        ctx: ResourceContext = ResourceContext()
        await _stop_provider_impl(pb.StopProvider.Request(), context=None)

        assert ctx.stop_requested is True

    @pytest.mark.asyncio
    async def test_stopping_twice_is_harmless(self) -> None:
        """A second Ctrl-C sends StopProvider again; it must not be an error."""
        first = await _stop_provider_impl(pb.StopProvider.Request(), context=None)
        second = await _stop_provider_impl(pb.StopProvider.Request(), context=None)

        assert not first.Error
        assert not second.Error
        assert is_stop_requested() is True


class TestStopProviderLeavesTheServerRunning:
    """The regression guard: Stop must not tear the plugin down."""

    @pytest.mark.asyncio
    async def test_the_server_is_not_stopped(self) -> None:
        """Terraform still has calls in flight and stops the process itself."""
        mock_server = AsyncMock()
        previous = hub.get_component("singleton", "rpc_plugin_server")
        hub.register("singleton", "rpc_plugin_server", lambda: mock_server)
        try:
            await _stop_provider_impl(pb.StopProvider.Request(), context=None)
        finally:
            if previous is None:
                hub.unregister("singleton", "rpc_plugin_server")
            else:
                hub.register("singleton", "rpc_plugin_server", previous)

        mock_server.stop.assert_not_called()

    @pytest.mark.asyncio
    async def test_it_returns_without_waiting_on_anything(self) -> None:
        """Stop must answer immediately; Terraform is holding the call open."""
        response = await _stop_provider_impl(pb.StopProvider.Request(), context=None)

        assert isinstance(response, pb.StopProvider.Response)


class TestStopProviderMetrics:
    """Tests for StopProvider metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self) -> None:
        """Test that handler increments request counter."""
        with patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests:
            await StopProviderHandler(pb.StopProvider.Request(), context=None)

            mock_requests.inc.assert_called_once_with(handler="StopProvider")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(self) -> None:
        """Test that handler records duration metric."""
        with patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration:
            await StopProviderHandler(pb.StopProvider.Request(), context=None)

            assert mock_duration.observe.called
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "StopProvider"
            assert call_args[0][0] >= 0


class TestStopProviderLogging:
    """Tests for StopProvider logging behavior."""

    @pytest.mark.asyncio
    async def test_impl_logs_the_request(self) -> None:
        with patch("pyvider.protocols.tfprotov6.handlers.stop_provider.logger") as mock_logger:
            await _stop_provider_impl(pb.StopProvider.Request(), context=None)

            assert mock_logger.info.called

    @pytest.mark.asyncio
    async def test_handler_with_context_object(self) -> None:
        """A gRPC context object is accepted and ignored."""
        response = await StopProviderHandler(pb.StopProvider.Request(), context=object())

        assert isinstance(response, pb.StopProvider.Response)


# 🐍🏗️🔚
