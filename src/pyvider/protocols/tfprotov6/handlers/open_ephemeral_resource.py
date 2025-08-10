from typing import Any

import attrs
import msgpack

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.telemetry import logger

from .utils import create_diagnostic_from_exception, cty_to_attrs_instance
from .utils_timestamp import datetime_to_proto


async def OpenEphemeralResourceHandler(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Handles opening an ephemeral resource."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found."
            )

        schema = resource_class.get_schema()
        config_cty = unmarshal(request.config, schema=schema.block)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        ctx = EphemeralResourceContext(config=config_instance)
        resource_instance = resource_class()

        result_obj, private_state_obj, renew_at = await resource_instance.open(ctx)

        # Marshal the results back to the wire format
        if result_obj:
            raw_result = attrs.asdict(result_obj)
            response.result.CopyFrom(marshal(raw_result, schema=schema.block))

        if private_state_obj:
            response.private = msgpack.packb(
                attrs.asdict(private_state_obj), use_bin_type=True
            )

        if renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(renew_at))

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=True
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response
