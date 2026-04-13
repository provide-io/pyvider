#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema handler response structure."""

from collections.abc import Iterator

from provide.testkit.mocking import patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    GetProviderSchemaHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestGetProviderSchemaHandlerStructure:
    """Tests for GetProviderSchema handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that handler returns GetProviderSchema.Response."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once"
        ) as mock_compute:
            mock_compute.return_value = pb.GetProviderSchema.Response()

            response = await GetProviderSchemaHandler(sample_request, context=None)

            assert isinstance(response, pb.GetProviderSchema.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(
        self, sample_request: pb.GetProviderSchema.Request, clear_schema_cache: Iterator[None]
    ) -> None:
        """Test that handler delegates to implementation."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.get_provider_schema._get_provider_schema_impl"
        ) as mock_impl:
            mock_impl.return_value = pb.GetProviderSchema.Response()

            await GetProviderSchemaHandler(sample_request, context=None)

            mock_impl.assert_called_once_with(sample_request, None)
