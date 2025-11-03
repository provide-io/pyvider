#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable
from typing import ParamSpec, TypeVar

from provide.foundation import logger

P = ParamSpec("P")
T = TypeVar("T")


def register_resource(
    name: str, component_of: str | None = None, test_only: bool = False
) -> Callable[[type], type]:
    """
    Decorator to register a resource and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_resource = True  # type: ignore[attr-defined]
        cls._registered_name = name  # type: ignore[attr-defined]
        cls._is_test_only = test_only  # type: ignore[attr-defined]
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(
            "📊 Marked resource for discovery",
            resource=name,
            capability=component_of,
            test_only=test_only,
        )
        return cls

    return decorator


# 🐍🏗️🔚
