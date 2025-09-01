#
# pyvider/protocols/tfprotov6/handlers/upgrade_resource_state.py
#

import json
from typing import Any

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    DynamicValue,
)
from provide.foundation import logger


async def UpgradeResourceStateHandler(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """
    Handle UpgradeResourceState requests. For now, this is a pass-through
    as we are not implementing schema versioning. It must return the state
    it was given, unmodified.
    """
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
