#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable

from provide.foundation import logger


def register_ephemeral_resource(name: str) -> Callable[[type], type]:
    """
    Decorator to register an ephemeral resource under the 'ephemeral_resources' component type.

    Args:
        name (str): The unique name of the ephemeral resource to register.

    Returns:
        class: The decorated ephemeral resource class.
    """

    def decorator(cls: type) -> type:
        from pyvider.hub import hub

        hub.register("ephemeral_resource", name, cls)
        logger.debug(f"Registered ephemeral resource '{name}'")
        return cls

    return decorator


# 🐍🏗️🔚
