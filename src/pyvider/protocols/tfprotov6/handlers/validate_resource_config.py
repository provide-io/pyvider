import time
from typing import Any

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
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
