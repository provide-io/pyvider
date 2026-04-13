#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema handler."""

import asyncio

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    GetProviderSchemaHandler,
    _collect_data_source_schemas,
    _collect_function_schemas,
    _collect_resource_schemas,
    _compute_schema_once,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request():
    """Create a sample GetProviderSchema request."""
    return pb.GetProviderSchema.Request()


@pytest.fixture
def mock_provider_instance():
    """Create a mock provider instance."""
    mock_provider = MagicMock()
    mock_provider.schema = MagicMock()
    return mock_provider


@pytest.fixture
def mock_resource_class():
    """Create a mock resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_class.get_schema.return_value = mock_schema
    mock_class._is_test_only = False  # Needed for get_filtered_components
    return mock_class


@pytest.fixture
def clear_schema_cache():
    """Clear the schema cache before each test."""
    import pyvider.protocols.tfprotov6.handlers.get_provider_schema as module

    module._schema_future = None
    module._task = None
    yield
    module._schema_future = None
    module._task = None


class TestGetProviderSchemaHandlerStructure:
    """Tests for GetProviderSchema handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request, clear_schema_cache) -> None:
        """Test that handler returns GetProviderSchema.Response."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            mock_compute.return_value = pb.GetProviderSchema.Response()

            response = await GetProviderSchemaHandler(sample_request, context=None)

            assert isinstance(response, pb.GetProviderSchema.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self, sample_request, clear_schema_cache) -> None:
        """Test that handler delegates to implementation."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._get_provider_schema_impl"
        ) as mock_impl:
            mock_impl.return_value = pb.GetProviderSchema.Response()

            await GetProviderSchemaHandler(sample_request, context=None)

            mock_impl.assert_called_once_with(sample_request, None)


class TestCollectResourceSchemas:
    """Tests for resource schema collection."""

    @pytest.mark.asyncio
    async def test_collects_resource_schemas_successfully(self, mock_resource_class) -> None:
        """Test successful collection of resource schemas."""
        diagnostics = []

        with (
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
        ):
            mock_hub.get_components.return_value = {"test_resource": mock_resource_class}
            mock_hub.get_component.return_value = None  # No provider_context
            mock_to_proto.return_value = pb.Schema()

            result = await _collect_resource_schemas(diagnostics)

            assert "test_resource" in result
            assert isinstance(result["test_resource"], pb.Schema)
            assert len(diagnostics) == 0

    @pytest.mark.asyncio
    async def test_handles_resource_schema_error(self) -> None:
        """Test handling of errors during resource schema collection."""
        diagnostics = []
        mock_class = MagicMock()
        mock_class.get_schema.side_effect = RuntimeError("Schema error")
        mock_class._is_test_only = False  # Needed for get_filtered_components

        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.return_value = {"error_resource": mock_class}
            mock_hub.get_component.return_value = None  # No provider_context

            result = await _collect_resource_schemas(diagnostics)

            assert "error_resource" not in result
            assert len(diagnostics) == 1
            assert diagnostics[0].severity == pb.Diagnostic.WARNING
            assert "error_resource" in diagnostics[0].summary


class TestCollectDataSourceSchemas:
    """Tests for data source schema collection."""

    @pytest.mark.asyncio
    async def test_collects_data_source_schemas_successfully(self) -> None:
        """Test successful collection of data source schemas."""
        diagnostics = []
        mock_class = MagicMock()
        mock_schema = MagicMock()
        mock_class.get_schema.return_value = mock_schema
        mock_class._is_test_only = False  # Needed for get_filtered_components

        with (
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
        ):
            mock_hub.get_components.return_value = {"test_data_source": mock_class}
            mock_hub.get_component.return_value = None  # No provider_context
            mock_to_proto.return_value = pb.Schema()

            result = await _collect_data_source_schemas(diagnostics)

            assert "test_data_source" in result
            assert isinstance(result["test_data_source"], pb.Schema)
            assert len(diagnostics) == 0

    @pytest.mark.asyncio
    async def test_handles_data_source_schema_error(self) -> None:
        """Test handling of errors during data source schema collection."""
        diagnostics = []
        mock_class = MagicMock()
        mock_class.get_schema.side_effect = RuntimeError("Schema error")
        mock_class._is_test_only = False  # Needed for get_filtered_components

        with patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub:
            mock_hub.get_components.return_value = {"error_ds": mock_class}
            mock_hub.get_component.return_value = None  # No provider_context

            result = await _collect_data_source_schemas(diagnostics)

            assert "error_ds" not in result
            assert len(diagnostics) == 1
            assert diagnostics[0].severity == pb.Diagnostic.WARNING


