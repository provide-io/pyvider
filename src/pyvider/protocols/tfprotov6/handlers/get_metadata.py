#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import get_filtered_components
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("GetMetadata")
async def GetMetadataHandler(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Get provider metadata with dynamically discovered resources."""
    return await _get_metadata_impl(request, context)


def _advertise(component_type: str, metadata_class: Any, name_field: str = "type_name") -> list[Any]:
    """Advertise every production component of one kind.

    Terraform routes an RPC only to a type name it was told about here, so the
    same production/test filter has to apply to all of them alike.
    """
    entries = []
    for name in get_filtered_components(component_type):
        entries.append(metadata_class(**{name_field: name}))
        logger.debug(
            "Component discovered during metadata collection",
            operation="get_metadata",
            component_type=component_type,
            component_name=name,
        )
    return entries


async def _get_metadata_impl(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    logger.debug(
        "GetMetadata handler called",
        operation="get_metadata",
        handler="GetMetadata",
    )

    try:
        resources = _advertise("resource", pb.GetMetadata.ResourceMetadata)
        data_sources = _advertise("data_source", pb.GetMetadata.DataSourceMetadata)
        functions = _advertise("function", pb.GetMetadata.FunctionMetadata, name_field="name")
        ephemeral_resources = _advertise("ephemeral_resource", pb.GetMetadata.EphemeralMetadata)
        # State stores back the pluggable remote-state RPCs, list resources back
        # ListResource, and actions back the action RPCs.
        state_stores = _advertise("state_store", pb.GetMetadata.StateStoreMetadata)
        list_resources = _advertise("list_resource", pb.GetMetadata.ListResourceMetadata)
        actions = _advertise("action", pb.GetMetadata.ActionMetadata)

        logger.info(
            "GetMetadata completed successfully",
            operation="get_metadata",
            resource_count=len(resources),
            data_source_count=len(data_sources),
            function_count=len(functions),
            ephemeral_resource_count=len(ephemeral_resources),
            state_store_count=len(state_stores),
            list_resource_count=len(list_resources),
            action_count=len(actions),
        )

        return pb.GetMetadata.Response(
            server_capabilities=pb.ServerCapabilities(
                plan_destroy=True,
                get_provider_schema_optional=True,
                move_resource_state=True,
                generate_resource_config=True,
            ),
            resources=resources,
            data_sources=data_sources,
            functions=functions,
            ephemeral_resources=ephemeral_resources,
            list_resources=list_resources,
            state_stores=state_stores,
            actions=actions,
            diagnostics=[],
        )

    except Exception as e:
        logger.error(
            "GetMetadata handler failed",
            operation="get_metadata",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Failed to discover provider metadata: {e!s}\n\n"
            f"Suggestion: Ensure all resources, data sources, and functions are properly registered "
            f"using @resource, @data_source, and @function decorators.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that component decorators are applied correctly\n"
            f"  2. Verify that the hub discovery process completed successfully\n"
            f"  3. Review provider logs for component registration errors\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {e!s}"
        )

        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Provider metadata discovery failed",
                    detail=error_detail,
                )
            ]
        )


# 🐍🏗️🔚
