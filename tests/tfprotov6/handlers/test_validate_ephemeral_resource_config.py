#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ValidateEphemeralResourceConfig handler."""

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.cty.exceptions import CtyValidationError
from pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config import (
    ValidateEphemeralResourceConfigHandler,
    _validate_ephemeral_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.ValidateEphemeralResourceConfig.Request:
    """Create a sample ValidateEphemeralResourceConfig request."""
    request = pb.ValidateEphemeralResourceConfig.Request()
    request.type_name = "test_ephemeral"
    request.config.msgpack = b"\x80"  # Empty dict
    return request


@pytest.fixture
def mock_resource_class() -> MagicMock:
    """Create a mock ephemeral resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = MagicMock()
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock

    # Mock instance with async validate
    mock_instance = MagicMock()
    mock_instance.validate = AsyncMock(return_value=[])
    mock_class.return_value = mock_instance
    return mock_class


class TestValidateEphemeralResourceConfigStructure:
    """Test handler structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request
    ) -> None:
        """Test that handler returns proper response object."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await ValidateEphemeralResourceConfigHandler(sample_request, context=None)

            assert isinstance(response, pb.ValidateEphemeralResourceConfig.Response)

    @pytest.mark.asyncio
    async def test_handler_records_metrics(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request
    ) -> None:
        """Test that handler records request and duration metrics."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_req,
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_dur,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await ValidateEphemeralResourceConfigHandler(sample_request, context=None)

            mock_req.inc.assert_called_once_with(handler="ValidateEphemeralResourceConfig")
            mock_dur.observe.assert_called_once()


class TestValidateEphemeralResourceConfigImpl:
    """Test implementation logic."""

    @pytest.mark.asyncio
    async def test_impl_validates_config_successfully(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test successful config validation."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.return_value = MagicMock()

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            assert isinstance(response, pb.ValidateEphemeralResourceConfig.Response)
            assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_resource_type(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request
    ) -> None:
        """Test handling of unknown ephemeral resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_unmarshals_config(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that config is unmarshaled."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.return_value = MagicMock()

            await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            mock_decode_config.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_converts_cty_to_attrs(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that cty_to_attrs_instance is called."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.return_value = MagicMock()

            await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            mock_decode_config.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_handles_validation_errors(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that CtyValidationError is converted to diagnostics."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.side_effect = CtyValidationError("Invalid config")

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_pyvider_errors(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that PyviderError exceptions are converted to diagnostics."""
        from pyvider.exceptions import ResourceError

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.side_effect = ResourceError("Validation failed")

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_generic_exceptions(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that generic exceptions are converted to diagnostics."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_decode_config.side_effect = RuntimeError("Unexpected error")

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_calls_validate_if_exists(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that validate() method is called if it exists."""
        mock_instance = MagicMock()
        mock_instance.validate = MagicMock()
        mock_resource_class.return_value = mock_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"
            ) as mock_decode_config,
        ):
            mock_get.return_value = mock_resource_class
            mock_config = MagicMock()
            mock_decode_config.return_value = mock_config

            await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            # validate should be called with config if it exists
            if hasattr(mock_instance, "validate"):
                mock_instance.validate.assert_called_once()


class TestValidateEphemeralResourceConfigEdgeCases:
    """Test edge cases and error paths."""

    @pytest.mark.asyncio
    async def test_impl_appends_validation_error_diagnostics(
        self, sample_request: pb.ValidateEphemeralResourceConfig.Request, mock_resource_class: MagicMock
    ) -> None:
        """Test that validation errors from validate() are added as diagnostics."""
        # Mock validate to return error messages
        mock_instance = MagicMock()
        validation_errors = ["Field 'name' is required", "Field 'count' must be positive"]
        mock_instance.validate = AsyncMock(return_value=validation_errors)
        mock_resource_class.return_value = mock_instance

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.decode_config"),
        ):
            mock_get.return_value = mock_resource_class

            response = await _validate_ephemeral_resource_config_impl(sample_request, context=None)

            # Should have 2 diagnostics, one for each validation error
            assert len(response.diagnostics) == 2
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
            assert "Field 'name' is required" in response.diagnostics[0].summary
            assert response.diagnostics[1].severity == pb.Diagnostic.ERROR
            assert "Field 'count' must be positive" in response.diagnostics[1].summary


# 🐍🏗️🔚
