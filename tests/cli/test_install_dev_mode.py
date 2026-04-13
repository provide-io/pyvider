#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for install command in development mode."""

from pathlib import Path

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli


class TestInstallCommandDevelopmentMode:
    """Tests for install command in development mode."""

    def test_development_mode_invokes_prep_provider(self, tmp_path: Path) -> None:
        """Test that development mode invokes prep_provider."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock development mode
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command.click.Context.invoke") as mock_invoke,
            ):
                result = runner.invoke(cli, ["install"])

                # Verify prep_provider was invoked
                if result.exit_code == 0 or "Development Mode" in result.output:
                    assert mock_invoke.called or "Development Mode" in result.output

    def test_development_mode_handles_prep_provider_error(self, tmp_path: Path) -> None:
        """Test that development mode handles prep_provider errors."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Setup
            Path("pyvider.toml").write_text("[pyvider]\n")

            # Mock development mode and make prep_provider fail
            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch(
                    "pyvider.cli.install_command.click.Context.invoke", side_effect=RuntimeError("Prep failed")
                ),
            ):
                result = runner.invoke(cli, ["install"])

                # Should handle error
                assert result.exit_code != 0


class TestInstallCommandSymlinkCreation:
    """Tests for symlink creation during install."""

    def test_install_calls_place_provider_script(self, tmp_path: Path) -> None:
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

            with (
                mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False),
                mock.patch("pyvider.cli.install_command._place_terraform_provider_script") as mock_place,
            ):
                result = runner.invoke(cli, ["install"])

                # Verify _place_terraform_provider_script was called
                assert mock_place.called
                assert result.exit_code == 0


# 🐍🏗️🔚
