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


async def _get_metadata_impl(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    logger.debug(
        "GetMetadata handler called",
        operation="get_metadata",
        handler="GetMetadata",
    )

    try:
        # Discover production-usable resources, filtering test-only components when needed.
        all_resources = get_filtered_components("resource")
        resources = []
        for resource_name in all_resources:
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=resource_name))
            logger.debug(
                "Resource discovered during metadata collection",
                operation="get_metadata",
                component_type="resource",
                component_name=resource_name,
            )

        # Data sources should respect the same production/test-mode filter behavior.
        all_data_sources = get_filtered_components("data_source")
        data_sources = []
        for ds_name in all_data_sources:
            data_sources.append(pb.GetMetadata.DataSourceMetadata(type_name=ds_name))
            logger.debug(
                "Data source discovered during metadata collection",
                operation="get_metadata",
                component_type="data_source",
                component_name=ds_name,
            )

        # Functions should respect the same production/test-mode filter behavior.
        all_functions = get_filtered_components("function")
        functions = []
        for func_name in all_functions:
            functions.append(pb.GetMetadata.FunctionMetadata(name=func_name))
            logger.debug(
                "Function discovered during metadata collection",
                operation="get_metadata",
                component_type="function",
                component_name=func_name,
            )

        # Ephemerals should respect production/test-mode filtering.
        all_ephemerals = get_filtered_components("ephemeral_resource")
        ephemeral_resources = []
        for name in all_ephemerals:
            ephemeral_resources.append(pb.GetMetadata.EphemeralMetadata(type_name=name))
            logger.debug(
                "Ephemeral resource discovered during metadata collection",
                operation="get_metadata",
                component_type="ephemeral_resource",
                component_name=name,
            )

        # State stores registered via @register_state_store back the pluggable
        # remote-state RPCs; Terraform needs them advertised to route those calls.
        all_state_stores = get_filtered_components("state_store")
        state_stores = []
        for name in all_state_stores:
            state_stores.append(pb.GetMetadata.StateStoreMetadata(type_name=name))
            logger.debug(
                "State store discovered during metadata collection",
                operation="get_metadata",
                component_type="state_store",
                component_name=name,
            )

        # List resources registered via @register_list_resource answer the
        # ListResource RPC; Terraform only calls it for advertised type names.
        all_list_resources = get_filtered_components("list_resource")
        list_resources = []
        for name in all_list_resources:
            list_resources.append(pb.GetMetadata.ListResourceMetadata(type_name=name))
            logger.debug(
                "List resource discovered during metadata collection",
                operation="get_metadata",
                component_type="list_resource",
                component_name=name,
            )

        # Actions registered via @register_action back the action RPCs.
        all_actions = get_filtered_components("action")
        actions = []
        for name in all_actions:
            actions.append(pb.GetMetadata.ActionMetadata(type_name=name))
            logger.debug(
                "Action discovered during metadata collection",
                operation="get_metadata",
                component_type="action",
                component_name=name,
            )

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
