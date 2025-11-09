#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

import attrs
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
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def RenewEphemeralResourceHandler(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Handles renewing an ephemeral resource's lease."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="RenewEphemeralResource")

    try:
        return await _renew_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="RenewEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="RenewEphemeralResource")


async def _renew_ephemeral_resource_impl(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource renew operation",
        operation="renew_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during renew operation",
                operation="renew_ephemeral_resource",
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
                operation="renew_ephemeral_resource",
                resource_type=request.type_name,
            )
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot renew.\n\n"
                f"Suggestion: Ephemeral resources that support renewal must define a private_state_class.\n\n"
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

        new_private_state_obj, new_renew_at = await resource_instance.renew(ctx)

        if new_private_state_obj:
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), use_bin_type=True)

        if new_renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(new_renew_at))

        logger.info(
            "Ephemeral resource renew completed successfully",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            has_new_private_state=new_private_state_obj is not None,
            has_new_renew_at=new_renew_at is not None,
        )

    except PyviderError as e:
        logger.error(
            "Ephemeral resource renew failed with known error",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource renew failed with unexpected error",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
