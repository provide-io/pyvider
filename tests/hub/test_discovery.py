#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ComponentDiscovery."""

from abc import ABC, abstractmethod
from unittest.mock import MagicMock, patch

import pytest

from pyvider.hub.components import ComponentRegistry
from pyvider.hub.discovery import ComponentDiscovery


@pytest.fixture
def hub() -> ComponentRegistry:
    """Create a test hub."""
    return ComponentRegistry()


@pytest.fixture
def discovery(hub: ComponentRegistry) -> ComponentDiscovery:
    """Create a discovery instance."""
    return ComponentDiscovery(hub)


class TestComponentDiscoveryInit:
    """Test ComponentDiscovery initialization."""

    def test_init_with_hub(self, hub: ComponentRegistry) -> None:
        """Test initialization with hub."""
        discovery = ComponentDiscovery(hub)

        assert discovery.hub is hub
        assert discovery._discovered_modules == set()
        assert discovery.import_errors == []


class TestDiscoverAll:
    """Test discover_all method."""

    @pytest.mark.asyncio
    async def test_discover_all_no_entry_points(self, discovery: ComponentDiscovery) -> None:
        """Test discover_all when no entry points are found."""
        # Mock entry_points to return empty
        with patch("importlib.metadata.entry_points") as mock_entry_points:
            mock_entry_points.return_value = []

            with patch.object(discovery, "_discover_package") as mock_discover:
                await discovery.discover_all()

                # Should not discover anything when no entry points exist
                mock_discover.assert_not_called()

    @pytest.mark.asyncio
    async def test_discover_all_with_entry_points(self, discovery: ComponentDiscovery) -> None:
        """Test discover_all when entry points are found."""
        # Create mock entry points
        mock_ep1 = MagicMock()
        mock_ep1.name = "test_package"
        mock_ep1.value = "test.module"

        mock_ep2 = MagicMock()
        mock_ep2.name = "another_package"
        mock_ep2.value = "another.module"

        with patch("importlib.metadata.entry_points") as mock_entry_points:
            mock_entry_points.return_value = [mock_ep1, mock_ep2]

            with patch.object(discovery, "_discover_package") as mock_discover:
                await discovery.discover_all()

                # Should discover both entry points
                assert mock_discover.call_count == 2
                mock_discover.assert_any_call("test.module", strict=False)
                mock_discover.assert_any_call("another.module", strict=False)

    @pytest.mark.asyncio
    async def test_discover_all_entry_points_query_error(self, discovery: ComponentDiscovery) -> None:
        """Test discover_all when querying entry points fails."""
        with patch("importlib.metadata.entry_points") as mock_entry_points:
            mock_entry_points.side_effect = RuntimeError("Entry point query failed")

            # Should not raise, just log error and return
            await discovery.discover_all()

            # No packages should be discovered
            assert len(discovery._discovered_modules) == 0

    @pytest.mark.asyncio
    async def test_discover_all_strict_mode(self, discovery: ComponentDiscovery) -> None:
        """Test discover_all in strict mode propagates errors."""
        # Create a mock entry point that will trigger an error
        mock_ep = MagicMock()
        mock_ep.name = "test_package"
        mock_ep.value = "test.module"

        with patch("importlib.metadata.entry_points") as mock_entry_points:
            mock_entry_points.return_value = [mock_ep]

            with patch.object(discovery, "_discover_package") as mock_discover:
                mock_discover.side_effect = ImportError("Test import error")

                with pytest.raises(ImportError, match="Test import error"):
                    await discovery.discover_all(strict=True)


class TestDiscoverPackage:
    """Test _discover_package method."""

    @pytest.mark.asyncio
    async def test_discover_package_success(self, discovery: ComponentDiscovery) -> None:
        """Test successful package discovery via fallback (no register_components)."""
        mock_module = MagicMock(spec=[])  # Empty spec so register_components is absent
        mock_module.__name__ = "test.module"
        mock_module.__path__ = []  # Not a package with submodules

        with patch("importlib.import_module") as mock_import:
            mock_import.return_value = mock_module

            with patch.object(discovery, "_process_module") as mock_process:
                await discovery._discover_package("test.module", strict=False)

                mock_import.assert_called_once_with("test.module")
                mock_process.assert_called_once_with(mock_module)
                assert "test.module" in discovery._discovered_modules

    @pytest.mark.asyncio
    async def test_discover_package_already_discovered(self, discovery: ComponentDiscovery) -> None:
        """Test that already discovered packages are skipped."""
        discovery._discovered_modules.add("test.module")

        with patch("importlib.import_module") as mock_import:
            await discovery._discover_package("test.module", strict=False)

            # Should not attempt to import
            mock_import.assert_not_called()

    @pytest.mark.asyncio
    async def test_discover_package_import_error_non_strict(self, discovery: ComponentDiscovery) -> None:
        """Test ImportError handling in non-strict mode."""
        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = ImportError("Module not found")

            # Should not raise in non-strict mode
            await discovery._discover_package("nonexistent.module", strict=False)

            # Error should be recorded
            assert len(discovery.import_errors) == 1
            assert discovery.import_errors[0][0] == "nonexistent.module"
            assert isinstance(discovery.import_errors[0][1], ImportError)

    @pytest.mark.asyncio
    async def test_discover_package_import_error_strict(self, discovery: ComponentDiscovery) -> None:
        """Test ImportError handling in strict mode."""
        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = ImportError("Module not found")

            # Should raise in strict mode
            with pytest.raises(ImportError, match="Module not found"):
                await discovery._discover_package("nonexistent.module", strict=True)

    @pytest.mark.asyncio
    async def test_discover_package_module_not_found_error(self, discovery: ComponentDiscovery) -> None:
        """Test ModuleNotFoundError handling."""
        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = ModuleNotFoundError("No module named 'test'")

            # Should not raise in non-strict mode
            await discovery._discover_package("test.module", strict=False)

            # Error should be recorded
            assert len(discovery.import_errors) == 1
            assert discovery.import_errors[0][0] == "test.module"
            assert isinstance(discovery.import_errors[0][1], ModuleNotFoundError)

    @pytest.mark.asyncio
    async def test_discover_package_generic_exception_non_strict(self, discovery: ComponentDiscovery) -> None:
        """Test generic exception handling in non-strict mode."""
        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = RuntimeError("Unexpected error")

            # Should not raise in non-strict mode
            await discovery._discover_package("test.module", strict=False)

            # Error should be recorded
            assert len(discovery.import_errors) == 1
            assert discovery.import_errors[0][0] == "test.module"
            assert isinstance(discovery.import_errors[0][1], RuntimeError)

    @pytest.mark.asyncio
    async def test_discover_package_generic_exception_strict(self, discovery: ComponentDiscovery) -> None:
        """Test generic exception handling in strict mode."""
        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = RuntimeError("Unexpected error")

            # Should raise in strict mode
            with pytest.raises(RuntimeError, match="Unexpected error"):
                await discovery._discover_package("test.module", strict=True)


