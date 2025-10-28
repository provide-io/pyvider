#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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
        cls._is_registered_capability = True  # type: ignore
        cls._registered_name = name  # type: ignore
        return cls

    return decorator


def requires_capability(func: F) -> F:
    """
    Decorator that automatically injects a component's parent capability
    instance as a keyword argument into the decorated method.
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        component_instance = args[0]
        parent_capability_name = getattr(component_instance.__class__, "_parent_capability", "provider")

        # ctx = next((arg for arg in args if isinstance(arg, ResourceContext)), None)
        provider = hub.get_component("singleton", "provider")
        if not provider:
            raise ResourceError("Provider not available for capability injection.")

        if parent_capability_name == "provider":
            return await func(*args, **kwargs)

        capability_instance = hub.get_component("capability", parent_capability_name)
        if not capability_instance:
            raise ResourceError(f"Required parent capability '{parent_capability_name}' not found in context.")

        kwargs[parent_capability_name] = capability_instance
        return await func(*args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # type: ignore[return-value]
    else:

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            parent_cap_name = getattr(func, "_parent_capability", "provider")

            provider = hub.get_component("singleton", "provider")
            if not provider:
                raise ResourceError("Provider not available for capability injection.")

            if parent_cap_name == "provider":
                return func(*args, **kwargs)

            capability_instance = hub.get_component("capability", parent_cap_name)
            if not capability_instance:
                raise ResourceError(f"Required parent capability '{parent_cap_name}' not found in context.")

            kwargs[parent_cap_name] = capability_instance
            return func(*args, **kwargs)

        return sync_wrapper  # type: ignore[return-value]


# 🐍🏗️🔚
