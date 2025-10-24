#
# pyvider/protocols/tfprotov6/handlers/get_metadata.py
#

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def GetMetadataHandler(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Get provider metadata with dynamically discovered resources."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="GetMetadata")

    try:
        return await _get_metadata_impl(request, context)
    except Exception:
        handler_errors.inc(handler="GetMetadata")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="GetMetadata")


async def _get_metadata_impl(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug(
        "GetMetadata handler called",
        operation="get_metadata",
        handler="GetMetadata",
    )

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.get_components("resource"):
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=resource_name))
            logger.debug(
                "Resource discovered during metadata collection",
                operation="get_metadata",
                component_type="resource",
                component_name=resource_name,
            )

        # Get data sources if any
        data_sources = []
        for ds_name in hub.get_components("data_source"):
            data_sources.append(pb.GetMetadata.DataSourceMetadata(type_name=ds_name))
            logger.debug(
                "Data source discovered during metadata collection",
                operation="get_metadata",
                component_type="data_source",
                component_name=ds_name,
            )

        # Get functions if any
        functions = []
        for func_name in hub.get_components("function"):
            functions.append(pb.GetMetadata.FunctionMetadata(name=func_name))
            logger.debug(
                "Function discovered during metadata collection",
                operation="get_metadata",
                component_type="function",
                component_name=func_name,
            )

        logger.info(
            "GetMetadata completed successfully",
            operation="get_metadata",
            resource_count=len(resources),
            data_source_count=len(data_sources),
            function_count=len(functions),
        )

        response = pb.GetMetadata.Response(
            server_capabilities=pb.ServerCapabilities(
                plan_destroy=True,
                # THE FIX: This flag MUST be True to allow Terraform to use
                # GetMetadata for function discovery alongside GetProviderSchema.
                get_provider_schema_optional=True,
                move_resource_state=True,
            ),
            resources=resources,
            data_sources=data_sources,
            functions=functions,
            diagnostics=[],
        )

        return response

    except Exception as e:
        logger.error(
            "GetMetadata handler failed",
            operation="get_metadata",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Failed to discover provider metadata: {str(e)}\n\n"
            f"Suggestion: Ensure all resources, data sources, and functions are properly registered "
            f"using @resource, @data_source, and @function decorators.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that component decorators are applied correctly\n"
            f"  2. Verify that the hub discovery process completed successfully\n"
            f"  3. Review provider logs for component registration errors\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {str(e)}"
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


# 🐍🏗⛮️
