#
# pyvider/protocols/tfprotov6/handlers/upgrade_resource_state.py
#

import json
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
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    DynamicValue,
)


@resilient()
async def UpgradeResourceStateHandler(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """
    Handle UpgradeResourceState requests. For now, this is a pass-through
    as we are not implementing schema versioning. It must return the state
    it was given, unmodified.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="UpgradeResourceState")

    try:
        return await _upgrade_resource_state_impl(request, context)
    except Exception:
        handler_errors.inc(handler="UpgradeResourceState")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="UpgradeResourceState")


async def _upgrade_resource_state_impl(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )
