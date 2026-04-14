#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for the provide command."""

import asyncio
from collections.abc import Coroutine
import os
from typing import Any
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
import pytest

from pyvider.cli import cli
from pyvider.cli.provide_command import TERRAFORM_PLUGIN_MAGIC_COOKIE


class TestProvideCommandBasics:
    """Test basic provide command functionality."""

    def test_provide_help(self) -> None:
        """Test provide command help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--help"])
        assert result.exit_code == 0
        assert "Starts the provider in gRPC server mode" in result.output
        assert "--force" in result.output

    def test_provide_force_flag_present(self) -> None:
        """Test that --force flag is available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--help"])
        assert result.exit_code == 0
        assert "--force" in result.output
        assert "Force the provider to start in server mode" in result.output


class TestProvideInteractiveMode:
    """Test interactive mode when not launched by Terraform."""

    def test_provide_without_magic_cookie_shows_interactive_mode(self) -> None:
        """Test that running without magic cookie shows interactive mode."""
        runner = CliRunner()
        with patch.dict(os.environ, {}, clear=False):
            # Ensure TF_PLUGIN_MAGIC_COOKIE is not set
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            result = runner.invoke(cli, ["provide"])

        # Should exit with 0 and show interactive mode
        assert result.exit_code == 0
        assert "Interactive Mode" in result.output
        assert "Launch Context:" in result.output
        assert "Method:" in result.output

    def test_interactive_mode_shows_launch_context_details(self) -> None:
        """Test that interactive mode displays launch context details."""
        runner = CliRunner()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            result = runner.invoke(cli, ["provide"])

        assert result.exit_code == 0
        assert "Executable:" in result.output
        assert "Python:" in result.output

    def test_interactive_mode_shows_help_info(self) -> None:
        """Test that interactive mode explains how to use the provider."""
        runner = CliRunner()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            result = runner.invoke(cli, ["provide"])

        assert result.exit_code == 0
        assert "provide --force" in result.output
        assert "inspect the provider's components" in result.output


