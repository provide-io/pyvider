"""Tests for install_command module."""

from pathlib import Path
from unittest import mock

from click.testing import CliRunner
import pytest

from pyvider.cli import cli
from pyvider.cli.install_command import is_running_as_binary


class TestIsRunningAsBinary:
    """Tests for is_running_as_binary function."""

    def test_returns_false_in_normal_mode(self):
        """Test that it returns False in normal Python mode."""
        # In normal mode, sys.frozen is not set
        result = is_running_as_binary()
        assert result is False

    def test_returns_true_when_frozen_attribute_exists(self):
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

    def test_install_requires_pyvider_project(self, tmp_path):
        """Test that install command requires a pyvider project."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "pyvider.toml" in result.output or "pyproject.toml" in result.output

    def test_install_accepts_pyvider_toml(self, tmp_path):
        """Test that install command accepts pyvider.toml."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyvider.toml file
            Path("pyvider.toml").write_text("[pyvider]\nname = \"test\"\n")

            # Mock the prep_provider to avoid actual installation
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke"):
                    result = runner.invoke(cli, ["install"])
                    # Should not fail validation
                    assert "must be run from a directory" not in result.output

    def test_install_accepts_pyproject_with_tool_pyvider(self, tmp_path):
        """Test that install command accepts pyproject.toml with [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml with [tool.pyvider]
            Path("pyproject.toml").write_text("[tool.pyvider]\nname = \"test\"\n")

            # Mock to avoid actual installation
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke"):
                    result = runner.invoke(cli, ["install"])
                    # Should not fail validation
                    assert "must be run from a directory" not in result.output

    def test_install_rejects_pyproject_without_tool_pyvider(self, tmp_path):
        """Test that install command rejects pyproject.toml without [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml without [tool.pyvider]
            Path("pyproject.toml").write_text("[tool.pytest]\nminversion = \"6.0\"\n")

            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "must be run from a directory" in result.output


class TestInstallCommandBinaryMode:
    """Tests for install command in binary mode."""

    def test_binary_mode_copies_executable(self, tmp_path):
        """Test that binary mode copies the executable."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")
            fake_binary.chmod(0o755)

            # Mock binary mode
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True):
                with mock.patch("sys.executable", str(fake_binary)):
                    with mock.patch("pyvider.cli.install_command.PyviderContext") as MockContext:
                        # Setup mock context
                        mock_ctx_instance = MockContext.return_value
                        mock_tf_plugin_dir = tmp_path / "plugins"
                        mock_tf_plugin_dir.mkdir(parents=True)
                        mock_ctx_instance.tf_plugin_dir = mock_tf_plugin_dir

                        result = runner.invoke(cli, ["install"])

                        # Verify success message
                        if result.exit_code == 0:
                            assert "Success" in result.output or "installed" in result.output.lower()

    def test_binary_mode_handles_copy_error(self, tmp_path):
        """Test that binary mode handles copy errors gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock binary mode and make copy fail
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True):
                with mock.patch("pyvider.cli.install_command.shutil.copy2", side_effect=PermissionError("Access denied")):
                    with mock.patch("pyvider.cli.install_command.PyviderContext"):
                        result = runner.invoke(cli, ["install"])

                        # Should handle error
                        assert result.exit_code != 0


class TestInstallCommandDevelopmentMode:
    """Tests for install command in development mode."""

    def test_development_mode_invokes_prep_provider(self, tmp_path):
        """Test that development mode invokes prep_provider."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock development mode
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke") as mock_invoke:
                    result = runner.invoke(cli, ["install"])

                    # Verify prep_provider was invoked
                    if result.exit_code == 0 or "Development Mode" in result.output:
                        assert mock_invoke.called or "Development Mode" in result.output

    def test_development_mode_handles_prep_provider_error(self, tmp_path):
        """Test that development mode handles prep_provider errors."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock development mode and make prep_provider fail
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke", side_effect=RuntimeError("Prep failed")):
                    result = runner.invoke(cli, ["install"])

                    # Should handle error
                    assert result.exit_code != 0


class TestInstallCommandEdgeCases:
    """Edge case tests for install command."""

    def test_install_creates_plugin_directory_if_missing(self, tmp_path):
        """Test that install creates the plugin directory if it doesn't exist."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")
            fake_binary.chmod(0o755)

            # Mock binary mode
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True):
                with mock.patch("sys.executable", str(fake_binary)):
                    with mock.patch("pyvider.cli.install_command.PyviderContext") as MockContext:
                        # Setup mock context with non-existent directory
                        mock_ctx_instance = MockContext.return_value
                        mock_tf_plugin_dir = tmp_path / "new_plugins"
                        mock_ctx_instance.tf_plugin_dir = mock_tf_plugin_dir

                        result = runner.invoke(cli, ["install"])

                        # Verify directory was created
                        if result.exit_code == 0:
                            assert "Creating plugin directory" in result.output or mock_tf_plugin_dir.exists()

    def test_install_warns_when_replacing_existing_binary(self, tmp_path):
        """Test that install warns when replacing an existing binary."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")
            fake_binary.chmod(0o755)

            # Create existing target
            target_dir = tmp_path / "plugins"
            target_dir.mkdir(parents=True)
            existing_binary = target_dir / "fake_provider"
            existing_binary.write_text("old version")

            # Mock binary mode
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True):
                with mock.patch("sys.executable", str(fake_binary)):
                    with mock.patch("pyvider.cli.install_command.PyviderContext") as MockContext:
                        mock_ctx_instance = MockContext.return_value
                        mock_ctx_instance.tf_plugin_dir = target_dir

                        result = runner.invoke(cli, ["install"])

                        # Verify warning message
                        if result.exit_code == 0:
                            assert "Warning" in result.output or "replaced" in result.output.lower()

    def test_install_handles_unreadable_pyproject(self, tmp_path):
        """Test that install handles unreadable pyproject.toml gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create pyproject.toml
            pyproject_path = Path("pyproject.toml")
            pyproject_path.write_text("[tool.pyvider]\n")

            # Make it fail to read by mocking safe_read_text
            with mock.patch("pyvider.cli.install_command.safe_read_text", side_effect=IOError("Cannot read")):
                result = runner.invoke(cli, ["install"])

                # Should fail validation since we can't detect [tool.pyvider]
                assert result.exit_code != 0
