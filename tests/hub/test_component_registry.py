from unittest.mock import MagicMock, patch

import pytest

from pyvider.exceptions import ComponentRegistryError
from pyvider.hub.components import ComponentRegistry


def sample_function(): pass

@pytest.fixture
def test_hub() -> ComponentRegistry:
    """Provides a clean ComponentRegistry instance for each test."""
    return ComponentRegistry()

class TestComponentRegistry:
    def test_register_and_get_component(self, test_hub: ComponentRegistry):
        test_hub.register("resource", "sample_resource", sample_function)
        assert test_hub.get_component("resource", "sample_resource") == sample_function

    def test_get_nonexistent_component(self, test_hub: ComponentRegistry):
        assert test_hub.get_component("resource", "nonexistent") is None

    def test_unregister_component(self, test_hub: ComponentRegistry):
        test_hub.register("function", "temp_func", sample_function)
        test_hub.unregister("function", "temp_func")
        assert test_hub.get_component("function", "temp_func") is None

    def test_unregister_nonexistent_component_raises_error(self, test_hub: ComponentRegistry):
        with pytest.raises(ComponentRegistryError):
            test_hub.unregister("function", "nonexistent")

    @patch('pyvider.hub.components.logger')
    def test_register_duplicate_component_different_instance(self, mock_logger: MagicMock, test_hub: ComponentRegistry):
        test_hub.register("function", "sample_func", sample_function)
        def another_sample_function(): pass
        test_hub.register("function", "sample_func", another_sample_function)
        assert test_hub.get_component("function", "sample_func") == another_sample_function
        mock_logger.warning.assert_called_once()
        assert "is being replaced" in mock_logger.warning.call_args[0][0]

    @patch('pyvider.hub.components.logger')
    def test_register_duplicate_component_same_instance(self, mock_logger: MagicMock, test_hub: ComponentRegistry):
        test_hub.register("function", "sample_func", sample_function)
        test_hub.register("function", "sample_func", sample_function)

        found_log = any(
            "Skipping redundant registration" in call[0][0]
            for call in mock_logger.debug.call_args_list
        )
        assert found_log, "Expected 'Skipping redundant registration' debug log not found"


# 🐍🏗️🧪🪄
