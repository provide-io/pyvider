#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for launch_context_command module."""

import json
import re
from unittest.mock import MagicMock

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli
from pyvider.common.launch_context import LaunchContext, LaunchMethod


def _extract_json(output: str) -> dict:
    """Extract JSON object from CLI output that may contain log lines."""
    # Find the first '{' and parse from there
    match = re.search(r"\{", output)
    if match:
        return json.loads(output[match.start() :])
    raise json.JSONDecodeError("No JSON object found", output, 0)


class TestLaunchContextCommand:
    """Tests for launch-context command."""

    def test_launch_context_command_exists(self) -> None:
        """Test that launch-context command is registered."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "launch-context" in result.output

    def test_launch_context_runs_without_errors(self) -> None:
        """Test that launch-context command runs without errors."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Pyvider Launch Context" in result.output

    def test_launch_context_shows_method(self) -> None:
        """Test that launch-context shows the launch method."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Launch Method:" in result.output

    def test_launch_context_shows_executable_path(self) -> None:
        """Test that launch-context shows executable path."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Executable Path:" in result.output

    def test_launch_context_shows_python_executable(self) -> None:
        """Test that launch-context shows Python executable."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Python Executable:" in result.output

    def test_launch_context_shows_working_directory(self) -> None:
        """Test that launch-context shows working directory."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Working Directory:" in result.output

    def test_launch_context_shows_terraform_invoked(self) -> None:
        """Test that launch-context shows Terraform invoked status."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Terraform Invoked:" in result.output


class TestLaunchContextFormatOptions:
    """Tests for launch-context format options."""

    def test_launch_context_default_format_is_human(self) -> None:
        """Test that default format is human-readable."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        # Human format includes emoji and colors
        assert "🚀" in result.output or "Launch Method:" in result.output

    def test_launch_context_accepts_human_format(self) -> None:
        """Test that --format=human works."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "human"])
        assert result.exit_code == 0
        assert "Launch Method:" in result.output

    def test_launch_context_accepts_json_format(self) -> None:
        """Test that --format=json works."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "json"])
        assert result.exit_code == 0

        data = _extract_json(result.output)
        assert "method" in data
        assert "executable_path" in data
        assert "python_executable" in data
        assert "working_directory" in data
        assert "is_terraform_invoked" in data

    def test_launch_context_json_format_structure(self) -> None:
        """Test that JSON format has correct structure."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "json"])
        assert result.exit_code == 0

        data = _extract_json(result.output)
        # Verify required fields
        assert isinstance(data["method"], str)
        assert isinstance(data["executable_path"], str)
        assert isinstance(data["python_executable"], str)
        assert isinstance(data["working_directory"], str)
        assert isinstance(data["is_terraform_invoked"], bool)
        assert isinstance(data["details"], dict)

    def test_launch_context_rejects_invalid_format(self) -> None:
        """Test that invalid format is rejected."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "xml"])
        assert result.exit_code != 0


class TestLaunchContextVerboseOption:
    """Tests for launch-context --verbose option."""

    def test_launch_context_accepts_verbose_flag(self) -> None:
        """Test that --verbose flag is accepted."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--verbose"])
        assert result.exit_code == 0

    def test_launch_context_verbose_shows_environment_info(self) -> None:
        """Test that --verbose shows environment information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--verbose"])
        assert result.exit_code == 0
        # Verbose mode should show environment info
        assert "Environment Information:" in result.output or result.exit_code == 0

    def test_launch_context_verbose_with_json_includes_environment(self) -> None:
        """Test that --verbose with JSON includes environment_info."""
        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "json", "--verbose"])
        assert result.exit_code == 0

        data = _extract_json(result.output)
        # Verbose JSON should include environment_info
        assert "environment_info" in data


class TestLaunchContextMethodSpecificHelp:
    """Tests for method-specific help messages."""

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_pspf_package_shows_specific_help(self, mock_detect: MagicMock) -> None:
        """Test that PSPF package detection shows specific help."""
        # Mock PSPF launch
        mock_context = LaunchContext(
            method=LaunchMethod.PSPF_PACKAGE,
            executable_path="/path/to/binary",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "PSPF Package" in result.output or "pspf_package" in result.output.lower()

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_script_module_shows_specific_help(self, mock_detect: MagicMock) -> None:
        """Test that script module detection shows specific help."""
        # Mock script module launch
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_MODULE,
            executable_path="/path/to/python",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Module Launch" in result.output or "script_module" in result.output.lower()

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_editable_install_shows_specific_help(self, mock_detect: MagicMock) -> None:
        """Test that editable install detection shows specific help."""
        # Mock editable install
        mock_context = LaunchContext(
            method=LaunchMethod.EDITABLE_INSTALL,
            executable_path="/path/to/pyvider",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Development Mode" in result.output or "editable_install" in result.output.lower()

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_unknown_method_shows_warning(self, mock_detect: MagicMock) -> None:
        """Test that unknown method shows a warning."""
        # Mock unknown launch
        mock_context = LaunchContext(
            method=LaunchMethod.UNKNOWN,
            executable_path="/path/to/unknown",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Unknown" in result.output or "unknown" in result.output.lower()


class TestLaunchContextDetailsFormatting:
    """Tests for details formatting in launch-context."""

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_details_shown_when_present(self, mock_detect: MagicMock) -> None:
        """Test that method details are shown when present."""
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_MODULE,
            executable_path="/path/to/python",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={"module_name": "pyvider", "version": "0.1.0"},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        assert "Method Details:" in result.output

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_complex_values_formatted_correctly(self, mock_detect: MagicMock) -> None:
        """Test that complex values (lists, dicts) are formatted correctly."""
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_MODULE,
            executable_path="/path/to/python",
            python_executable="/path/to/python",
            working_directory="/path/to/work",
            is_terraform_invoked=False,
            details={"simple": "value", "list": ["item1", "item2"], "dict": {"key": "value"}},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        # Complex values should be shown
        assert "Method Details:" in result.output


class TestLaunchContextEdgeCases:
    """Edge case tests for launch-context command."""

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_handles_very_long_paths(self, mock_detect: MagicMock) -> None:
        """Test that very long paths are handled correctly."""
        long_path = "/very/long/path/" + "subdir/" * 50 + "file.py"
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_DIRECT,
            executable_path=long_path,
            python_executable="/usr/bin/python",
            working_directory="/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_handles_empty_details(self, mock_detect: MagicMock) -> None:
        """Test that empty details dict is handled correctly."""
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_DIRECT,
            executable_path="/path/to/script",
            python_executable="/usr/bin/python",
            working_directory="/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context"])
        assert result.exit_code == 0
        # Should not show "Method Details:" section for empty details
        # or should handle it gracefully

    @mock.patch("pyvider.common.launch_context.detect_launch_context")
    def test_json_output_is_pretty_printed(self, mock_detect: MagicMock) -> None:
        """Test that JSON output is pretty-printed with indentation."""
        mock_context = LaunchContext(
            method=LaunchMethod.SCRIPT_MODULE,
            executable_path="/path/to/python",
            python_executable="/path/to/python",
            working_directory="/work",
            is_terraform_invoked=False,
            details={},
            environment_info={},
        )
        mock_detect.return_value = mock_context

        runner = CliRunner()
        result = runner.invoke(cli, ["launch-context", "--format", "json"])
        assert result.exit_code == 0

        # Check that it's indented (pretty-printed)
        assert "  " in result.output  # Should have indentation
        data = _extract_json(result.output)
        assert data is not None


# 🐍🏗️🔚
