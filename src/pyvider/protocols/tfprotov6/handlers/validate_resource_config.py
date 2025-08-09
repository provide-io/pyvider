#
# pyvider/protocols/tfprotov6/handlers/validate_resource_config.py
#
# pyvider/protocols/tfprotov6/handlers/validate_resource_config.py
#
# pyvider/protocols/tfprotov6/handlers/validate_resource_config.py
#

from typing import Any

from pyvider.conversion import unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb

from .utils import create_diagnostic_from_exception, cty_to_attrs_instance


async def ValidateResourceConfigHandler(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
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


# 🐍🏗️⚙️🪄