class TestCollectFunctionSchemas:
    """Tests for function schema collection."""

    @pytest.mark.asyncio
    async def test_collects_function_schemas_successfully(self) -> None:
        """Test successful collection of function schemas."""
        diagnostics = []
        mock_func = MagicMock()
        mock_func._is_test_only = False  # Needed for get_filtered_components

        with (
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            mock_hub.get_components.return_value = {"test_function": mock_func}
            mock_hub.get_component.return_value = None  # No provider_context
            mock_to_dict.return_value = {"name": "test_function"}
            mock_to_proto.return_value = pb.Function()

            result = await _collect_function_schemas(diagnostics)

            assert "test_function" in result
            assert isinstance(result["test_function"], pb.Function)
            assert len(diagnostics) == 0

    @pytest.mark.asyncio
    async def test_handles_function_schema_error(self) -> None:
        """Test handling of errors during function schema collection."""
        diagnostics = []
        mock_func = MagicMock()
        mock_func._is_test_only = False  # Needed for get_filtered_components

        with (
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.function_to_dict") as mock_to_dict,
        ):
            mock_hub.get_components.return_value = {"error_func": mock_func}
            mock_hub.get_component.return_value = None  # No provider_context
            mock_to_dict.side_effect = RuntimeError("Function error")

            result = await _collect_function_schemas(diagnostics)

            assert "error_func" not in result
            assert len(diagnostics) == 1
            assert diagnostics[0].severity == pb.Diagnostic.WARNING


class TestComputeSchemaOnce:
    """Tests for schema computation."""

    @pytest.mark.asyncio
    async def test_computes_schema_successfully(self, mock_provider_instance) -> None:
        """Test successful schema computation."""
        with (
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
            mock_get_component.return_value = mock_provider_instance
            mock_to_proto.return_value = pb.Schema()
            mock_resources.return_value = {}
            mock_data_sources.return_value = {}
            mock_functions.return_value = {}

            response = await _compute_schema_once()

            assert isinstance(response, pb.GetProviderSchema.Response)
            assert isinstance(response.provider, pb.Schema)

    @pytest.mark.asyncio
    async def test_handles_missing_provider(self) -> None:
        """Test handling of missing provider instance."""
        with patch("pyvider.hub.hub.get_component") as mock_get_component:
            mock_get_component.return_value = None

            response = await _compute_schema_once()

            assert isinstance(response, pb.GetProviderSchema.Response)
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR

    @pytest.mark.asyncio
    async def test_handles_computation_error(self, mock_provider_instance) -> None:
        """Test handling of errors during schema computation."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get_component,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
        ):
            mock_get_component.return_value = mock_provider_instance
            mock_to_proto.side_effect = RuntimeError("Conversion error")

            response = await _compute_schema_once()

            assert isinstance(response, pb.GetProviderSchema.Response)
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR


class TestGetProviderSchemaMetrics:
    """Tests for GetProviderSchema metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request, clear_schema_cache) -> None:
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
    async def test_handler_records_duration_metric(self, sample_request, clear_schema_cache) -> None:
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
    async def test_handler_records_error_metric_on_failure(self, sample_request, clear_schema_cache) -> None:
        """Test that handler increments error counter on failure."""
        with patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._get_provider_schema_impl"
            ) as mock_impl:
                mock_impl.side_effect = RuntimeError("Test error")

                with pytest.raises(RuntimeError):
                    await GetProviderSchemaHandler(sample_request, context=None)

                mock_errors.inc.assert_called_once_with(handler="GetProviderSchema")


