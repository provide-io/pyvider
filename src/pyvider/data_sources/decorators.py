#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Callable

from provide.foundation import logger


def register_data_source(
    name: str, component_of: str | None = None, test_only: bool = False
) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore[attr-defined]
        cls._registered_name = name  # type: ignore[attr-defined]
        cls._is_test_only = test_only  # type: ignore[attr-defined]
        if component_of:
            cls._parent_capability = component_of  # type: ignore[attr-defined]
        logger.debug(
            "Marked data source for discovery",
            name=name,
            capability=component_of,
            test_only=test_only,
        )
        return cls

    return decorator


# 🐍🏗️🔚
