#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import json
from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    DynamicValue,
)


@rpc_handler("UpgradeResourceState")
async def UpgradeResourceStateHandler(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """
    Handle UpgradeResourceState requests. For now, this is a pass-through
    as we are not implementing schema versioning. It must return the state
    it was given, unmodified.
    """
    return await _upgrade_resource_state_impl(request, context)


async def _upgrade_resource_state_impl(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug(
        "Starting resource state upgrade operation",
        operation="upgrade_resource_state",
        resource_type=request.type_name,
        version=request.version,
    )

    try:
        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
            logger.debug(
                "Passing through existing state (no upgrade logic)",
                operation="upgrade_resource_state",
                resource_type=request.type_name,
                state_size=len(upgraded_state_json),
            )
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")
            logger.debug(
                "No state to upgrade, returning empty state",
                operation="upgrade_resource_state",
                resource_type=request.type_name,
            )

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.info(
            "Resource state upgrade completed successfully",
            operation="upgrade_resource_state",
            resource_type=request.type_name,
        )
        return response

    except Exception as e:
        logger.error(
            "Resource state upgrade failed",
            operation="upgrade_resource_state",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=(
                        f"Failed to upgrade resource state: {e}\n\n"
                        "Suggestion: This may indicate a state format incompatibility.\n\n"
                        "Troubleshooting:\n"
                        "  1. Check the resource state version matches provider expectations\n"
                        "  2. Review provider logs for state parsing errors\n"
                        "  3. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
                    ),
                )
            ]
        )


# 🐍🏗️🔚
