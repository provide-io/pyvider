import asyncio

import pytest

from pyvider.common.encryption import CONFIG_KEY_NAME
from pyvider.hub import hub
from pyvider.hub.discovery import ComponentDiscovery

# Import testkit fixtures with fallback
try:
    from provide.testkit import clean_event_loop as _clean_event_loop

    # Create a session-scoped version for pyvider's needs
    @pytest.fixture(scope="session")
    def event_loop():
        """Create an instance of the default event loop for the session."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()

    # Also provide function-scoped version for tests that need it
    clean_event_loop = _clean_event_loop
except ImportError:
    # Fallback to the original implementation if testkit is not available
    @pytest.fixture(scope="session")
    def event_loop():
        """Create an instance of the default event loop for the session."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()

    # Alias for compatibility
    clean_event_loop = event_loop


@pytest.fixture(scope="session", autouse=True)
def discovered_components_session(event_loop):
    """
    A session-scoped fixture that runs component discovery once.
    This ensures the hub is populated for all tests that need it.

    Skip during mutmut runs to avoid stdio conflicts.
    """
    import os
    import sys

    # Skip discovery if running under mutmut (check for mutmut cache)
    if (os.environ.get('MUTANT_UNDER_TEST') or
        os.path.exists('.mutmut-cache') or
        'mutmut' in sys.argv[0]):
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


@pytest.fixture
async def provider_in_hub(discovered_components_session):
    """
    A function-scoped fixture that instantiates, sets up, and registers a
    PyviderProvider instance in the hub. This is crucial for handlers that
    depend on a live provider instance with its capabilities.
    """
    from pyvider.providers.context import ProviderContext
    from pyvider.providers.provider import PyviderProvider

    provider_ctx = ProviderContext(config=None)
    hub.register("singleton", "provider_context", provider_ctx)

    provider = PyviderProvider()
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
def encryption_key_env(monkeypatch):
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
