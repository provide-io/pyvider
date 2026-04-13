#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("MoveResourceState")
async def MoveResourceStateHandler(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    """Handle move resource state request."""
    return await _move_resource_state_impl(request, context)


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
