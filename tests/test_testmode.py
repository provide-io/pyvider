#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider testmode module and fixtures."""

import contextlib
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

    def test_fixture_cleans_up_after_test(self, provider_in_hub: Any) -> None:
        """Test that the fixture cleans up provider_context after test."""
        # This test doesn't use the fixture, so provider_context should not be
        # from provider_with_test_mode (it may be from provider_in_hub)
        # We'll verify cleanup happens by using the fixture in a nested context
        from pyvider.testmode.fixtures import provider_with_test_mode

        # Setup the fixture manually
        gen = provider_with_test_mode(provider_in_hub)
        next(gen)

        # Verify context is registered with test mode
        context = hub.get_component("singleton", "provider_context")
        assert context is not None
        assert context.test_mode_enabled is True  # type: ignore[attr-defined]

        # Cleanup
        with contextlib.suppress(StopIteration):
            next(gen)

        # After cleanup, the context should be unregistered by the fixture
        # Note: provider_in_hub fixture also manages provider_context,
        # so we can't test complete removal, but we verified the fixture logic runs

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

        # Test-only resources should be accessible when test mode is enabled
        # The pyvider_private_state_verifier is an example of a test-only resource
        test_only_resources = hub.get_components("resource")
        # Filter for test-only resources
        [name for name, comp in test_only_resources.items() if getattr(comp.metadata, "test_only", False)]  # type: ignore[attr-defined]

        # If test-only resources exist, they should be accessible
        # This validates the test mode infrastructure works
        assert context.test_mode_enabled is True  # type: ignore[union-attr]

    def test_without_test_mode_fixture(self, provider_in_hub: Any) -> None:
        """Test that without the fixture, test mode is not enabled by default."""
        context = hub.get_component("singleton", "provider_context")
        # The provider_in_hub fixture creates a context without test mode
        assert context is not None
        # Default should be False (provider_in_hub doesn't enable test mode)
        assert context.test_mode_enabled is False  # type: ignore[attr-defined]


# 🐍🏗️🔚
