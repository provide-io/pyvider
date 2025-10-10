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

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", {}):
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=resource_name))
            logger.debug(f"Discovered resource: {resource_name}")

        # Get data sources if any
        data_sources = []
        for ds_name in hub.registry.get("data_source", {}):
            data_sources.append(pb.GetMetadata.DataSourceMetadata(type_name=ds_name))
            logger.debug(f"Discovered data source: {ds_name}")

        # Get functions if any
        functions = []
        for func_name in hub.registry.get("function", {}):
            functions.append(pb.GetMetadata.FunctionMetadata(name=func_name))
            logger.debug(f"Discovered function: {func_name}")

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
        logger.error(f"Error in GetMetadata: {e}", exc_info=True)
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


# 🐍🏗⛮️
