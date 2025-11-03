#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def CloseEphemeralResourceHandler(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Handles closing an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="CloseEphemeralResource")

    try:
        return await _close_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="CloseEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="CloseEphemeralResource")


async def _close_ephemeral_resource_impl(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource close operation",
        operation="close_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during close operation",
                operation="close_ephemeral_resource",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator.\n\n"
                f"Troubleshooting:\n"
                f"  1. Verify the ephemeral resource module is imported\n"
                f"  2. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  3. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
        if not resource_class.private_state_class:
            logger.error(
                "Ephemeral resource missing private_state_class",
                operation="close_ephemeral_resource",
                resource_type=request.type_name,
            )
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot close.\n\n"
                f"Suggestion: Ephemeral resources must define a private_state_class for lifecycle management.\n\n"
                f"Documentation: See ephemeral resource documentation for private state usage."
            )

        private_data = msgpack.unpackb(request.private, raw=False)
        private_state_instance = resource_class.private_state_class(**private_data)

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

        ctx = EphemeralResourceContext(
            private_state=private_state_instance, test_mode_enabled=test_mode_enabled
        )
        resource_instance = resource_class()

        await resource_instance.close(ctx)

        logger.info(
            "Ephemeral resource close completed successfully",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
        )

    except PyviderError as e:
        logger.error(
            "Ephemeral resource close failed with known error",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource close failed with unexpected error",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
