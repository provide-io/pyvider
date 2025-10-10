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
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
