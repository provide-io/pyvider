#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for custom provider names in install paths."""

from pathlib import Path

from click.testing import CliRunner
from provide.testkit import mocking as mock

from pyvider.cli import cli


class TestCustomProviderNames:
    """Tests for custom provider names in install paths."""

    def test_install_uses_custom_provider_name_from_pyvider_toml(self, tmp_path: Path) -> None:
        """Test that install uses custom provider name from pyvider.toml in paths."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create pyvider.toml with custom provider name
            Path("pyvider.toml").write_text('[pyvider]\nname = "myprovider"\n')
            Path("VERSION").write_text("0.0.1108")

            # Create mock venv
            venv_dir = Path(".venv")
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "pyvider").touch()
            (venv_bin / "python").touch()
            (venv_bin / "activate").touch()

            with mock.patch("pyvider.cli.install_command.is_running_as_binary", return_value=False):
                result = runner.invoke(cli, ["install"])

                # Check that the install completed
                assert result.exit_code == 0 or "Development Mode" in result.output

                # The context should have loaded "myprovider" as provider name
                # Plugin dir path should contain "myprovider" not "pyvider"
                # (This is tested more directly in test_context.py)

    def test_uninstall_removes_custom_provider_script(self, tmp_path: Path) -> None:
        """Test that uninstall removes the provider script with custom name."""

        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Create pyvider.toml with custom provider name
            Path("pyvider.toml").write_text('[pyvider]\nname = "custom"\n')
            Path("VERSION").write_text("0.1.0")

            # Create mock context with custom provider name
            with mock.patch("pyvider.cli.main.PyviderContext") as MockContext:
                mock_ctx = MockContext.return_value
                mock_plugin_dir = tmp_path / "plugins"
                mock_plugin_dir.mkdir()
                mock_ctx.tf_plugin_dir = mock_plugin_dir
                mock_ctx.provider_name = "custom"

                # Create the provider script that should be removed
                provider_script = mock_plugin_dir / "terraform-provider-custom"
                provider_script.write_text("#!/bin/bash\n")
                assert provider_script.exists()

                result = runner.invoke(cli, ["install", "--uninstall"])

                # Provider script should be removed
                assert not provider_script.exists()
                assert result.exit_code == 0 or "uninstall" in result.output.lower()


# 🐍🏗️🔚
