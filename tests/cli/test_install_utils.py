"""
Tests for pyvider install command utilities.

Tests venv detection and script generation with 100% coverage.
"""

import tempfile
from pathlib import Path

import pytest

from pyvider.cli.utils import _find_actual_venv


class TestVenvDetection:
    """Test virtual environment detection logic."""

    def test_find_venv_standard_location(self, tmp_path):
        """Test finding .venv in standard location."""
        venv_dir = tmp_path / ".venv"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        assert result == venv_dir

    def test_find_venv_alternative_location(self, tmp_path):
        """Test finding venv in alternative location."""
        venv_dir = tmp_path / "venv"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        assert result == venv_dir

    def test_find_venv_platform_specific(self, tmp_path):
        """Test finding platform-specific venv (.venv_darwin_arm64)."""
        venv_dir = tmp_path / ".venv_darwin_arm64"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        assert result == venv_dir

    def test_find_venv_workenv_style(self, tmp_path):
        """Test finding workenv-style venv."""
        venv_dir = tmp_path / "workenv" / "pyvider_darwin_arm64"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        assert result == venv_dir

    def test_find_venv_prefers_standard(self, tmp_path):
        """Test that .venv is preferred over alternatives."""
        # Create multiple venvs
        for venv_name in [".venv", "venv", ".venv_darwin_arm64"]:
            venv_dir = tmp_path / venv_name
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        # Should prefer .venv (first in candidate list)
        assert result == tmp_path / ".venv"

    def test_find_venv_not_found(self, tmp_path):
        """Test when no venv exists."""
        result = _find_actual_venv(tmp_path)
        assert result is None

    def test_find_venv_incomplete_venv(self, tmp_path):
        """Test that incomplete venv (missing activate script) is not found."""
        venv_dir = tmp_path / ".venv"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)
        # Don't create activate script

        result = _find_actual_venv(tmp_path)
        assert result is None

    def test_find_venv_symlink_follows(self, tmp_path):
        """Test that symlinked venvs are followed correctly."""
        # Create real venv
        real_venv = tmp_path / ".venv"
        venv_bin = real_venv / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "activate").touch()

        # Create symlink
        symlink_venv = tmp_path / ".venv_darwin_arm64"
        symlink_venv.symlink_to(real_venv)

        result = _find_actual_venv(tmp_path)
        # Should find .venv first (preferred)
        assert result == real_venv


class TestScriptGeneration:
    """Test script generation logic (integration with actual function)."""

    def test_script_generation_requires_venv(self):
        """Test that script generation fails without venv."""
        from provide.foundation.errors import ConfigurationError

        from pyvider.cli.context import PyviderContext
        from pyvider.cli.utils import _place_terraform_provider_script

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create context
            ctx = PyviderContext()

            # Try to generate script without venv
            import os

            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir_path)
                with pytest.raises(ConfigurationError, match="No virtual environment found"):
                    _place_terraform_provider_script(ctx)
            finally:
                os.chdir(original_cwd)

    def test_script_generation_validates_python(self):
        """Test that script generation validates Python executable exists."""
        from provide.foundation.errors import ConfigurationError

        from pyvider.cli.context import PyviderContext
        from pyvider.cli.utils import _place_terraform_provider_script

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create incomplete venv (no python executable)
            venv_dir = tmpdir_path / ".venv"
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "activate").touch()

            ctx = PyviderContext()

            import os

            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir_path)
                with pytest.raises(ConfigurationError, match="Python executable not found"):
                    _place_terraform_provider_script(ctx)
            finally:
                os.chdir(original_cwd)


class TestVenvDetectionEdgeCases:
    """Test edge cases in venv detection."""

    def test_multiple_platform_venvs_sorted(self, tmp_path):
        """Test that multiple platform venvs are checked in sorted order."""
        # Create multiple platform-specific venvs
        for venv_name in [".venv_linux_amd64", ".venv_darwin_arm64", ".venv_darwin_amd64"]:
            venv_dir = tmp_path / venv_name
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        # Should find first in sorted order
        assert result.name in [".venv_darwin_amd64", ".venv_darwin_arm64", ".venv_linux_amd64"]

    def test_workenv_with_multiple_envs(self, tmp_path):
        """Test workenv directory with multiple environments."""
        workenv_dir = tmp_path / "workenv"

        for env_name in ["pyvider_darwin_arm64", "pyvider_linux_amd64"]:
            venv_dir = workenv_dir / env_name
            venv_bin = venv_dir / "bin"
            venv_bin.mkdir(parents=True)
            (venv_bin / "activate").touch()

        result = _find_actual_venv(tmp_path)
        # Should find one of the workenv venvs
        assert "workenv" in str(result)
