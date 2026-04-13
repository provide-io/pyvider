#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider CLI with new flexible options."""

from pathlib import Path

from click.testing import CliRunner
import pytest

from pyvider.cli import cli

# Import testkit fixtures with fallback
try:
    from provide.testkit import temp_file
except ImportError:
    import tempfile

    @pytest.fixture
    def temp_file() -> str:
        """Fallback temp_file fixture."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            yield f.name
        Path(f.name).unlink(missing_ok=True)


class TestPyviderCLI:
    """Test the main pyvider CLI."""

    def test_cli_launches_without_errors(self) -> None:
        """Test that the CLI launches without errors."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Pyvider CLI Tool" in result.output

    def test_cli_accepts_log_level_option(self) -> None:
        """Test that --log-level option is accepted."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--log-level", "DEBUG", "--help"])
        assert result.exit_code == 0

    def test_cli_accepts_log_format_option(self) -> None:
        """Test that --log-format option is accepted."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--log-format", "json", "--help"])
        assert result.exit_code == 0

    def test_cli_accepts_log_file_option(self, temp_file: str) -> None:
        """Test that --log-file option is accepted."""
        log_file = str(temp_file) + ".log"

        runner = CliRunner()
        result = runner.invoke(cli, ["--log-file", log_file, "--help"])
        assert result.exit_code == 0

    def test_cli_accepts_output_options(self) -> None:
        """Test that output options are accepted."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "--no-color", "--no-emoji", "--help"])
        assert result.exit_code == 0

    def test_cli_no_verbose_or_quiet_options(self) -> None:
        """Test that --verbose and --quiet options are NOT present."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "--verbose" not in result.output
        assert "--quiet" not in result.output
        assert "-v" not in result.output.replace("pyvider", "")  # Ignore 'pyvider' itself
        assert "-q" not in result.output

    def test_cli_no_debug_option(self) -> None:
        """Test that --debug option is NOT present (replaced by --log-level debug)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "--debug" not in result.output

    def test_provide_command_exists(self) -> None:
        """Test that the provide command exists."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--help"])
        assert result.exit_code == 0
        assert "Starts the provider in gRPC server mode" in result.output

    def test_components_command_exists(self) -> None:
        """Test that the components command exists."""
        runner = CliRunner()
        result = runner.invoke(cli, ["components", "--help"])
        assert result.exit_code == 0
        assert "Manage, inspect, and diagnose Pyvider components" in result.output

    def test_config_command_exists(self) -> None:
        """Test that the config command exists."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "--help"])
        assert result.exit_code == 0
        assert "Manage and display Pyvider configuration" in result.output


class TestOptionsAtSubcommandLevel:
    """Test that options work at subcommand level."""

    def test_components_accepts_log_level(self) -> None:
        """Test that components command accepts --log-level."""
        runner = CliRunner()
        result = runner.invoke(cli, ["components", "--log-level", "WARNING", "--help"])
        assert result.exit_code == 0

    def test_config_accepts_log_format(self) -> None:
        """Test that config command accepts --log-format."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "--log-format", "json", "--help"])
        assert result.exit_code == 0

    def test_options_can_be_at_root_or_subcommand(self) -> None:
        """Test that options can be specified at root or subcommand level."""
        runner = CliRunner()

        # Options at root level
        result = runner.invoke(cli, ["--log-level", "ERROR", "components", "--help"])
        assert result.exit_code == 0

        # Options at subcommand level
        result = runner.invoke(cli, ["components", "--log-level", "ERROR", "--help"])
        assert result.exit_code == 0


class TestInteractiveMode:
    """Test interactive mode behavior."""

    def test_interactive_mode_when_no_subcommand(self) -> None:
        """Test that interactive mode is triggered when no subcommand is given."""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        # When not run by Terraform, it should show interactive mode
        assert "Interactive Mode" in result.output
        # The command name in the message depends on how it's invoked
        assert "provide --force" in result.output

    def test_interactive_mode_shows_launch_context(self) -> None:
        """Test that interactive mode displays launch context."""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert "Launch Context:" in result.output
        assert "Method:" in result.output
        assert "Executable:" in result.output


class TestProvideCommand:
    """Test the provide command specifically."""

    def test_provide_command_force_option(self) -> None:
        """Test that provide command accepts --force option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide", "--help"])
        assert result.exit_code == 0
        assert "--force" in result.output

    def test_provide_command_without_force_shows_help(self) -> None:
        """Test that provide command without --force shows help in interactive mode."""
        runner = CliRunner()
        result = runner.invoke(cli, ["provide"])
        # Without magic cookie and without --force, should show interactive mode
        assert "Interactive Mode" in result.output or "Provider Detection Error" in result.output


class TestConfigCommand:
    """Test the config command."""

    def test_config_show_command_exists(self) -> None:
        """Test that config show command exists."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "show", "--help"])
        assert result.exit_code == 0
        assert "Displays the current Pyvider configuration" in result.output


class TestComponentsCommand:
    """Test the components command."""

    def test_components_list_command_exists(self) -> None:
        """Test that components list command exists."""
        runner = CliRunner()
        # The components group runs discovery which may take time
        # Just check that the group itself works
        result = runner.invoke(cli, ["components", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output  # Check that list command is shown

    def test_components_diagnose_command_exists(self) -> None:
        """Test that components diagnose command exists."""
        runner = CliRunner()
        # Check that diagnose is listed in components help
        result = runner.invoke(cli, ["components", "--help"])
        assert result.exit_code == 0
        assert "diagnose" in result.output  # Check that diagnose command is shown


class TestJSONOutput:
    """Test JSON output functionality."""

    def test_json_flag_affects_output(self) -> None:
        """Test that --json flag affects output format."""
        runner = CliRunner()
        # This would need a command that actually outputs JSON when the flag is set
        # For now, just verify the flag is accepted
        result = runner.invoke(cli, ["--json", "--help"])
        assert result.exit_code == 0


# 🐍🏗️🔚
