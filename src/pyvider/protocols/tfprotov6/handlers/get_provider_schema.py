#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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
from pyvider.protocols.tfprotov6.handlers.utils import get_all_components
import pyvider.protocols.tfprotov6.protobuf as pb

# --- Module-level Cache using asyncio.Future ---
_schema_future: asyncio.Future[pb.GetProviderSchema.Response] | None = None
_task: asyncio.Task | None = None  # Store a reference to the task
_cache_lock = asyncio.Lock()  # Lock to protect the creation of the Future itself


async def _collect_resource_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    all_resources = get_all_components("resource")
    for name, resource_class in all_resources.items():
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
    all_data_sources = get_all_components("data_source")
    for name, ds_class in all_data_sources.items():
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
    all_functions = get_all_components("function")
    for name, func_obj in all_functions.items():
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
    logger.debug(
        "Computing provider schema for the first time",
        operation="compute_schema",
    )

    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            logger.error(
                "Provider instance not found during schema computation",
                operation="compute_schema",
            )
            raise RuntimeError(
                "Provider instance not found in hub.\n\n"
                "This indicates the provider's setup() method may have failed or "
                "the provider was not properly registered.\n\n"
                "Troubleshooting:\n"
                "  1. Ensure the provider class has the @provider decorator\n"
                "  2. Verify the provider's setup() method completed successfully\n"
                "  3. Check provider logs for initialization errors\n"
                "  4. Verify component discovery completed without errors"
            )

        logger.debug(
            "Converting provider schema to protocol buffer format",
            operation="compute_schema",
            provider_name=provider_instance.metadata.name,
        )

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        logger.debug(
            "Collecting component schemas",
            operation="compute_schema",
        )

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

        logger.info(
            "Provider schema computed and cached successfully",
            operation="compute_schema",
            provider_name=provider_instance.metadata.name,
            resource_count=len(resource_schemas),
            data_source_count=len(data_source_schemas),
            function_count=len(functions),
            warning_count=len([d for d in diagnostics if d.severity == pb.Diagnostic.WARNING]),
        )

        return response

    except Exception as e:
        logger.error(
            "Failed to compute provider schema",
            operation="compute_schema",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Failed to compute provider schema: {e}\n\n"
            f"Suggestion: This usually indicates an issue with provider initialization "
            f"or schema definition.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that all resources/data sources have valid schema definitions\n"
            f"  2. Verify component discovery completed successfully\n"
            f"  3. Review provider logs for initialization errors\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {e}"
        )

        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Provider schema computation failed",
                    detail=error_detail,
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
    logger.debug(
        "GetProviderSchema handler called",
        operation="get_provider_schema",
        cache_exists=_schema_future is not None,
    )

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


# 🐍🏗️🔚
