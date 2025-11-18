#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable
from typing import Any

from provide.foundation import logger


def register_function(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
    test_only: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        func._is_test_only = test_only  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
            "test_only": test_only,
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(
            "Debug info",
            capability=component_of,
            test_only=test_only,
        )
        return func

    return decorator


# 🐍🏗️🔚
