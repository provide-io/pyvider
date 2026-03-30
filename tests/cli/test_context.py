#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI context module."""

from pathlib import Path
from typing import Any

from provide.testkit import mocking as mock  # type: ignore[import-untyped]
import pytest

from pyvider.cli.context import PyviderContext


class TestPyviderContextInitialization:
    """Tests for PyviderContext initialization."""

    def test_context_initializes_without_errors(self) -> None:
        """Test that PyviderContext initializes without errors."""
        ctx = PyviderContext()
        assert ctx is not None

    def test_context_has_config(self) -> None:
        """Test that context has config attribute."""
        ctx = PyviderContext()
        assert hasattr(ctx, "config")
        assert ctx.config is not None

    def test_context_has_home_directory(self) -> None:
        """Test that context has home directory set."""
        ctx = PyviderContext()
        assert ctx.home is not None
        assert isinstance(ctx.home, Path)
        assert ctx.home.exists()

    def test_context_has_local_bin_dir(self) -> None:
        """Test that context has local bin directory set."""
        ctx = PyviderContext()
        assert ctx.local_bin_dir is not None
        assert isinstance(ctx.local_bin_dir, Path)
        assert ctx.local_bin_dir == ctx.home / ".local" / "bin"

    def test_context_has_terraform_os(self) -> None:
        """Test that context has terraform OS set."""
        ctx = PyviderContext()
        assert ctx.tf_os is not None
        assert isinstance(ctx.tf_os, str)
        # Should be one of: darwin, linux, windows
        assert ctx.tf_os in ["darwin", "linux", "windows", "freebsd"]

    def test_context_has_terraform_arch(self) -> None:
        """Test that context has terraform architecture set."""
        ctx = PyviderContext()
        assert ctx.tf_arch is not None
        assert isinstance(ctx.tf_arch, str)
        # Should be one of: amd64, arm64, arm, 386
        assert ctx.tf_arch in ["amd64", "arm64", "arm", "386"]

    def test_context_has_pyvider_version(self) -> None:
        """Test that context has pyvider version set."""
        ctx = PyviderContext()
        assert ctx.pyvider_version is not None
        assert isinstance(ctx.pyvider_version, str)
        # Version should be non-empty
        assert len(ctx.pyvider_version) > 0

    def test_context_has_tf_plugin_dir(self) -> None:
        """Test that context has terraform plugin directory set."""
        ctx = PyviderContext()
        assert ctx.tf_plugin_dir is not None
        assert isinstance(ctx.tf_plugin_dir, Path)
        # Should be under home directory
        assert str(ctx.tf_plugin_dir).startswith(str(ctx.home))
        # Should contain .terraform.d
        assert ".terraform.d" in str(ctx.tf_plugin_dir)


