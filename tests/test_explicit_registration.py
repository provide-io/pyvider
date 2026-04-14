#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the explicit register_components discovery protocol."""

import types
from unittest.mock import MagicMock, patch

import pytest

from pyvider.hub.components import ComponentRegistry
from pyvider.hub.discovery import ComponentDiscovery


class TestExplicitRegistration:
    """Test the register_components fast path in discovery."""

    @pytest.mark.asyncio
    async def test_register_components_function_called(self) -> None:
        """When a package has register_components(hub), it should be called
        and pkgutil.walk_packages should NOT be invoked."""
        hub = ComponentRegistry()
        discovery = ComponentDiscovery(hub)

        mock_package = types.ModuleType("mock_components")
        mock_register = MagicMock()
        mock_package.register_components = mock_register  # type: ignore[attr-defined]

        with patch.object(discovery, "_process_module") as mock_process:
            # Patch importlib.import_module at the module where it's used
            import pyvider.hub.discovery as disc_mod

            original_import = disc_mod.importlib.import_module
            disc_mod.importlib.import_module = lambda name: mock_package  # type: ignore[assignment]
            try:
                await discovery._discover_package("mock_components", strict=False)
            finally:
                disc_mod.importlib.import_module = original_import  # type: ignore[assignment]

        mock_register.assert_called_once_with(hub)
        # _process_module should NOT be called (fast path skips it)
        mock_process.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_register_components_function_called(self) -> None:
        """When register_components is async, it should be awaited."""
        hub = ComponentRegistry()
        discovery = ComponentDiscovery(hub)

        mock_package = types.ModuleType("mock_async_components")
        call_args: list[ComponentRegistry] = []

        async def async_register(h: ComponentRegistry) -> None:
            call_args.append(h)

        mock_package.register_components = async_register  # type: ignore[attr-defined]

        import pyvider.hub.discovery as disc_mod

        original_import = disc_mod.importlib.import_module
        disc_mod.importlib.import_module = lambda name: mock_package  # type: ignore[assignment]
        try:
            await discovery._discover_package("mock_async_components", strict=False)
        finally:
            disc_mod.importlib.import_module = original_import  # type: ignore[assignment]

        assert call_args == [hub]

    @pytest.mark.asyncio
    async def test_fallback_to_walk_when_no_register_function(self) -> None:
        """Without register_components, discovery should fall back to
        walking packages and scanning for markers."""
        hub = ComponentRegistry()
        discovery = ComponentDiscovery(hub)

        mock_package = types.ModuleType("plain_package")
        mock_package.__path__ = ["/fake/path"]  # type: ignore[attr-defined]

        import pyvider.hub.discovery as disc_mod

        original_import = disc_mod.importlib.import_module
        original_walk = disc_mod.pkgutil.walk_packages
        disc_mod.importlib.import_module = lambda name: mock_package  # type: ignore[assignment]
        disc_mod.pkgutil.walk_packages = lambda *a, **kw: iter([])  # type: ignore[assignment]
        try:
            with patch.object(discovery, "_process_module") as mock_process:
                await discovery._discover_package("plain_package", strict=False)
        finally:
            disc_mod.importlib.import_module = original_import  # type: ignore[assignment]
            disc_mod.pkgutil.walk_packages = original_walk  # type: ignore[assignment]

        mock_process.assert_called_once_with(mock_package)

    @pytest.mark.asyncio
    async def test_register_components_registers_in_hub(self) -> None:
        """Verify that register_components can actually register components."""
        hub = ComponentRegistry()
        discovery = ComponentDiscovery(hub)

        mock_package = types.ModuleType("real_registration")

        def register(h: ComponentRegistry) -> None:
            h.register("resource", "test_resource", MagicMock)
            h.register("data_source", "test_ds", MagicMock)

        mock_package.register_components = register  # type: ignore[attr-defined]

        import pyvider.hub.discovery as disc_mod

        original_import = disc_mod.importlib.import_module
        disc_mod.importlib.import_module = lambda name: mock_package  # type: ignore[assignment]
        try:
            await discovery._discover_package("real_registration", strict=False)
        finally:
            disc_mod.importlib.import_module = original_import  # type: ignore[assignment]

        assert hub.get_component("resource", "test_resource") is MagicMock
        assert hub.get_component("data_source", "test_ds") is MagicMock

    @pytest.mark.asyncio
    async def test_discovery_skips_already_discovered_packages(self) -> None:
        """Packages should only be discovered once."""
        hub = ComponentRegistry()
        discovery = ComponentDiscovery(hub)

        mock_package = types.ModuleType("once_only")
        mock_register = MagicMock()
        mock_package.register_components = mock_register  # type: ignore[attr-defined]

        import pyvider.hub.discovery as disc_mod

        original_import = disc_mod.importlib.import_module
        disc_mod.importlib.import_module = lambda name: mock_package  # type: ignore[assignment]
        try:
            await discovery._discover_package("once_only", strict=False)
            await discovery._discover_package("once_only", strict=False)
        finally:
            disc_mod.importlib.import_module = original_import  # type: ignore[assignment]

        mock_register.assert_called_once()


# 🐍🏗️🔚
