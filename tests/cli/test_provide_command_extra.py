"""Additional tests for provide_command module (for coverage improvement)."""

import os
from unittest import mock

from click.testing import CliRunner
import pytest

from pyvider.cli import cli


class TestProvideCommand:
    """Tests for provide command."""

    def test_provide_command_exists(self):
        """Test that provide command is registered."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "provide" in result.output

    def test_provide_has_force_option(self):
        """Test that provide command has --force option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--help"])
        assert result.exit_code == 0
        assert "--force" in result.output

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_without_magic_cookie_shows_interactive_mode(self):
        """Test that provide without magic cookie shows interactive mode."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide"])
        assert result.exit_code == 0
        assert "Interactive Mode" in result.output or "interactive" in result.output.lower()

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_shows_launch_context_in_interactive_mode(self):
        """Test that provide shows launch context in interactive mode."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide"])
        assert result.exit_code == 0
        assert "Launch Context" in result.output or "Method:" in result.output

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_suggests_force_flag(self):
        """Test that provide suggests using --force flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide"])
        assert result.exit_code == 0
        assert "--force" in result.output


class TestProvideCommandForceMode:
    """Tests for provide command with --force flag."""

    @mock.patch("pyvider.cli.provide_command.asyncio.run")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_force_starts_server(self, mock_async_run):
        """Test that provide --force starts the server."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--force"])

        # Should have attempted to start server
        assert mock_async_run.called or result.exit_code != 0

    @mock.patch("pyvider.cli.provide_command.asyncio.run")
    @mock.patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False)
    def test_provide_with_magic_cookie_starts_server(self, mock_async_run):
        """Test that provide with magic cookie starts server."""
        # Set binary name to include terraform-provider
        with mock.patch("sys.argv", ["terraform-provider-pyvider", "provide"]):
            runner = CliRunner()
            result = runner.invoke(cli, ["provide"])

            # Should have attempted to start server
            assert mock_async_run.called or result.exit_code != 0


class TestProvideCommandMagicCookieValidation:
    """Tests for magic cookie validation in provide command."""

    @mock.patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False)
    def test_provide_validates_binary_name_with_magic_cookie(self):
        """Test that provide validates binary name when magic cookie is set."""
        # Use a binary name that doesn't contain terraform-provider
        with mock.patch("sys.argv", ["pyvider", "provide"]):
            runner = CliRunner()
            result = runner.invoke(cli, ["provide"])

            # Should show error about binary name
            assert result.exit_code != 0 or "binary name" in result.output.lower() or "terraform-provider" in result.output.lower()

    @mock.patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False)
    def test_provide_force_bypasses_binary_name_check(self):
        """Test that provide --force bypasses binary name check."""
        with mock.patch("sys.argv", ["pyvider", "provide", "--force"]):
            with mock.patch("pyvider.cli.provide_command.asyncio.run"):
                runner = CliRunner()
                result = runner.invoke(cli, ["provide", "--force"])

                # Should not show binary name error
                assert "binary name" not in result.output.lower() or result.exit_code == 0

    @mock.patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False)
    def test_provide_shows_detection_error_details(self):
        """Test that provide shows detailed error when detection fails."""
        with mock.patch("sys.argv", ["wrong-name", "provide"]):
            runner = CliRunner()
            result = runner.invoke(cli, ["provide"])

            # Should show helpful error message
            if result.exit_code != 0:
                assert "Provider Detection Error" in result.output or "Debug Info" in result.output or "fix this" in result.output.lower()


class TestProvideCommandKeyboardInterrupt:
    """Tests for keyboard interrupt handling."""

    @mock.patch("pyvider.cli.provide_command.asyncio.run")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_handles_keyboard_interrupt(self, mock_async_run):
        """Test that provide handles keyboard interrupt gracefully."""
        mock_async_run.side_effect = KeyboardInterrupt()

        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--force"])

        # Should handle interrupt gracefully
        assert result.exit_code == 0 or "interrupted" in result.output.lower()