class TestPyviderContextProviderName:
    """Tests for provider name reading from config."""

    def test_context_has_provider_name_attribute(self) -> None:
        """Test that context has provider_name attribute."""
        ctx = PyviderContext()
        assert hasattr(ctx, "provider_name")
        assert isinstance(ctx.provider_name, str)

    def test_provider_name_defaults_to_pyvider(self) -> None:
        """Test that provider_name defaults to 'pyvider' when no config exists."""
        ctx = PyviderContext()
        assert ctx.provider_name == "pyvider"

    def test_provider_name_from_pyvider_toml(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test reading provider name from pyvider.toml config file."""
        # Create a temporary pyvider.toml config file
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text('[pyvider]\nname = "myprovider"\n')

        # Set environment variable to use our config file
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        ctx = PyviderContext()
        assert ctx.provider_name == "myprovider"

    def test_provider_name_affects_plugin_path(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test that provider name is used in plugin directory path."""
        # Create config with custom provider name
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text('[pyvider]\nname = "custom"\n')

        # Set environment variable to use our config file
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        ctx = PyviderContext()
        assert "custom" in str(ctx.tf_plugin_dir)
        assert "pyvider" not in str(ctx.tf_plugin_dir).replace("\\", "/").split("/providers/")[1]


class TestPyviderContextPluginPath:
    """Tests for plugin path construction."""

    def test_plugin_path_structure(self) -> None:
        """Test that plugin path has correct structure."""
        ctx = PyviderContext()
        plugin_dir = ctx.tf_plugin_dir

        # Path should follow: ~/.terraform.d/plugins/local/providers/{name}/{version}/{os}_{arch}
        parts = plugin_dir.parts
        assert ".terraform.d" in parts
        assert "plugins" in parts
        assert "local" in parts
        assert "providers" in parts
        # Provider name should be in path (defaults to "pyvider" without config)
        assert ctx.provider_name in parts

    def test_plugin_path_contains_version(self) -> None:
        """Test that plugin path contains version."""
        ctx = PyviderContext()
        assert ctx.pyvider_version in str(ctx.tf_plugin_dir)

    def test_plugin_path_contains_platform(self) -> None:
        """Test that plugin path contains platform info."""
        ctx = PyviderContext()
        platform_string = f"{ctx.tf_os}_{ctx.tf_arch}"
        assert platform_string in str(ctx.tf_plugin_dir)


class TestPyviderContextComponentDiscovery:
    """Tests for component discovery in context."""

    def test_context_has_components_discovered_flag(self) -> None:
        """Test that context has components_discovered flag."""
        ctx = PyviderContext()
        assert hasattr(ctx, "components_discovered")
        assert isinstance(ctx.components_discovered, bool)
        # Initially should be False
        assert ctx.components_discovered is False

    def test_context_has_discovery_errors_list(self) -> None:
        """Test that context has discovery_errors list."""
        ctx = PyviderContext()
        assert hasattr(ctx, "discovery_errors")
        assert isinstance(ctx.discovery_errors, list)
        # Initially should be empty
        assert len(ctx.discovery_errors) == 0

    @pytest.mark.asyncio
    async def test_ensure_components_discovered_runs(self) -> None:
        """Test that _ensure_components_discovered can be called."""
        ctx = PyviderContext()

        # Mock the registry and discovery
        mock_registry = mock.MagicMock()
        mock_discovery_cls = mock.MagicMock()
        mock_discovery_instance = mock.MagicMock()
        mock_discovery_instance.discover_all = mock.AsyncMock()
        mock_discovery_instance.import_errors = []
        mock_discovery_cls.return_value = mock_discovery_instance

        await ctx._ensure_components_discovered(mock_registry, mock_discovery_cls, print, print)

        assert ctx.components_discovered is True
        assert mock_discovery_instance.discover_all.called

    @pytest.mark.asyncio
    async def test_ensure_components_discovered_only_runs_once(self) -> None:
        """Test that _ensure_components_discovered only runs once."""
        ctx = PyviderContext()
        ctx.components_discovered = True  # Already discovered

        # Mock the discovery
        mock_registry = mock.MagicMock()
        mock_discovery_cls = mock.MagicMock()
        mock_discovery_instance = mock.MagicMock()
        mock_discovery_instance.discover_all = mock.AsyncMock()
        mock_discovery_cls.return_value = mock_discovery_instance

        await ctx._ensure_components_discovered(mock_registry, mock_discovery_cls, print, print)

        # Discovery should not have been called
        assert not mock_discovery_instance.discover_all.called

    @pytest.mark.asyncio
    async def test_ensure_components_discovered_captures_errors(self) -> None:
        """Test that _ensure_components_discovered captures import errors."""
        ctx = PyviderContext()

        # Mock the registry and discovery with errors
        mock_registry = mock.MagicMock()
        mock_discovery_cls = mock.MagicMock()
        mock_discovery_instance = mock.MagicMock()
        mock_discovery_instance.discover_all = mock.AsyncMock()
        mock_discovery_instance.import_errors = [("test_module", ImportError("Test error"))]
        mock_discovery_cls.return_value = mock_discovery_instance

        await ctx._ensure_components_discovered(mock_registry, mock_discovery_cls, print, print)

        assert ctx.components_discovered is True
        assert len(ctx.discovery_errors) == 1
        assert ctx.discovery_errors[0][0] == "test_module"

    @pytest.mark.asyncio
    async def test_ensure_components_discovered_handles_discovery_failure(self) -> None:
        """Test that _ensure_components_discovered handles discovery failures."""
        ctx = PyviderContext()

        # Mock the registry and discovery to raise an error
        mock_registry = mock.MagicMock()
        mock_discovery_cls = mock.MagicMock()
        mock_discovery_instance = mock.MagicMock()
        mock_discovery_instance.discover_all = mock.AsyncMock(side_effect=RuntimeError("Discovery failed"))
        mock_discovery_cls.return_value = mock_discovery_instance

        await ctx._ensure_components_discovered(mock_registry, mock_discovery_cls, print, print)

        # Should have captured the error
        assert ctx.components_discovered is False
        assert len(ctx.discovery_errors) == 1
        assert ctx.discovery_errors[0][0] == "discovery_runner"


class TestPyviderContextInheritance:
    """Tests for PyviderContext inheritance from CLIContext."""

    def test_context_inherits_from_cli_context(self) -> None:
        """Test that PyviderContext inherits from foundation's CLIContext."""
        from provide.foundation.context import CLIContext

        ctx = PyviderContext()
        assert isinstance(ctx, CLIContext)

    def test_context_has_foundation_attributes(self) -> None:
        """Test that context has attributes from foundation CLIContext."""
        ctx = PyviderContext()
        # CLIContext should provide these
        assert hasattr(ctx, "log_level")
        assert hasattr(ctx, "log_format")


class TestPyviderContextEdgeCases:
    """Edge case tests for PyviderContext."""

    def test_context_handles_missing_version_config(self) -> None:
        """Test that context handles missing version in config."""
        with mock.patch("pyvider.cli.context._read_version_from_file", return_value="0.1.0"):
            # Should use the version from _read_version_from_file
            ctx = PyviderContext()
            assert ctx.pyvider_version == "0.1.0"

    def test_multiple_context_instances_are_independent(self) -> None:
        """Test that multiple context instances are independent."""
        ctx1 = PyviderContext()
        ctx2 = PyviderContext()

        assert ctx1 is not ctx2

        # Modifying one shouldn't affect the other
        ctx1.components_discovered = True
        assert ctx2.components_discovered is False

    def test_context_discovery_errors_are_mutable(self) -> None:
        """Test that discovery_errors can be modified."""
        ctx = PyviderContext()

        test_error = ("test_module", ImportError("test"))
        ctx.discovery_errors.append(test_error)

        assert len(ctx.discovery_errors) == 1
        assert ctx.discovery_errors[0] == test_error

    @pytest.mark.asyncio
    async def test_ensure_components_discovered_with_non_strict_mode(self) -> None:
        """Test that discovery runs in non-strict mode."""
        ctx = PyviderContext()

        # Mock the discovery
        mock_registry = mock.MagicMock()
        mock_discovery_cls = mock.MagicMock()
        mock_discovery_instance = mock.MagicMock()
        mock_discovery_instance.discover_all = mock.AsyncMock()
        mock_discovery_instance.import_errors = []
        mock_discovery_cls.return_value = mock_discovery_instance

        await ctx._ensure_components_discovered(mock_registry, mock_discovery_cls, print, print)

        # Verify discover_all was called with strict=False
        mock_discovery_instance.discover_all.assert_called_once_with(strict=False)


# 🐍🏗️🔚
