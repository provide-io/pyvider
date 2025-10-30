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

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception, cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def OpenEphemeralResourceHandler(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Handles opening an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="OpenEphemeralResource")

    try:
        return await _open_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="OpenEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="OpenEphemeralResource")


async def _open_ephemeral_resource_impl(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource open operation",
        operation="open_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during open operation",
                operation="open_ephemeral_resource",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the ephemeral resource class has the @ephemeral decorator\n"
                f"  2. Verify the ephemeral resource module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  4. Review provider logs for component registration errors\n"
                f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )

        schema = resource_class.get_schema()
        config_cty = unmarshal(request.config, schema=schema.block)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

        ctx = EphemeralResourceContext(config=config_instance, test_mode_enabled=test_mode_enabled)
        resource_instance = resource_class()

        result_obj, private_state_obj, renew_at = await resource_instance.open(ctx)

        # Marshal the results back to the wire format
        if result_obj:
            raw_result = attrs.asdict(result_obj)
            response.result.CopyFrom(marshal(raw_result, schema=schema.block))

        if private_state_obj:
            response.private = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=True)

        if renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(renew_at))

        logger.info(
            "Ephemeral resource open completed successfully",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            has_result=result_obj is not None,
            has_private_state=private_state_obj is not None,
            has_renew_at=renew_at is not None,
        )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Ephemeral resource open failed with known error",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource open failed with unexpected error",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