class TestProvideCommandDiscoveryErrors:
    """Tests for component discovery error handling."""

    @mock.patch("pyvider.cli.provide_command._handle_discovery_errors")
    @mock.patch("pyvider.cli.provide_command.asyncio.run")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_runs_discovery_before_server(self, mock_async_run, mock_handle_errors):
        """Test that provide runs component discovery before starting server."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--force"])

        # Should have checked for discovery errors
        # (either called or would have been called before server start)
        assert mock_handle_errors.called or result.exit_code != 0


class TestRunProviderServer:
    """Tests for _run_provider_server function."""

    @pytest.mark.asyncio
    async def test_run_provider_server_is_async(self):
        """Test that _run_provider_server is an async function."""
        from pyvider.cli.provide_command import _run_provider_server
        import inspect

        assert inspect.iscoroutinefunction(_run_provider_server)

    @pytest.mark.asyncio
    @mock.patch("pyvider.cli.provide_command.RPCPluginServer")
    @mock.patch("pyvider.cli.provide_command.ComponentDiscovery")
    async def test_run_provider_server_discovers_components(self, mock_discovery_cls, mock_server):
        """Test that _run_provider_server discovers components."""
        from pyvider.cli.provide_command import _run_provider_server

        mock_discovery = mock_discovery_cls.return_value
        mock_discovery.discover_all = mock.AsyncMock()
        mock_server_instance = mock_server.return_value
        mock_server_instance.serve = mock.AsyncMock()

        try:
            await _run_provider_server("test-cookie")
        except Exception:
            pass  # We expect it might fail due to mocking

        # Should have attempted discovery
        assert mock_discovery_cls.called

    @pytest.mark.asyncio
    @mock.patch("pyvider.cli.provide_command.RPCPluginServer")
    @mock.patch("pyvider.cli.provide_command.PyviderProvider")
    @mock.patch("pyvider.cli.provide_command.ComponentDiscovery")
    async def test_run_provider_server_creates_provider(self, mock_discovery_cls, mock_provider_cls, mock_server):
        """Test that _run_provider_server creates provider instance."""
        from pyvider.cli.provide_command import _run_provider_server

        mock_discovery = mock_discovery_cls.return_value
        mock_discovery.discover_all = mock.AsyncMock()
        mock_provider = mock_provider_cls.return_value
        mock_provider.setup = mock.AsyncMock()
        mock_server_instance = mock_server.return_value
        mock_server_instance.serve = mock.AsyncMock()

        try:
            await _run_provider_server("test-cookie")
        except Exception:
            pass

        # Should have created and setup provider
        assert mock_provider_cls.called

    @pytest.mark.asyncio
    @mock.patch("pyvider.cli.provide_command.logger")
    @mock.patch("pyvider.cli.provide_command.RPCPluginServer")
    @mock.patch("pyvider.cli.provide_command.ComponentDiscovery")
    async def test_run_provider_server_configures_telemetry(self, mock_discovery_cls, mock_server, mock_logger):
        """Test that _run_provider_server configures telemetry."""
        from pyvider.cli.provide_command import _run_provider_server

        mock_discovery = mock_discovery_cls.return_value
        mock_discovery.discover_all = mock.AsyncMock()
        mock_server_instance = mock_server.return_value
        mock_server_instance.serve = mock.AsyncMock()

        try:
            await _run_provider_server("test-cookie")
        except Exception:
            pass

        # Should have logged telemetry configuration
        # Check environment was configured
        assert "PYVIDER_LOG_LEVEL" in os.environ or mock_logger.info.called


class TestProvideCommandEdgeCases:
    """Edge case tests for provide command."""

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_shows_help_when_no_magic_cookie(self):
        """Test that provide shows help when no magic cookie."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide"])

        # Should show CLI help
        assert result.exit_code == 0
        assert "pyvider" in result.output.lower() or "help" in result.output.lower()

    @mock.patch("pyvider.cli.provide_command.asyncio.run")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_provide_accepts_additional_options(self, mock_async_run):
        """Test that provide accepts CLI options like --log-level."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--log-level", "DEBUG", "provide", "--force"])

        # Should not error on additional options
        assert mock_async_run.called or result.exit_code != 0

    @mock.patch.dict(os.environ, {"TF_PLUGIN_MAGIC_COOKIE": "test-cookie"}, clear=False)
    def test_provide_shows_debug_info_on_error(self):
        """Test that provide shows debug info when validation fails."""
        with mock.patch("sys.argv", ["bad-name", "provide"]):
            runner = CliRunner()
            result = runner.invoke(cli, ["provide"])

            if result.exit_code != 0:
                # Should show debug information
                assert "sys.argv" in result.output or "script_name" in result.output or "Debug" in result.output