class TestProcessModule:
    """Test _process_module method."""

    @pytest.mark.asyncio
    async def test_process_module_with_registered_resource(self, discovery: ComponentDiscovery) -> None:
        """Test processing module with registered resource."""

        class TestResource:
            _is_registered_resource = True
            _registered_name = "test_resource"

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("TestResource", TestResource)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = True

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    with patch("inspect.isabstract") as mock_isabstract:
                        mock_isabstract.return_value = False

                        await discovery._process_module(mock_module)

                        # Should register resource
                        assert discovery.hub.get_component("resource", "test_resource") == TestResource

    @pytest.mark.asyncio
    async def test_process_module_with_registered_data_source(self, discovery: ComponentDiscovery) -> None:
        """Test processing module with registered data source."""

        class TestDataSource:
            _is_registered_data_source = True
            _registered_name = "test_data_source"

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("TestDataSource", TestDataSource)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = True

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    with patch("inspect.isabstract") as mock_isabstract:
                        mock_isabstract.return_value = False

                        await discovery._process_module(mock_module)

                        # Should register data source
                        assert discovery.hub.get_component("data_source", "test_data_source") == TestDataSource

    @pytest.mark.asyncio
    async def test_process_module_with_registered_function(self, discovery: ComponentDiscovery) -> None:
        """Test processing module with registered function."""

        def test_function() -> None:
            pass

        test_function._is_registered_function = True
        test_function._registered_name = "test_function"

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("test_function", test_function)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = False

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = True

                    await discovery._process_module(mock_module)

                    # Should register function
                    assert discovery.hub.get_component("function", "test_function") == test_function

    @pytest.mark.asyncio
    async def test_process_module_with_registered_capability(self, discovery: ComponentDiscovery) -> None:
        """Test processing module with registered capability."""

        class TestCapability:
            _is_registered_capability = True
            _registered_name = "test_capability"

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("TestCapability", TestCapability)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = True

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    with patch("inspect.isabstract") as mock_isabstract:
                        mock_isabstract.return_value = False

                        await discovery._process_module(mock_module)

                        # Should register capability
                        assert discovery.hub.get_component("capability", "test_capability") == TestCapability

    @pytest.mark.asyncio
    async def test_process_module_skips_abstract_classes(self, discovery: ComponentDiscovery) -> None:
        """Test that abstract classes are skipped."""

        class AbstractTestClass(ABC):
            _is_registered_resource = True
            _registered_name = "abstract_resource"

            @abstractmethod
            def abstract_method(self) -> None:
                pass

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("AbstractTestClass", AbstractTestClass)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = True

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    with patch("inspect.isabstract") as mock_isabstract:
                        mock_isabstract.return_value = True

                        await discovery._process_module(mock_module)

                        # Should not register abstract class
                        assert discovery.hub.get_component("resource", "abstract_resource") is None

    @pytest.mark.asyncio
    async def test_process_module_skips_non_class_non_function(self, discovery: ComponentDiscovery) -> None:
        """Test that non-class, non-function objects are skipped."""
        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("some_variable", "value"), ("some_int", 42)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = False

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    await discovery._process_module(mock_module)

                    # Should not register anything
                    assert len(discovery.hub.list_components()) == 0

    @pytest.mark.asyncio
    async def test_process_module_without_registered_name(self, discovery: ComponentDiscovery) -> None:
        """Test that components without _registered_name are not registered."""

        class TestResourceNoName:
            _is_registered_resource = True
            # Missing _registered_name

        mock_module = MagicMock()
        mock_module.__name__ = "test.module"

        with patch("inspect.getmembers") as mock_members:
            mock_members.return_value = [("TestResourceNoName", TestResourceNoName)]

            with patch("inspect.isclass") as mock_isclass:
                mock_isclass.return_value = True

                with patch("inspect.isfunction") as mock_isfunction:
                    mock_isfunction.return_value = False

                    with patch("inspect.isabstract") as mock_isabstract:
                        mock_isabstract.return_value = False

                        await discovery._process_module(mock_module)

                        # Should not register (no name)
                        components = discovery.hub.list_components()
                        assert len(components.get("resource", [])) == 0


# 🐍🏗️🔚
