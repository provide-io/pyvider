#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception, cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def ValidateEphemeralResourceConfigHandler(
    request: pb.ValidateEphemeralResourceConfig.Request, context: Any
) -> pb.ValidateEphemeralResourceConfig.Response:
    """Handles validation of an ephemeral resource's configuration."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateEphemeralResourceConfig")

    try:
        return await _validate_ephemeral_resource_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateEphemeralResourceConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateEphemeralResourceConfig")


async def _validate_ephemeral_resource_config_impl(
    request: pb.ValidateEphemeralResourceConfig.Request, context: Any
) -> pb.ValidateEphemeralResourceConfig.Response:
    """Implementation of ValidateEphemeralResourceConfig handler."""
    logger.debug(
        "Starting ephemeral resource config validation",
        operation="validate_ephemeral_resource_config",
        resource_type=request.type_name,
    )

    response = pb.ValidateEphemeralResourceConfig.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during validation",
                operation="validate_ephemeral_resource_config",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the ephemeral resource class has the @ephemeral decorator\n"
                f"  2. Verify the ephemeral resource module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )

        schema = resource_class.get_schema()
        config_cty = unmarshal(request.config, schema=schema.block)

        # Perform built-in CTY validation first. This will raise on failure.
        schema.validate_config(config_cty.value)

        # Perform custom provider-defined validation.
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
        resource_instance = resource_class()
        validation_errors = await resource_instance.validate(config_instance)

        if validation_errors:
            logger.warning(
                "Ephemeral resource configuration validation failed",
                operation="validate_ephemeral_resource_config",
                resource_type=request.type_name,
                error_count=len(validation_errors),
            )
            for err_msg in validation_errors:
                diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
                response.diagnostics.append(diag)
        else:
            logger.debug(
                "Ephemeral resource configuration validation succeeded",
                operation="validate_ephemeral_resource_config",
                resource_type=request.type_name,
            )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Ephemeral resource validation failed with known error",
            operation="validate_ephemeral_resource_config",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource validation failed with unexpected error",
            operation="validate_ephemeral_resource_config",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
