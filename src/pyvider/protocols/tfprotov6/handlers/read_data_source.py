#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.conversion import marshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import DataSourceError, Deferral, PyviderError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    check_test_only_access,
    create_diagnostic_from_exception,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@rpc_handler("ReadDataSource")
async def ReadDataSourceHandler(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Handle read data source request."""
    return await _read_data_source_impl(request, context)


def _registered_data_source(type_name: str) -> Any:
    """The registered data source class, or an error naming what to check."""
    ds_class = hub.get_component("data_source", type_name)
    if not ds_class:
        registered = hub.get_components("data_source")
        logger.error(
            "Data source type not found during read operation",
            operation="read_data_source",
            data_source_type=type_name,
            registered_data_sources=list(registered.keys()) if registered else [],
        )
        err = DataSourceError(
            f"Data source type '{type_name}' not registered.\n\n"
            f"Suggestion: Ensure the data source is registered using the @data_source decorator "
            f"and that component discovery has completed successfully.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that the data source class has the @data_source decorator\n"
            f"  2. Verify the data source module is imported by the provider\n"
            f"  3. Run 'pyvider components list' to see registered data sources\n"
            f"  4. Review provider logs for component registration errors\n"
            f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
        )
        err.add_context("data_source.type_name", type_name)
        err.add_context("terraform.summary", "Unknown data source type")
        err.add_context(
            "terraform.detail",
            f"The data source type '{type_name}' is not registered with this provider.",
        )
        raise err

    # Check if this is a test-only component accessed without test mode
    check_test_only_access(ds_class, type_name, "data_source")
    return ds_class


def _capability_kwargs(ds_class: Any, type_name: str) -> dict[str, Any]:
    """The capability a data source was registered under, ready to pass to read().

    A data source registered with `component_of` receives its parent capability
    as a keyword argument; one registered directly on the provider receives none.
    """
    parent_capability = getattr(ds_class, "_parent_capability", None)

    logger.debug(
        "Checking capability injection for data source",
        operation="read_data_source",
        data_source_type=type_name,
        parent_capability=parent_capability,
    )

    if not parent_capability or parent_capability == "provider":
        logger.debug(
            "No capability injection needed for data source",
            operation="read_data_source",
            data_source_type=type_name,
        )
        return {}

    capability_class = hub.get_component("capability", parent_capability)
    if not capability_class:
        logger.warning(
            "Capability not found for data source",
            operation="read_data_source",
            data_source_type=type_name,
            capability_name=parent_capability,
        )
        return {}

    # Ensure we have an instance, not a class
    capability_instance = capability_class() if isinstance(capability_class, type) else capability_class
    logger.debug(
        "Auto-injected capability for data source",
        operation="read_data_source",
        data_source_type=type_name,
        capability_name=parent_capability,
    )
    return {parent_capability: capability_instance}


def _write_state(
    response: pb.ReadDataSource.Response, ds_schema: Any, state_attrs_obj: Any, type_name: str
) -> None:
    """Marshal what read() returned into the response, or record that it returned nothing."""
    if state_attrs_obj is None:
        response.state.msgpack = b"\xc0"  # Represents null
        logger.info(
            "Data source read completed with null state",
            operation="read_data_source",
            data_source_type=type_name,
            has_state=False,
        )
        return

    raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
    state_cty = ds_schema.block.to_cty_type().validate(raw_state_dict)
    response.state.msgpack = marshal(state_cty, schema=ds_schema.block).msgpack

    logger.info(
        "Data source read completed successfully with state",
        operation="read_data_source",
        data_source_type=type_name,
        has_state=True,
    )


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
    resource_context: Any = None
    try:
        ds_class = _registered_data_source(request.type_name)
        ds_schema = ds_class.get_schema()
        config_instance = decode_config(ds_class, request.config)

        data_source = ds_class()

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
        resource_context = ResourceContext(config=config_instance, test_mode_enabled=test_mode_enabled)

        read_kwargs = _capability_kwargs(ds_class, request.type_name)

        logger.debug(
            "Calling data source read method",
            operation="read_data_source",
            data_source_type=request.type_name,
            injected_capabilities=list(read_kwargs.keys()),
        )
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        _write_state(response, ds_schema, state_attrs_obj, request.type_name)

    except Deferral as e:
        logger.info(
            "Response deferred",
            operation="read_data_source",
            data_source_type=request.type_name,
            reason=e.reason.name,
        )
        if not getattr(request.client_capabilities, "deferral_allowed", False):
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary="Invalid Deferral",
                detail="The provider raised a Deferral but Terraform did not set deferral_allowed for this request.",
            )
            response.diagnostics.append(diag)
        else:
            response.deferred.reason = pb.Deferred.Reason.Value(e.reason.name)  # type: ignore[assignment]
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
