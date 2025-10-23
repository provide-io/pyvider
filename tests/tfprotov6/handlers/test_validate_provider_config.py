"""Tests for ValidateProviderConfig handler."""

from provide.testkit.mocking import patch
import pytest

from pyvider.protocols.tfprotov6.handlers.validate_provider_config import (
    ValidateProviderConfigHandler,
    _validate_provider_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request():
    """Create sample ValidateProviderConfig request."""
    return pb.ValidateProviderConfig.Request()


class TestValidateProviderConfigStructure:
    """Test handler structure and basic functionality."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request):
        """Test handler returns correct response type."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)

    @pytest.mark.asyncio
    async def test_handler_returns_empty_diagnostics_on_success(self, sample_request):
        """Test handler returns empty diagnostics when validation passes."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert len(response.diagnostics) == 0


class TestValidateProviderConfigImplementation:
    """Test handler implementation details."""

    @pytest.mark.asyncio
    async def test_impl_successful_validation(self, sample_request):
        """Test successful validation returns empty diagnostics."""
        response = await _validate_provider_config_impl(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)
        assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_exception(self, sample_request):
        """Test implementation handles exceptions gracefully."""
        # Patch logger.trace to raise an exception
        with patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.logger") as mock_logger:
            mock_logger.trace.side_effect = RuntimeError("Test error")

            response = await _validate_provider_config_impl(sample_request, context=None)

            # Should return response with error diagnostic
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
            assert "Provider configuration validation failed" in response.diagnostics[0].summary


class TestValidateProviderConfigMetrics:
    """Test metrics recording."""

    @pytest.mark.asyncio
    async def test_records_request_metric(self, sample_request):
        """Test request counter incremented."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_provider_config.handler_requests"
        ) as mock_requests:
            await ValidateProviderConfigHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="ValidateProviderConfig")

    @pytest.mark.asyncio
    async def test_records_duration_metric(self, sample_request):
        """Test duration observer called."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_provider_config.handler_duration"
        ) as mock_duration:
            await ValidateProviderConfigHandler(sample_request, context=None)

            assert mock_duration.observe.call_count == 1
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "ValidateProviderConfig"

    @pytest.mark.asyncio
    async def test_records_error_metric_on_exception(self, sample_request):
        """Test error counter incremented on exception."""
        with patch(
            "pyvider.protocols.tfprotov6.handlers.validate_provider_config.handler_errors"
        ) as mock_errors:
            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_provider_config._validate_provider_config_impl"
            ) as mock_impl:
                mock_impl.side_effect = RuntimeError("Test error")

                with pytest.raises(RuntimeError):
                    await ValidateProviderConfigHandler(sample_request, context=None)

                mock_errors.inc.assert_called_once_with(handler="ValidateProviderConfig")


class TestValidateProviderConfigEdgeCases:
    """Test edge cases."""

    @pytest.mark.asyncio
    async def test_with_none_context(self, sample_request):
        """Test with None context."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)
