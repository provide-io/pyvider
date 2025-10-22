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


async def x__open_ephemeral_resource_impl__mutmut_orig(
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


async def x__open_ephemeral_resource_impl__mutmut_1(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(None)
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


async def x__open_ephemeral_resource_impl__mutmut_2(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = None
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


async def x__open_ephemeral_resource_impl__mutmut_3(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = None
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


async def x__open_ephemeral_resource_impl__mutmut_4(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component(None, request.type_name)
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


async def x__open_ephemeral_resource_impl__mutmut_5(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", None)
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


async def x__open_ephemeral_resource_impl__mutmut_6(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component(request.type_name)
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


async def x__open_ephemeral_resource_impl__mutmut_7(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", )
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


async def x__open_ephemeral_resource_impl__mutmut_8(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("XXephemeral_resourceXX", request.type_name)
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


async def x__open_ephemeral_resource_impl__mutmut_9(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("EPHEMERAL_RESOURCE", request.type_name)
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


async def x__open_ephemeral_resource_impl__mutmut_10(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if resource_class:
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


async def x__open_ephemeral_resource_impl__mutmut_11(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(None)

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


async def x__open_ephemeral_resource_impl__mutmut_12(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(f"EPHEMERAL 📖 Opening resource '{request.type_name}'")
    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Ephemeral resource type '{request.type_name}' not found.")

        schema = None
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


async def x__open_ephemeral_resource_impl__mutmut_13(
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
        config_cty = None
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


async def x__open_ephemeral_resource_impl__mutmut_14(
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
        config_cty = unmarshal(None, schema=schema.block)
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


async def x__open_ephemeral_resource_impl__mutmut_15(
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
        config_cty = unmarshal(request.config, schema=None)
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


async def x__open_ephemeral_resource_impl__mutmut_16(
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
        config_cty = unmarshal(schema=schema.block)
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


async def x__open_ephemeral_resource_impl__mutmut_17(
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
        config_cty = unmarshal(request.config, )
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


async def x__open_ephemeral_resource_impl__mutmut_18(
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
        config_instance = None

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


async def x__open_ephemeral_resource_impl__mutmut_19(
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
        config_instance = cty_to_attrs_instance(None, resource_class.config_class)

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


async def x__open_ephemeral_resource_impl__mutmut_20(
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
        config_instance = cty_to_attrs_instance(config_cty, None)

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


async def x__open_ephemeral_resource_impl__mutmut_21(
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
        config_instance = cty_to_attrs_instance(resource_class.config_class)

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


async def x__open_ephemeral_resource_impl__mutmut_22(
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
        config_instance = cty_to_attrs_instance(config_cty, )

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


async def x__open_ephemeral_resource_impl__mutmut_23(
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

        ctx = None
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


async def x__open_ephemeral_resource_impl__mutmut_24(
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

        ctx = EphemeralResourceContext(config=None)
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


async def x__open_ephemeral_resource_impl__mutmut_25(
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
        resource_instance = None

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


async def x__open_ephemeral_resource_impl__mutmut_26(
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

        result_obj, private_state_obj, renew_at = None

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


async def x__open_ephemeral_resource_impl__mutmut_27(
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

        result_obj, private_state_obj, renew_at = await resource_instance.open(None)

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


async def x__open_ephemeral_resource_impl__mutmut_28(
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
            raw_result = None
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


async def x__open_ephemeral_resource_impl__mutmut_29(
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
            raw_result = attrs.asdict(None)
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


async def x__open_ephemeral_resource_impl__mutmut_30(
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
            response.result.CopyFrom(None)

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


async def x__open_ephemeral_resource_impl__mutmut_31(
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
            response.result.CopyFrom(marshal(None, schema=schema.block))

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


async def x__open_ephemeral_resource_impl__mutmut_32(
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
            response.result.CopyFrom(marshal(raw_result, schema=None))

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


async def x__open_ephemeral_resource_impl__mutmut_33(
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
            response.result.CopyFrom(marshal(schema=schema.block))

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


async def x__open_ephemeral_resource_impl__mutmut_34(
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
            response.result.CopyFrom(marshal(raw_result, ))

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


async def x__open_ephemeral_resource_impl__mutmut_35(
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
            response.private = None

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


async def x__open_ephemeral_resource_impl__mutmut_36(
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
            response.private = msgpack.packb(None, use_bin_type=True)

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


async def x__open_ephemeral_resource_impl__mutmut_37(
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
            response.private = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=None)

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


async def x__open_ephemeral_resource_impl__mutmut_38(
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
            response.private = msgpack.packb(use_bin_type=True)

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


async def x__open_ephemeral_resource_impl__mutmut_39(
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
            response.private = msgpack.packb(attrs.asdict(private_state_obj), )

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


async def x__open_ephemeral_resource_impl__mutmut_40(
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
            response.private = msgpack.packb(attrs.asdict(None), use_bin_type=True)

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


async def x__open_ephemeral_resource_impl__mutmut_41(
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
            response.private = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=False)

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


async def x__open_ephemeral_resource_impl__mutmut_42(
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
            response.renew_at.CopyFrom(None)

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


async def x__open_ephemeral_resource_impl__mutmut_43(
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
            response.renew_at.CopyFrom(datetime_to_proto(None))

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


async def x__open_ephemeral_resource_impl__mutmut_44(
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
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_45(
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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_46(
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
        response.diagnostics.append(None)
    except Exception as e:
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_47(
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
        logger.error(None, exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_48(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=None)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_49(
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
        logger.error(exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_50(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_51(
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
        logger.error(f"EPHEMERAL 💥 Unhandled error opening '{request.type_name}'", exc_info=False)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_52(
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
        diag = None
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_53(
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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_54(
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
        response.diagnostics.append(None)

    logger.debug(
        f"EPHEMERAL 📖 Open for '{request.type_name}' complete. Diagnostics: {len(response.diagnostics)}"
    )
    return response


async def x__open_ephemeral_resource_impl__mutmut_55(
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
        None
    )
    return response

x__open_ephemeral_resource_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__open_ephemeral_resource_impl__mutmut_1': x__open_ephemeral_resource_impl__mutmut_1, 
    'x__open_ephemeral_resource_impl__mutmut_2': x__open_ephemeral_resource_impl__mutmut_2, 
    'x__open_ephemeral_resource_impl__mutmut_3': x__open_ephemeral_resource_impl__mutmut_3, 
    'x__open_ephemeral_resource_impl__mutmut_4': x__open_ephemeral_resource_impl__mutmut_4, 
    'x__open_ephemeral_resource_impl__mutmut_5': x__open_ephemeral_resource_impl__mutmut_5, 
    'x__open_ephemeral_resource_impl__mutmut_6': x__open_ephemeral_resource_impl__mutmut_6, 
    'x__open_ephemeral_resource_impl__mutmut_7': x__open_ephemeral_resource_impl__mutmut_7, 
    'x__open_ephemeral_resource_impl__mutmut_8': x__open_ephemeral_resource_impl__mutmut_8, 
    'x__open_ephemeral_resource_impl__mutmut_9': x__open_ephemeral_resource_impl__mutmut_9, 
    'x__open_ephemeral_resource_impl__mutmut_10': x__open_ephemeral_resource_impl__mutmut_10, 
    'x__open_ephemeral_resource_impl__mutmut_11': x__open_ephemeral_resource_impl__mutmut_11, 
    'x__open_ephemeral_resource_impl__mutmut_12': x__open_ephemeral_resource_impl__mutmut_12, 
    'x__open_ephemeral_resource_impl__mutmut_13': x__open_ephemeral_resource_impl__mutmut_13, 
    'x__open_ephemeral_resource_impl__mutmut_14': x__open_ephemeral_resource_impl__mutmut_14, 
    'x__open_ephemeral_resource_impl__mutmut_15': x__open_ephemeral_resource_impl__mutmut_15, 
    'x__open_ephemeral_resource_impl__mutmut_16': x__open_ephemeral_resource_impl__mutmut_16, 
    'x__open_ephemeral_resource_impl__mutmut_17': x__open_ephemeral_resource_impl__mutmut_17, 
    'x__open_ephemeral_resource_impl__mutmut_18': x__open_ephemeral_resource_impl__mutmut_18, 
    'x__open_ephemeral_resource_impl__mutmut_19': x__open_ephemeral_resource_impl__mutmut_19, 
    'x__open_ephemeral_resource_impl__mutmut_20': x__open_ephemeral_resource_impl__mutmut_20, 
    'x__open_ephemeral_resource_impl__mutmut_21': x__open_ephemeral_resource_impl__mutmut_21, 
    'x__open_ephemeral_resource_impl__mutmut_22': x__open_ephemeral_resource_impl__mutmut_22, 
    'x__open_ephemeral_resource_impl__mutmut_23': x__open_ephemeral_resource_impl__mutmut_23, 
    'x__open_ephemeral_resource_impl__mutmut_24': x__open_ephemeral_resource_impl__mutmut_24, 
    'x__open_ephemeral_resource_impl__mutmut_25': x__open_ephemeral_resource_impl__mutmut_25, 
    'x__open_ephemeral_resource_impl__mutmut_26': x__open_ephemeral_resource_impl__mutmut_26, 
    'x__open_ephemeral_resource_impl__mutmut_27': x__open_ephemeral_resource_impl__mutmut_27, 
    'x__open_ephemeral_resource_impl__mutmut_28': x__open_ephemeral_resource_impl__mutmut_28, 
    'x__open_ephemeral_resource_impl__mutmut_29': x__open_ephemeral_resource_impl__mutmut_29, 
    'x__open_ephemeral_resource_impl__mutmut_30': x__open_ephemeral_resource_impl__mutmut_30, 
    'x__open_ephemeral_resource_impl__mutmut_31': x__open_ephemeral_resource_impl__mutmut_31, 
    'x__open_ephemeral_resource_impl__mutmut_32': x__open_ephemeral_resource_impl__mutmut_32, 
    'x__open_ephemeral_resource_impl__mutmut_33': x__open_ephemeral_resource_impl__mutmut_33, 
    'x__open_ephemeral_resource_impl__mutmut_34': x__open_ephemeral_resource_impl__mutmut_34, 
    'x__open_ephemeral_resource_impl__mutmut_35': x__open_ephemeral_resource_impl__mutmut_35, 
    'x__open_ephemeral_resource_impl__mutmut_36': x__open_ephemeral_resource_impl__mutmut_36, 
    'x__open_ephemeral_resource_impl__mutmut_37': x__open_ephemeral_resource_impl__mutmut_37, 
    'x__open_ephemeral_resource_impl__mutmut_38': x__open_ephemeral_resource_impl__mutmut_38, 
    'x__open_ephemeral_resource_impl__mutmut_39': x__open_ephemeral_resource_impl__mutmut_39, 
    'x__open_ephemeral_resource_impl__mutmut_40': x__open_ephemeral_resource_impl__mutmut_40, 
    'x__open_ephemeral_resource_impl__mutmut_41': x__open_ephemeral_resource_impl__mutmut_41, 
    'x__open_ephemeral_resource_impl__mutmut_42': x__open_ephemeral_resource_impl__mutmut_42, 
    'x__open_ephemeral_resource_impl__mutmut_43': x__open_ephemeral_resource_impl__mutmut_43, 
    'x__open_ephemeral_resource_impl__mutmut_44': x__open_ephemeral_resource_impl__mutmut_44, 
    'x__open_ephemeral_resource_impl__mutmut_45': x__open_ephemeral_resource_impl__mutmut_45, 
    'x__open_ephemeral_resource_impl__mutmut_46': x__open_ephemeral_resource_impl__mutmut_46, 
    'x__open_ephemeral_resource_impl__mutmut_47': x__open_ephemeral_resource_impl__mutmut_47, 
    'x__open_ephemeral_resource_impl__mutmut_48': x__open_ephemeral_resource_impl__mutmut_48, 
    'x__open_ephemeral_resource_impl__mutmut_49': x__open_ephemeral_resource_impl__mutmut_49, 
    'x__open_ephemeral_resource_impl__mutmut_50': x__open_ephemeral_resource_impl__mutmut_50, 
    'x__open_ephemeral_resource_impl__mutmut_51': x__open_ephemeral_resource_impl__mutmut_51, 
    'x__open_ephemeral_resource_impl__mutmut_52': x__open_ephemeral_resource_impl__mutmut_52, 
    'x__open_ephemeral_resource_impl__mutmut_53': x__open_ephemeral_resource_impl__mutmut_53, 
    'x__open_ephemeral_resource_impl__mutmut_54': x__open_ephemeral_resource_impl__mutmut_54, 
    'x__open_ephemeral_resource_impl__mutmut_55': x__open_ephemeral_resource_impl__mutmut_55
}

def _open_ephemeral_resource_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__open_ephemeral_resource_impl__mutmut_orig, x__open_ephemeral_resource_impl__mutmut_mutants, args, kwargs)
    return result 

_open_ephemeral_resource_impl.__signature__ = _mutmut_signature(x__open_ephemeral_resource_impl__mutmut_orig)
x__open_ephemeral_resource_impl__mutmut_orig.__name__ = 'x__open_ephemeral_resource_impl'
