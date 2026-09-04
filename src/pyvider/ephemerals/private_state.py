#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Rebuilding the private state Terraform hands back to Renew and Close."""

from __future__ import annotations

from typing import Any

import msgpack  # type: ignore[import-untyped]
from provide.foundation import logger

from pyvider.exceptions import ResourceError

__all__ = ["rebuild_private_state"]


def rebuild_private_state(resource_class: Any, private: bytes, type_name: str) -> Any | None:
    """Turn the private bytes from Renew or Close back into the resource's object.

    Private state is optional in the protocol: `OpenEphemeralResource.Response`
    carries it as an optional field, and Renew and Close carry back whatever Open
    produced, or nothing. Terraform closes every ephemeral resource it opened
    either way (transform_ephemeral_resource_close.go), so an ephemeral resource
    that keeps no private state -- the ordinary case for one that just reads a
    value -- must still close cleanly.

    Both handlers used to require a `private_state_class` and then call
    `msgpack.unpackb` on the bytes unconditionally. `msgpack.unpackb(b"")` raises
    `ValueError: Unpack failed: incomplete input`, so every such close failed.

    Returns None when there is nothing to rebuild, which is what the resource's
    own hooks then see as `ctx.private_state`.
    """
    if not private:
        return None

    private_state_class = getattr(resource_class, "private_state_class", None)
    if private_state_class is None:
        # Terraform is handing back bytes this resource once produced, but the
        # class that describes them is gone. Saying so is more use than a
        # KeyError from deep inside the resource's own hook.
        logger.warning(
            "Ephemeral resource received private state but declares no private_state_class",
            operation="ephemeral_private_state",
            resource_type=type_name,
            private_state_size=len(private),
        )
        return None

    try:
        private_data = msgpack.unpackb(private, raw=False)
    except Exception as e:
        err = ResourceError(
            f"The private state for ephemeral resource '{type_name}' could not be read.\n\n"
            f"Suggestion: this is the value the resource returned from open(); it should "
            f"round-trip through msgpack.\n\n"
            f"Original error: {type(e).__name__}: {e}"
        )
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Ephemeral private state could not be read")
        raise err from e

    return private_state_class(**private_data)


# 🐍🏗️🔚
