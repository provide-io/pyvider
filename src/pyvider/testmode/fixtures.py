#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider Test Mode Fixtures.

Provides pytest fixtures for testing Pyvider components that require test mode,
particularly test-only resources and data sources.

Fixtures:
- `provider_with_test_mode`: Enables test mode for test-only components

Example usage:
    >>> @pytest.mark.usefixtures("provider_with_test_mode")
    >>> async def test_test_only_resource():
    ...     # Test mode is enabled, test-only components can be accessed
    ...     # Test proceeds with test mode enabled"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def provider_with_test_mode(provider_in_hub: Any) -> Generator[None]:
    """
    Enable test mode for test-only components.

    This fixture creates and registers a ProviderContext with test_mode_enabled=True,
    allowing tests to access components marked with test_only=True (like
    pyvider_private_state_verifier).

    The fixture depends on the provider_in_hub fixture to ensure the provider
    is registered before enabling test mode.

    Yields:
        None

    Example:
        >>> @pytest.mark.usefixtures("provider_with_test_mode")
        >>> async def test_private_state_verifier():
        ...     # Test mode is enabled, can access test-only resources
        ...     # ... test implementation ...

    Note:
        This fixture automatically cleans up the provider_context registration
        on teardown to ensure test isolation.
    """
    from attrs import define

    from pyvider.hub import hub
    from pyvider.providers.context import ProviderContext

    @define
    class TestConfig:
        pyvider_testmode: bool = True

    # Create and register provider context with test mode enabled
    context = ProviderContext(config=TestConfig(), test_mode_enabled=True)
    hub.register("singleton", "provider_context", context)

    yield

    # Clean up
    hub.unregister("singleton", "provider_context")


# 🐍🏗️🔚
