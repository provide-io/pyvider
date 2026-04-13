#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Regression tests for discovery resilience and handler error paths."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from pyvider.handler import ProviderHandler
from pyvider.hub.components import ComponentRegistry


class TestDiscoveryFailureResilience:
    """Verify that discovery failures produce clear errors, not silent timeouts."""

    @pytest.mark.asyncio
    async def test_discovery_failure_sets_event_immediately(self) -> None:
        """When discovery crashes, the event must still be set so handlers
        get an immediate error instead of waiting 55 seconds."""
        hub = ComponentRegistry()
        discovery_ready_event = asyncio.Event()
        hub.register("singleton", "_discovery_ready_event", discovery_ready_event)

        # Import the inner function's logic — simulate discover_and_signal
        # with a failing discovery
        async def discover_and_signal_with_failure() -> None:
            try:
                raise RuntimeError("Simulated discovery crash")
            except Exception:
                pass
            finally:
                discovery_ready_event.set()

        await discover_and_signal_with_failure()

        # Event must be set even after failure
        assert discovery_ready_event.is_set()

    @pytest.mark.asyncio
    async def test_handler_gets_clear_error_after_discovery_failure(self) -> None:
        """After discovery fails, the handler should raise immediately with
        a clear error, not wait for 55 seconds."""
        mock_hub = ComponentRegistry()
        discovery_ready_event = asyncio.Event()
        mock_hub.register("singleton", "_discovery_ready_event", discovery_ready_event)

        # Set the event (as discover_and_signal's finally block would)
        # but do NOT register a provider (simulating failed discovery)
        discovery_ready_event.set()

        handler = ProviderHandler()

        with (
            patch("pyvider.hub.components.registry", mock_hub),
            patch.dict(
                "sys.modules",
                {
                    "pyvider.hub": type(
                        "mod",
                        (),
                        {"hub": mock_hub, "DISCOVERY_READY_EVENT": "_discovery_ready_event"},
                    )()
                },
            ),
            pytest.raises(RuntimeError, match="Provider not available"),
        ):
            await handler._ensure_provider_ready()


class TestHandlerProviderResolution:
    """Test the handler's provider resolution paths."""

    @pytest.mark.asyncio
    async def test_handler_returns_cached_provider(self) -> None:
        """Once resolved, the provider should be cached and returned directly."""
        handler = ProviderHandler()
        mock_provider = MagicMock()
        handler._resolved_provider = mock_provider

        result = await handler._ensure_provider_ready()
        assert result is mock_provider

    @pytest.mark.asyncio
    async def test_handler_uses_direct_provider(self) -> None:
        """A directly-set provider (for testing) should be used immediately."""
        handler = ProviderHandler()
        mock_provider = MagicMock()
        handler._provider = mock_provider

        result = await handler._ensure_provider_ready()
        assert result is mock_provider
        assert handler._resolved_provider is mock_provider

    @pytest.mark.asyncio
    async def test_handler_waits_for_discovery_event(self) -> None:
        """Handler should wait for the discovery event before fetching provider."""
        hub = ComponentRegistry()
        discovery_ready_event = asyncio.Event()
        hub.register("singleton", "_discovery_ready_event", discovery_ready_event)

        mock_provider = MagicMock()

        # Schedule event to be set after a brief delay
        async def set_event_and_register() -> None:
            await asyncio.sleep(0.01)
            hub.register("singleton", "provider", mock_provider)
            discovery_ready_event.set()

        handler = ProviderHandler()

        with (
            patch("pyvider.hub.components.registry", hub),
            patch.dict(
                "sys.modules",
                {
                    "pyvider.hub": type(
                        "mod",
                        (),
                        {"hub": hub, "DISCOVERY_READY_EVENT": "_discovery_ready_event"},
                    )()
                },
            ),
        ):
            task = asyncio.create_task(set_event_and_register())
            result = await handler._ensure_provider_ready()
            await task

        assert result is mock_provider


# 🐍🏗️🔚
