#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from pyvider.exceptions import ResourceError
from pyvider.hub import hub

F = TypeVar("F", bound=Callable[..., Any])


def register_capability(name: str) -> Callable[[type], type]:
    """Decorator to register a capability class for discovery."""

    def decorator(cls: type) -> type:
        cls._is_registered_capability = True  # type: ignore[attr-defined]
        cls._registered_name = name  # type: ignore[attr-defined]
        return cls

    return decorator


def _parent_capability_name(component_instance: Any, func: Callable[..., Any]) -> str:
    """Find the capability a component was registered under.

    `@register_resource(component_of=...)` and `@register_data_source(...)` stamp
    `_parent_capability` on the **class**. The sync wrapper used to read it off
    the undecorated function instead, where those decorators never put it, so it
    saw the "provider" default every time and injected nothing at all -- silently,
    since injecting nothing is also what a provider-level component wants. Only
    `@register_function` stamps a function, and functions are dispatched by
    call_function.py rather than through this decorator.

    Both are consulted, so a function carrying the attribute directly still works.
    """
    from_class = getattr(type(component_instance), "_parent_capability", None)
    if from_class:
        return str(from_class)
    return str(getattr(func, "_parent_capability", "provider"))


def _resolve_parent_capability(component_instance: Any, func: Callable[..., Any]) -> tuple[str, Any] | None:
    """Resolve the capability to inject, or None when there is nothing to inject.

    Shared by both wrappers. They had a copy each, and the copies disagreed about
    where the capability name lives and about what comes out of the hub -- which
    is the failure this function exists to make impossible rather than to fix
    twice.
    """
    provider = hub.get_component("singleton", "provider")
    if not provider:
        raise ResourceError("Provider not available for capability injection.")

    name = _parent_capability_name(component_instance, func)
    if name == "provider":
        return None

    capability = hub.get_component("capability", name)
    if not capability:
        raise ResourceError(f"Required parent capability '{name}' not found in context.")

    # Discovery registers the decorated class object itself, so what the hub holds
    # is a class; `HubComponents.get_components("capability")` is annotated
    # `dict[str, type[BaseCapability]]` and says so. This used to hand the class
    # straight to the component, which then called instance methods on a class and
    # read state that no instance held. read_data_source.py and call_function.py
    # both instantiate at their own injection sites; this is the third. A hub
    # holding an instance already -- as tests and injected registries may -- is
    # left alone.
    instance = capability() if isinstance(capability, type) else capability
    return name, instance


def requires_capability(func: F) -> F:
    """
    Decorator that automatically injects a component's parent capability
    instance as a keyword argument into the decorated method.
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        resolved = _resolve_parent_capability(args[0] if args else None, func)
        if resolved is not None:
            name, capability = resolved
            kwargs[name] = capability
        return await func(*args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # type: ignore[return-value]

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        resolved = _resolve_parent_capability(args[0] if args else None, func)
        if resolved is not None:
            name, capability = resolved
            kwargs[name] = capability
        return func(*args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


# 🐍🏗️🔚
