#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ReadDataSource handler."""

from typing import Any

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.cty import CtyObject, CtyString
from pyvider.cty.exceptions import CtyValidationError
from pyvider.protocols.tfprotov6.handlers.read_data_source import (
    ReadDataSourceHandler,
    _read_data_source_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@pytest.fixture
def sample_request() -> pb.ReadDataSource.Request:
    """Create a sample ReadDataSource request."""
    request = pb.ReadDataSource.Request()
    request.type_name = "test_data_source"
    request.config.msgpack = b""
    return request


@pytest.fixture
def mock_data_source_class() -> MagicMock:
    """Create a mock data source class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock
    mock_class._is_test_only = False
    return mock_class


class TestReadDataSourceHandlerStructure:
    """Tests for ReadDataSource handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.ReadDataSource.Request) -> None:
        """Test that handler returns ReadDataSource.Response."""
        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            mock_hub.get_component.return_value = None

            response = await ReadDataSourceHandler(sample_request, context=None)

            assert isinstance(response, pb.ReadDataSource.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self, sample_request: pb.ReadDataSource.Request) -> None:
        """Test that handler delegates to implementation."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.read_data_source._read_data_source_impl"
        ) as mock_impl:
            mock_impl.return_value = pb.ReadDataSource.Response()

            await ReadDataSourceHandler(sample_request, context=None)

            mock_impl.assert_called_once_with(sample_request, None)


class TestReadDataSourceImpl:
    """Tests for ReadDataSource implementation."""

    @pytest.mark.asyncio
    async def test_impl_reads_data_successfully(
        self, sample_request: pb.ReadDataSource.Request, mock_data_source_class: MagicMock
    ) -> None:
        """Test successful data source read."""
        mock_instance = AsyncMock()
        mock_instance.read.return_value = MagicMock(name="test_data")
        mock_data_source_class.return_value = mock_instance
        # Prevent capability injection by not having _parent_capability
        mock_data_source_class._parent_capability = None

        # Create a properly mocked schema with to_cty_type method
        mock_block = MagicMock()
        mock_block.to_cty_type.return_value = CtyObject(attribute_types={"name": CtyString()})
        mock_schema = MagicMock()
        mock_schema.block = mock_block
        mock_data_source_class.get_schema.return_value = mock_schema

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"
            ) as mock_cty_to_attrs,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.attrs_to_dict_for_cty"
            ) as mock_attrs_to_dict,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.marshal") as mock_marshal,
        ):
            mock_hub.get_component.return_value = mock_data_source_class
            mock_unmarshal.return_value = MagicMock()
            mock_cty_to_attrs.return_value = MagicMock()
            mock_attrs_to_dict.return_value = {"name": "test"}
            mock_marshal.return_value = MagicMock(msgpack=b"\x00")

            response = await _read_data_source_impl(sample_request, context=None)

            assert isinstance(response, pb.ReadDataSource.Response)
            assert len(response.diagnostics) == 0
            mock_instance.read.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_handles_none_result(
        self, sample_request: pb.ReadDataSource.Request, mock_data_source_class: MagicMock
    ) -> None:
        """Test handling of None return from data source."""
        mock_instance = AsyncMock()
        mock_instance.read.return_value = None
        mock_data_source_class.return_value = mock_instance
        # Prevent capability injection
        mock_data_source_class._parent_capability = None

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"),
        ):
            mock_hub.get_component.return_value = mock_data_source_class

            response = await _read_data_source_impl(sample_request, context=None)

            assert response.state.msgpack == b"\xc0"  # null msgpack

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_data_source(self, sample_request: pb.ReadDataSource.Request) -> None:
        """Test handling of unknown data source type."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.create_diagnostic_from_exception"
            ) as mock_create_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Not found")
            mock_create_diag.return_value = mock_diag

            response = await _read_data_source_impl(sample_request, context=None)

            assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_impl_handles_cty_validation_error(
        self, sample_request: pb.ReadDataSource.Request, mock_data_source_class: MagicMock
    ) -> None:
        """Test handling of CTY validation errors."""
        mock_instance = AsyncMock()
        mock_instance.read.return_value = MagicMock()
        mock_data_source_class.return_value = mock_instance

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.create_diagnostic_from_exception"
            ) as mock_create_diag,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"),
        ):
            mock_hub.get_component.return_value = mock_data_source_class
            mock_unmarshal.side_effect = CtyValidationError("Invalid type")
            mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Invalid type")
            mock_create_diag.return_value = mock_diag

            response = await _read_data_source_impl(sample_request, context=None)

            assert len(response.diagnostics) == 1


