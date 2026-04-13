#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for capability registration and injection decorators."""

import asyncio
from contextlib import suppress

import pytest

from pyvider.capabilities.decorators import register_capability, requires_capability
from pyvider.exceptions import ResourceError
from pyvider.hub import hub


def _restore_component(component_type: str, name: str, original: object | None) -> None:
    if original is not None:
        hub.register(component_type, name, original)
    else:
        with suppress(Exception):
            hub.unregister(component_type, name)


def test_register_capability_marks_class() -> None:
    @register_capability("dummy-capability")
    class DummyCapability:
        pass

    assert DummyCapability._is_registered_capability is True
    assert DummyCapability._registered_name == "dummy-capability"


def test_requires_capability_injects_parent_for_sync_methods() -> None:
    existing_provider = hub.get_component("singleton", "provider")
    existing_capability = hub.get_component("capability", "dummy_parent")

    provider_stub = object()
    capability_stub = object()
    hub.register("singleton", "provider", provider_stub)
    hub.register("capability", "dummy_parent", capability_stub)

    def method(self: object, *, dummy_parent: object | None = None) -> object | None:
        return dummy_parent

    method._parent_capability = "dummy_parent"  # type: ignore[attr-defined]
    wrapped = requires_capability(method)

    class Component:
        execute = wrapped

    instance = Component()
    try:
        result = instance.execute()
        assert result is capability_stub
    finally:
        _restore_component("capability", "dummy_parent", existing_capability)
        _restore_component("singleton", "provider", existing_provider)


def test_requires_capability_async_raises_when_provider_missing() -> None:
    existing_provider = hub.get_component("singleton", "provider")
    if existing_provider is not None:
        hub.unregister("singleton", "provider")

    @requires_capability
    async def async_method(self: object) -> str:
        return "unreachable"

    class Component:
        pass

    instance = Component()
    with pytest.raises(ResourceError, match="Provider not available"):
        asyncio.run(async_method(instance))

    if existing_provider is not None:
        hub.register("singleton", "provider", existing_provider)


def test_requires_capability_async_injects_parent() -> None:
    existing_provider = hub.get_component("singleton", "provider")
    existing_capability = hub.get_component("capability", "async_parent")

    provider_stub = object()
    capability_stub = object()
    hub.register("singleton", "provider", provider_stub)
    hub.register("capability", "async_parent", capability_stub)

    class Component:
        _parent_capability = "async_parent"

        @requires_capability
        async def do_work(self: object, *, async_parent: object | None = None) -> object | None:
            return async_parent

    component = Component()
    try:
        result = asyncio.run(component.do_work())
        assert result is capability_stub
    finally:
        _restore_component("capability", "async_parent", existing_capability)
        _restore_component("singleton", "provider", existing_provider)


# 🐍🏗️🔚
