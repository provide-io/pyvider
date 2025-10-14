import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def RenewEphemeralResourceHandler(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Handles renewing an ephemeral resource's lease."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="RenewEphemeralResource")

    try:
        return await _renew_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="RenewEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="RenewEphemeralResource")


async def _renew_ephemeral_resource_impl(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")
        if not resource_class.private_state_class:
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot renew."
            )

        private_data = msgpack.unpackb(request.private, raw=False)
        private_state_instance = resource_class.private_state_class(**private_data)

        ctx = EphemeralResourceContext(private_state=private_state_instance)
        resource_instance = resource_class()

        new_private_state_obj, new_renew_at = await resource_instance.renew(ctx)

        if new_private_state_obj:
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), use_bin_type=True)

        if new_renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(new_renew_at))

    except PyviderError as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            f"EPHEMERAL 💥 Unhandled error renewing '{request.type_name}'",
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response
