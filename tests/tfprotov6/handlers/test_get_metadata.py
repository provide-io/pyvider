#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetMetadata handler."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_metadata import (
    GetMetadataHandler,
    _get_metadata_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.GetMetadata.Request:
    """Create a sample GetMetadata request."""
    return pb.GetMetadata.Request()


@pytest.fixture
def mock_hub_with_components() -> MagicMock:
    """Create a mock hub with registered components."""
    mock_hub = MagicMock()
    mock_hub.get_components.side_effect = lambda component_type: {
        "resource": {"test_resource": MagicMock(), "another_resource": MagicMock()},
        "data_source": {"test_data_source": MagicMock()},
        "function": {"test_function": MagicMock(), "another_function": MagicMock()},
    }.get(component_type, {})
    return mock_hub


@pytest.fixture
def mock_hub_empty() -> MagicMock:
    """Create a mock hub with no registered components."""
    mock_hub = MagicMock()
    mock_hub.get_components.return_value = {}
    return mock_hub


class TestGetMetadataHandlerStructure:
    """Tests for GetMetadata handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that handler returns GetMetadata.Response."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.return_value = {}

            response = await GetMetadataHandler(sample_request, context=None)

            assert isinstance(response, pb.GetMetadata.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that handler delegates to implementation."""
        with patch("pyvider.protocols.tfprotov6.handlers.get_metadata._get_metadata_impl") as mock_impl:
            mock_impl.return_value = pb.GetMetadata.Response()

            await GetMetadataHandler(sample_request, context=None)

            mock_impl.assert_called_once_with(sample_request, None)


class TestGetMetadataImpl:
    """Tests for GetMetadata implementation."""

    @pytest.mark.asyncio
    async def test_impl_discovers_resources(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that implementation discovers registered resources."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components):
            response = await _get_metadata_impl(sample_request, context=None)

            assert isinstance(response, pb.GetMetadata.Response)
            assert len(response.resources) == 2
            resource_names = [r.type_name for r in response.resources]
            assert "test_resource" in resource_names
            assert "another_resource" in resource_names

    @pytest.mark.asyncio
    async def test_impl_discovers_data_sources(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that implementation discovers registered data sources."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components):
            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.data_sources) == 1
            assert response.data_sources[0].type_name == "test_data_source"

    @pytest.mark.asyncio
    async def test_impl_discovers_functions(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that implementation discovers registered functions."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components):
            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.functions) == 2
            function_names = [f.name for f in response.functions]
            assert "test_function" in function_names
            assert "another_function" in function_names

    @pytest.mark.asyncio
    async def test_impl_sets_server_capabilities(
        self, sample_request: pb.GetMetadata.Request, mock_hub_empty: MagicMock
    ) -> None:
        """Test that implementation sets correct server capabilities."""
        with patch("pyvider.hub.hub", mock_hub_empty):
            response = await _get_metadata_impl(sample_request, context=None)

            assert response.server_capabilities.plan_destroy is True
            assert response.server_capabilities.get_provider_schema_optional is True
            assert response.server_capabilities.move_resource_state is True

    @pytest.mark.asyncio
    async def test_impl_handles_empty_registry(
        self, sample_request: pb.GetMetadata.Request, mock_hub_empty: MagicMock
    ) -> None:
        """Test that implementation handles empty registry gracefully."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_empty):
            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.resources) == 0
            assert len(response.data_sources) == 0
            assert len(response.functions) == 0
            assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_exception(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that implementation handles exceptions gracefully."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.side_effect = RuntimeError("Registry error")

            response = await _get_metadata_impl(sample_request, context=None)

            assert isinstance(response, pb.GetMetadata.Response)
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
            assert "Provider metadata discovery failed" in response.diagnostics[0].summary

    @pytest.mark.asyncio
    async def test_impl_returns_no_diagnostics_on_success(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that successful execution returns no diagnostics."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components):
            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.diagnostics) == 0


class TestGetMetadataMetrics:
    """Tests for GetMetadata metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that handler increments request counter."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
        ):
            mock_hub.get_components.return_value = {}

            await GetMetadataHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="GetMetadata")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that handler records duration metric."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
        ):
            mock_hub.get_components.return_value = {}

            await GetMetadataHandler(sample_request, context=None)

            assert mock_duration.observe.called
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "GetMetadata"
            assert call_args[0][0] >= 0

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(
        self, sample_request: pb.GetMetadata.Request
    ) -> None:
        """Test that handler increments error counter on failure."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch("pyvider.protocols.tfprotov6.handlers.get_metadata._get_metadata_impl") as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await GetMetadataHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="GetMetadata")


class TestGetMetadataLogging:
    """Tests for GetMetadata logging behavior."""

    @pytest.mark.asyncio
    async def test_impl_logs_discovery(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that implementation logs component discovery."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.get_metadata.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components),
        ):
            await _get_metadata_impl(sample_request, context=None)

            # Check that GetMetadata was logged
            assert any("GetMetadata" in str(call) for call in mock_logger.debug.call_args_list)

    @pytest.mark.asyncio
    async def test_impl_logs_discovered_resources(
        self, sample_request: pb.GetMetadata.Request, mock_hub_with_components: MagicMock
    ) -> None:
        """Test that discovered resources are logged."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.get_metadata.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub", mock_hub_with_components),
        ):
            await _get_metadata_impl(sample_request, context=None)

            # Check that resource discovery was logged
            assert any("resource" in str(call).lower() for call in mock_logger.debug.call_args_list)

    @pytest.mark.asyncio
    async def test_impl_logs_errors(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test that errors are logged."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.get_metadata.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
        ):
            mock_hub.get_components.side_effect = RuntimeError("Test error")

            await _get_metadata_impl(sample_request, context=None)

            mock_logger.error.assert_called_once()
            assert "GetMetadata handler failed" in str(mock_logger.error.call_args)


class TestGetMetadataEdgeCases:
    """Edge case tests for GetMetadata handler."""

    @pytest.mark.asyncio
    async def test_with_context_object(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test handler with non-None context."""
        context = MagicMock()

        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.return_value = {}

            response = await GetMetadataHandler(sample_request, context=context)

            assert isinstance(response, pb.GetMetadata.Response)

    @pytest.mark.asyncio
    async def test_with_only_resources(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test with only resources registered."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.side_effect = lambda comp_type: (
                {"res1": MagicMock()} if comp_type == "resource" else {}
            )

            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.resources) == 1
            assert len(response.data_sources) == 0
            assert len(response.functions) == 0

    @pytest.mark.asyncio
    async def test_with_only_data_sources(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test with only data sources registered."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.side_effect = lambda comp_type: (
                {"ds1": MagicMock()} if comp_type == "data_source" else {}
            )

            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.resources) == 0
            assert len(response.data_sources) == 1
            assert len(response.functions) == 0

    @pytest.mark.asyncio
    async def test_with_only_functions(self, sample_request: pb.GetMetadata.Request) -> None:
        """Test with only functions registered."""
        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.side_effect = lambda comp_type: (
                {"func1": MagicMock()} if comp_type == "function" else {}
            )

            response = await _get_metadata_impl(sample_request, context=None)

            assert len(response.resources) == 0
            assert len(response.data_sources) == 0
            assert len(response.functions) == 1


# 🐍🏗️🔚
