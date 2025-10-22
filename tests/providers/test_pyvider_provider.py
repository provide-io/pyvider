"""Tests for pyvider/providers/provider.py - the main provider orchestrator."""

import pytest

from pyvider.exceptions import FrameworkConfigurationError
from pyvider.hub import hub
from pyvider.providers.provider import PyviderProvider
from pyvider.providers.context import ProviderContext


class TestPyviderProviderInitialization:
    """Tests for PyviderProvider initialization."""

    def test_provider_initialization(self):
        """Test that PyviderProvider initializes correctly."""
        provider = PyviderProvider()
        assert provider.metadata.name == "pyvider"
        assert provider.metadata.version == "0.1.0"
        assert isinstance(provider.capabilities, dict)

    def test_provider_has_class_level_capabilities(self):
        """Test that capabilities is a ClassVar dict."""
        # Class variable should exist
        assert hasattr(PyviderProvider, "capabilities")


class TestPyviderProviderSetup:
    """Tests for PyviderProvider setup process."""

    @pytest.fixture(autouse=True)
    def cleanup_hub(self):
        """Clean up hub after each test."""
        yield
        # Clean up any registered components
        if hub.get_component("singleton", "provider"):
            hub.unregister("singleton", "provider")
        if hub.get_component("singleton", "provider_context"):
            hub.unregister("singleton", "provider_context")

    async def test_setup_creates_schema(self):
        """Test that setup creates the provider schema."""
        provider = PyviderProvider()
        await provider.setup()

        # Schema should be created
        assert provider._final_schema is not None
        assert provider.config_class is not None

    async def test_setup_registers_self_as_capability(self):
        """Test that setup registers provider as 'provider' capability."""
        provider = PyviderProvider()
        await provider.setup()

        # Provider should be registered as a capability
        assert "provider" in provider.capabilities
        assert provider.capabilities["provider"] is provider

    async def test_setup_processes_capabilities(self):
        """Test that setup processes registered capabilities."""
        from pyvider.capabilities.base import BaseCapability

        # Create a mock capability
        class MockCapability(BaseCapability):
            def get_schema_contribution(self):
                return {"test_attr": "value"}

        # Register it
        hub.register("capability", "mock_cap", MockCapability)

        try:
            provider = PyviderProvider()
            await provider.setup()

            # Capability should be instantiated
            assert "mock_cap" in provider.capabilities
        finally:
            # Clean up
            hub.unregister("capability", "mock_cap")

    async def test_setup_validates_component_capabilities(self):
        """Test that setup validates components reference valid capabilities."""
        # Create a mock component with invalid capability reference
        class MockComponent:
            _parent_capability = "nonexistent_capability"

        # Register it
        hub.register("resource", "bad_component", MockComponent)

        try:
            provider = PyviderProvider()
            with pytest.raises(
                FrameworkConfigurationError,
                match="associated with capability 'nonexistent_capability'",
            ):
                await provider.setup()
        finally:
            # Clean up
            hub.unregister("resource", "bad_component")

    async def test_setup_allows_components_with_provider_capability(self):
        """Test that components can reference 'provider' capability."""

        class MockComponent:
            _parent_capability = "provider"

        # Register it
        hub.register("data_source", "valid_component", MockComponent)

        try:
            provider = PyviderProvider()
            # Should not raise
            await provider.setup()
        finally:
            # Clean up
            hub.unregister("data_source", "valid_component")

    async def test_setup_with_provider_context(self):
        """Test setup with provider context in hub."""
        provider_ctx = ProviderContext(config={"test": "config"})
        hub.register("singleton", "provider_context", provider_ctx)

        try:
            provider = PyviderProvider()
            await provider.setup()

            # Should complete successfully
            assert provider._final_schema is not None
        finally:
            hub.unregister("singleton", "provider_context")

    async def test_setup_without_provider_context(self):
        """Test setup without provider context in hub."""
        # Ensure no provider context
        if hub.get_component("singleton", "provider_context"):
            hub.unregister("singleton", "provider_context")

        provider = PyviderProvider()
        # Should not raise even without context
        await provider.setup()
        assert provider._final_schema is not None

    async def test_setup_creates_config_class_from_schema(self):
        """Test that setup creates a config class from the schema."""
        provider = PyviderProvider()
        await provider.setup()

        # Config class should be created and named appropriately
        assert provider.config_class is not None
        assert provider.config_class.__name__ == "ProviderConfig"


class TestPyviderProviderCapabilityIntegration:
    """Tests for capability integration in PyviderProvider."""

    @pytest.fixture(autouse=True)
    def cleanup_hub(self):
        """Clean up hub after each test."""
        yield
        # Clean up
        for cap_name in ["test_cap_1", "test_cap_2"]:
            if hub.get_component("capability", cap_name):
                hub.unregister("capability", cap_name)

    async def test_multiple_capabilities_contribute_to_schema(self):
        """Test that multiple capabilities can contribute to the schema."""
        from pyvider.capabilities.base import BaseCapability

        class Capability1(BaseCapability):
            def get_schema_contribution(self):
                return {"attr1": "value1"}

        class Capability2(BaseCapability):
            def get_schema_contribution(self):
                return {"attr2": "value2"}

        hub.register("capability", "test_cap_1", Capability1)
        hub.register("capability", "test_cap_2", Capability2)

        provider = PyviderProvider()
        await provider.setup()

        # Both capabilities should be registered
        assert "test_cap_1" in provider.capabilities
        assert "test_cap_2" in provider.capabilities

    async def test_capability_without_schema_contribution(self):
        """Test capability that doesn't contribute to schema."""
        from pyvider.capabilities.base import BaseCapability

        class MinimalCapability(BaseCapability):
            # No get_schema_contribution method
            pass

        hub.register("capability", "minimal_cap", MinimalCapability)

        try:
            provider = PyviderProvider()
            # Should not raise even if capability has no schema contribution
            await provider.setup()
            assert "minimal_cap" in provider.capabilities
        finally:
            hub.unregister("capability", "minimal_cap")
