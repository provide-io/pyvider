#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ValidateProviderConfig handler."""

from unittest.mock import MagicMock

from provide.testkit.mocking import patch
import pytest

from pyvider.protocols.tfprotov6.handlers.validate_provider_config import (
    ValidateProviderConfigHandler,
    _validate_provider_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.ValidateProviderConfig.Request:
    """Create sample ValidateProviderConfig request."""
    return pb.ValidateProviderConfig.Request()


class TestValidateProviderConfigStructure:
    """Test handler structure and basic functionality."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test handler returns correct response type."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)

    @pytest.mark.asyncio
    async def test_handler_returns_empty_diagnostics_on_success(
        self, sample_request: pb.ValidateProviderConfig.Request
    ) -> None:
        """Test handler returns empty diagnostics when validation passes."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert len(response.diagnostics) == 0


class TestValidateProviderConfigImplementation:
    """Test handler implementation details."""

    @pytest.mark.asyncio
    async def test_impl_successful_validation(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test successful validation returns empty diagnostics."""
        response = await _validate_provider_config_impl(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)
        assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_exception(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test implementation handles exceptions gracefully."""
        # Create a mock request that raises an exception when bool() is called on msgpack
        bad_request = MagicMock()
        bad_request.config.msgpack.__bool__ = MagicMock(side_effect=RuntimeError("Test error"))

        response = await _validate_provider_config_impl(bad_request, context=None)

        # Should return response with error diagnostic
        assert len(response.diagnostics) == 1
        assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
        assert "Provider configuration validation failed" in response.diagnostics[0].summary


class TestValidateProviderConfigMetrics:
    """Test metrics recording."""

    @pytest.mark.asyncio
    async def test_records_request_metric(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test request counter incremented."""
        with patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests:
            await ValidateProviderConfigHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="ValidateProviderConfig")

    @pytest.mark.asyncio
    async def test_records_duration_metric(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test duration observer called."""
        with patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration:
            await ValidateProviderConfigHandler(sample_request, context=None)

            assert mock_duration.observe.call_count == 1
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "ValidateProviderConfig"

    @pytest.mark.asyncio
    async def test_records_error_metric_on_exception(
        self, sample_request: pb.ValidateProviderConfig.Request
    ) -> None:
        """Test error counter incremented on exception."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_provider_config._validate_provider_config_impl"
            ) as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await ValidateProviderConfigHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="ValidateProviderConfig")


class TestValidateProviderConfigTestModeDetection:
    """Test test mode detection and logging."""

    @pytest.mark.asyncio
    async def test_detects_test_mode_enabled(self) -> None:
        """Test that test mode enabled is detected and logged."""
        from pyvider.cty import CtyBool, CtyObject, CtyValue

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.unmarshal") as mock_unmarshal,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.logger") as mock_logger,
        ):
            mock_provider = MagicMock()
            mock_schema = MagicMock()

            mock_schema.block = CtyObject(attribute_types={"pyvider_testmode": CtyBool()})
            mock_provider.schema = mock_schema

            # Create a config class that will have pyvider_testmode = True
            mock_config_class = MagicMock()
            mock_config_instance = MagicMock()
            mock_config_instance.pyvider_testmode = True
            mock_config_class.return_value = mock_config_instance
            mock_provider.config_class = mock_config_class

            mock_hub.get_component.return_value = mock_provider

            # Mock unmarshal to return a non-unknown value
            mock_cty_value = CtyValue(True, CtyBool())
            mock_unmarshal.return_value = mock_cty_value

            # Create request with config
            request = pb.ValidateProviderConfig.Request()
            request.config.msgpack = b"\xc3"  # True in msgpack

            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_provider_config.BaseResource.from_cty"
            ) as mock_from_cty:
                mock_from_cty.return_value = mock_config_instance

                response = await _validate_provider_config_impl(request, context=None)

                # Should log warning about test mode
                assert any("test mode ENABLED" in str(call) for call in mock_logger.warning.call_args_list)
                assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_detects_test_mode_disabled(self) -> None:
        """Test that test mode disabled is detected and logged."""
        from pyvider.cty import CtyBool, CtyObject, CtyValue

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.unmarshal") as mock_unmarshal,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.logger") as mock_logger,
        ):
            mock_provider = MagicMock()
            mock_schema = MagicMock()
            mock_schema.block = CtyObject(attribute_types={"pyvider_testmode": CtyBool()})
            mock_provider.schema = mock_schema

            mock_config_class = MagicMock()
            mock_config_instance = MagicMock()
            mock_config_instance.pyvider_testmode = False
            mock_config_class.return_value = mock_config_instance
            mock_provider.config_class = mock_config_class

            mock_hub.get_component.return_value = mock_provider

            mock_cty_value = CtyValue(False, CtyBool())
            mock_unmarshal.return_value = mock_cty_value

            request = pb.ValidateProviderConfig.Request()
            request.config.msgpack = b"\xc2"  # False in msgpack

            with patch(
                "pyvider.protocols.tfprotov6.handlers.validate_provider_config.BaseResource.from_cty"
            ) as mock_from_cty:
                mock_from_cty.return_value = mock_config_instance

                response = await _validate_provider_config_impl(request, context=None)

                # Should log debug about test mode NOT enabled
                assert any("test mode NOT enabled" in str(call) for call in mock_logger.debug.call_args_list)
                assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_handles_config_parsing_error_gracefully(self) -> None:
        """Test that config parsing errors don't fail validation."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.unmarshal") as mock_unmarshal,
            patch("pyvider.protocols.tfprotov6.handlers.validate_provider_config.logger") as mock_logger,
        ):
            mock_provider = MagicMock()
            mock_hub.get_component.return_value = mock_provider

            # Make unmarshal raise an exception
            mock_unmarshal.side_effect = ValueError("Invalid config format")

            request = pb.ValidateProviderConfig.Request()
            request.config.msgpack = b"\x00"

            response = await _validate_provider_config_impl(request, context=None)

            # Should log debug about parse error but still succeed
            assert any("Could not parse config" in str(call) for call in mock_logger.debug.call_args_list)
            assert len(response.diagnostics) == 0


class TestValidateProviderConfigEdgeCases:
    """Test edge cases."""

    @pytest.mark.asyncio
    async def test_with_none_context(self, sample_request: pb.ValidateProviderConfig.Request) -> None:
        """Test with None context."""
        response = await ValidateProviderConfigHandler(sample_request, context=None)

        assert isinstance(response, pb.ValidateProviderConfig.Response)


# 🐍🏗️🔚
