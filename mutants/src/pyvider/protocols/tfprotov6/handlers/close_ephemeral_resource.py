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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


async def x__close_ephemeral_resource_impl__mutmut_orig(
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


async def x__close_ephemeral_resource_impl__mutmut_1(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(None)
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


async def x__close_ephemeral_resource_impl__mutmut_2(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = None
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


async def x__close_ephemeral_resource_impl__mutmut_3(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = None
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


async def x__close_ephemeral_resource_impl__mutmut_4(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component(None, request.type_name)
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


async def x__close_ephemeral_resource_impl__mutmut_5(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", None)
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


async def x__close_ephemeral_resource_impl__mutmut_6(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component(request.type_name)
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


async def x__close_ephemeral_resource_impl__mutmut_7(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", )
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


async def x__close_ephemeral_resource_impl__mutmut_8(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("XXephemeral_resourceXX", request.type_name)
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


async def x__close_ephemeral_resource_impl__mutmut_9(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("EPHEMERAL_RESOURCE", request.type_name)
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


async def x__close_ephemeral_resource_impl__mutmut_10(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if resource_class:
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


async def x__close_ephemeral_resource_impl__mutmut_11(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(None)
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


async def x__close_ephemeral_resource_impl__mutmut_12(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 🔒 Closing resource '{request.type_name}'")
    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")
        if resource_class.private_state_class:
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


async def x__close_ephemeral_resource_impl__mutmut_13(
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
                None
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


async def x__close_ephemeral_resource_impl__mutmut_14(
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

        private_data = None
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


async def x__close_ephemeral_resource_impl__mutmut_15(
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

        private_data = msgpack.unpackb(None, raw=False)
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


async def x__close_ephemeral_resource_impl__mutmut_16(
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

        private_data = msgpack.unpackb(request.private, raw=None)
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


async def x__close_ephemeral_resource_impl__mutmut_17(
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

        private_data = msgpack.unpackb(raw=False)
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


async def x__close_ephemeral_resource_impl__mutmut_18(
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

        private_data = msgpack.unpackb(request.private, )
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


async def x__close_ephemeral_resource_impl__mutmut_19(
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

        private_data = msgpack.unpackb(request.private, raw=True)
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


async def x__close_ephemeral_resource_impl__mutmut_20(
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
        private_state_instance = None

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


async def x__close_ephemeral_resource_impl__mutmut_21(
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

        ctx = None
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


async def x__close_ephemeral_resource_impl__mutmut_22(
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

        ctx = EphemeralResourceContext(private_state=None)
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


async def x__close_ephemeral_resource_impl__mutmut_23(
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
        resource_instance = None

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


async def x__close_ephemeral_resource_impl__mutmut_24(
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

        await resource_instance.close(None)

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


async def x__close_ephemeral_resource_impl__mutmut_25(
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
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_26(
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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_27(
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
        response.diagnostics.append(None)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_28(
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
        logger.error(None, exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_29(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=None)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_30(
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
        logger.error(exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_31(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_32(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error closing '{request.type_name}'", exc_info=False)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_33(
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
        diag = None
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_34(
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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_35(
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
        response.diagnostics.append(None)

    logger.debug(
        f"EPHEMERAL 🔒 Close for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__close_ephemeral_resource_impl__mutmut_36(
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
        None
    )
    return response

x__close_ephemeral_resource_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__close_ephemeral_resource_impl__mutmut_1': x__close_ephemeral_resource_impl__mutmut_1, 
    'x__close_ephemeral_resource_impl__mutmut_2': x__close_ephemeral_resource_impl__mutmut_2, 
    'x__close_ephemeral_resource_impl__mutmut_3': x__close_ephemeral_resource_impl__mutmut_3, 
    'x__close_ephemeral_resource_impl__mutmut_4': x__close_ephemeral_resource_impl__mutmut_4, 
    'x__close_ephemeral_resource_impl__mutmut_5': x__close_ephemeral_resource_impl__mutmut_5, 
    'x__close_ephemeral_resource_impl__mutmut_6': x__close_ephemeral_resource_impl__mutmut_6, 
    'x__close_ephemeral_resource_impl__mutmut_7': x__close_ephemeral_resource_impl__mutmut_7, 
    'x__close_ephemeral_resource_impl__mutmut_8': x__close_ephemeral_resource_impl__mutmut_8, 
    'x__close_ephemeral_resource_impl__mutmut_9': x__close_ephemeral_resource_impl__mutmut_9, 
    'x__close_ephemeral_resource_impl__mutmut_10': x__close_ephemeral_resource_impl__mutmut_10, 
    'x__close_ephemeral_resource_impl__mutmut_11': x__close_ephemeral_resource_impl__mutmut_11, 
    'x__close_ephemeral_resource_impl__mutmut_12': x__close_ephemeral_resource_impl__mutmut_12, 
    'x__close_ephemeral_resource_impl__mutmut_13': x__close_ephemeral_resource_impl__mutmut_13, 
    'x__close_ephemeral_resource_impl__mutmut_14': x__close_ephemeral_resource_impl__mutmut_14, 
    'x__close_ephemeral_resource_impl__mutmut_15': x__close_ephemeral_resource_impl__mutmut_15, 
    'x__close_ephemeral_resource_impl__mutmut_16': x__close_ephemeral_resource_impl__mutmut_16, 
    'x__close_ephemeral_resource_impl__mutmut_17': x__close_ephemeral_resource_impl__mutmut_17, 
    'x__close_ephemeral_resource_impl__mutmut_18': x__close_ephemeral_resource_impl__mutmut_18, 
    'x__close_ephemeral_resource_impl__mutmut_19': x__close_ephemeral_resource_impl__mutmut_19, 
    'x__close_ephemeral_resource_impl__mutmut_20': x__close_ephemeral_resource_impl__mutmut_20, 
    'x__close_ephemeral_resource_impl__mutmut_21': x__close_ephemeral_resource_impl__mutmut_21, 
    'x__close_ephemeral_resource_impl__mutmut_22': x__close_ephemeral_resource_impl__mutmut_22, 
    'x__close_ephemeral_resource_impl__mutmut_23': x__close_ephemeral_resource_impl__mutmut_23, 
    'x__close_ephemeral_resource_impl__mutmut_24': x__close_ephemeral_resource_impl__mutmut_24, 
    'x__close_ephemeral_resource_impl__mutmut_25': x__close_ephemeral_resource_impl__mutmut_25, 
    'x__close_ephemeral_resource_impl__mutmut_26': x__close_ephemeral_resource_impl__mutmut_26, 
    'x__close_ephemeral_resource_impl__mutmut_27': x__close_ephemeral_resource_impl__mutmut_27, 
    'x__close_ephemeral_resource_impl__mutmut_28': x__close_ephemeral_resource_impl__mutmut_28, 
    'x__close_ephemeral_resource_impl__mutmut_29': x__close_ephemeral_resource_impl__mutmut_29, 
    'x__close_ephemeral_resource_impl__mutmut_30': x__close_ephemeral_resource_impl__mutmut_30, 
    'x__close_ephemeral_resource_impl__mutmut_31': x__close_ephemeral_resource_impl__mutmut_31, 
    'x__close_ephemeral_resource_impl__mutmut_32': x__close_ephemeral_resource_impl__mutmut_32, 
    'x__close_ephemeral_resource_impl__mutmut_33': x__close_ephemeral_resource_impl__mutmut_33, 
    'x__close_ephemeral_resource_impl__mutmut_34': x__close_ephemeral_resource_impl__mutmut_34, 
    'x__close_ephemeral_resource_impl__mutmut_35': x__close_ephemeral_resource_impl__mutmut_35, 
    'x__close_ephemeral_resource_impl__mutmut_36': x__close_ephemeral_resource_impl__mutmut_36
}

def _close_ephemeral_resource_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__close_ephemeral_resource_impl__mutmut_orig, x__close_ephemeral_resource_impl__mutmut_mutants, args, kwargs)
    return result 

_close_ephemeral_resource_impl.__signature__ = _mutmut_signature(x__close_ephemeral_resource_impl__mutmut_orig)
x__close_ephemeral_resource_impl__mutmut_orig.__name__ = 'x__close_ephemeral_resource_impl'