class TestGetProviderSchemaLogging:
    """Tests for GetProviderSchema logging behavior."""

    @pytest.mark.asyncio
    async def test_compute_logs_success(self, mock_provider_instance) -> None:
        """Test that successful computation is logged."""
        with patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.logger") as mock_logger:
            with patch("pyvider.hub.hub.get_component") as mock_get_component:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
                ) as mock_to_proto:
                    with patch(
                        "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_resource_schemas"
                    ) as mock_resources:
                        with patch(
                            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_data_source_schemas"
                        ) as mock_data_sources:
                            with patch(
                                "pyvider.protocols.tfprotov6.handlers.get_provider_schema._collect_function_schemas"
                            ) as mock_functions:

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
    async def test_compute_logs_errors(self, mock_provider_instance) -> None:
        """Test that errors are logged."""
        with patch("pyvider.protocols.tfprotov6.handlers.get_provider_schema.logger") as mock_logger:
            with patch("pyvider.hub.hub.get_component") as mock_get_component:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
                ) as mock_to_proto:
                    mock_get_component.return_value = mock_provider_instance
                    mock_to_proto.side_effect = RuntimeError("Test error")

                    await _compute_schema_once()

                    mock_logger.error.assert_called_once()
                    assert "Failed to compute" in str(mock_logger.error.call_args)


class TestGetProviderSchemaCaching:
    """Tests for schema caching behavior."""

    @pytest.mark.asyncio
    async def test_schema_computed_once(self, sample_request, clear_schema_cache) -> None:
        """Test that schema is computed only once for multiple calls."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            mock_compute.return_value = pb.GetProviderSchema.Response()

            # Make multiple calls
            response1 = await GetProviderSchemaHandler(sample_request, context=None)
            response2 = await GetProviderSchemaHandler(sample_request, context=None)
            response3 = await GetProviderSchemaHandler(sample_request, context=None)

            # Computation should only happen once
            assert mock_compute.call_count == 1
            assert response1 is response2
            assert response2 is response3

    @pytest.mark.asyncio
    async def test_concurrent_calls_use_same_future(self, sample_request, clear_schema_cache) -> None:
        """Test that concurrent calls await the same Future."""
        call_count = 0

        async def slow_compute():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # Simulate slow computation
            return pb.GetProviderSchema.Response()

        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once",
            side_effect=slow_compute,
        ):
            # Launch multiple concurrent calls
            tasks = [GetProviderSchemaHandler(sample_request, context=None) for _ in range(5)]
            responses = await asyncio.gather(*tasks)

            # All should return same response
            assert all(r is responses[0] for r in responses)
            # Computation should only happen once
            assert call_count == 1


class TestGetProviderSchemaEdgeCases:
    """Edge case tests for GetProviderSchema handler."""

    @pytest.mark.asyncio
    async def test_with_context_object(self, sample_request, clear_schema_cache) -> None:
        """Test handler with non-None context."""
        context = MagicMock()

        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            mock_compute.return_value = pb.GetProviderSchema.Response()

            response = await GetProviderSchemaHandler(sample_request, context=context)

            assert isinstance(response, pb.GetProviderSchema.Response)

    @pytest.mark.asyncio
    async def test_empty_collections(self, mock_provider_instance, clear_schema_cache) -> None:
        """Test with no resources, data sources, or functions."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get_component,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_provider_schema.pvs_schema_to_proto"
            ) as mock_to_proto,
            patch("pyvider.protocols.tfprotov6.handlers.utils.hub") as mock_hub,
        ):
            mock_get_component.return_value = mock_provider_instance
            mock_to_proto.return_value = pb.Schema()
            mock_hub.get_components.return_value = {}
            mock_hub.get_component.return_value = None  # No provider_context

            response = await _compute_schema_once()

            assert isinstance(response, pb.GetProviderSchema.Response)
            assert len(response.resource_schemas) == 0
            assert len(response.data_source_schemas) == 0
            assert len(response.functions) == 0

    @pytest.mark.asyncio
    async def test_catastrophic_schema_computation_failure(self, sample_request, clear_schema_cache) -> None:
        """Test handling of catastrophic failure during schema computation."""
        # This tests the exception path in _set_future_result (lines 179-181)
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            # Make _compute_schema_once raise an exception
            mock_compute.side_effect = RuntimeError("Catastrophic computation error")

            # The exception should propagate up from the Future
            with pytest.raises(RuntimeError, match="Catastrophic computation error"):
                await GetProviderSchemaHandler(sample_request, context=None)


# 🐍🏗️🔚
