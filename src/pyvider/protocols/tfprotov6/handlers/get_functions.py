"""
GetFunctions handler implementation for Terraform protocol v6.
This handler uses a multi-layer approach to convert domain function objects
to protocol-specific messages, maintaining clean separation of concerns.
It also caches the result to avoid redundant work on repeated calls.
"""

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.functions.adapters import function_to_dict
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.adapters.function_adapter import dict_to_proto_function
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    Function,
    GetFunctions,
)

# Module-level cache for the function definitions.
_cached_functions: dict[str, Function] | None = None
_cache_lock = None  # Will be initialized as an asyncio.Lock


async def _get_functions_once() -> dict[str, Function]:
    """
    Computes the function dictionary only once and caches it.
    This is the core fix to prevent log spam.
    """
    global _cached_functions, _cache_lock
    if _cache_lock is None:
        import asyncio

        _cache_lock = asyncio.Lock()

    async with _cache_lock:
        if _cached_functions is not None:
            logger.debug("🧰🔍✅ Returning cached function definitions.")
            return _cached_functions

        logger.debug("🧰🔍🔄 Computing and caching function definitions for the first time...")

        from pyvider.hub import hub

        functions: dict[str, Function] = {}
        registered_funcs = hub.get_components("function")

        for name, func_obj in registered_funcs.items():
            try:
                func_dict = function_to_dict(func_obj)
                if func_dict:
                    proto_func = dict_to_proto_function(func_dict)
                    if proto_func:
                        functions[name] = proto_func
            except Exception as e:
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


@resilient()
async def GetFunctionsHandler(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """
    Handle GetFunctions requests by returning all registered functions.
    This now uses a cached result to improve performance and reduce log noise.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="GetFunctions")

    try:
        return await _get_functions_impl(request, context)
    except Exception:
        handler_errors.inc(handler="GetFunctions")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="GetFunctions")


async def _get_functions_impl(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=True)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )
