import asyncio

import pytest

from pyvider.common.encryption import CONFIG_KEY_NAME
from pyvider.hub import hub
from pyvider.hub.discovery import ComponentDiscovery


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def discovered_components_session(event_loop):
    """
    A session-scoped fixture that runs component discovery once.
    This ensures the hub is populated for all tests that need it.
    """
    print("\n--- Running session-wide component discovery for tests ---")
    discovery = ComponentDiscovery(hub)
    event_loop.run_until_complete(discovery.discover_all())
    print("--- Component discovery complete ---")
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


# 🐍🏗️🧪🪄