class TestReadDataSourceMetrics:
    """Tests for ReadDataSource metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request: pb.ReadDataSource.Request) -> None:
        """Test that handler increments request counter."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            await ReadDataSourceHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="ReadDataSource")

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(
        self, sample_request: pb.ReadDataSource.Request
    ) -> None:
        """Test that handler increments error counter on failure."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source._read_data_source_impl") as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await ReadDataSourceHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="ReadDataSource")


class TestReadDataSourceCapabilityInjection:
    """Tests for capability injection in data sources."""

    @pytest.mark.asyncio
    async def test_injects_capability_when_parent_capability_is_class(
        self, sample_request: pb.ReadDataSource.Request
    ) -> None:
        """Test that capability class is instantiated when _parent_capability is set."""
        from pyvider.cty import CtyString, CtyValue

        # Create a complete mock data source class with all required attributes
        mock_ds_class = MagicMock()
        mock_ds_class._parent_capability = "test_capability"
        mock_ds_class.config_class = MagicMock
        mock_ds_class._is_test_only = False

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
        mock_ds_class.get_schema.return_value = mock_schema

        # Create mock capability class (type, not instance)
        mock_capability_class = type("MockCapability", (), {})

        # Track if read was called
        read_called_with_kwargs = {}

        async def mock_read(ctx: ResourceContext, **kwargs: Any) -> None:
            read_called_with_kwargs.update(kwargs)

        mock_ds_instance = MagicMock()
        mock_ds_instance.read = mock_read
        mock_ds_class.return_value = mock_ds_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"
            ) as mock_cty_to_attrs,
        ):
            from pyvider.cty import CtyString, CtyValue

            # Configure mock_get to return appropriate values
            def get_component_side_effect(component_type: str, name: str) -> MagicMock | type | None:
                if component_type == "data_source" and name == "test_data_source":
                    return mock_ds_class
                elif component_type == "capability" and name == "test_capability":
                    return mock_capability_class
                return None

            mock_get.side_effect = get_component_side_effect
            mock_unmarshal.return_value = CtyValue.null(CtyString())
            mock_cty_to_attrs.return_value = None

            await _read_data_source_impl(sample_request, context=None)

            # Check that capability was injected
            assert "test_capability" in read_called_with_kwargs
            # Should have instantiated the class
            assert read_called_with_kwargs["test_capability"] is not None

    @pytest.mark.asyncio
    async def test_handles_capability_instance_directly(
        self, sample_request: pb.ReadDataSource.Request
    ) -> None:
        """Test that capability instance is used directly if not a class."""
        from pyvider.cty import CtyString, CtyValue

        # Create complete mock data source
        mock_ds_class = MagicMock()
        mock_ds_class._parent_capability = "test_capability"
        mock_ds_class.config_class = MagicMock
        mock_ds_class._is_test_only = False

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
        mock_ds_class.get_schema.return_value = mock_schema

        # Create an instance (not a class) - not a type
        mock_capability_instance = MagicMock()
        # Make it not a type
        type(mock_capability_instance).__name__ = "MockInstance"

        read_called_with_kwargs = {}

        async def mock_read(ctx: ResourceContext, **kwargs: Any) -> None:
            read_called_with_kwargs.update(kwargs)

        mock_ds_instance = MagicMock()
        mock_ds_instance.read = mock_read
        mock_ds_class.return_value = mock_ds_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"
            ) as mock_cty_to_attrs,
        ):
            mock_get.side_effect = lambda comp_type, name: {
                ("data_source", "test_data_source"): mock_ds_class,
                ("capability", "test_capability"): mock_capability_instance,
            }.get((comp_type, name))

            mock_unmarshal.return_value = CtyValue.null(CtyString())
            mock_cty_to_attrs.return_value = None

            await _read_data_source_impl(sample_request, context=None)

            # Check that capability instance was used directly
            assert "test_capability" in read_called_with_kwargs
            assert read_called_with_kwargs["test_capability"] is mock_capability_instance

    @pytest.mark.asyncio
    async def test_warns_when_capability_not_found(self, sample_request: pb.ReadDataSource.Request) -> None:
        """Test that warning is logged when capability not found."""
        from pyvider.cty import CtyString, CtyValue

        # Create complete mock
        mock_ds_class = MagicMock()
        mock_ds_class._parent_capability = "missing_capability"
        mock_ds_class.config_class = MagicMock
        mock_ds_class._is_test_only = False

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
        mock_ds_class.get_schema.return_value = mock_schema

        read_called_with_kwargs = {}

        async def mock_read(ctx: ResourceContext, **kwargs: Any) -> None:
            read_called_with_kwargs.update(kwargs)

        mock_ds_instance = MagicMock()
        mock_ds_instance.read = mock_read
        mock_ds_class.return_value = mock_ds_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"
            ) as mock_cty_to_attrs,
        ):
            mock_get.side_effect = lambda comp_type, name: {
                ("data_source", "test_data_source"): mock_ds_class,
                ("capability", "missing_capability"): None,
            }.get((comp_type, name))

            from pyvider.cty import CtyString, CtyValue

            mock_unmarshal.return_value = CtyValue.null(CtyString())
            mock_cty_to_attrs.return_value = None

            await _read_data_source_impl(sample_request, context=None)

            # Should still succeed, just without the capability
            assert "missing_capability" not in read_called_with_kwargs


class TestReadDataSourceContextDiagnostics:
    """Tests for context diagnostics handling."""

    @pytest.mark.asyncio
    async def test_appends_context_diagnostics_to_response(
        self, sample_request: pb.ReadDataSource.Request
    ) -> None:
        """Test that context diagnostics are appended to response."""
        from pyvider.cty import CtyString, CtyValue

        # Create complete mock
        mock_ds_class = MagicMock()
        mock_ds_class._parent_capability = None
        mock_ds_class.config_class = MagicMock
        mock_ds_class._is_test_only = False

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
        mock_ds_class.get_schema.return_value = mock_schema

        # Create a ResourceContext with diagnostics
        from pyvider.resources.context import ResourceContext

        resource_context_with_diags = ResourceContext(config=None)
        diag = pb.Diagnostic(severity=pb.Diagnostic.WARNING, summary="Context warning")
        resource_context_with_diags.diagnostics.append(diag)

        async def mock_read(ctx: ResourceContext) -> None:
            # Store diagnostic in context
            ctx.diagnostics.append(diag)

        mock_ds_instance = MagicMock()
        mock_ds_instance.read = mock_read
        mock_ds_class.return_value = mock_ds_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"
            ) as mock_cty_to_attrs,
        ):
            mock_get.return_value = mock_ds_class

            from pyvider.cty import CtyString, CtyValue

            mock_unmarshal.return_value = CtyValue.null(CtyString())
            mock_cty_to_attrs.return_value = None

            response = await _read_data_source_impl(sample_request, context=None)

            # Check that context diagnostic was added to response
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].summary == "Context warning"


# 🐍🏗️🔚
