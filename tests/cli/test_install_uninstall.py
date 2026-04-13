#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for install command uninstall and reinstall functionality."""

from pathlib import Path

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli
from pyvider.cli.install_command import _uninstall_provider


class TestUninstallCommand:
    """Tests for --uninstall flag and _uninstall_provider function."""

    def test_uninstall_provider_removes_script(self, tmp_path: Path) -> None:
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

    def test_uninstall_provider_removes_symlink(self, tmp_path: Path) -> None:
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

    def test_uninstall_provider_idempotent(self, tmp_path: Path) -> None:
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

    def test_uninstall_requires_pyvider_project(self, tmp_path: Path) -> None:
        """Test that --uninstall requires a pyvider project."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["install", "--uninstall"])
            # Should fail validation
            assert result.exit_code != 0
            assert "pyvider.toml" in result.output or "pyproject.toml" in result.output


class TestReinstallCommand:
    """Tests for --reinstall flag."""

    def test_reinstall_uninstalls_then_installs(self, tmp_path: Path) -> None:
        """Test that --reinstall performs uninstall then install."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command._find_actual_venv", return_value=None),
                mock.patch("pyvider.cli.install_command._place_terraform_provider_script"),
            ):
                result = runner.invoke(cli, ["install", "--reinstall"])

                # Should succeed
                assert result.exit_code == 0
                # Should indicate reinstall in output
                assert "Reinstalling" in result.output or "reinstall" in result.output.lower()


class TestMutuallyExclusiveFlags:
    """Tests for mutually exclusive flag validation."""

    def test_uninstall_and_reinstall_are_mutually_exclusive(self, tmp_path: Path) -> None:
        """Test that --uninstall and --reinstall cannot be used together."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            result = runner.invoke(cli, ["install", "--uninstall", "--reinstall"])

            # Should fail
            assert result.exit_code != 0
            assert "mutually exclusive" in result.output.lower()


# 🐍🏗️🔚
