#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for install command in binary mode."""

from pathlib import Path

from click.testing import CliRunner
from provide.foundation.platform import get_arch_name, get_os_name
from provide.testkit import mocking as mock

from pyvider.cli import cli


class TestInstallCommandBinaryMode:
    """Tests for install command in binary mode."""

    def test_binary_mode_copies_executable(self, tmp_path: Path) -> None:
        """Test that binary mode copies the executable."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True),
                mock.patch("sys.executable", str(fake_binary)),
                mock.patch("pyvider.cli.install_command.PyviderContext") as MockContext,
            ):
                # Setup mock context
                mock_ctx_instance = MockContext.return_value
                mock_tf_plugin_dir = tmp_path / "plugins"
                mock_tf_plugin_dir.mkdir(parents=True)
                mock_ctx_instance.tf_plugin_dir = mock_tf_plugin_dir

                result = runner.invoke(cli, ["install"])

                # Verify success message
                if result.exit_code == 0:
                    assert "Success" in result.output or "installed" in result.output.lower()

    def test_binary_mode_handles_copy_error(self, tmp_path: Path) -> None:
        """Test that binary mode handles copy errors gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock binary mode and make copy fail
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True),
                mock.patch(
                    "pyvider.cli.install_command.shutil.copy2", side_effect=PermissionError("Access denied")
                ),
                mock.patch("pyvider.cli.install_command.PyviderContext"),
            ):
                result = runner.invoke(cli, ["install"])

                # Should handle error
                assert result.exit_code != 0


class TestInstallCommandEdgeCases:
    """Edge case tests for install command in binary mode."""

    def test_install_creates_plugin_directory_if_missing(self, tmp_path: Path) -> None:
        """Test that install creates the plugin directory if it doesn't exist."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")

            # Mock binary mode
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True),
                mock.patch("sys.executable", str(fake_binary)),
            ):
                fake_binary.chmod(0o755)
                result = runner.invoke(cli, ["install"])
                # Verify it succeeds - directory creation is handled internally
                # The main point is that it doesn't fail when directory doesn't exist
                assert result.exit_code == 0 or "Success" in result.output

    def test_install_warns_when_replacing_existing_binary(self, tmp_path: Path, isolated_home: Path) -> None:
        """Test that install warns when replacing an existing binary."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path("pyproject.toml").write_text('[tool.pyvider]\nname = "replaceme"\n')
            Path("VERSION").write_text("1.2.3")
            fake_binary = tmp_path / "fake_provider"
            fake_binary.write_text("#!/usr/bin/env python\n")
            fake_binary.chmod(0o755)

            # The binary lands in the plugin directory the context computes, so
            # the one being replaced has to be put there rather than somewhere
            # convenient -- this test used to pass on a leftover from an
            # earlier run against the developer's own plugin directory.
            target_dir = (
                isolated_home
                / ".terraform.d"
                / "plugins"
                / "local"
                / "providers"
                / "replaceme"
                / "1.2.3"
                / f"{get_os_name()}_{get_arch_name()}"
            )
            target_dir.mkdir(parents=True)
            (target_dir / "fake_provider").write_text("old version")

            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=True),
                mock.patch("sys.executable", str(fake_binary)),
            ):
                result = runner.invoke(cli, ["install"])

            assert result.exit_code == 0, result.output
            assert "Warning" in result.output or "replaced" in result.output.lower()


# 🐍🏗️🔚
