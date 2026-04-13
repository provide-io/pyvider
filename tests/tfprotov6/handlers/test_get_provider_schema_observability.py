#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema observability (metrics and logging)."""

from collections.abc import Iterator

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    GetProviderSchemaHandler,
    _compute_schema_once,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestGetProviderSchemaMetrics:
    """Tests for GetProviderSchema metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that handler increments request counter."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
            ) as mock_compute,
        ):
            mock_compute.return_value = pb.GetProviderSchema.Response()

            await GetProviderSchemaHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="GetProviderSchema")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that handler records duration metric."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
            ) as mock_compute,
        ):
            mock_compute.return_value = pb.GetProviderSchema.Response()

            await GetProviderSchemaHandler(sample_request, context=None)

            assert mock_duration.observe.called
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "GetProviderSchema"
            assert call_args[0][0] >= 0

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that handler increments error counter on failure."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._get_provider_schema_impl"
            ) as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await GetProviderSchemaHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="GetProviderSchema")


class TestGetProviderSchemaLogging:
    """Tests for GetProviderSchema logging behavior."""

    @pytest.mark.asyncio
    async def test_compute_logs_success(self, mock_provider_instance: MagicMock) -> None:
        """Test that successful computation is logged."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.logger") as mock_logger,
            patch("pyvider.hub.hub.get_component") as mock_get_component,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_resource_schemas"
            ) as mock_resources,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_data_source_schemas"
            ) as mock_data_sources,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_function_schemas"
            ) as mock_functions,
        ):

            def get_component_side_effect(scope, name):
                if name == "_discovery_ready_event":
                    return None  # Skip discovery wait
                return mock_provider_instance

            mock_get_component.side_effect = get_component_side_effect
            mock_to_proto.return_value = pb.Schema()
            mock_resources.return_value = {}
            mock_data_sources.return_value = {}
            mock_functions.return_value = {}

            await _compute_schema_once()

            # Check that success was logged
            assert any(
                "computed" in str(call).lower() and "successfully" in str(call).lower()
                for call in mock_logger.info.call_args_list
            )

    @pytest.mark.asyncio
    async def test_compute_logs_errors(self, mock_provider_instance: MagicMock) -> None:
        """Test that errors are logged."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.logger") as mock_logger,
            patch("pyvider.hub.hub.get_component") as mock_get_component,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
        ):
            mock_get_component.return_value = mock_provider_instance
            mock_to_proto.side_effect = RuntimeError("Test error")

            await _compute_schema_once()

            mock_logger.error.assert_called_once()
            assert "Failed to compute" in str(mock_logger.error.call_args)
