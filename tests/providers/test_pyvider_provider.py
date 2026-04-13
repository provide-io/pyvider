#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for PyviderProvider."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.exceptions import FrameworkConfigurationError
from pyvider.providers.provider import PyviderProvider


class TestPyviderProviderInitialization:
    """Tests for PyviderProvider initialization."""

    def test_provider_initializes_with_correct_metadata(self) -> None:
        """Test that PyviderProvider initializes with correct metadata."""
        provider = PyviderProvider()
        assert provider.metadata.name == "pyvider"
        assert provider.metadata.version == "0.1.0"
        assert provider._configured is False

    def test_provider_has_empty_capabilities_initially(self) -> None:
        """Test that a fresh PyviderProvider starts with an empty, per-instance capabilities dict."""
        provider = PyviderProvider()
        assert isinstance(provider.capabilities, dict)
        assert provider.capabilities == {}


class TestPyviderProviderSetup:
    """Tests for PyviderProvider setup method."""

    @pytest.mark.asyncio
    async def test_setup_creates_schema_with_pyvider_testmode(self) -> None:
        """Test that setup creates schema with pyvider_testmode attribute."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            # Mock hub to return no capabilities and components
            mock_hub.get_components.side_effect = lambda comp_type: {}
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            await provider.setup()

            assert provider._final_schema is not None
            assert "pyvider_testmode" in provider._final_schema.block.attributes
            assert provider.config_class is not None

    @pytest.mark.asyncio
    async def test_setup_aggregates_capability_schemas(self) -> None:
        """Test that setup aggregates schema contributions from capabilities."""
        from pyvider.schema import a_str

        with patch("pyvider.providers.provider.hub") as mock_hub:
            # Create a mock capability with schema contribution
            mock_cap_class = MagicMock()
            mock_cap_instance = MagicMock()
            # Use a real attribute instead of MagicMock
            mock_cap_instance.get_schema_contribution.return_value = {
                "custom_attr": a_str(description="Custom attribute from capability")
            }
            mock_cap_class.return_value = mock_cap_instance

            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_capability": mock_cap_class} if comp_type == "capability" else {}
            )
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            await provider.setup()

            # Should have both pyvider_testmode and custom_attr
            assert "pyvider_testmode" in provider._final_schema.block.attributes
            assert "custom_attr" in provider._final_schema.block.attributes

    @pytest.mark.asyncio
    async def test_setup_stores_capabilities_in_dict(self) -> None:
        """Test that setup stores capability instances in capabilities dict."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            mock_cap_class = MagicMock()
            mock_cap_instance = MagicMock()
            mock_cap_class.return_value = mock_cap_instance

            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_cap": mock_cap_class} if comp_type == "capability" else {}
            )
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            await provider.setup()

            # Should have test_cap and provider itself
            assert "test_cap" in provider.capabilities
            assert provider.capabilities["test_cap"] is mock_cap_instance
            assert "provider" in provider.capabilities
            assert provider.capabilities["provider"] is provider

    @pytest.mark.asyncio
    async def test_setup_passes_provider_config_to_capabilities(self) -> None:
        """Test that setup passes provider config to capability constructors."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            mock_provider_ctx = MagicMock()
            mock_provider_ctx.config = {"test_key": "test_value"}

            mock_cap_class = MagicMock()
            mock_cap_instance = MagicMock()
            mock_cap_class.return_value = mock_cap_instance

            def get_component_side_effect(comp_type: str, name: str | None = None) -> MagicMock | None:
                if comp_type == "singleton" and name == "provider_context":
                    # Return a factory function that returns the mock provider context
                    return lambda: mock_provider_ctx
                return None

            mock_hub.get_component.side_effect = get_component_side_effect
            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_cap": mock_cap_class} if comp_type == "capability" else {}
            )

            provider = PyviderProvider()
            await provider.setup()

            # Verify capability was instantiated with provider config
            mock_cap_class.assert_called_once_with(config=mock_provider_ctx.config)

    @pytest.mark.asyncio
    async def test_setup_validates_component_capability_associations(self) -> None:
        """Test that setup validates components reference registered capabilities."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            # Create a component that references a missing capability
            mock_resource = MagicMock()
            mock_resource._parent_capability = "missing_capability"

            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_resource": mock_resource} if comp_type == "resource" else {}
            )
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()

            # Should raise FrameworkConfigurationError
            with pytest.raises(
                FrameworkConfigurationError,
                match="Component 'test_resource' is associated with capability 'missing_capability'",
            ):
                await provider.setup()

    @pytest.mark.asyncio
    async def test_setup_allows_components_with_provider_capability(self) -> None:
        """Test that components can reference the default 'provider' capability."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            # Create a component that references "provider" capability
            mock_resource = MagicMock()
            mock_resource._parent_capability = "provider"

            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_resource": mock_resource} if comp_type == "resource" else {}
            )
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            # Should not raise - "provider" is always available
            await provider.setup()

    @pytest.mark.asyncio
    async def test_setup_allows_components_without_parent_capability(self) -> None:
        """Test that components without _parent_capability default to 'provider'."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            # Create a component without _parent_capability attribute
            mock_data_source = MagicMock(spec=[])  # No attributes

            mock_hub.get_components.side_effect = lambda comp_type: (
                {"test_ds": mock_data_source} if comp_type == "data_source" else {}
            )
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            # Should not raise - defaults to "provider"
            await provider.setup()


class TestPyviderProviderSchemaAccess:
    """Tests for schema access after setup."""

    @pytest.mark.asyncio
    async def test_schema_accessible_after_setup(self) -> None:
        """Test that schema property is accessible after setup."""
        with patch("pyvider.providers.provider.hub") as mock_hub:
            mock_hub.get_components.side_effect = lambda comp_type: {}
            mock_hub.get_component.return_value = None

            provider = PyviderProvider()
            await provider.setup()

            # Should not raise
            schema = provider.schema
            assert schema is not None
            assert "pyvider_testmode" in schema.block.attributes


# 🐍🏗️🔚
