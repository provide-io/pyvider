#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for structured logging across protocol handlers.

This module verifies that all enhanced protocol handlers use consistent,
structured logging with:
- operation field in all log statements
- Appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Relevant contextual information
- Success and failure tracking"""

import contextlib

import msgpack
from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

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
from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import (
    _upgrade_resource_state_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    _validate_data_resource_config_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config import (
    _validate_ephemeral_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import a_str, s_resource


def _upgradable_resource() -> MagicMock:
    """UpgradeResourceState resolves the resource to learn the version to compare against.

    Registered at version 0 to match the requests below, so these exercise the
    pass-through rather than an upgrade.
    """
    resource = MagicMock()
    resource.get_schema.return_value = s_resource(attributes={"name": a_str(optional=True)}, version=0)
    return resource


class TestOperationFieldPresence:
    """Test that all handlers include 'operation' field in logs."""

    @pytest.mark.asyncio
    async def test_read_data_source_logs_with_operation(self) -> None:
        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None
            request = pb.ReadDataSource.Request(type_name="test_ds")
            request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

            with contextlib.suppress(Exception):
                await _read_data_source_impl(request, context=None)

            # Check that debug was called with operation field
            assert mock_logger.debug.called
            call_kwargs = mock_logger.debug.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "read_data_source"

    @pytest.mark.asyncio
    async def test_validate_data_resource_logs_with_operation(self) -> None:
        request = pb.ValidateDataResourceConfig.Request(type_name="test_ds")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _validate_data_resource_config_impl(request, context=None)

            assert mock_logger.debug.called
            call_kwargs = mock_logger.debug.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "validate_data_resource_config"

    @pytest.mark.asyncio
    async def test_open_ephemeral_logs_with_operation(self) -> None:
        """Test open_ephemeral_resource includes operation field."""
        request = pb.OpenEphemeralResource.Request(type_name="test_eph")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.hub"),
        ):
            with contextlib.suppress(Exception):
                await _open_ephemeral_resource_impl(request, context=None)

            assert mock_logger.debug.called
            call_kwargs = mock_logger.debug.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "open_ephemeral_resource"

    @pytest.mark.asyncio
    async def test_upgrade_resource_state_logs_with_operation(self) -> None:
        """Test upgrade_resource_state includes operation field."""
        request = pb.UpgradeResourceState.Request(type_name="test_resource", version=0)
        request.raw_state.CopyFrom(pb.RawState(json=b"{}"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.logger") as mock_logger,
            patch(
                "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.hub.get_component",
                return_value=_upgradable_resource(),
            ),
        ):
            await _upgrade_resource_state_impl(request, context=None)

            assert mock_logger.debug.called
            call_kwargs = mock_logger.debug.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "upgrade_resource_state"


class TestErrorLogging:
    """Test that handlers log errors with proper structured data."""

    @pytest.mark.asyncio
    async def test_read_data_source_logs_error_with_context(self) -> None:
        """Test that read_data_source logs errors with error_type and error_message."""
        request = pb.ReadDataSource.Request(type_name="test_ds")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _read_data_source_impl(request, context=None)

            # Should have logged an error
            assert mock_logger.error.called
            call_kwargs = mock_logger.error.call_args[1]
            assert "operation" in call_kwargs
            assert "error_type" in call_kwargs
            assert "data_source_type" in call_kwargs

    @pytest.mark.asyncio
    async def test_validate_ephemeral_logs_error_with_type(self) -> None:
        """Test that validate_ephemeral logs errors with error_type."""
        request = pb.ValidateEphemeralResourceConfig.Request(type_name="test_eph")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch(
                "pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.logger"
            ) as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _validate_ephemeral_resource_config_impl(request, context=None)

            assert mock_logger.error.called
            call_kwargs = mock_logger.error.call_args[1]
            assert "error_type" in call_kwargs
            assert "resource_type" in call_kwargs


class TestSuccessLogging:
    """Test that handlers log successful operations."""

    @pytest.mark.asyncio
    async def test_close_ephemeral_logs_success(self) -> None:
        """Test that close_ephemeral logs successful completion."""
        request = pb.CloseEphemeralResource.Request(type_name="test_eph")
        private_data = {"test": "data"}
        request.private = msgpack.packb(private_data)

        mock_class = MagicMock()
        mock_class.private_state_class = MagicMock
        mock_instance = AsyncMock()
        mock_instance.close = AsyncMock()
        mock_class.return_value = mock_instance

        with (
            patch("pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = mock_class

            await _close_ephemeral_resource_impl(request, context=None)

            # Should log success with INFO level
            assert mock_logger.info.called
            call_kwargs = mock_logger.info.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "close_ephemeral_resource"

    @pytest.mark.asyncio
    async def test_upgrade_resource_state_logs_success(self) -> None:
        """Test that upgrade_resource_state logs successful completion."""
        request = pb.UpgradeResourceState.Request(type_name="test_resource", version=0)
        request.raw_state.CopyFrom(pb.RawState(json=b"{}"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.logger") as mock_logger,
            patch(
                "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.hub.get_component",
                return_value=_upgradable_resource(),
            ),
        ):
            await _upgrade_resource_state_impl(request, context=None)

            # Should log info on success
            assert mock_logger.info.called
            call_kwargs = mock_logger.info.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "upgrade_resource_state"


class TestWarningLogging:
    """Test that handlers log warnings appropriately."""

    @pytest.mark.asyncio
    async def test_import_resource_state_logs_structured_context(self) -> None:
        """The error path carries structured context: an error with no operation or
        resource type in it cannot be traced back to a request."""
        request = pb.ImportResourceState.Request(type_name="test_resource", id="test-id")

        with patch("pyvider.protocols.tfprotov6.handlers.import_resource_state.logger") as mock_logger:
            await _import_resource_state_impl(request, context=None)

            assert mock_logger.error.called
            call_kwargs = mock_logger.error.call_args[1]
            assert call_kwargs["operation"] == "import_resource_state"
            assert call_kwargs["resource_type"] == "test_resource"
            assert call_kwargs["import_id"] == "test-id"

    @pytest.mark.asyncio
    async def test_move_resource_state_logs_entry(self) -> None:
        """Test that move_resource_state logs structured entry/context."""
        request = pb.MoveResourceState.Request(source_type_name="source", target_type_name="target")

        with patch("pyvider.protocols.tfprotov6.handlers.move_resource_state.logger") as mock_logger:
            await _move_resource_state_impl(request, context=None)

            assert mock_logger.debug.called
            call_kwargs = mock_logger.info.call_args[1]
            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "move_resource_state"
            assert mock_logger.info.called

            assert "operation" in call_kwargs
            assert call_kwargs["operation"] == "move_resource_state"


class TestLogLevelConsistency:
    """Test that log levels are used consistently."""

    @pytest.mark.asyncio
    async def test_handlers_use_debug_for_entry(self) -> None:
        """Test that handlers use DEBUG for entry logging."""
        request = pb.ValidateDataResourceConfig.Request(type_name="test_ds")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _validate_data_resource_config_impl(request, context=None)

            # First call should be debug for entry
            assert mock_logger.debug.called

    @pytest.mark.asyncio
    async def test_handlers_use_info_for_success(self) -> None:
        """Test that handlers use INFO for success logging."""
        request = pb.UpgradeResourceState.Request(type_name="test_resource", version=0)
        request.raw_state.CopyFrom(pb.RawState(json=b"{}"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.logger") as mock_logger,
            patch(
                "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.hub.get_component",
                return_value=_upgradable_resource(),
            ),
        ):
            await _upgrade_resource_state_impl(request, context=None)

            # Success should be logged with info
            assert mock_logger.info.called

    @pytest.mark.asyncio
    async def test_handlers_use_error_for_failures(self) -> None:
        request = pb.ReadDataSource.Request(type_name="test_ds")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _read_data_source_impl(request, context=None)

            # Failure should be logged with error
            assert mock_logger.error.called


class TestContextualInformation:
    """Test that logs include relevant contextual information."""

    @pytest.mark.asyncio
    async def test_read_data_source_includes_data_source_type(self) -> None:
        """Test that read_data_source logs include data_source_type."""
        request = pb.ReadDataSource.Request(type_name="test_ds")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.read_data_source.hub") as mock_hub,
        ):
            mock_hub.get_component.return_value = None

            with contextlib.suppress(Exception):
                await _read_data_source_impl(request, context=None)

            call_kwargs = mock_logger.debug.call_args[1]
            assert "data_source_type" in call_kwargs
            assert call_kwargs["data_source_type"] == "test_ds"

    @pytest.mark.asyncio
    async def test_upgrade_resource_state_includes_resource_type(self) -> None:
        """Test that upgrade logs include resource_type."""
        request = pb.UpgradeResourceState.Request(type_name="test_resource", version=0)
        request.raw_state.CopyFrom(pb.RawState(json=b"{}"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.logger") as mock_logger,
            patch(
                "pyvider.protocols.tfprotov6.handlers.upgrade_resource_state.hub.get_component",
                return_value=_upgradable_resource(),
            ),
        ):
            await _upgrade_resource_state_impl(request, context=None)

            call_kwargs = mock_logger.debug.call_args[1]
            assert "resource_type" in call_kwargs
            assert call_kwargs["resource_type"] == "test_resource"

    @pytest.mark.asyncio
    async def test_error_logs_include_registered_components(self) -> None:
        """Test that error logs include registered component lists for debugging."""
        request = pb.OpenEphemeralResource.Request(type_name="test_eph")
        request.config.CopyFrom(pb.DynamicValue(msgpack=b"\x80"))

        with (
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.logger") as mock_logger,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.hub") as mock_hub,
            patch(
                "pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.create_diagnostic_from_exception"
            ) as mock_diag,
        ):
            mock_hub.get_component.return_value = None
            mock_hub.get_components.return_value = {"other_eph": MagicMock()}
            mock_diag.return_value = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test")

            await _open_ephemeral_resource_impl(request, context=None)

            # Verify error was logged with resource_type
            call_kwargs = mock_logger.error.call_args[1]
            assert "resource_type" in call_kwargs
            assert call_kwargs["resource_type"] == "test_eph"


# 🐍🏗️🔚
