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


async def _read_data_source_impl(
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
