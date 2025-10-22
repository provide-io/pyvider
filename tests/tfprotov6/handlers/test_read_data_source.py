"""Tests for ReadDataSource handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.handlers.read_data_source import (
    ReadDataSourceHandler,
    _read_data_source_impl,
)
from pyvider.cty import CtyString, CtyObject
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError


@pytest.fixture
def sample_request():
    """Create a sample ReadDataSource request."""
    request = pb.ReadDataSource.Request()
    request.type_name = "test_data_source"
    request.config.msgpack = b""
    return request


@pytest.fixture
def mock_data_source_class():
    """Create a mock data source class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock
    return mock_class


class TestReadDataSourceHandlerStructure:
    """Tests for ReadDataSource handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request):
        """Test that handler returns ReadDataSource.Response."""
        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            mock_hub.get_component.return_value = None

            response = await ReadDataSourceHandler(sample_request, context=None)

            assert isinstance(response, pb.ReadDataSource.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self, sample_request):
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
    async def test_impl_reads_data_successfully(self, sample_request, mock_data_source_class):
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

        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal:
                with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance") as mock_cty_to_attrs:
                    with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.attrs_to_dict_for_cty") as mock_attrs_to_dict:
                        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.marshal") as mock_marshal:
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
    async def test_impl_handles_none_result(self, sample_request, mock_data_source_class):
        """Test handling of None return from data source."""
        mock_instance = AsyncMock()
        mock_instance.read.return_value = None
        mock_data_source_class.return_value = mock_instance
        # Prevent capability injection
        mock_data_source_class._parent_capability = None

        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal"):
                with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"):
                    mock_hub.get_component.return_value = mock_data_source_class

                    response = await _read_data_source_impl(sample_request, context=None)

                    assert response.state.msgpack == b"\xc0"  # null msgpack

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_data_source(self, sample_request):
        """Test handling of unknown data source type."""
        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.create_diagnostic_from_exception") as mock_create_diag:
                mock_hub.get_component.return_value = None
                mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Not found")
                mock_create_diag.return_value = mock_diag

                response = await _read_data_source_impl(sample_request, context=None)

                assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_impl_handles_cty_validation_error(self, sample_request, mock_data_source_class):
        """Test handling of CTY validation errors."""
        mock_instance = AsyncMock()
        mock_instance.read.return_value = MagicMock()
        mock_data_source_class.return_value = mock_instance

        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
            with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.unmarshal") as mock_unmarshal:
                with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.create_diagnostic_from_exception") as mock_create_diag:
                    with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.cty_to_attrs_instance"):
                        mock_hub.get_component.return_value = mock_data_source_class
                        mock_unmarshal.side_effect = CtyValidationError("Invalid type")
                        mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Invalid type")
                        mock_create_diag.return_value = mock_diag

                        response = await _read_data_source_impl(sample_request, context=None)

                        assert len(response.diagnostics) == 1


class TestReadDataSourceMetrics:
    """Tests for ReadDataSource metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request):
        """Test that handler increments request counter."""
        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.handler_requests") as mock_requests:
            with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub:
                mock_hub.get_component.return_value = None

                await ReadDataSourceHandler(sample_request, context=None)

                mock_requests.inc.assert_called_once_with(handler="ReadDataSource")

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(self, sample_request):
        """Test that handler increments error counter on failure."""
        with patch("pyvider.protocols.tfprotov6.handlers.read_data_source.handler_errors") as mock_errors:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source._read_data_source_impl"
            ) as mock_impl:
                mock_impl.side_effect = RuntimeError("Test error")

                with pytest.raises(RuntimeError):
                    await ReadDataSourceHandler(sample_request, context=None)

                mock_errors.inc.assert_called_once_with(handler="ReadDataSource")
