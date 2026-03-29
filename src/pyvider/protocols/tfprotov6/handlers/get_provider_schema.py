#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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


async def _collect_schemas(
    component_type: str,
    diagnostics: list[pb.Diagnostic],
    converter: Any = None,
) -> dict[str, Any]:
    """Collect and convert schemas for any component type.

    Args:
        component_type: Type of component ('resource', 'data_source', 'function')
        diagnostics: List to append diagnostic messages to
        converter: Optional async converter function for functions

    Returns:
        Dictionary of converted schemas keyed by component name

    """
    schemas = {}
    all_components = get_all_components(component_type)

    for name, component in all_components.items():
        try:
            if component_type == "function":
                # Functions use a different conversion path
                func_dict = function_to_dict(component)
                if func_dict:
                    proto_func = dict_to_proto_function(func_dict)
                    if proto_func:
                        schemas[name] = proto_func
            else:
                # Resources and data sources use schema conversion
                schema_obj = component.get_schema()
                schemas[name] = await pvs_schema_to_proto(schema_obj)  # type: ignore[assignment]
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for {component_type} '{name}'",
                    detail=str(e),
                )
            )

    return schemas


async def _collect_resource_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    return await _collect_schemas("resource", diagnostics)


async def _collect_data_source_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    return await _collect_schemas("data_source", diagnostics)


async def _collect_function_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    return await _collect_schemas("function", diagnostics)


async def _compute_schema_once() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug(
        "Computing provider schema for the first time",
        operation="compute_schema",
    )

    diagnostics: list[Any] = []
    try:
        # Wait for component discovery to complete before collecting schemas
        # Discovery runs in the background and signals via an event when done
        discovery_ready_event = hub.get_component("singleton", "_discovery_ready_event")
        if discovery_ready_event is not None:
            logger.debug(
                "Waiting for component discovery to complete",
                operation="compute_schema",
            )
            try:
                # 55 seconds: Terraform kills unresponsive plugins at 60 seconds.
                await asyncio.wait_for(discovery_ready_event.wait(), timeout=55.0)
                logger.debug(
                    "Component discovery completed, proceeding with schema computation",
                    operation="compute_schema",
                )
            except TimeoutError:
                logger.warning(
                    "Component discovery timeout, proceeding with partial schema",
                    operation="compute_schema",
                )
        else:
            logger.debug(
                "Discovery event not found in hub, assuming discovery already complete",
                operation="compute_schema",
            )

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
