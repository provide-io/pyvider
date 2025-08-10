from typing import Any

from pyvider.conversion import unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.telemetry import logger

from .utils import create_diagnostic_from_exception, cty_to_attrs_instance


async def ValidateEphemeralResourceConfigHandler(
    request: pb.ValidateEphemeralResourceConfig.Request, context: Any
) -> pb.ValidateEphemeralResourceConfig.Response:
    """Handles validation of an ephemeral resource's configuration."""
    logger.debug(f"EPHEMERAL 🔎 Validating config for '{request.type_name}'")
    response = pb.ValidateEphemeralResourceConfig.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found."
            )

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
