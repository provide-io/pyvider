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
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception, cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def ValidateResourceConfigHandler(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Handle validate resource config request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateResourceConfig")

    try:
        return await _validate_resource_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateResourceConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateResourceConfig")


async def _validate_resource_config_impl(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()

    logger.debug(
        "ValidateResourceConfig handler called",
        operation="validate_resource_config",
        resource_type=request.type_name,
        has_config=bool(request.config.msgpack),
    )

    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            logger.error(
                "Resource type not found during config validation",
                operation="validate_resource_config",
                resource_type=request.type_name,
                registered_resources=list(hub.get_components("resource").keys())
                if hub.get_components("resource")
                else [],
            )

            err = ResourceError(
                f"Resource type '{request.type_name}' not registered.\n\n"
                f"Suggestion: Ensure the resource is registered using the @resource decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the resource class has the @resource decorator\n"
                f"  2. Verify the resource module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered resources\n"
                f"  4. Review provider logs for component registration errors"
            )
            err.add_context("resource.type_name", request.type_name)
            raise err

        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            logger.debug(
                "Skipping custom validation - config contains unknown values",
                operation="validate_resource_config",
                resource_type=request.type_name,
            )
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        logger.debug(
            "Invoking resource validate method",
            operation="validate_resource_config",
            resource_type=request.type_name,
        )

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        if validation_errors:
            logger.warning(
                "Resource configuration validation failed",
                operation="validate_resource_config",
                resource_type=request.type_name,
                error_count=len(validation_errors),
                errors=validation_errors,
            )

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

        if not validation_errors:
            logger.info(
                "Resource configuration validation passed",
                operation="validate_resource_config",
                resource_type=request.type_name,
            )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "ValidateResourceConfig failed with framework error",
            operation="validate_resource_config",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "ValidateResourceConfig failed with unexpected error",
            operation="validate_resource_config",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
