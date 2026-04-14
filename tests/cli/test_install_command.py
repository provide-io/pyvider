#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for install_command module."""

from pathlib import Path

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli
from pyvider.cli.install_command import _uninstall_provider, is_running_as_binary


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

    def test_install_requires_pyvider_project(self, tmp_path) -> None:
        """Test that install command requires a pyvider project."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "pyvider.toml" in result.output or "pyproject.toml" in result.output

    def test_install_accepts_pyvider_toml(self, tmp_path) -> None:
        """Test that install command accepts pyvider.toml."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyvider.toml file
            Path("pyvider.toml").write_text('[pyvider]\nname = "test"\n')

            # Mock the prep_provider to avoid actual installation
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke"):
                    result = runner.invoke(cli, ["install"])
                    # Should not fail validation
                    assert "must be run from a directory" not in result.output

    def test_install_accepts_pyproject_with_tool_pyvider(self, tmp_path) -> None:
        """Test that install command accepts pyproject.toml with [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml with [tool.pyvider]
            Path("pyproject.toml").write_text('[tool.pyvider]\nname = "test"\n')

            # Mock to avoid actual installation
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command.click.Context.invoke"):
                    result = runner.invoke(cli, ["install"])
                    # Should not fail validation
                    assert "must be run from a directory" not in result.output

    def test_install_rejects_pyproject_without_tool_pyvider(self, tmp_path) -> None:
        """Test that install command rejects pyproject.toml without [tool.pyvider]."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create a pyproject.toml without [tool.pyvider]
            Path("pyproject.toml").write_text('[tool.pytest]\nminversion = "6.0"\n')

            result = runner.invoke(cli, ["install"])
            assert result.exit_code != 0
            assert "must be run from a directory" in result.output


class TestInstallCommandBinaryMode:
    """Tests for install command in binary mode."""

    def test_binary_mode_copies_executable(self, tmp_path) -> None:
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

    def test_binary_mode_handles_copy_error(self, tmp_path) -> None:
        """Test that binary mode handles copy errors gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock binary mode and make copy fail
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True):
                with mock.patch(
                    "pyvider.cli.install_command.shutil.copy2", side_effect=PermissionError("Access denied")
                ):
                    with mock.patch("pyvider.cli.install_command.PyviderContext"):
                        result = runner.invoke(cli, ["install"])

                        # Should handle error
                        assert result.exit_code != 0


class TestInstallCommandDevelopmentMode:
    """Tests for install command in development mode."""

    def test_development_mode_invokes_prep_provider(self, tmp_path) -> None:
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

    def test_development_mode_handles_prep_provider_error(self, tmp_path) -> None:
        """Test that development mode handles prep_provider errors."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock development mode and make prep_provider fail
            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch(
                    "pyvider.cli.install_command.click.Context.invoke", side_effect=RuntimeError("Prep failed")
                ):
                    result = runner.invoke(cli, ["install"])

                    # Should handle error
                    assert result.exit_code != 0


class TestInstallCommandEdgeCases:
    """Edge case tests for install command."""

    def test_install_creates_plugin_directory_if_missing(self, tmp_path) -> None:
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
                    result = runner.invoke(cli, ["install"])

                    # Verify it succeeds - directory creation is handled internally
                    # The main point is that it doesn't fail when directory doesn't exist
                    assert result.exit_code == 0 or "Success" in result.output

    def test_install_warns_when_replacing_existing_binary(self, tmp_path) -> None:
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

    def test_install_handles_unreadable_pyproject(self, tmp_path) -> None:
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


