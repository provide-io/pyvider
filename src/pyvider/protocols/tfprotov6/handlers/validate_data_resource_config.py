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
async def ValidateDataResourceConfigHandler(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Handle validate data resource config request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateDataResourceConfig")

    try:
        return await _validate_data_resource_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateDataResourceConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateDataResourceConfig")


async def _validate_data_resource_config_impl(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    logger.debug(
        "Starting data source config validation",
        operation="validate_data_resource_config",
        data_source_type=request.type_name,
    )

    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            logger.error(
                "Data source type not found during validation",
                operation="validate_data_resource_config",
                data_source_type=request.type_name,
                registered_data_sources=list(hub.get_components("data_source").keys())
                if hub.get_components("data_source")
                else [],
            )
            raise ValueError(
                f"Data source type '{request.type_name}' not registered.\n\n"
                f"Suggestion: Ensure the data source is registered using the @data_source decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the data source class has the @data_source decorator\n"
                f"  2. Verify the data source module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered data sources\n"
                f"  4. Review provider logs for component registration errors\n"
                f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        if validation_errors:
            logger.warning(
                "Data source configuration validation failed",
                operation="validate_data_resource_config",
                data_source_type=request.type_name,
                error_count=len(validation_errors),
            )
            for err_msg in validation_errors:
                diag = pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary=err_msg,
                )
                response.diagnostics.append(diag)
        else:
            logger.debug(
                "Data source configuration validation succeeded",
                operation="validate_data_resource_config",
                data_source_type=request.type_name,
            )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Data source validation failed with known error",
            operation="validate_data_resource_config",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Data source validation failed with unexpected error",
            operation="validate_data_resource_config",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
