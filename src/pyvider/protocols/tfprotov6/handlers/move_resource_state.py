#
# pyvider/protocols/tfprotov6/handlers/move_resource_state.py
#

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
    logger.warning("👋🫴🤝 Unimplemented: MoveResourceState was called.")
    return pb.MoveResourceState.Response(diagnostics=[])


# 🐍🏗⛮️
