import time
from typing import Any

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
async def ValidateResourceConfigHandler(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Handle validate resource config request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateResourceConfig")

    try:
        return await _validate_resource_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateResourceConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateResourceConfig")


async def x__validate_resource_config_impl__mutmut_orig(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_1(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_2(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = None
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_3(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component(None, request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_4(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", None)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_5(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component(request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_6(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", )
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_7(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("XXresourceXX", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_8(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("RESOURCE", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_9(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_10(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(None)
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_11(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = None

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_12(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = None

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_13(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(None, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_14(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=None)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_15(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_16(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, )

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_17(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = None

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_18(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(None, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_19(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, None)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_20(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_21(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, )

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_22(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is not None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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


async def x__validate_resource_config_impl__mutmut_23(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = None
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


async def x__validate_resource_config_impl__mutmut_24(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = None

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


async def x__validate_resource_config_impl__mutmut_25(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(None)

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


async def x__validate_resource_config_impl__mutmut_26(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = None
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_27(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=None, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_28(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=None)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_29(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_30(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, )
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_31(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(None)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_32(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_33(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_34(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_35(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = None
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_36(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

        resource_handler = resource_class()
        validation_errors = await resource_handler.validate(config_instance)

        for err_msg in validation_errors:
            diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=err_msg)
            response.diagnostics.append(diag)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    return response


async def x__validate_resource_config_impl__mutmut_37(
    request: pb.ValidateResourceConfig.Request, context: Any
) -> pb.ValidateResourceConfig.Response:
    """Implementation of ValidateResourceConfig handler."""
    response = pb.ValidateResourceConfig.Response()
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")
        resource_schema = resource_class.get_schema()

        config_cty = unmarshal(request.config, schema=resource_schema.block)

        # Try to create typed attrs instance from CTY config
        # If values are unknown/computed, this will return None (expected during planning)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        # If config_instance is None, skip custom validation
        # Resources should use ctx.is_field_unknown() to handle unknown values properly
        if config_instance is None:
            # Schema validation already passed, custom validation not possible with unknown values
            return response

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
        response.diagnostics.append(None)

    return response

x__validate_resource_config_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__validate_resource_config_impl__mutmut_1': x__validate_resource_config_impl__mutmut_1, 
    'x__validate_resource_config_impl__mutmut_2': x__validate_resource_config_impl__mutmut_2, 
    'x__validate_resource_config_impl__mutmut_3': x__validate_resource_config_impl__mutmut_3, 
    'x__validate_resource_config_impl__mutmut_4': x__validate_resource_config_impl__mutmut_4, 
    'x__validate_resource_config_impl__mutmut_5': x__validate_resource_config_impl__mutmut_5, 
    'x__validate_resource_config_impl__mutmut_6': x__validate_resource_config_impl__mutmut_6, 
    'x__validate_resource_config_impl__mutmut_7': x__validate_resource_config_impl__mutmut_7, 
    'x__validate_resource_config_impl__mutmut_8': x__validate_resource_config_impl__mutmut_8, 
    'x__validate_resource_config_impl__mutmut_9': x__validate_resource_config_impl__mutmut_9, 
    'x__validate_resource_config_impl__mutmut_10': x__validate_resource_config_impl__mutmut_10, 
    'x__validate_resource_config_impl__mutmut_11': x__validate_resource_config_impl__mutmut_11, 
    'x__validate_resource_config_impl__mutmut_12': x__validate_resource_config_impl__mutmut_12, 
    'x__validate_resource_config_impl__mutmut_13': x__validate_resource_config_impl__mutmut_13, 
    'x__validate_resource_config_impl__mutmut_14': x__validate_resource_config_impl__mutmut_14, 
    'x__validate_resource_config_impl__mutmut_15': x__validate_resource_config_impl__mutmut_15, 
    'x__validate_resource_config_impl__mutmut_16': x__validate_resource_config_impl__mutmut_16, 
    'x__validate_resource_config_impl__mutmut_17': x__validate_resource_config_impl__mutmut_17, 
    'x__validate_resource_config_impl__mutmut_18': x__validate_resource_config_impl__mutmut_18, 
    'x__validate_resource_config_impl__mutmut_19': x__validate_resource_config_impl__mutmut_19, 
    'x__validate_resource_config_impl__mutmut_20': x__validate_resource_config_impl__mutmut_20, 
    'x__validate_resource_config_impl__mutmut_21': x__validate_resource_config_impl__mutmut_21, 
    'x__validate_resource_config_impl__mutmut_22': x__validate_resource_config_impl__mutmut_22, 
    'x__validate_resource_config_impl__mutmut_23': x__validate_resource_config_impl__mutmut_23, 
    'x__validate_resource_config_impl__mutmut_24': x__validate_resource_config_impl__mutmut_24, 
    'x__validate_resource_config_impl__mutmut_25': x__validate_resource_config_impl__mutmut_25, 
    'x__validate_resource_config_impl__mutmut_26': x__validate_resource_config_impl__mutmut_26, 
    'x__validate_resource_config_impl__mutmut_27': x__validate_resource_config_impl__mutmut_27, 
    'x__validate_resource_config_impl__mutmut_28': x__validate_resource_config_impl__mutmut_28, 
    'x__validate_resource_config_impl__mutmut_29': x__validate_resource_config_impl__mutmut_29, 
    'x__validate_resource_config_impl__mutmut_30': x__validate_resource_config_impl__mutmut_30, 
    'x__validate_resource_config_impl__mutmut_31': x__validate_resource_config_impl__mutmut_31, 
    'x__validate_resource_config_impl__mutmut_32': x__validate_resource_config_impl__mutmut_32, 
    'x__validate_resource_config_impl__mutmut_33': x__validate_resource_config_impl__mutmut_33, 
    'x__validate_resource_config_impl__mutmut_34': x__validate_resource_config_impl__mutmut_34, 
    'x__validate_resource_config_impl__mutmut_35': x__validate_resource_config_impl__mutmut_35, 
    'x__validate_resource_config_impl__mutmut_36': x__validate_resource_config_impl__mutmut_36, 
    'x__validate_resource_config_impl__mutmut_37': x__validate_resource_config_impl__mutmut_37
}

def _validate_resource_config_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__validate_resource_config_impl__mutmut_orig, x__validate_resource_config_impl__mutmut_mutants, args, kwargs)
    return result 

_validate_resource_config_impl.__signature__ = _mutmut_signature(x__validate_resource_config_impl__mutmut_orig)
x__validate_resource_config_impl__mutmut_orig.__name__ = 'x__validate_resource_config_impl'
