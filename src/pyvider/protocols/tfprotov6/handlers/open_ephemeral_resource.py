import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception, cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def OpenEphemeralResourceHandler(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Handles opening an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="OpenEphemeralResource")

    try:
        return await _open_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="OpenEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="OpenEphemeralResource")


async def _open_ephemeral_resource_impl(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")

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
            response.private = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=True)

        if renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(renew_at))

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response
