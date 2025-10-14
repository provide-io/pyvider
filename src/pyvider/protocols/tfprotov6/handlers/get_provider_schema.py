import asyncio
import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import pvs_schema_to_proto
from pyvider.functions.adapters import function_to_dict
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.adapters.function_adapter import (
    dict_to_proto_function,
)
import pyvider.protocols.tfprotov6.protobuf as pb

# --- Module-level Cache using asyncio.Future ---
_schema_future: asyncio.Future[pb.GetProviderSchema.Response] | None = None
_task: asyncio.Task | None = None  # Store a reference to the task
_cache_lock = asyncio.Lock()  # Lock to protect the creation of the Future itself


async def _collect_resource_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def _collect_data_source_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def _collect_function_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def _compute_schema_once() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


@resilient()
async def GetProviderSchemaHandler(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """
    Handles the GetProviderSchema RPC request using a robust, race-condition-free
    asyncio.Future to ensure the schema is computed only once.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="GetProviderSchema")

    try:
        return await _get_provider_schema_impl(request, context)
    except Exception:
        handler_errors.inc(handler="GetProviderSchema")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="GetProviderSchema")


async def _get_provider_schema_impl(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def _set_future_result(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(e)
