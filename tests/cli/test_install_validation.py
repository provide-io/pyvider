#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for install command validation logic."""

from pathlib import Path

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli
from pyvider.cli.install_command import is_running_as_binary


class TestIsRunningAsBinary:
    """Tests for is_running_as_binary function."""

    def test_returns_false_in_normal_mode(self) -> None:
        """Test that it returns False in normal Python mode."""
        # In normal mode, sys.frozen is not set
        result = is_running_as_binary()
        assert result is False

    def test_returns_true_when_frozen_attribute_exists(self) -> None:
        """Test that it returns True when sys.frozen is set."""
        import sys

        original = getattr(sys, "frozen", None)
        try:
            sys.frozen = True
            result = is_running_as_binary()
            assert result is True
        finally:
            if original is None:
                if hasattr(sys, "frozen"):
                    delattr(sys, "frozen")
            else:
                sys.frozen = original


class TestInstallCommandValidation:
    """Tests for install command validation logic."""

    def test_install_requires_pyvider_project(self, tmp_path: Path) -> None:
        """Test that install command requires a pyvider project."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "pyvider.toml" in result.output or "pyproject.toml" in result.output

    def test_install_accepts_pyvider_toml(self, tmp_path: Path) -> None:
        """Test that install command accepts pyvider.toml."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyvider.toml file
            Path("pyvider.toml").write_text('[pyvider]\nname = "test"\n')

            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command.click.Context.invoke"),
            ):
                result = runner.invoke(cli, ["install"])
                # Should not fail validation
                assert "must be run from a directory" not in result.output

    def test_install_accepts_pyproject_with_tool_pyvider(self, tmp_path: Path) -> None:
        """Test that install command accepts pyproject.toml with [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml with [tool.pyvider]
            Path("pyproject.toml").write_text('[tool.pyvider]\nname = "test"\n')

            # Mock to avoid actual installation
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command.click.Context.invoke"),
            ):
                result = runner.invoke(cli, ["install"])
                # Should not fail validation
                assert "must be run from a directory" not in result.output

    def test_install_rejects_pyproject_without_tool_pyvider(self, tmp_path: Path) -> None:
        """Test that install command rejects pyproject.toml without [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml without [tool.pyvider]
            Path("pyproject.toml").write_text('[tool.pytest]\nminversion = "6.0"\n')

            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "must be run from a directory" in result.output

    def test_install_accepts_pyproject_with_pyvider_section(self, tmp_path: Path) -> None:
        """Test that install command accepts pyproject.toml with [pyvider] section."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml with [pyvider] (not [tool.pyvider])
            Path("pyproject.toml").write_text('[pyvider]\nname = "test"\n')

            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command.click.Context.invoke"),
            ):
                result = runner.invoke(cli, ["install"])
                # Should not fail validation
                assert "must be run from a directory" not in result.output

    def test_install_handles_unreadable_pyproject(self, tmp_path: Path) -> None:
        """Test that install handles unreadable pyproject.toml gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create pyproject.toml
            pyproject_path = Path("pyproject.toml")
            pyproject_path.write_text("[tool.pyvider]\n")

            # Make it fail to read by mocking safe_read_text
            with mock.patch("pyvider.cli.install_command.safe_read_text", side_effect=OSError("Cannot read")):
                result = runner.invoke(cli, ["install"])

                # Should fail validation since we can't detect [tool.pyvider]
                assert result.exit_code != 0


# 🐍🏗️🔚
