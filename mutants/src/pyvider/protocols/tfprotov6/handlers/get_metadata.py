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


async def x__get_metadata_impl__mutmut_orig(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_1(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug(None)

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


async def x__get_metadata_impl__mutmut_2(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("XXGetMetadata calledXX")

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


async def x__get_metadata_impl__mutmut_3(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("getmetadata called")

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


async def x__get_metadata_impl__mutmut_4(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GETMETADATA CALLED")

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


async def x__get_metadata_impl__mutmut_5(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = None
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


async def x__get_metadata_impl__mutmut_6(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get(None, {}):
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


async def x__get_metadata_impl__mutmut_7(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", None):
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


async def x__get_metadata_impl__mutmut_8(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get({}):
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


async def x__get_metadata_impl__mutmut_9(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", ):
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


async def x__get_metadata_impl__mutmut_10(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("XXresourceXX", {}):
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


async def x__get_metadata_impl__mutmut_11(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("RESOURCE", {}):
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


async def x__get_metadata_impl__mutmut_12(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", {}):
            resources.append(None)
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


async def x__get_metadata_impl__mutmut_13(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", {}):
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=None))
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


async def x__get_metadata_impl__mutmut_14(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    from pyvider.hub import hub

    logger.debug("GetMetadata called")

    try:
        # Dynamically discover registered resources
        resources = []
        for resource_name in hub.registry.get("resource", {}):
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=resource_name))
            logger.debug(None)

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


async def x__get_metadata_impl__mutmut_15(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        data_sources = None
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


async def x__get_metadata_impl__mutmut_16(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get(None, {}):
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


async def x__get_metadata_impl__mutmut_17(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get("data_source", None):
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


async def x__get_metadata_impl__mutmut_18(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get({}):
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


async def x__get_metadata_impl__mutmut_19(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get("data_source", ):
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


async def x__get_metadata_impl__mutmut_20(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get("XXdata_sourceXX", {}):
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


async def x__get_metadata_impl__mutmut_21(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for ds_name in hub.registry.get("DATA_SOURCE", {}):
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


async def x__get_metadata_impl__mutmut_22(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            data_sources.append(None)
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


async def x__get_metadata_impl__mutmut_23(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            data_sources.append(pb.GetMetadata.DataSourceMetadata(type_name=None))
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


async def x__get_metadata_impl__mutmut_24(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            logger.debug(None)

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


async def x__get_metadata_impl__mutmut_25(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        functions = None
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


async def x__get_metadata_impl__mutmut_26(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get(None, {}):
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


async def x__get_metadata_impl__mutmut_27(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get("function", None):
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


async def x__get_metadata_impl__mutmut_28(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get({}):
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


async def x__get_metadata_impl__mutmut_29(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get("function", ):
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


async def x__get_metadata_impl__mutmut_30(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get("XXfunctionXX", {}):
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


async def x__get_metadata_impl__mutmut_31(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        for func_name in hub.registry.get("FUNCTION", {}):
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


async def x__get_metadata_impl__mutmut_32(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            functions.append(None)
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


async def x__get_metadata_impl__mutmut_33(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            functions.append(pb.GetMetadata.FunctionMetadata(name=None))
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


async def x__get_metadata_impl__mutmut_34(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            logger.debug(None)

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


async def x__get_metadata_impl__mutmut_35(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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

        response = None

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


async def x__get_metadata_impl__mutmut_36(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            server_capabilities=None,
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


async def x__get_metadata_impl__mutmut_37(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            resources=None,
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


async def x__get_metadata_impl__mutmut_38(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            data_sources=None,
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


async def x__get_metadata_impl__mutmut_39(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            functions=None,
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


async def x__get_metadata_impl__mutmut_40(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            diagnostics=None,
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


async def x__get_metadata_impl__mutmut_41(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_42(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_43(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_44(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_45(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_46(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                plan_destroy=None,
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


async def x__get_metadata_impl__mutmut_47(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                get_provider_schema_optional=None,
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


async def x__get_metadata_impl__mutmut_48(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                move_resource_state=None,
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


async def x__get_metadata_impl__mutmut_49(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_50(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_51(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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


async def x__get_metadata_impl__mutmut_52(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                plan_destroy=False,
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


async def x__get_metadata_impl__mutmut_53(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                get_provider_schema_optional=False,
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


async def x__get_metadata_impl__mutmut_54(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                move_resource_state=False,
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


async def x__get_metadata_impl__mutmut_55(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        logger.error(None, exc_info=True)
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_56(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        logger.error(f"Error in GetMetadata: {e}", exc_info=None)
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_57(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        logger.error(exc_info=True)
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_58(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        logger.error(f"Error in GetMetadata: {e}", )
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_59(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
        logger.error(f"Error in GetMetadata: {e}", exc_info=False)
        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_60(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
            diagnostics=None
        )


async def x__get_metadata_impl__mutmut_61(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    severity=None,
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_62(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    summary=None,
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_63(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    detail=None,
                )
            ]
        )


async def x__get_metadata_impl__mutmut_64(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    summary="GetMetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_65(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_66(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    )
            ]
        )


async def x__get_metadata_impl__mutmut_67(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    summary="XXGetMetadata errorXX",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_68(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    summary="getmetadata error",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_69(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    summary="GETMETADATA ERROR",
                    detail=str(e),
                )
            ]
        )


async def x__get_metadata_impl__mutmut_70(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
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
                    detail=str(None),
                )
            ]
        )

x__get_metadata_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_metadata_impl__mutmut_1': x__get_metadata_impl__mutmut_1, 
    'x__get_metadata_impl__mutmut_2': x__get_metadata_impl__mutmut_2, 
    'x__get_metadata_impl__mutmut_3': x__get_metadata_impl__mutmut_3, 
    'x__get_metadata_impl__mutmut_4': x__get_metadata_impl__mutmut_4, 
    'x__get_metadata_impl__mutmut_5': x__get_metadata_impl__mutmut_5, 
    'x__get_metadata_impl__mutmut_6': x__get_metadata_impl__mutmut_6, 
    'x__get_metadata_impl__mutmut_7': x__get_metadata_impl__mutmut_7, 
    'x__get_metadata_impl__mutmut_8': x__get_metadata_impl__mutmut_8, 
    'x__get_metadata_impl__mutmut_9': x__get_metadata_impl__mutmut_9, 
    'x__get_metadata_impl__mutmut_10': x__get_metadata_impl__mutmut_10, 
    'x__get_metadata_impl__mutmut_11': x__get_metadata_impl__mutmut_11, 
    'x__get_metadata_impl__mutmut_12': x__get_metadata_impl__mutmut_12, 
    'x__get_metadata_impl__mutmut_13': x__get_metadata_impl__mutmut_13, 
    'x__get_metadata_impl__mutmut_14': x__get_metadata_impl__mutmut_14, 
    'x__get_metadata_impl__mutmut_15': x__get_metadata_impl__mutmut_15, 
    'x__get_metadata_impl__mutmut_16': x__get_metadata_impl__mutmut_16, 
    'x__get_metadata_impl__mutmut_17': x__get_metadata_impl__mutmut_17, 
    'x__get_metadata_impl__mutmut_18': x__get_metadata_impl__mutmut_18, 
    'x__get_metadata_impl__mutmut_19': x__get_metadata_impl__mutmut_19, 
    'x__get_metadata_impl__mutmut_20': x__get_metadata_impl__mutmut_20, 
    'x__get_metadata_impl__mutmut_21': x__get_metadata_impl__mutmut_21, 
    'x__get_metadata_impl__mutmut_22': x__get_metadata_impl__mutmut_22, 
    'x__get_metadata_impl__mutmut_23': x__get_metadata_impl__mutmut_23, 
    'x__get_metadata_impl__mutmut_24': x__get_metadata_impl__mutmut_24, 
    'x__get_metadata_impl__mutmut_25': x__get_metadata_impl__mutmut_25, 
    'x__get_metadata_impl__mutmut_26': x__get_metadata_impl__mutmut_26, 
    'x__get_metadata_impl__mutmut_27': x__get_metadata_impl__mutmut_27, 
    'x__get_metadata_impl__mutmut_28': x__get_metadata_impl__mutmut_28, 
    'x__get_metadata_impl__mutmut_29': x__get_metadata_impl__mutmut_29, 
    'x__get_metadata_impl__mutmut_30': x__get_metadata_impl__mutmut_30, 
    'x__get_metadata_impl__mutmut_31': x__get_metadata_impl__mutmut_31, 
    'x__get_metadata_impl__mutmut_32': x__get_metadata_impl__mutmut_32, 
    'x__get_metadata_impl__mutmut_33': x__get_metadata_impl__mutmut_33, 
    'x__get_metadata_impl__mutmut_34': x__get_metadata_impl__mutmut_34, 
    'x__get_metadata_impl__mutmut_35': x__get_metadata_impl__mutmut_35, 
    'x__get_metadata_impl__mutmut_36': x__get_metadata_impl__mutmut_36, 
    'x__get_metadata_impl__mutmut_37': x__get_metadata_impl__mutmut_37, 
    'x__get_metadata_impl__mutmut_38': x__get_metadata_impl__mutmut_38, 
    'x__get_metadata_impl__mutmut_39': x__get_metadata_impl__mutmut_39, 
    'x__get_metadata_impl__mutmut_40': x__get_metadata_impl__mutmut_40, 
    'x__get_metadata_impl__mutmut_41': x__get_metadata_impl__mutmut_41, 
    'x__get_metadata_impl__mutmut_42': x__get_metadata_impl__mutmut_42, 
    'x__get_metadata_impl__mutmut_43': x__get_metadata_impl__mutmut_43, 
    'x__get_metadata_impl__mutmut_44': x__get_metadata_impl__mutmut_44, 
    'x__get_metadata_impl__mutmut_45': x__get_metadata_impl__mutmut_45, 
    'x__get_metadata_impl__mutmut_46': x__get_metadata_impl__mutmut_46, 
    'x__get_metadata_impl__mutmut_47': x__get_metadata_impl__mutmut_47, 
    'x__get_metadata_impl__mutmut_48': x__get_metadata_impl__mutmut_48, 
    'x__get_metadata_impl__mutmut_49': x__get_metadata_impl__mutmut_49, 
    'x__get_metadata_impl__mutmut_50': x__get_metadata_impl__mutmut_50, 
    'x__get_metadata_impl__mutmut_51': x__get_metadata_impl__mutmut_51, 
    'x__get_metadata_impl__mutmut_52': x__get_metadata_impl__mutmut_52, 
    'x__get_metadata_impl__mutmut_53': x__get_metadata_impl__mutmut_53, 
    'x__get_metadata_impl__mutmut_54': x__get_metadata_impl__mutmut_54, 
    'x__get_metadata_impl__mutmut_55': x__get_metadata_impl__mutmut_55, 
    'x__get_metadata_impl__mutmut_56': x__get_metadata_impl__mutmut_56, 
    'x__get_metadata_impl__mutmut_57': x__get_metadata_impl__mutmut_57, 
    'x__get_metadata_impl__mutmut_58': x__get_metadata_impl__mutmut_58, 
    'x__get_metadata_impl__mutmut_59': x__get_metadata_impl__mutmut_59, 
    'x__get_metadata_impl__mutmut_60': x__get_metadata_impl__mutmut_60, 
    'x__get_metadata_impl__mutmut_61': x__get_metadata_impl__mutmut_61, 
    'x__get_metadata_impl__mutmut_62': x__get_metadata_impl__mutmut_62, 
    'x__get_metadata_impl__mutmut_63': x__get_metadata_impl__mutmut_63, 
    'x__get_metadata_impl__mutmut_64': x__get_metadata_impl__mutmut_64, 
    'x__get_metadata_impl__mutmut_65': x__get_metadata_impl__mutmut_65, 
    'x__get_metadata_impl__mutmut_66': x__get_metadata_impl__mutmut_66, 
    'x__get_metadata_impl__mutmut_67': x__get_metadata_impl__mutmut_67, 
    'x__get_metadata_impl__mutmut_68': x__get_metadata_impl__mutmut_68, 
    'x__get_metadata_impl__mutmut_69': x__get_metadata_impl__mutmut_69, 
    'x__get_metadata_impl__mutmut_70': x__get_metadata_impl__mutmut_70
}

def _get_metadata_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__get_metadata_impl__mutmut_orig, x__get_metadata_impl__mutmut_mutants, args, kwargs)
    return result 

_get_metadata_impl.__signature__ = _mutmut_signature(x__get_metadata_impl__mutmut_orig)
x__get_metadata_impl__mutmut_orig.__name__ = 'x__get_metadata_impl'


# 🐍🏗⛮️
