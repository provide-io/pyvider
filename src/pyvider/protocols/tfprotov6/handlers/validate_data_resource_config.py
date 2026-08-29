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
from pyvider.protocols.tfprotov6.handlers._diagnostics import unknown_type_diagnostic
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("ValidateDataResourceConfig")
async def ValidateDataResourceConfigHandler(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Handle validate data resource config request."""
    return await _validate_data_resource_config_impl(request, context)


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
            # Return the diagnostic rather than raising: a bare exception is
            # caught below and rendered as "Internal Provider Error", which
            # hides the type name and the list of what *is* registered — the
            # two things that let a practitioner fix a typo themselves. Actions
            # and list resources already answer an unknown type this way.
            response.diagnostics.append(
                unknown_type_diagnostic(
                    "data source",
                    request.type_name,
                    hub.get_components("data_source") or {},
                    "@register_data_source",
                )
            )
            return response

        config_instance = decode_config(ds_class, request.config, validate=True)

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
