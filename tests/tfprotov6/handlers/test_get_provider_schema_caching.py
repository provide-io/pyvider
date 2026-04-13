#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema caching and edge cases."""

import asyncio
from collections.abc import Iterator

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    GetProviderSchemaHandler,
    _compute_schema_once,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestGetProviderSchemaCaching:
    """Tests for schema caching behavior."""

    @pytest.mark.asyncio
    async def test_schema_computed_once(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
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
    async def test_concurrent_calls_use_same_future(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that concurrent calls await the same Future."""
        call_count = 0

        async def slow_compute() -> pb.GetProviderSchema.Response:
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
    async def test_with_context_object(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test handler with non-None context."""
        context = MagicMock()

        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            mock_compute.return_value = pb.GetProviderSchema.Response()

            response = await GetProviderSchemaHandler(sample_request, context=context)

            assert isinstance(response, pb.GetProviderSchema.Response)

    @pytest.mark.asyncio
    async def test_empty_collections(
        self, mock_provider_instance: MagicMock, clear_schema_cache: Iterator[None]
    ) -> None:
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
    async def test_catastrophic_schema_computation_failure(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
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
