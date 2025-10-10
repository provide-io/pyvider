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
    logger.debug(f"EPHEMERAL 🔎 Validating config for '{request.type_name}'")
    response = pb.ValidateEphemeralResourceConfig.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")

        schema = resource_class.get_schema()
        config_cty = unmarshal(request.config, schema=schema.block)

        # Perform built-in CTY validation first. This will raise on failure.
        schema.validate_config(config_cty.value)

        # Perform custom provider-defined validation.
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
        resource_instance = resource_class()
        validation_errors = await resource_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            f"EPHEMERAL 💥 Unhandled error validating '{request.type_name}'",
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔎 Validation for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response