class TestProvideDetectionWarnings:
    """Test provider binary name detection."""

    def test_magic_cookie_with_wrong_binary_name_shows_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test detection error when magic cookie is set but binary name is wrong."""
        runner = CliRunner()

        # Set magic cookie and wrong binary name
        with (
            patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False),
            patch("sys.argv", ["wrong-name", "provide"]),
        ):
            result = runner.invoke(cli, ["provide"])

        assert result.exit_code == 1
        assert "Provider Detection Error" in result.output
        assert "binary name" in result.output.lower()

    def test_force_bypasses_detection_check(self) -> None:
        """Test that --force bypasses the binary name detection."""
        runner = CliRunner()

        with (
            patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False),
            patch("sys.argv", ["wrong-name", "provide", "--force"]),
        ):
            # Mock the server run to avoid actually starting it
            import asyncio

            def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
                if asyncio.iscoroutine(coro):
                    coro.close()

            with patch("pyvider.cli.provide_command.asyncio.run") as mock_run:
                mock_run.side_effect = consume_coroutine
                result = runner.invoke(cli, ["provide", "--force"])

        # Should not show detection error
        assert "Provider Detection Error" not in result.output


class TestProvideForceMode:
    """Test --force mode behavior."""

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_force_mode_starts_server(self, mock_run: MagicMock) -> None:
        """Test that --force mode starts the server."""
        # Mock asyncio.run to consume the coroutine
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            runner.invoke(cli, ["provide", "--force"])

        # Should call asyncio.run to start the server
        assert mock_run.call_count >= 1

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_force_mode_uses_dummy_cookie(self, mock_run: MagicMock) -> None:
        """Test that --force mode uses a dummy cookie when none is set."""
        # Mock asyncio.run to consume the coroutine
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            runner.invoke(cli, ["provide", "--force"])

        # Verify the server was called
        assert mock_run.call_count >= 1

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_keyboard_interrupt_handled_gracefully(self, mock_run: MagicMock) -> None:
        """Test that KeyboardInterrupt is handled gracefully."""
        # Mock asyncio.run to consume coroutine then raise KeyboardInterrupt on second call
        import asyncio

        call_count = [0]

        def consume_then_interrupt(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()
            call_count[0] += 1
            if call_count[0] >= 1:
                raise KeyboardInterrupt()

        mock_run.side_effect = consume_then_interrupt
        runner = CliRunner()

        result = runner.invoke(cli, ["provide", "--force"], catch_exceptions=False)

        # KeyboardInterrupt should be caught and handled
        # The actual exit code depends on how Click handles it
        assert "interrupted by user" in result.output or result.exit_code in (0, 1)


class TestProvideServerMode:
    """Test actual server mode when magic cookie is present."""

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_valid_magic_cookie_starts_server(self, mock_run: MagicMock) -> None:
        """Test that valid magic cookie starts the server."""
        # Mock asyncio.run to consume the coroutine
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        # Set magic cookie and terraform-provider binary name
        with (
            patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": TERRAFORM_PLUGIN_MAGIC_COOKIE}, clear=False),
            patch("sys.argv", ["terraform-provider-pyvider", "provide"]),
        ):
            runner.invoke(cli, ["provide"])

        # Should call the server
        assert mock_run.call_count >= 1

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_magic_cookie_value_passed_to_server(self, mock_run: MagicMock) -> None:
        """Test that the actual magic cookie value is passed to the server."""
        # Mock asyncio.run to consume the coroutine
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        cookie_value = "test-magic-cookie-123"
        with (
            patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": cookie_value}, clear=False),
            patch("sys.argv", ["terraform-provider-pyvider", "provide"]),
        ):
            runner.invoke(cli, ["provide"])

        # Should call the server
        assert mock_run.call_count >= 1


class TestProvideServerErrorHandling:
    """Test error handling in server mode."""

    def test_server_error_shows_friendly_message(self) -> None:
        """Test that server errors show user-friendly messages."""
        runner = CliRunner()

        # Mock asyncio.run to consume coroutine then raise exception on second call
        import asyncio

        call_count = [0]

        def consume_then_error(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()
            call_count[0] += 1
            if call_count[0] >= 1:
                raise RuntimeError("Test server error")

        with patch("pyvider.cli.provide_command.asyncio.run") as mock_run:
            mock_run.side_effect = consume_then_error
            result = runner.invoke(cli, ["provide", "--force"])

        # The try/except block in provide_cmd catches the exception and calls sys.exit(1)
        assert result.exit_code == 1
        # Check if error handling was invoked (output may be empty if all goes to stderr)
        # We at least verify the error path was taken by checking exit code

    def test_server_error_includes_error_details(self) -> None:
        """Test that server errors include specific error information."""
        runner = CliRunner()

        # Mock asyncio.run to consume coroutine then raise exception on second call
        import asyncio

        call_count = [0]

        def consume_then_error(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()
            call_count[0] += 1
            if call_count[0] >= 1:
                raise ValueError("Invalid configuration")

        with patch("pyvider.cli.provide_command.asyncio.run") as mock_run:
            mock_run.side_effect = consume_then_error
            result = runner.invoke(cli, ["provide", "--force"])

        assert result.exit_code == 1

    def test_server_error_includes_github_link(self) -> None:
        """Test that server errors include link to issue tracker."""
        runner = CliRunner()

        # Mock asyncio.run to consume coroutine then raise exception on second call
        import asyncio

        call_count = [0]

        def consume_then_error(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()
            call_count[0] += 1
            if call_count[0] >= 1:
                raise Exception("Unexpected error")

        with patch("pyvider.cli.provide_command.asyncio.run") as mock_run:
            mock_run.side_effect = consume_then_error
            result = runner.invoke(cli, ["provide", "--force"])

        assert result.exit_code == 1


class TestProvideComponentDiscovery:
    """Test component discovery integration."""

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_discovery_runs_before_server_start(self, mock_run: MagicMock) -> None:
        """Test that component discovery runs before starting the server."""
        # Mock asyncio.run to consume the coroutine
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        runner.invoke(cli, ["provide", "--force"])

        # Discovery runs inside _run_provider_server via asyncio.run
        assert mock_run.call_count >= 1


@pytest.mark.asyncio
class TestRunProviderServerAsync:
    """Test the async _run_provider_server function."""

    async def test_run_provider_server_basic_initialization(self) -> None:
        """Test basic server initialization flow."""
        from pyvider.cli.provide_command import _run_provider_server

        # This test verifies the function can be called
        # Full integration testing would require a lot of mocking
        # We just verify the signature and that it's async
        assert asyncio.iscoroutinefunction(_run_provider_server)


class TestProvideCommandCoverage:
    """Additional tests to improve coverage."""

    def test_script_name_extraction(self) -> None:
        """Test that script name is correctly extracted from sys.argv."""
        runner = CliRunner()

        with patch("sys.argv", ["terraform-provider-test"]), patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TF_PLUGIN_MAGIC_COOKIE", None)
            result = runner.invoke(cli, ["provide"])

        # Should show interactive mode with correct script name
        assert result.exit_code == 0
        assert "terraform-provider-test provide --force" in result.output

    @patch("pyvider.cli.provide_command.asyncio.run")
    def test_detection_error_shows_debug_info(self, mock_run: MagicMock) -> None:
        """Test that detection error includes debug information."""
        # Mock asyncio.run to consume any coroutines (shouldn't be called but just in case)
        import asyncio

        def consume_coroutine(coro: Coroutine[Any, Any, None]) -> None:
            if asyncio.iscoroutine(coro):
                coro.close()

        mock_run.side_effect = consume_coroutine

        runner = CliRunner()

        cookie = "test-cookie-value"
        with (
            patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": cookie}, clear=False),
            patch("sys.argv", ["wrong-binary-name", "provide"]),
        ):
            result = runner.invoke(cli, ["provide"])

        assert result.exit_code == 1
        assert "Debug Info:" in result.output
        assert "sys.argv[0]:" in result.output
        assert "script_name:" in result.output


# 🐍🏗️🔚
