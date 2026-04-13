#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetProviderSchema schema collection functions."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    _collect_data_source_schemas,
    _collect_function_schemas,
    _collect_resource_schemas,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestCollectResourceSchemas:
    """Tests for resource schema collection."""

    @pytest.mark.asyncio
    async def test_collects_resource_schemas_successfully(self, mock_resource_class: MagicMock) -> None:
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
