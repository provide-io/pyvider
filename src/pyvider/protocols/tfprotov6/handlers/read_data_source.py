#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import DataSourceError, PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    check_test_only_access,
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
    logger.debug(
        "Starting data source read operation",
        operation="read_data_source",
        data_source_type=request.type_name,
    )

    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            logger.error(
                "Data source type not found during read operation",
                operation="read_data_source",
                data_source_type=request.type_name,
                registered_data_sources=list(hub.get_components("data_source").keys())
                if hub.get_components("data_source")
                else [],
            )

            err = DataSourceError(
                f"Data source type '{request.type_name}' not registered.\n\n"
                f"Suggestion: Ensure the data source is registered using the @data_source decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the data source class has the @data_source decorator\n"
                f"  2. Verify the data source module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered data sources\n"
                f"  4. Review provider logs for component registration errors\n"
                f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
            err.add_context("data_source.type_name", request.type_name)
            err.add_context("terraform.summary", "Unknown data source type")
            err.add_context(
                "terraform.detail",
                f"The data source type '{request.type_name}' is not registered with this provider.",
            )
            raise err

        # Check if this is a test-only component accessed without test mode
        check_test_only_access(ds_class, request.type_name, "data_source")

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
        resource_context = ResourceContext(config=config_instance, test_mode_enabled=test_mode_enabled)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)

        logger.debug(
            "Checking capability injection for data source",
            operation="read_data_source",
            data_source_type=request.type_name,
            parent_capability=parent_capability,
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
                    "Auto-injected capability for data source",
                    operation="read_data_source",
                    data_source_type=request.type_name,
                    capability_name=parent_capability,
                )
            else:
                logger.warning(
                    "Capability not found for data source",
                    operation="read_data_source",
                    data_source_type=request.type_name,
                    capability_name=parent_capability,
                )
        else:
            logger.debug(
                "No capability injection needed for data source",
                operation="read_data_source",
                data_source_type=request.type_name,
            )

        logger.debug(
            "Calling data source read method",
            operation="read_data_source",
            data_source_type=request.type_name,
            injected_capabilities=list(read_kwargs.keys()),
        )
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack

            logger.info(
                "Data source read completed successfully with state",
                operation="read_data_source",
                data_source_type=request.type_name,
                has_state=True,
            )
        else:
            response.state.msgpack = b"\xc0"  # Represents null
            logger.info(
                "Data source read completed with null state",
                operation="read_data_source",
                data_source_type=request.type_name,
                has_state=False,
            )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Data source read failed with known error",
            operation="read_data_source",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Data source read failed with unexpected error",
            operation="read_data_source",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        logger.debug(
            "Adding resource context diagnostics to response",
            operation="read_data_source",
            data_source_type=request.type_name,
            diagnostic_count=len(resource_context.diagnostics),
        )
        response.diagnostics.extend(resource_context.diagnostics)

    return response


# 🐍🏗️🔚
