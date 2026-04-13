#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("ImportResourceState")
async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Handle import resource state request."""
    return await _import_resource_state_impl(request, context)


async def _import_resource_state_impl(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning(
        "Import resource state operation not yet implemented",
        operation="import_resource_state",
        resource_type=request.type_name,
        import_id=request.id,
    )

    # Return diagnostic indicating feature not yet implemented
    diag = pb.Diagnostic(
        severity=pb.Diagnostic.WARNING,
        summary="Import not yet implemented",
        detail=(
            f"Resource import for type '{request.type_name}' is not yet implemented.\n\n"
            "Suggestion: This provider does not currently support importing existing resources. "
            "You will need to create resources using Terraform instead.\n\n"
            "Workaround: Define the resource in your Terraform configuration and apply it."
        ),
    )
    return pb.ImportResourceState.Response(diagnostics=[diag])


# 🐍🏗️🔚
