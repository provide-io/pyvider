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


async def x__renew_ephemeral_resource_impl__mutmut_orig(
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


async def x__renew_ephemeral_resource_impl__mutmut_1(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(None)
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


async def x__renew_ephemeral_resource_impl__mutmut_2(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = None
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


async def x__renew_ephemeral_resource_impl__mutmut_3(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = None
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


async def x__renew_ephemeral_resource_impl__mutmut_4(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component(None, request.type_name)
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


async def x__renew_ephemeral_resource_impl__mutmut_5(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", None)
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


async def x__renew_ephemeral_resource_impl__mutmut_6(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component(request.type_name)
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


async def x__renew_ephemeral_resource_impl__mutmut_7(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", )
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


async def x__renew_ephemeral_resource_impl__mutmut_8(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("XXephemeral_resourceXX", request.type_name)
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


async def x__renew_ephemeral_resource_impl__mutmut_9(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("EPHEMERAL_RESOURCE", request.type_name)
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


async def x__renew_ephemeral_resource_impl__mutmut_10(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if resource_class:
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


async def x__renew_ephemeral_resource_impl__mutmut_11(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(None)
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


async def x__renew_ephemeral_resource_impl__mutmut_12(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(f"EPHEMERAL ⏳ Renewing resource '{request.type_name}'")
    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")
        if resource_class.private_state_class:
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


async def x__renew_ephemeral_resource_impl__mutmut_13(
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
                None
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


async def x__renew_ephemeral_resource_impl__mutmut_14(
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

        private_data = None
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


async def x__renew_ephemeral_resource_impl__mutmut_15(
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

        private_data = msgpack.unpackb(None, raw=False)
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


async def x__renew_ephemeral_resource_impl__mutmut_16(
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

        private_data = msgpack.unpackb(request.private, raw=None)
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


async def x__renew_ephemeral_resource_impl__mutmut_17(
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

        private_data = msgpack.unpackb(raw=False)
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


async def x__renew_ephemeral_resource_impl__mutmut_18(
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

        private_data = msgpack.unpackb(request.private, )
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


async def x__renew_ephemeral_resource_impl__mutmut_19(
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

        private_data = msgpack.unpackb(request.private, raw=True)
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


async def x__renew_ephemeral_resource_impl__mutmut_20(
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
        private_state_instance = None

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


async def x__renew_ephemeral_resource_impl__mutmut_21(
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

        ctx = None
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


async def x__renew_ephemeral_resource_impl__mutmut_22(
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

        ctx = EphemeralResourceContext(private_state=None)
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


async def x__renew_ephemeral_resource_impl__mutmut_23(
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
        resource_instance = None

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


async def x__renew_ephemeral_resource_impl__mutmut_24(
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

        new_private_state_obj, new_renew_at = None

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


async def x__renew_ephemeral_resource_impl__mutmut_25(
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

        new_private_state_obj, new_renew_at = await resource_instance.renew(None)

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


async def x__renew_ephemeral_resource_impl__mutmut_26(
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
            response.private = None

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


async def x__renew_ephemeral_resource_impl__mutmut_27(
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
            response.private = msgpack.packb(None, use_bin_type=True)

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


async def x__renew_ephemeral_resource_impl__mutmut_28(
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
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), use_bin_type=None)

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


async def x__renew_ephemeral_resource_impl__mutmut_29(
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
            response.private = msgpack.packb(use_bin_type=True)

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


async def x__renew_ephemeral_resource_impl__mutmut_30(
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
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), )

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


async def x__renew_ephemeral_resource_impl__mutmut_31(
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
            response.private = msgpack.packb(attrs.asdict(None), use_bin_type=True)

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


async def x__renew_ephemeral_resource_impl__mutmut_32(
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
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), use_bin_type=False)

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


async def x__renew_ephemeral_resource_impl__mutmut_33(
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
            response.renew_at.CopyFrom(None)

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


async def x__renew_ephemeral_resource_impl__mutmut_34(
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
            response.renew_at.CopyFrom(datetime_to_proto(None))

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


async def x__renew_ephemeral_resource_impl__mutmut_35(
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
        diag = None
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


async def x__renew_ephemeral_resource_impl__mutmut_36(
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
        diag = await create_diagnostic_from_exception(None)
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


async def x__renew_ephemeral_resource_impl__mutmut_37(
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
        response.diagnostics.append(None)
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


async def x__renew_ephemeral_resource_impl__mutmut_38(
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
            None,
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_39(
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
            exc_info=None,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_40(
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
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_41(
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
            )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_42(
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
            exc_info=False,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_43(
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
        diag = None
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_44(
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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_45(
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
        response.diagnostics.append(None)

    logger.debug(
        f"EPHEMERAL ⏳ Renew for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__renew_ephemeral_resource_impl__mutmut_46(
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
        None
    )
    return response

x__renew_ephemeral_resource_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__renew_ephemeral_resource_impl__mutmut_1': x__renew_ephemeral_resource_impl__mutmut_1, 
    'x__renew_ephemeral_resource_impl__mutmut_2': x__renew_ephemeral_resource_impl__mutmut_2, 
    'x__renew_ephemeral_resource_impl__mutmut_3': x__renew_ephemeral_resource_impl__mutmut_3, 
    'x__renew_ephemeral_resource_impl__mutmut_4': x__renew_ephemeral_resource_impl__mutmut_4, 
    'x__renew_ephemeral_resource_impl__mutmut_5': x__renew_ephemeral_resource_impl__mutmut_5, 
    'x__renew_ephemeral_resource_impl__mutmut_6': x__renew_ephemeral_resource_impl__mutmut_6, 
    'x__renew_ephemeral_resource_impl__mutmut_7': x__renew_ephemeral_resource_impl__mutmut_7, 
    'x__renew_ephemeral_resource_impl__mutmut_8': x__renew_ephemeral_resource_impl__mutmut_8, 
    'x__renew_ephemeral_resource_impl__mutmut_9': x__renew_ephemeral_resource_impl__mutmut_9, 
    'x__renew_ephemeral_resource_impl__mutmut_10': x__renew_ephemeral_resource_impl__mutmut_10, 
    'x__renew_ephemeral_resource_impl__mutmut_11': x__renew_ephemeral_resource_impl__mutmut_11, 
    'x__renew_ephemeral_resource_impl__mutmut_12': x__renew_ephemeral_resource_impl__mutmut_12, 
    'x__renew_ephemeral_resource_impl__mutmut_13': x__renew_ephemeral_resource_impl__mutmut_13, 
    'x__renew_ephemeral_resource_impl__mutmut_14': x__renew_ephemeral_resource_impl__mutmut_14, 
    'x__renew_ephemeral_resource_impl__mutmut_15': x__renew_ephemeral_resource_impl__mutmut_15, 
    'x__renew_ephemeral_resource_impl__mutmut_16': x__renew_ephemeral_resource_impl__mutmut_16, 
    'x__renew_ephemeral_resource_impl__mutmut_17': x__renew_ephemeral_resource_impl__mutmut_17, 
    'x__renew_ephemeral_resource_impl__mutmut_18': x__renew_ephemeral_resource_impl__mutmut_18, 
    'x__renew_ephemeral_resource_impl__mutmut_19': x__renew_ephemeral_resource_impl__mutmut_19, 
    'x__renew_ephemeral_resource_impl__mutmut_20': x__renew_ephemeral_resource_impl__mutmut_20, 
    'x__renew_ephemeral_resource_impl__mutmut_21': x__renew_ephemeral_resource_impl__mutmut_21, 
    'x__renew_ephemeral_resource_impl__mutmut_22': x__renew_ephemeral_resource_impl__mutmut_22, 
    'x__renew_ephemeral_resource_impl__mutmut_23': x__renew_ephemeral_resource_impl__mutmut_23, 
    'x__renew_ephemeral_resource_impl__mutmut_24': x__renew_ephemeral_resource_impl__mutmut_24, 
    'x__renew_ephemeral_resource_impl__mutmut_25': x__renew_ephemeral_resource_impl__mutmut_25, 
    'x__renew_ephemeral_resource_impl__mutmut_26': x__renew_ephemeral_resource_impl__mutmut_26, 
    'x__renew_ephemeral_resource_impl__mutmut_27': x__renew_ephemeral_resource_impl__mutmut_27, 
    'x__renew_ephemeral_resource_impl__mutmut_28': x__renew_ephemeral_resource_impl__mutmut_28, 
    'x__renew_ephemeral_resource_impl__mutmut_29': x__renew_ephemeral_resource_impl__mutmut_29, 
    'x__renew_ephemeral_resource_impl__mutmut_30': x__renew_ephemeral_resource_impl__mutmut_30, 
    'x__renew_ephemeral_resource_impl__mutmut_31': x__renew_ephemeral_resource_impl__mutmut_31, 
    'x__renew_ephemeral_resource_impl__mutmut_32': x__renew_ephemeral_resource_impl__mutmut_32, 
    'x__renew_ephemeral_resource_impl__mutmut_33': x__renew_ephemeral_resource_impl__mutmut_33, 
    'x__renew_ephemeral_resource_impl__mutmut_34': x__renew_ephemeral_resource_impl__mutmut_34, 
    'x__renew_ephemeral_resource_impl__mutmut_35': x__renew_ephemeral_resource_impl__mutmut_35, 
    'x__renew_ephemeral_resource_impl__mutmut_36': x__renew_ephemeral_resource_impl__mutmut_36, 
    'x__renew_ephemeral_resource_impl__mutmut_37': x__renew_ephemeral_resource_impl__mutmut_37, 
    'x__renew_ephemeral_resource_impl__mutmut_38': x__renew_ephemeral_resource_impl__mutmut_38, 
    'x__renew_ephemeral_resource_impl__mutmut_39': x__renew_ephemeral_resource_impl__mutmut_39, 
    'x__renew_ephemeral_resource_impl__mutmut_40': x__renew_ephemeral_resource_impl__mutmut_40, 
    'x__renew_ephemeral_resource_impl__mutmut_41': x__renew_ephemeral_resource_impl__mutmut_41, 
    'x__renew_ephemeral_resource_impl__mutmut_42': x__renew_ephemeral_resource_impl__mutmut_42, 
    'x__renew_ephemeral_resource_impl__mutmut_43': x__renew_ephemeral_resource_impl__mutmut_43, 
    'x__renew_ephemeral_resource_impl__mutmut_44': x__renew_ephemeral_resource_impl__mutmut_44, 
    'x__renew_ephemeral_resource_impl__mutmut_45': x__renew_ephemeral_resource_impl__mutmut_45, 
    'x__renew_ephemeral_resource_impl__mutmut_46': x__renew_ephemeral_resource_impl__mutmut_46
}

def _renew_ephemeral_resource_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__renew_ephemeral_resource_impl__mutmut_orig, x__renew_ephemeral_resource_impl__mutmut_mutants, args, kwargs)
    return result 

_renew_ephemeral_resource_impl.__signature__ = _mutmut_signature(x__renew_ephemeral_resource_impl__mutmut_orig)
x__renew_ephemeral_resource_impl__mutmut_orig.__name__ = 'x__renew_ephemeral_resource_impl'
