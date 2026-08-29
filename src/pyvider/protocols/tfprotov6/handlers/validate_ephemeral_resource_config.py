#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("ValidateEphemeralResourceConfig")
async def ValidateEphemeralResourceConfigHandler(
    request: pb.ValidateEphemeralResourceConfig.Request, context: Any
) -> pb.ValidateEphemeralResourceConfig.Response:
    """Handles validation of an ephemeral resource's configuration."""
    return await _validate_ephemeral_resource_config_impl(request, context)


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

        config_instance = decode_config(resource_class, request.config, validate=True)
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
