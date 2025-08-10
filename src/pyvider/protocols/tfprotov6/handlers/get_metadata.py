#
# pyvider/protocols/tfprotov6/handlers/get_metadata.py
#

from typing import Any

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.telemetry import logger


async def GetMetadataHandler(
    request: pb.GetMetadata.Request, context: Any
) -> pb.GetMetadata.Response:
    """Get provider metadata with dynamically discovered resources."""
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
