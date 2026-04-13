#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema schema computation."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    _compute_schema_once,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestComputeSchemaOnce:
    """Tests for schema computation."""

    @pytest.mark.asyncio
    async def test_computes_schema_successfully(self, mock_provider_instance: MagicMock) -> None:
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
    async def test_handles_computation_error(self, mock_provider_instance: MagicMock) -> None:
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
