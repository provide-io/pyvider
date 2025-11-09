#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import asyncio
from collections.abc import AsyncGenerator, Generator
import os
from pathlib import Path
import sys

import pytest

from pyvider.common.encryption import CONFIG_KEY_NAME
from pyvider.hub import hub
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.providers import BaseProvider

# Import test mode fixtures to make them available to all tests
pytest_plugins = ["pyvider.testmode.fixtures"]


@pytest.fixture(scope="session")
def event_loop() -> asyncio.BaseEventLoop:
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def discovered_components_session(event_loop: asyncio.BaseEventLoop) -> Generator[None, None, None]:
    """
    A session-scoped fixture that runs component discovery once.
    This ensures the hub is populated for all tests that need it.

    Skip during mutmut runs to avoid stdio conflicts.
    """

    # Skip discovery if running under mutmut (check for mutmut cache)
    if os.environ.get("MUTANT_UNDER_TEST") or Path(".mutmut-cache").exists() or "mutmut" in sys.argv[0]:
        yield
        return

    try:
        print("\n--- Running session-wide component discovery for tests ---")
        discovery = ComponentDiscovery(hub)
        event_loop.run_until_complete(discovery.discover_all())
        print("--- Component discovery complete ---")
    except (ValueError, OSError) as e:
        # If there's an I/O error (e.g., from mutmut), skip discovery
        if "I/O operation on closed file" in str(e):
            pass
        else:
            raise
    yield


@pytest.fixture(scope="session", autouse=True)
def suppress_logging_during_mutmut() -> Generator[None, None, None]:
    """
    Automatically suppress all logging during mutmut runs to avoid I/O errors.

    Mutmut redirects stdio which causes structlog to fail with
    'I/O operation on closed file' errors. We work around this by redirecting
    stdout/stderr to /dev/null.
    """

    # Check if running under mutmut
    is_mutmut = (
        os.environ.get("MUTANT_UNDER_TEST") or Path(".mutmut-cache").exists() or "mutmut" in sys.argv[0]
    )

    if is_mutmut:
        # Save original stdout/stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # Redirect to /dev/null
        with Path(os.devnull).open("w") as devnull:
            sys.stdout = devnull
            sys.stderr = devnull

            yield

        # Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    else:
        yield


@pytest.fixture
async def provider_in_hub(
    discovered_components_session: Generator[None, None, None],
) -> AsyncGenerator[BaseProvider, None]:
    """
    A function-scoped fixture that instantiates, sets up, and registers a
    test provider instance in the hub. This is crucial for handlers that
    depend on a live provider instance with its capabilities.
    """
    from pyvider.providers.base import BaseProvider, ProviderMetadata
    from pyvider.providers.context import ProviderContext

    provider_ctx = ProviderContext(config=None)
    hub.register("singleton", "provider_context", provider_ctx)

    # Create a minimal test provider
    provider = BaseProvider(metadata=ProviderMetadata(name="test", version="0.0.1"))
    await provider.setup()
    hub.register("singleton", "provider", provider)

    provider_ctx.provider = provider

    yield provider

    # Teardown
    if hub.get_component("singleton", "provider"):
        hub.unregister("singleton", "provider")
    if hub.get_component("singleton", "provider_context"):
        hub.unregister("singleton", "provider_context")


@pytest.fixture
def encryption_key_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """
    A shared fixture that sets the required encryption key environment variable
    for any test that needs to perform private state encryption.
    """
    env_var_name = f"PYVIDER_{CONFIG_KEY_NAME.upper()}"
    secret_key = "test-secret-key-for-pytest-session"
    monkeypatch.setenv(env_var_name, secret_key)

    from pyvider.common import encryption

    encryption._ENCRYPTION_KEY = None
    yield
    monkeypatch.delenv(env_var_name, raising=False)
    encryption._ENCRYPTION_KEY = None


# 🐍🏗️🔚
