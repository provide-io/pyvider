#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def MoveResourceStateHandler(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    """Handle move resource state request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="MoveResourceState")

    try:
        return await _move_resource_state_impl(request, context)
    except Exception:
        handler_errors.inc(handler="MoveResourceState")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="MoveResourceState")


async def _move_resource_state_impl(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    """Implementation of MoveResourceState handler."""
    logger.warning(
        "Move resource state operation not yet implemented",
        operation="move_resource_state",
        target_type_name=request.target_type_name,
        source_type_name=request.source_type_name if hasattr(request, "source_type_name") else None,
    )

    # Return diagnostic indicating feature not yet implemented
    diag = pb.Diagnostic(
        severity=pb.Diagnostic.WARNING,
        summary="Resource move not yet implemented",
        detail=(
            f"Moving resources to type '{request.target_type_name}' is not yet implemented.\n\n"
            "Suggestion: This provider does not currently support moving resources between types. "
            "You will need to recreate the resource instead.\n\n"
            "Workaround: Destroy the old resource and create a new one with the desired type."
        ),
    )
    return pb.MoveResourceState.Response(diagnostics=[diag])


# 🐍🏗️🔚
