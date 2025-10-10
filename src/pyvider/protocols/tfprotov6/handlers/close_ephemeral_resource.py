import time
from typing import Any

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


@resilient()
async def CloseEphemeralResourceHandler(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Handles closing an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="CloseEphemeralResource")

    try:
        return await _close_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="CloseEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="CloseEphemeralResource")


async def _close_ephemeral_resource_impl(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")
        if not resource_class.private_state_class:
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot close."
            )

        private_data = msgpack.unpackb(request.private, raw=False)
        private_state_instance = resource_class.private_state_class(**private_data)

        ctx = EphemeralResourceContext(private_state=private_state_instance)
        resource_instance = resource_class()

        await resource_instance.close(ctx)

    except PyviderError as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response
