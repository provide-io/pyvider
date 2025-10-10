#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
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
async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Handle import resource state request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ImportResourceState")

    try:
        return await _import_resource_state_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ImportResourceState")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ImportResourceState")


async def _import_resource_state_impl(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


# 🐍🏗⛮️
