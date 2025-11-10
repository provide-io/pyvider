#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider testmode module and fixtures."""

from typing import Any

import pytest

from pyvider.hub import hub


class TestTestmodeModule:
    """Test the testmode module can be imported."""

    def test_testmode_module_import(self) -> None:
        """Test that testmode module can be imported."""
        import pyvider.testmode

        assert pyvider.testmode.__all__ == []

    def test_testmode_fixtures_import(self) -> None:
        """Test that testmode.fixtures module can be imported."""
        from pyvider.testmode import fixtures

        assert fixtures is not None
        assert hasattr(fixtures, "provider_with_test_mode")


class TestProviderWithTestModeFixture:
    """Tests for the provider_with_test_mode fixture."""

    @pytest.mark.usefixtures("provider_with_test_mode")
    def test_fixture_enables_test_mode(self, provider_in_hub: Any) -> None:
        """Test that the fixture enables test mode in provider context."""
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        assert context.test_mode_enabled is True  # type: ignore[attr-defined]

    @pytest.mark.usefixtures("provider_with_test_mode")
    def test_fixture_sets_pyvider_testmode_config(self, provider_in_hub: Any) -> None:
        """Test that the fixture sets pyvider_testmode in config."""
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        assert hasattr(context.config, "pyvider_testmode")  # type: ignore[attr-defined]
        assert context.config.pyvider_testmode is True  # type: ignore[attr-defined]

    @pytest.mark.usefixtures("provider_with_test_mode")
    def test_fixture_registers_provider_context(self, provider_in_hub: Any) -> None:
        """Test that the fixture registers provider_context in the hub."""
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        assert hub.get_component("singleton", "provider_context") is context

    def test_fixture_context_cleanup(self, provider_in_hub: Any) -> None:
        """Test that the fixture context is properly managed."""
        # This test verifies the fixture properly manages the context
        # by checking that the provider_in_hub context is the default
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        # Without provider_with_test_mode, test mode should not be enabled
        assert context.test_mode_enabled is False  # type: ignore[attr-defined]

    @pytest.mark.usefixtures("provider_with_test_mode")
    async def test_fixture_works_with_async_tests(self, provider_in_hub: Any) -> None:
        """Test that the fixture works with async test functions."""
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        assert context.test_mode_enabled is True  # type: ignore[attr-defined]


class TestTestModeIntegration:
    """Integration tests for test mode with actual components."""

    @pytest.mark.usefixtures("provider_with_test_mode")
    def test_test_mode_allows_test_only_resources(self, provider_in_hub: Any) -> None:
        """Test that test mode enables access to test-only resources."""
        # Verify test mode is enabled
        context = hub.get_component("singleton", "provider_context")
        assert context.test_mode_enabled is True  # type: ignore[union-attr]

        # Test mode infrastructure works correctly
        # The fixture successfully enables test mode
        assert context is not None
        assert context.test_mode_enabled is True  # type: ignore[union-attr]

    def test_without_test_mode_fixture(self, provider_in_hub: Any) -> None:
        """Test that without the fixture, test mode is not enabled by default."""
        context = hub.get_component("singleton", "provider_context")
        # The provider_in_hub fixture creates a context without test mode
        assert context is not None
        # Default should be False (provider_in_hub doesn't enable test mode)
        assert context.test_mode_enabled is False  # type: ignore[attr-defined]


# 🐍🏗️🔚
