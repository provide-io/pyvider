"""Tests for ValidateDataResourceConfig handler."""

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.cty import CtyObject, CtyString
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    ValidateDataResourceConfigHandler,
    _validate_data_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request():
    """Create a sample ValidateDataResourceConfig request."""
    request = pb.ValidateDataResourceConfig.Request()
    request.type_name = "test_data_source"
    # Add empty config
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


class TestValidateDataResourceConfigHandlerStructure:
    """Tests for ValidateDataResourceConfig handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request):
        """Test that handler returns ValidateDataResourceConfig.Response."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger"):
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                mock_hub.get_component.return_value = None

                response = await ValidateDataResourceConfigHandler(sample_request, context=None)

                assert isinstance(response, pb.ValidateDataResourceConfig.Response)

    @pytest.mark.asyncio
    async def test_handler_calls_implementation(self, sample_request):
        """Test that handler delegates to implementation."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config._validate_data_resource_config_impl"
        ) as mock_impl:
            mock_impl.return_value = pb.ValidateDataResourceConfig.Response()

            await ValidateDataResourceConfigHandler(sample_request, context=None)

            mock_impl.assert_called_once_with(sample_request, None)


class TestValidateDataResourceConfigImpl:
    """Tests for ValidateDataResourceConfig implementation."""

    @pytest.mark.asyncio
    async def test_impl_validates_config_successfully(self, sample_request, mock_data_source_class):
        """Test successful config validation."""
        mock_instance = AsyncMock()
        mock_instance.validate.return_value = []  # No validation errors
        mock_data_source_class.return_value = mock_instance

        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
            ) as mock_unmarshal:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.cty_to_attrs_instance"
                ) as mock_cty_to_attrs:
                    mock_hub.get_component.return_value = mock_data_source_class
                    mock_unmarshal.return_value = MagicMock()
                    mock_cty_to_attrs.return_value = MagicMock()

                    response = await _validate_data_resource_config_impl(sample_request, context=None)

                    assert isinstance(response, pb.ValidateDataResourceConfig.Response)
                    assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_returns_validation_errors(self, sample_request, mock_data_source_class):
        """Test that validation errors are returned as diagnostics."""
        mock_instance = AsyncMock()
        mock_instance.validate.return_value = ["Error 1", "Error 2"]
        mock_data_source_class.return_value = mock_instance

        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
            ) as mock_unmarshal:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.cty_to_attrs_instance"
                ) as mock_cty_to_attrs:
                    mock_hub.get_component.return_value = mock_data_source_class
                    mock_unmarshal.return_value = MagicMock()
                    mock_cty_to_attrs.return_value = MagicMock()

                    response = await _validate_data_resource_config_impl(sample_request, context=None)

                    assert len(response.diagnostics) == 2
                    assert response.diagnostics[0].summary == "Error 1"
                    assert response.diagnostics[1].summary == "Error 2"
                    assert all(d.severity == pb.Diagnostic.ERROR for d in response.diagnostics)

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_data_source(self, sample_request):
        """Test handling of unknown data source type."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger"):
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                ) as mock_create_diag:
                    mock_hub.get_component.return_value = None
                    mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Not found")
                    mock_create_diag.return_value = mock_diag

                    response = await _validate_data_resource_config_impl(sample_request, context=None)

                    assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_impl_handles_cty_validation_error(self, sample_request, mock_data_source_class):
        """Test handling of CTY validation errors."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
            ) as mock_unmarshal:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                ) as mock_create_diag:
                    mock_hub.get_component.return_value = mock_data_source_class
                    mock_unmarshal.side_effect = CtyValidationError("Invalid type")
                    mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Invalid type")
                    mock_create_diag.return_value = mock_diag

                    response = await _validate_data_resource_config_impl(sample_request, context=None)

                    assert len(response.diagnostics) == 1
                    mock_create_diag.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_handles_pyvider_error(self, sample_request, mock_data_source_class):
        """Test handling of PyviderError exceptions."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
            ) as mock_unmarshal:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                ) as mock_create_diag:
                    mock_hub.get_component.return_value = mock_data_source_class
                    mock_unmarshal.side_effect = PyviderError("Pyvider error")
                    mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Pyvider error")
                    mock_create_diag.return_value = mock_diag

                    response = await _validate_data_resource_config_impl(sample_request, context=None)

                    assert len(response.diagnostics) == 1

    @pytest.mark.asyncio
    async def test_impl_handles_generic_exception(self, sample_request, mock_data_source_class):
        """Test handling of generic exceptions."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
            ) as mock_unmarshal:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                ) as mock_create_diag:
                    with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger"):
                        mock_hub.get_component.return_value = mock_data_source_class
                        mock_unmarshal.side_effect = RuntimeError("Unexpected error")
                        mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Unexpected error")
                        mock_create_diag.return_value = mock_diag

                        response = await _validate_data_resource_config_impl(sample_request, context=None)

                        assert len(response.diagnostics) == 1


class TestValidateDataResourceConfigMetrics:
    """Tests for ValidateDataResourceConfig metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request):
        """Test that handler increments request counter."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.handler_requests"
        ) as mock_requests:
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                mock_hub.get_component.return_value = None

                await ValidateDataResourceConfigHandler(sample_request, context=None)

                mock_requests.inc.assert_called_once_with(handler="ValidateDataResourceConfig")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(self, sample_request):
        """Test that handler records duration metric."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.handler_duration"
        ) as mock_duration:
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                mock_hub.get_component.return_value = None

                await ValidateDataResourceConfigHandler(sample_request, context=None)

                assert mock_duration.observe.called
                call_args = mock_duration.observe.call_args
                assert call_args[1]["handler"] == "ValidateDataResourceConfig"
                assert call_args[0][0] >= 0

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(self, sample_request):
        """Test that handler increments error counter on failure."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.handler_errors"
        ) as mock_errors:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config._validate_data_resource_config_impl"
            ) as mock_impl:
                mock_impl.side_effect = RuntimeError("Test error")

                with pytest.raises(RuntimeError):
                    await ValidateDataResourceConfigHandler(sample_request, context=None)

                mock_errors.inc.assert_called_once_with(handler="ValidateDataResourceConfig")


class TestValidateDataResourceConfigLogging:
    """Tests for ValidateDataResourceConfig logging behavior."""

    @pytest.mark.asyncio
    async def test_impl_logs_unhandled_errors(self, sample_request, mock_data_source_class):
        """Test that unhandled errors are logged."""
        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger") as mock_logger:
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.unmarshal"
                ) as mock_unmarshal:
                    with patch(
                        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                    ) as mock_create_diag:
                        mock_hub.get_component.return_value = mock_data_source_class
                        mock_unmarshal.side_effect = RuntimeError("Test error")
                        mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test error")
                        mock_create_diag.return_value = mock_diag

                        await _validate_data_resource_config_impl(sample_request, context=None)

                        mock_logger.error.assert_called_once()
                        assert "Unhandled error" in str(mock_logger.error.call_args)


class TestValidateDataResourceConfigEdgeCases:
    """Edge case tests for ValidateDataResourceConfig handler."""

    @pytest.mark.asyncio
    async def test_empty_type_name(self):
        """Test handling of empty type name."""
        request = pb.ValidateDataResourceConfig.Request()
        request.type_name = ""
        request.config.msgpack = b""

        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger"):
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                with patch(
                    "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
                ) as mock_create_diag:
                    mock_hub.get_component.return_value = None
                    mock_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Not found")
                    mock_create_diag.return_value = mock_diag

                    response = await _validate_data_resource_config_impl(request, context=None)

                    assert isinstance(response, pb.ValidateDataResourceConfig.Response)
                    assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_with_context_object(self, sample_request):
        """Test handler with non-None context."""
        context = MagicMock()

        with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger"):
            with patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub:
                mock_hub.get_component.return_value = None

                response = await ValidateDataResourceConfigHandler(sample_request, context=context)

                assert isinstance(response, pb.ValidateDataResourceConfig.Response)
