import time
from typing import Any

from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
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
async def ReadDataSourceHandler(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Handle read data source request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ReadDataSource")

    try:
        return await _read_data_source_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ReadDataSource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ReadDataSource")


async def x__read_data_source_impl__mutmut_orig(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_1(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = None
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_2(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = ""
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_3(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = None
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_4(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component(None, request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_5(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", None)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_6(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component(request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_7(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", )
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_8(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("XXdata_sourceXX", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_9(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("DATA_SOURCE", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_10(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_11(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(None)

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_12(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = None
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_13(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = None
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_14(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(None, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_15(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=None)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_16(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_17(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, )
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_18(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = None

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_19(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(None, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_20(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, None)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_21(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_22(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, )

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_23(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = None
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_24(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = None

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_25(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=None)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_26(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = None
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_27(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = None
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_28(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(None, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_29(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, None, None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_30(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr("_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_31(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_32(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", )
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_33(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "XX_parent_capabilityXX", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_34(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_PARENT_CAPABILITY", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_35(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            None
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_36(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability or parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_37(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability == "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_38(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "XXproviderXX":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_39(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "PROVIDER":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_40(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = None
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_41(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component(None, parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_42(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", None)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_43(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component(parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_44(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", )
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_45(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("XXcapabilityXX", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_46(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("CAPABILITY", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_47(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = None
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_48(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = None
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_49(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = None
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_50(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    None
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_51(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    None
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_52(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(None)

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_53(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(None)
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_54(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(None)}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_55(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = None

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_56(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(None, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_57(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(**read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_58(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, )

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_59(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_60(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = None
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_61(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(None)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_62(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = None
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_63(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = None

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_64(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(None)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_65(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = None
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_66(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(None, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_67(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=None)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_68(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_69(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, )
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_70(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = None
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_71(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = None  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_72(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"XX\xc0XX"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_73(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_74(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xC0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_75(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_76(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_77(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_78(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = None
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_79(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_80(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_81(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context or resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_data_source_impl__mutmut_82(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            raise ValueError(f"Data source type '{request.type_name}' not registered")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()
        resource_context = ResourceContext(config=config_instance)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)
        from provide.foundation import logger

        logger.debug(
            f"DATA_SOURCE_DISPATCH 🔍 Checking capability injection for '{request.type_name}' parent_capability={parent_capability}"
        )
        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    f"DATA_SOURCE_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{request.type_name}'"
                )
            else:
                logger.warning(
                    f"DATA_SOURCE_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{request.type_name}'"
                )
        else:
            logger.debug(f"DATA_SOURCE_DISPATCH ➡️ No capability injection needed for '{request.type_name}'")

        logger.debug(f"DATA_SOURCE_DISPATCH 🚀 Calling read with kwargs: {list(read_kwargs.keys())}")
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack
        else:
            response.state.msgpack = b"\xc0"  # Represents null

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(None)

    return response

x__read_data_source_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__read_data_source_impl__mutmut_1': x__read_data_source_impl__mutmut_1, 
    'x__read_data_source_impl__mutmut_2': x__read_data_source_impl__mutmut_2, 
    'x__read_data_source_impl__mutmut_3': x__read_data_source_impl__mutmut_3, 
    'x__read_data_source_impl__mutmut_4': x__read_data_source_impl__mutmut_4, 
    'x__read_data_source_impl__mutmut_5': x__read_data_source_impl__mutmut_5, 
    'x__read_data_source_impl__mutmut_6': x__read_data_source_impl__mutmut_6, 
    'x__read_data_source_impl__mutmut_7': x__read_data_source_impl__mutmut_7, 
    'x__read_data_source_impl__mutmut_8': x__read_data_source_impl__mutmut_8, 
    'x__read_data_source_impl__mutmut_9': x__read_data_source_impl__mutmut_9, 
    'x__read_data_source_impl__mutmut_10': x__read_data_source_impl__mutmut_10, 
    'x__read_data_source_impl__mutmut_11': x__read_data_source_impl__mutmut_11, 
    'x__read_data_source_impl__mutmut_12': x__read_data_source_impl__mutmut_12, 
    'x__read_data_source_impl__mutmut_13': x__read_data_source_impl__mutmut_13, 
    'x__read_data_source_impl__mutmut_14': x__read_data_source_impl__mutmut_14, 
    'x__read_data_source_impl__mutmut_15': x__read_data_source_impl__mutmut_15, 
    'x__read_data_source_impl__mutmut_16': x__read_data_source_impl__mutmut_16, 
    'x__read_data_source_impl__mutmut_17': x__read_data_source_impl__mutmut_17, 
    'x__read_data_source_impl__mutmut_18': x__read_data_source_impl__mutmut_18, 
    'x__read_data_source_impl__mutmut_19': x__read_data_source_impl__mutmut_19, 
    'x__read_data_source_impl__mutmut_20': x__read_data_source_impl__mutmut_20, 
    'x__read_data_source_impl__mutmut_21': x__read_data_source_impl__mutmut_21, 
    'x__read_data_source_impl__mutmut_22': x__read_data_source_impl__mutmut_22, 
    'x__read_data_source_impl__mutmut_23': x__read_data_source_impl__mutmut_23, 
    'x__read_data_source_impl__mutmut_24': x__read_data_source_impl__mutmut_24, 
    'x__read_data_source_impl__mutmut_25': x__read_data_source_impl__mutmut_25, 
    'x__read_data_source_impl__mutmut_26': x__read_data_source_impl__mutmut_26, 
    'x__read_data_source_impl__mutmut_27': x__read_data_source_impl__mutmut_27, 
    'x__read_data_source_impl__mutmut_28': x__read_data_source_impl__mutmut_28, 
    'x__read_data_source_impl__mutmut_29': x__read_data_source_impl__mutmut_29, 
    'x__read_data_source_impl__mutmut_30': x__read_data_source_impl__mutmut_30, 
    'x__read_data_source_impl__mutmut_31': x__read_data_source_impl__mutmut_31, 
    'x__read_data_source_impl__mutmut_32': x__read_data_source_impl__mutmut_32, 
    'x__read_data_source_impl__mutmut_33': x__read_data_source_impl__mutmut_33, 
    'x__read_data_source_impl__mutmut_34': x__read_data_source_impl__mutmut_34, 
    'x__read_data_source_impl__mutmut_35': x__read_data_source_impl__mutmut_35, 
    'x__read_data_source_impl__mutmut_36': x__read_data_source_impl__mutmut_36, 
    'x__read_data_source_impl__mutmut_37': x__read_data_source_impl__mutmut_37, 
    'x__read_data_source_impl__mutmut_38': x__read_data_source_impl__mutmut_38, 
    'x__read_data_source_impl__mutmut_39': x__read_data_source_impl__mutmut_39, 
    'x__read_data_source_impl__mutmut_40': x__read_data_source_impl__mutmut_40, 
    'x__read_data_source_impl__mutmut_41': x__read_data_source_impl__mutmut_41, 
    'x__read_data_source_impl__mutmut_42': x__read_data_source_impl__mutmut_42, 
    'x__read_data_source_impl__mutmut_43': x__read_data_source_impl__mutmut_43, 
    'x__read_data_source_impl__mutmut_44': x__read_data_source_impl__mutmut_44, 
    'x__read_data_source_impl__mutmut_45': x__read_data_source_impl__mutmut_45, 
    'x__read_data_source_impl__mutmut_46': x__read_data_source_impl__mutmut_46, 
    'x__read_data_source_impl__mutmut_47': x__read_data_source_impl__mutmut_47, 
    'x__read_data_source_impl__mutmut_48': x__read_data_source_impl__mutmut_48, 
    'x__read_data_source_impl__mutmut_49': x__read_data_source_impl__mutmut_49, 
    'x__read_data_source_impl__mutmut_50': x__read_data_source_impl__mutmut_50, 
    'x__read_data_source_impl__mutmut_51': x__read_data_source_impl__mutmut_51, 
    'x__read_data_source_impl__mutmut_52': x__read_data_source_impl__mutmut_52, 
    'x__read_data_source_impl__mutmut_53': x__read_data_source_impl__mutmut_53, 
    'x__read_data_source_impl__mutmut_54': x__read_data_source_impl__mutmut_54, 
    'x__read_data_source_impl__mutmut_55': x__read_data_source_impl__mutmut_55, 
    'x__read_data_source_impl__mutmut_56': x__read_data_source_impl__mutmut_56, 
    'x__read_data_source_impl__mutmut_57': x__read_data_source_impl__mutmut_57, 
    'x__read_data_source_impl__mutmut_58': x__read_data_source_impl__mutmut_58, 
    'x__read_data_source_impl__mutmut_59': x__read_data_source_impl__mutmut_59, 
    'x__read_data_source_impl__mutmut_60': x__read_data_source_impl__mutmut_60, 
    'x__read_data_source_impl__mutmut_61': x__read_data_source_impl__mutmut_61, 
    'x__read_data_source_impl__mutmut_62': x__read_data_source_impl__mutmut_62, 
    'x__read_data_source_impl__mutmut_63': x__read_data_source_impl__mutmut_63, 
    'x__read_data_source_impl__mutmut_64': x__read_data_source_impl__mutmut_64, 
    'x__read_data_source_impl__mutmut_65': x__read_data_source_impl__mutmut_65, 
    'x__read_data_source_impl__mutmut_66': x__read_data_source_impl__mutmut_66, 
    'x__read_data_source_impl__mutmut_67': x__read_data_source_impl__mutmut_67, 
    'x__read_data_source_impl__mutmut_68': x__read_data_source_impl__mutmut_68, 
    'x__read_data_source_impl__mutmut_69': x__read_data_source_impl__mutmut_69, 
    'x__read_data_source_impl__mutmut_70': x__read_data_source_impl__mutmut_70, 
    'x__read_data_source_impl__mutmut_71': x__read_data_source_impl__mutmut_71, 
    'x__read_data_source_impl__mutmut_72': x__read_data_source_impl__mutmut_72, 
    'x__read_data_source_impl__mutmut_73': x__read_data_source_impl__mutmut_73, 
    'x__read_data_source_impl__mutmut_74': x__read_data_source_impl__mutmut_74, 
    'x__read_data_source_impl__mutmut_75': x__read_data_source_impl__mutmut_75, 
    'x__read_data_source_impl__mutmut_76': x__read_data_source_impl__mutmut_76, 
    'x__read_data_source_impl__mutmut_77': x__read_data_source_impl__mutmut_77, 
    'x__read_data_source_impl__mutmut_78': x__read_data_source_impl__mutmut_78, 
    'x__read_data_source_impl__mutmut_79': x__read_data_source_impl__mutmut_79, 
    'x__read_data_source_impl__mutmut_80': x__read_data_source_impl__mutmut_80, 
    'x__read_data_source_impl__mutmut_81': x__read_data_source_impl__mutmut_81, 
    'x__read_data_source_impl__mutmut_82': x__read_data_source_impl__mutmut_82
}

def _read_data_source_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__read_data_source_impl__mutmut_orig, x__read_data_source_impl__mutmut_mutants, args, kwargs)
    return result 

_read_data_source_impl.__signature__ = _mutmut_signature(x__read_data_source_impl__mutmut_orig)
x__read_data_source_impl__mutmut_orig.__name__ = 'x__read_data_source_impl'
