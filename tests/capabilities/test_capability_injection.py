#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`@requires_capability` injects a usable capability, from either kind of method.

The hub holds capability *classes* -- discovery registers the decorated class
object itself, and `HubComponents.get_components("capability")` is annotated
`dict[str, type[BaseCapability]]`. Every consumer therefore has to instantiate
what it takes out, and the two handlers that inject capabilities do. This
decorator did not.

`_parent_capability` is stamped on the *class* by `@register_resource` and
`@register_data_source`. The async branch read it from the class; the sync
branch read it from the undecorated function, where those decorators never put
it.
"""

import asyncio
from collections.abc import Iterator
from contextlib import suppress
from typing import Any

import pytest

from pyvider.capabilities.decorators import requires_capability
from pyvider.exceptions import ResourceError
from pyvider.hub import hub


class _Store:
    """A capability with state, so injecting the class rather than an instance shows."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def record(self, what: str) -> str:
        self.calls.append(what)
        return what


@pytest.fixture
def registered_capability(request: pytest.FixtureRequest) -> Iterator[Any]:
    """Register `store` in the hub -- as a class or an instance -- for one test."""
    previous_provider = hub.get_component("singleton", "provider")
    previous = hub.get_component("capability", "store")
    hub.register("singleton", "provider", object())
    hub.register("capability", "store", request.param)
    yield request.param
    for kind, name, original in (
        ("capability", "store", previous),
        ("singleton", "provider", previous_provider),
    ):
        if original is not None:
            hub.register(kind, name, original)
        else:
            with suppress(Exception):
                hub.unregister(kind, name)


class _SyncComponent:
    """What `@register_resource(component_of="store")` produces: stamped on the class."""

    _parent_capability = "store"

    @requires_capability
    def run(self, *, store: Any = None) -> Any:
        return store


class _AsyncComponent:
    _parent_capability = "store"

    @requires_capability
    async def run(self, *, store: Any = None) -> Any:
        return store


@pytest.mark.parametrize("registered_capability", [_Store], indirect=True)
def test_sync_method_injects_from_the_class_attribute(registered_capability: Any) -> None:
    """The decorators stamp `_parent_capability` on the class, never on the function."""
    injected = _SyncComponent().run()

    assert injected is not None, "sync method received no capability at all"


@pytest.mark.parametrize("registered_capability", [_Store], indirect=True)
def test_sync_injection_is_an_instance(registered_capability: Any) -> None:
    injected = _SyncComponent().run()

    assert isinstance(injected, _Store)
    assert injected.record("used") == "used"


@pytest.mark.parametrize("registered_capability", [_Store], indirect=True)
def test_async_injection_is_an_instance(registered_capability: Any) -> None:
    injected = asyncio.run(_AsyncComponent().run())

    assert isinstance(injected, _Store)
    assert injected.record("used") == "used"


def test_an_instance_in_the_hub_is_injected_as_it_stands() -> None:
    """A hub holding an instance -- as tests and injected registries may -- is not re-made."""
    previous_provider = hub.get_component("singleton", "provider")
    previous = hub.get_component("capability", "store")
    instance = _Store()
    hub.register("singleton", "provider", object())
    hub.register("capability", "store", instance)
    try:
        assert _SyncComponent().run() is instance
        assert asyncio.run(_AsyncComponent().run()) is instance
    finally:
        for kind, name, original in (
            ("capability", "store", previous),
            ("singleton", "provider", previous_provider),
        ):
            if original is not None:
                hub.register(kind, name, original)
            else:
                with suppress(Exception):
                    hub.unregister(kind, name)


def test_sync_method_reports_a_capability_that_is_not_registered() -> None:
    """Unreachable before: the sync branch never looked the capability up."""
    previous_provider = hub.get_component("singleton", "provider")
    previous = hub.get_component("capability", "store")
    hub.register("singleton", "provider", object())
    with suppress(Exception):
        hub.unregister("capability", "store")
    try:
        with pytest.raises(ResourceError, match="store"):
            _SyncComponent().run()
    finally:
        if previous is not None:
            hub.register("capability", "store", previous)
        if previous_provider is not None:
            hub.register("singleton", "provider", previous_provider)
        else:
            with suppress(Exception):
                hub.unregister("singleton", "provider")


# 🐍🏗️🔚
