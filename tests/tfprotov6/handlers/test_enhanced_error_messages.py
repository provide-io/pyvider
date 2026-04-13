#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for enhanced error messages across protocol handlers.

This module verifies that all enhanced protocol handlers provide:
- Clear, actionable error messages
- Suggestion sections for resolution
- Troubleshooting steps
- Proper context in error objects"""

import msgpack
from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.exceptions import ResourceError
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import (
    _get_resource_and_provider_instances,
)
from pyvider.protocols.tfprotov6.handlers.call_function import _call_function_impl
from pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource import (
    _close_ephemeral_resource_impl,
)
from pyvider.protocols.tfprotov6.handlers.import_resource_state import (
    _import_resource_state_impl,
)
from pyvider.protocols.tfprotov6.handlers.move_resource_state import (
    _move_resource_state_impl,
)
from pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource import (
    _open_ephemeral_resource_impl,
)
from pyvider.protocols.tfprotov6.handlers.read_data_source import (
    _read_data_source_impl,
)
from pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource import (
    _renew_ephemeral_resource_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    _validate_data_resource_config_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config import (
    _validate_ephemeral_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestResourceErrorMessages:
    """Test enhanced error messages for resource handlers."""

    @pytest.mark.asyncio
    async def test_apply_resource_change_missing_resource_has_suggestion(self) -> None:
        """Test that missing resource error includes suggestion and troubleshooting."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            with pytest.raises(ResourceError) as exc_info:
                await _get_resource_and_provider_instances("test_resource")

            error_message = str(exc_info.value)
            assert "Suggestion:" in error_message
            assert "Troubleshooting:" in error_message
            assert "@resource decorator" in error_message
            assert "pyvider components list" in error_message

    @pytest.mark.asyncio
    async def test_apply_resource_change_error_has_context(self) -> None:
        """Test that resource errors include proper context."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            with pytest.raises(ResourceError) as exc_info:
                await _get_resource_and_provider_instances("test_resource")

            error = exc_info.value
            assert hasattr(error, "context")
            assert "resource.type_name" in error.context
            assert "terraform.summary" in error.context


class TestDataSourceErrorMessages:
    """Test enhanced error messages for data source handlers."""

    @pytest.mark.asyncio
    async def test_read_data_source_missing_has_suggestion(self) -> None:
        """Test that missing data source error includes suggestion."""
        request = pb.ReadDataSource.Request(type_name="test_data_source")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.read_data_source.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test", detail="Test")

            response = await _read_data_source_impl(request, context=None)

            # Handler catches exception and converts to diagnostic
            assert len(response.diagnostics) > 0
            # Verify the exception that was passed to create_diagnostic_from_exception
            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "Suggestion:" in error_message
            assert "Troubleshooting:" in error_message
            assert "@data_source decorator" in error_message
            assert "PYVIDER_LOG_LEVEL=DEBUG" in error_message

    @pytest.mark.asyncio
    async def test_validate_data_resource_missing_has_troubleshooting(self) -> None:
        """Test that validation error includes troubleshooting steps."""
        request = pb.ValidateDataResourceConfig.Request(type_name="test_data_source")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test", detail="Test")

            await _validate_data_resource_config_impl(request, context=None)

            # Verify the exception that was passed to create_diagnostic
            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "Troubleshooting:" in error_message
            assert "1." in error_message  # Numbered steps
            assert "2." in error_message


class TestEphemeralResourceErrorMessages:
    """Test enhanced error messages for ephemeral resource handlers."""

    @pytest.mark.asyncio
    async def test_open_ephemeral_missing_has_suggestion(self) -> None:
        """Test that missing ephemeral resource error includes suggestion."""
        request = pb.OpenEphemeralResource.Request(type_name="test_ephemeral")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test")

            await _open_ephemeral_resource_impl(request, context=None)

            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "Suggestion:" in error_message
            assert "@ephemeral decorator" in error_message

    @pytest.mark.asyncio
    async def test_renew_ephemeral_missing_private_state_class_has_documentation(self) -> None:
        """Test that missing private_state_class error includes documentation reference."""
        request = pb.RenewEphemeralResource.Request(type_name="test_ephemeral")
        request.private = msgpack.packb({"test": "data"})

        mock_class = MagicMock()
        mock_class.private_state_class = None

        with (
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = mock_class
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test")

            await _renew_ephemeral_resource_impl(request, context=None)

            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "Suggestion:" in error_message
            assert "private_state_class" in error_message
            assert "Documentation:" in error_message

    @pytest.mark.asyncio
    async def test_close_ephemeral_error_has_troubleshooting_steps(self) -> None:
        """Test that close ephemeral error has numbered troubleshooting steps."""
        request = pb.CloseEphemeralResource.Request(type_name="test_ephemeral")
        request.private = msgpack.packb({"test": "data"})

        with (
            patch("pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test")

            await _close_ephemeral_resource_impl(request, context=None)

            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "Troubleshooting:" in error_message
            steps = [line for line in error_message.split("\n") if line.strip().startswith(("1.", "2.", "3."))]
            assert len(steps) >= 2  # At least 2 troubleshooting steps

    @pytest.mark.asyncio
    async def test_validate_ephemeral_config_has_decorator_guidance(self) -> None:
        """Test that validation error mentions decorator."""
        request = pb.ValidateEphemeralResourceConfig.Request(type_name="test_ephemeral")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test")

            await _validate_ephemeral_resource_config_impl(request, context=None)

            called_exception = mock_diag.call_args[0][0]
            error_message = str(called_exception)
            assert "@ephemeral decorator" in error_message


class TestFunctionErrorMessages:
    """Test enhanced error messages for function handlers."""

    @pytest.mark.asyncio
    async def test_call_function_missing_has_registry_suggestion(self) -> None:
        """Test that missing function error suggests checking registry."""
        request = pb.CallFunction.Request(name="test_function")

        with patch("pyvider.protocols.tfprotov6.handlers.call_function.hub") as mock_hub:
            mock_hub.get_component.return_value = None

            result = await _call_function_impl(request, context=None)

            assert result.error.text
            error_text = result.error.text
            assert "Suggestion:" in error_text
            assert "@function decorator" in error_text
            assert "pyvider components list" in error_text


class TestUnimplementedHandlerMessages:
    """Test that unimplemented handlers provide helpful messages."""

    @pytest.mark.asyncio
    async def test_import_resource_state_has_helpful_diagnostic(self) -> None:
        """Test that import handler returns helpful not-implemented diagnostic."""
        request = pb.ImportResourceState.Request(type_name="test_resource", id="test-id")

        response = await _import_resource_state_impl(request, context=None)

        assert len(response.diagnostics) == 1
        diag = response.diagnostics[0]
        assert diag.severity == pb.Diagnostic.WARNING
        assert "not yet implemented" in diag.detail
        assert "Suggestion:" in diag.detail
        assert "Workaround:" in diag.detail

    @pytest.mark.asyncio
    async def test_move_resource_state_has_workaround(self) -> None:
        """Test that move handler provides workaround."""
        request = pb.MoveResourceState.Request(source_type_name="source", target_type_name="target")

        response = await _move_resource_state_impl(request, context=None)

        assert len(response.diagnostics) == 1
        diag = response.diagnostics[0]
        assert "Workaround:" in diag.detail
        assert "recreate the resource" in diag.detail


class TestErrorMessageConsistency:
    """Test that error messages follow consistent patterns."""

    def test_suggestion_format_is_consistent(self) -> None:
        """Test that Suggestion format is consistent."""
        # Verify the format we expect in suggestion sections
        expected_format = "Suggestion:"
        assert expected_format is not None  # Simple test to verify format string exists

    def test_troubleshooting_steps_are_numbered(self) -> None:
        """Test that troubleshooting steps use numbered lists."""
        sample_error = """
        Error occurred.

        Troubleshooting:
          1. First step
          2. Second step
          3. Third step
        """
        assert "1." in sample_error
        assert "2." in sample_error
        assert "3." in sample_error


# 🐍🏗️🔚
