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
async def ValidateDataResourceConfigHandler(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Handle validate data resource config request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateDataResourceConfig")

    try:
        return await _validate_data_resource_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateDataResourceConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateDataResourceConfig")


async def x__validate_data_resource_config_impl__mutmut_orig(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_1(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_2(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = None
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_3(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component(None, request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_4(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", None)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_5(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component(request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_6(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", )
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_7(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("XXdata_sourceXX", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_8(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("DATA_SOURCE", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_9(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_10(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(None)

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_11(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = None
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_12(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = None
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_13(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(None, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_14(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=None)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_15(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_16(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, )
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_17(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = None

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_18(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(None, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_19(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, None)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_20(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_21(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, )

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_22(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = None
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_23(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = None

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_24(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(None)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_25(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = None
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_26(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=None,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_27(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=None,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_28(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_29(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_30(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(None)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_31(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_32(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_33(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_34(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(None, exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_35(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=None)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_36(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_37(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_38(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("XXUnhandled error in ValidateDataResourceConfigHandlerXX", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_39(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("unhandled error in validatedataresourceconfighandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_40(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("UNHANDLED ERROR IN VALIDATEDATARESOURCECONFIGHANDLER", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_41(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=False)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_42(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = None
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_43(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    return response


async def x__validate_data_resource_config_impl__mutmut_44(
    request: pb.ValidateDataResourceConfig.Request, context: Any
) -> pb.ValidateDataResourceConfig.Response:
    """Implementation of ValidateDataResourceConfig handler."""
    response = pb.ValidateDataResourceConfig.Response()
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source_instance = ds_class()
        validation_errors = await data_source_instance.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary=err_msg,
            )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ValidateDataResourceConfigHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)

    return response

x__validate_data_resource_config_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__validate_data_resource_config_impl__mutmut_1': x__validate_data_resource_config_impl__mutmut_1, 
    'x__validate_data_resource_config_impl__mutmut_2': x__validate_data_resource_config_impl__mutmut_2, 
    'x__validate_data_resource_config_impl__mutmut_3': x__validate_data_resource_config_impl__mutmut_3, 
    'x__validate_data_resource_config_impl__mutmut_4': x__validate_data_resource_config_impl__mutmut_4, 
    'x__validate_data_resource_config_impl__mutmut_5': x__validate_data_resource_config_impl__mutmut_5, 
    'x__validate_data_resource_config_impl__mutmut_6': x__validate_data_resource_config_impl__mutmut_6, 
    'x__validate_data_resource_config_impl__mutmut_7': x__validate_data_resource_config_impl__mutmut_7, 
    'x__validate_data_resource_config_impl__mutmut_8': x__validate_data_resource_config_impl__mutmut_8, 
    'x__validate_data_resource_config_impl__mutmut_9': x__validate_data_resource_config_impl__mutmut_9, 
    'x__validate_data_resource_config_impl__mutmut_10': x__validate_data_resource_config_impl__mutmut_10, 
    'x__validate_data_resource_config_impl__mutmut_11': x__validate_data_resource_config_impl__mutmut_11, 
    'x__validate_data_resource_config_impl__mutmut_12': x__validate_data_resource_config_impl__mutmut_12, 
    'x__validate_data_resource_config_impl__mutmut_13': x__validate_data_resource_config_impl__mutmut_13, 
    'x__validate_data_resource_config_impl__mutmut_14': x__validate_data_resource_config_impl__mutmut_14, 
    'x__validate_data_resource_config_impl__mutmut_15': x__validate_data_resource_config_impl__mutmut_15, 
    'x__validate_data_resource_config_impl__mutmut_16': x__validate_data_resource_config_impl__mutmut_16, 
    'x__validate_data_resource_config_impl__mutmut_17': x__validate_data_resource_config_impl__mutmut_17, 
    'x__validate_data_resource_config_impl__mutmut_18': x__validate_data_resource_config_impl__mutmut_18, 
    'x__validate_data_resource_config_impl__mutmut_19': x__validate_data_resource_config_impl__mutmut_19, 
    'x__validate_data_resource_config_impl__mutmut_20': x__validate_data_resource_config_impl__mutmut_20, 
    'x__validate_data_resource_config_impl__mutmut_21': x__validate_data_resource_config_impl__mutmut_21, 
    'x__validate_data_resource_config_impl__mutmut_22': x__validate_data_resource_config_impl__mutmut_22, 
    'x__validate_data_resource_config_impl__mutmut_23': x__validate_data_resource_config_impl__mutmut_23, 
    'x__validate_data_resource_config_impl__mutmut_24': x__validate_data_resource_config_impl__mutmut_24, 
    'x__validate_data_resource_config_impl__mutmut_25': x__validate_data_resource_config_impl__mutmut_25, 
    'x__validate_data_resource_config_impl__mutmut_26': x__validate_data_resource_config_impl__mutmut_26, 
    'x__validate_data_resource_config_impl__mutmut_27': x__validate_data_resource_config_impl__mutmut_27, 
    'x__validate_data_resource_config_impl__mutmut_28': x__validate_data_resource_config_impl__mutmut_28, 
    'x__validate_data_resource_config_impl__mutmut_29': x__validate_data_resource_config_impl__mutmut_29, 
    'x__validate_data_resource_config_impl__mutmut_30': x__validate_data_resource_config_impl__mutmut_30, 
    'x__validate_data_resource_config_impl__mutmut_31': x__validate_data_resource_config_impl__mutmut_31, 
    'x__validate_data_resource_config_impl__mutmut_32': x__validate_data_resource_config_impl__mutmut_32, 
    'x__validate_data_resource_config_impl__mutmut_33': x__validate_data_resource_config_impl__mutmut_33, 
    'x__validate_data_resource_config_impl__mutmut_34': x__validate_data_resource_config_impl__mutmut_34, 
    'x__validate_data_resource_config_impl__mutmut_35': x__validate_data_resource_config_impl__mutmut_35, 
    'x__validate_data_resource_config_impl__mutmut_36': x__validate_data_resource_config_impl__mutmut_36, 
    'x__validate_data_resource_config_impl__mutmut_37': x__validate_data_resource_config_impl__mutmut_37, 
    'x__validate_data_resource_config_impl__mutmut_38': x__validate_data_resource_config_impl__mutmut_38, 
    'x__validate_data_resource_config_impl__mutmut_39': x__validate_data_resource_config_impl__mutmut_39, 
    'x__validate_data_resource_config_impl__mutmut_40': x__validate_data_resource_config_impl__mutmut_40, 
    'x__validate_data_resource_config_impl__mutmut_41': x__validate_data_resource_config_impl__mutmut_41, 
    'x__validate_data_resource_config_impl__mutmut_42': x__validate_data_resource_config_impl__mutmut_42, 
    'x__validate_data_resource_config_impl__mutmut_43': x__validate_data_resource_config_impl__mutmut_43, 
    'x__validate_data_resource_config_impl__mutmut_44': x__validate_data_resource_config_impl__mutmut_44
}

def _validate_data_resource_config_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__validate_data_resource_config_impl__mutmut_orig, x__validate_data_resource_config_impl__mutmut_mutants, args, kwargs)
    return result 

_validate_data_resource_config_impl.__signature__ = _mutmut_signature(x__validate_data_resource_config_impl__mutmut_orig)
x__validate_data_resource_config_impl__mutmut_orig.__name__ = 'x__validate_data_resource_config_impl'