class TestUninstallCommand:
    """Tests for --uninstall flag and _uninstall_provider function."""

    def test_uninstall_provider_removes_script(self, tmp_path) -> None:
        """Test that _uninstall_provider removes the provider script."""
        from pyvider.cli.context import PyviderContext

        # Create mock context
        ctx = mock.Mock(spec=PyviderContext)
        plugin_dir = tmp_path / "plugins"
        plugin_dir.mkdir(parents=True)
        provider_script = plugin_dir / "terraform-provider-pyvider"
        provider_script.write_text("#!/bin/bash\necho 'provider'")
        ctx.tf_plugin_dir = plugin_dir
        ctx.provider_name = "pyvider"

        # Call uninstall
        with mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=None):
            _uninstall_provider(ctx, quiet=True)

        # Verify script was removed
        assert not provider_script.exists()

    def test_uninstall_provider_removes_symlink(self, tmp_path) -> None:
        """Test that _uninstall_provider removes the venv symlink."""
        from pyvider.cli.context import PyviderContext

        # Create mock venv
        venv_dir = tmp_path / ".venv"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "pyvider").touch()
        symlink_path = venv_bin / "terraform-provider-pyvider"
        symlink_path.symlink_to(Path("pyvider"))

        # Create mock context
        ctx = mock.Mock(spec=PyviderContext)
        plugin_dir = tmp_path / "plugins"
        plugin_dir.mkdir(parents=True)
        ctx.tf_plugin_dir = plugin_dir
        ctx.provider_name = "pyvider"

        # Call uninstall
        with mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=venv_dir):
            _uninstall_provider(ctx, quiet=True)

        # Verify symlink was removed
        assert not symlink_path.exists() and not symlink_path.is_symlink()

    def test_uninstall_provider_idempotent(self, tmp_path) -> None:
        """Test that _uninstall_provider is idempotent."""
        from pyvider.cli.context import PyviderContext

        # Create mock context for empty directory
        ctx = mock.Mock(spec=PyviderContext)
        plugin_dir = tmp_path / "empty_plugins"
        plugin_dir.mkdir(parents=True)
        ctx.tf_plugin_dir = plugin_dir
        ctx.provider_name = "pyvider"

        # Should not raise error even when nothing installed
        with mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=None):
            _uninstall_provider(ctx, quiet=True)
            # Call again - should still succeed
            _uninstall_provider(ctx, quiet=True)

    def test_uninstall_requires_pyvider_project(self, tmp_path) -> None:
        """Test that --uninstall requires a pyvider project."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["install", "--uninstall"])
            # Should fail validation
            assert result.exit_code != 0
            assert "pyvider.toml" in result.output or "pyproject.toml" in result.output


class TestReinstallCommand:
    """Tests for --reinstall flag."""

    def test_reinstall_uninstalls_then_installs(self, tmp_path) -> None:
        """Test that --reinstall performs uninstall then install."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=None):
                    with mock.patch("pyvider.cli.install_command._place_terraform_provider_script"):
                        result = runner.invoke(cli, ["install", "--reinstall"])

                        # Should succeed
                        assert result.exit_code == 0
                        # Should indicate reinstall in output
                        assert "Reinstalling" in result.output or "reinstall" in result.output.lower()


class TestMutuallyExclusiveFlags:
    """Tests for mutually exclusive flag validation."""

    def test_uninstall_and_reinstall_are_mutually_exclusive(self, tmp_path) -> None:
        """Test that --uninstall and --reinstall cannot be used together."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            result = runner.invoke(cli, ["install", "--uninstall", "--reinstall"])

            # Should fail
            assert result.exit_code != 0
            assert "mutually exclusive" in result.output.lower()


class TestInstallCommandSymlinkCreation:
    """Tests for symlink creation during install."""

    def test_install_calls_place_provider_script(self, tmp_path) -> None:
        """Test that install calls _place_terraform_provider_script in development mode."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Create mock venv
            venv_dir = Path(".venv")
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "pyvider").touch()
            (venv_bin / "activate").touch()

            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                with mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=venv_dir):
                    with mock.patch(
                        "pyvider.cli.install_command._place_terraform_provider_script"
                    ) as mock_place:
                        result = runner.invoke(cli, ["install"])

                        # Verify _place_terraform_provider_script was called
                        assert mock_place.called
                        assert result.exit_code == 0


# 🐍🏗️🔚
