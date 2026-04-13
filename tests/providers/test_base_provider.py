#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider/providers/base.py."""

import pytest

from pyvider.exceptions import FrameworkConfigurationError, ProviderError
from pyvider.providers.base import BaseProvider, ProviderCapabilities, ProviderMetadata
from pyvider.schema import a_str, s_provider


class TestProviderCapabilities:
    """Tests for ProviderCapabilities class."""

    def test_default_capabilities(self) -> None:
        """Test that default capability values are set correctly."""
        caps = ProviderCapabilities()
        assert caps.plan_destroy is True
        assert caps.get_provider_schema_optional is False
        assert caps.move_resource_state is True

    def test_custom_capabilities(self) -> None:
        """Test creating capabilities with custom values."""
        caps = ProviderCapabilities(plan_destroy=False, get_provider_schema_optional=True)
        assert caps.plan_destroy is False
        assert caps.get_provider_schema_optional is True


class TestProviderMetadata:
    """Tests for ProviderMetadata class."""

    def test_metadata_creation(self) -> None:
        """Test creating provider metadata."""
        metadata = ProviderMetadata(name="test-provider", version="1.0.0")
        assert metadata.name == "test-provider"
        assert metadata.version == "1.0.0"
        assert metadata.protocol_version == "6"

    def test_metadata_with_custom_capabilities(self) -> None:
        """Test metadata with custom capabilities."""
        caps = ProviderCapabilities(plan_destroy=False)
        metadata = ProviderMetadata(name="test", version="1.0.0", capabilities=caps)
        assert metadata.capabilities.plan_destroy is False


class TestBaseProvider:
    """Tests for BaseProvider class."""

    def test_provider_initialization(self) -> None:
        """Test provider initialization."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)
        assert provider.metadata.name == "test"
        assert provider._configured is False
        assert provider._final_schema is None

    @pytest.mark.asyncio
    async def test_setup_hook(self) -> None:
        """Test setup hook is callable."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)
        # setup() should not raise
        await provider.setup()

    @pytest.mark.asyncio
    async def test_configure_provider(self) -> None:
        """Test configuring a provider."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)

        config = {"key": "value"}
        await provider.configure(config)
        assert provider._configured is True

    @pytest.mark.asyncio
    async def test_configure_twice_raises_error(self) -> None:
        """Test that configuring twice raises an error."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)

        config = {"key": "value"}
        await provider.configure(config)

        # Second configure should raise
        with pytest.raises(ProviderError, match="already been configured"):
            await provider.configure(config)

    def test_schema_before_setup_raises_error(self) -> None:
        """Test that accessing schema before setup raises error."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)

        with pytest.raises(FrameworkConfigurationError, match="before initialization"):
            _ = provider.schema

    @pytest.mark.asyncio
    async def test_schema_after_setup(self) -> None:
        """Test that schema is accessible after setup when set."""
        metadata = ProviderMetadata(name="test", version="1.0.0")
        provider = BaseProvider(metadata=metadata)

        # Manually set the schema (as setup() would do)
        provider._final_schema = s_provider(attributes={"test_attr": a_str()})

        # Now schema should be accessible
        schema = provider.schema
        assert schema is not None
        assert "test_attr" in schema.block.attributes


# 🐍🏗️🔚
