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
