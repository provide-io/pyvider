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


async def x__get_functions_once__mutmut_orig() -> dict[str, Function]:
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


async def x__get_functions_once__mutmut_1() -> dict[str, Function]:
    """
    Computes the function dictionary only once and caches it.
    This is the core fix to prevent log spam.
    """
    global _cached_functions, _cache_lock
    if _cache_lock is not None:
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


async def x__get_functions_once__mutmut_2() -> dict[str, Function]:
    """
    Computes the function dictionary only once and caches it.
    This is the core fix to prevent log spam.
    """
    global _cached_functions, _cache_lock
    if _cache_lock is None:
        import asyncio

        _cache_lock = None

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


async def x__get_functions_once__mutmut_3() -> dict[str, Function]:
    """
    Computes the function dictionary only once and caches it.
    This is the core fix to prevent log spam.
    """
    global _cached_functions, _cache_lock
    if _cache_lock is None:
        import asyncio

        _cache_lock = asyncio.Lock()

    async with _cache_lock:
        if _cached_functions is None:
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


async def x__get_functions_once__mutmut_4() -> dict[str, Function]:
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
            logger.debug(None)
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


async def x__get_functions_once__mutmut_5() -> dict[str, Function]:
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
            logger.debug("XX🧰🔍✅ Returning cached function definitions.XX")
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


async def x__get_functions_once__mutmut_6() -> dict[str, Function]:
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
            logger.debug("🧰🔍✅ returning cached function definitions.")
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


async def x__get_functions_once__mutmut_7() -> dict[str, Function]:
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
            logger.debug("🧰🔍✅ RETURNING CACHED FUNCTION DEFINITIONS.")
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


async def x__get_functions_once__mutmut_8() -> dict[str, Function]:
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

        logger.debug(None)

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


async def x__get_functions_once__mutmut_9() -> dict[str, Function]:
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

        logger.debug("XX🧰🔍🔄 Computing and caching function definitions for the first time...XX")

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


async def x__get_functions_once__mutmut_10() -> dict[str, Function]:
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

        logger.debug("🧰🔍🔄 computing and caching function definitions for the first time...")

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


async def x__get_functions_once__mutmut_11() -> dict[str, Function]:
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

        logger.debug("🧰🔍🔄 COMPUTING AND CACHING FUNCTION DEFINITIONS FOR THE FIRST TIME...")

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


async def x__get_functions_once__mutmut_12() -> dict[str, Function]:
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

        functions: dict[str, Function] = None
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


async def x__get_functions_once__mutmut_13() -> dict[str, Function]:
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
        registered_funcs = None

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


async def x__get_functions_once__mutmut_14() -> dict[str, Function]:
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
        registered_funcs = hub.get_components(None)

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


async def x__get_functions_once__mutmut_15() -> dict[str, Function]:
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
        registered_funcs = hub.get_components("XXfunctionXX")

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


async def x__get_functions_once__mutmut_16() -> dict[str, Function]:
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
        registered_funcs = hub.get_components("FUNCTION")

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


async def x__get_functions_once__mutmut_17() -> dict[str, Function]:
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
                func_dict = None
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


async def x__get_functions_once__mutmut_18() -> dict[str, Function]:
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
                func_dict = function_to_dict(None)
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


async def x__get_functions_once__mutmut_19() -> dict[str, Function]:
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
                    proto_func = None
                    if proto_func:
                        functions[name] = proto_func
            except Exception as e:
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_20() -> dict[str, Function]:
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
                    proto_func = dict_to_proto_function(None)
                    if proto_func:
                        functions[name] = proto_func
            except Exception as e:
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_21() -> dict[str, Function]:
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
                        functions[name] = None
            except Exception as e:
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_22() -> dict[str, Function]:
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
                logger.error(None, exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_23() -> dict[str, Function]:
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
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=None)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_24() -> dict[str, Function]:
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
                logger.error(exc_info=True)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_25() -> dict[str, Function]:
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
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", )
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_26() -> dict[str, Function]:
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
                logger.error(f"🧰🔍❌ Failed to process function '{name}': {e}", exc_info=False)
                # Optionally add a diagnostic here if you want to report this to Terraform

        _cached_functions = functions
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_27() -> dict[str, Function]:
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

        _cached_functions = None
        logger.info(f"🧰🔍✅ Cached {len(_cached_functions)} function definitions.")
        return _cached_functions


async def x__get_functions_once__mutmut_28() -> dict[str, Function]:
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
        logger.info(None)
        return _cached_functions

x__get_functions_once__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_functions_once__mutmut_1': x__get_functions_once__mutmut_1, 
    'x__get_functions_once__mutmut_2': x__get_functions_once__mutmut_2, 
    'x__get_functions_once__mutmut_3': x__get_functions_once__mutmut_3, 
    'x__get_functions_once__mutmut_4': x__get_functions_once__mutmut_4, 
    'x__get_functions_once__mutmut_5': x__get_functions_once__mutmut_5, 
    'x__get_functions_once__mutmut_6': x__get_functions_once__mutmut_6, 
    'x__get_functions_once__mutmut_7': x__get_functions_once__mutmut_7, 
    'x__get_functions_once__mutmut_8': x__get_functions_once__mutmut_8, 
    'x__get_functions_once__mutmut_9': x__get_functions_once__mutmut_9, 
    'x__get_functions_once__mutmut_10': x__get_functions_once__mutmut_10, 
    'x__get_functions_once__mutmut_11': x__get_functions_once__mutmut_11, 
    'x__get_functions_once__mutmut_12': x__get_functions_once__mutmut_12, 
    'x__get_functions_once__mutmut_13': x__get_functions_once__mutmut_13, 
    'x__get_functions_once__mutmut_14': x__get_functions_once__mutmut_14, 
    'x__get_functions_once__mutmut_15': x__get_functions_once__mutmut_15, 
    'x__get_functions_once__mutmut_16': x__get_functions_once__mutmut_16, 
    'x__get_functions_once__mutmut_17': x__get_functions_once__mutmut_17, 
    'x__get_functions_once__mutmut_18': x__get_functions_once__mutmut_18, 
    'x__get_functions_once__mutmut_19': x__get_functions_once__mutmut_19, 
    'x__get_functions_once__mutmut_20': x__get_functions_once__mutmut_20, 
    'x__get_functions_once__mutmut_21': x__get_functions_once__mutmut_21, 
    'x__get_functions_once__mutmut_22': x__get_functions_once__mutmut_22, 
    'x__get_functions_once__mutmut_23': x__get_functions_once__mutmut_23, 
    'x__get_functions_once__mutmut_24': x__get_functions_once__mutmut_24, 
    'x__get_functions_once__mutmut_25': x__get_functions_once__mutmut_25, 
    'x__get_functions_once__mutmut_26': x__get_functions_once__mutmut_26, 
    'x__get_functions_once__mutmut_27': x__get_functions_once__mutmut_27, 
    'x__get_functions_once__mutmut_28': x__get_functions_once__mutmut_28
}

def _get_functions_once(*args, **kwargs):
    result = _mutmut_trampoline(x__get_functions_once__mutmut_orig, x__get_functions_once__mutmut_mutants, args, kwargs)
    return result 

_get_functions_once.__signature__ = _mutmut_signature(x__get_functions_once__mutmut_orig)
x__get_functions_once__mutmut_orig.__name__ = 'x__get_functions_once'


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


async def x__get_functions_impl__mutmut_orig(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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


async def x__get_functions_impl__mutmut_1(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = None
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


async def x__get_functions_impl__mutmut_2(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=None, diagnostics=[])
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


async def x__get_functions_impl__mutmut_3(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=None)
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


async def x__get_functions_impl__mutmut_4(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(diagnostics=[])
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


async def x__get_functions_impl__mutmut_5(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, )
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


async def x__get_functions_impl__mutmut_6(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(None, exc_info=True)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_7(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=None)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_8(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(exc_info=True)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_9(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", )
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_10(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=False)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_11(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=True)
        return GetFunctions.Response(
            diagnostics=None
        )


async def x__get_functions_impl__mutmut_12(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=True)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    severity=None,
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_13(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    summary=None,
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_14(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    detail=None,
                )
            ]
        )


async def x__get_functions_impl__mutmut_15(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
    """Implementation of GetFunctions handler."""
    try:
        functions = await _get_functions_once()
        return GetFunctions.Response(functions=functions, diagnostics=[])
    except Exception as e:
        logger.error(f"🧰🔍💥 Unhandled error in GetFunctions: {e}", exc_info=True)
        return GetFunctions.Response(
            diagnostics=[
                Diagnostic(
                    summary="GetFunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_16(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_17(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    )
            ]
        )


async def x__get_functions_impl__mutmut_18(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    summary="XXGetFunctions errorXX",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_19(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    summary="getfunctions error",
                    detail=f"Internal error: {e}",
                )
            ]
        )


async def x__get_functions_impl__mutmut_20(request: pb.GetFunctions.Request, context: Any) -> pb.GetFunctions.Response:
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
                    summary="GETFUNCTIONS ERROR",
                    detail=f"Internal error: {e}",
                )
            ]
        )

x__get_functions_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_functions_impl__mutmut_1': x__get_functions_impl__mutmut_1, 
    'x__get_functions_impl__mutmut_2': x__get_functions_impl__mutmut_2, 
    'x__get_functions_impl__mutmut_3': x__get_functions_impl__mutmut_3, 
    'x__get_functions_impl__mutmut_4': x__get_functions_impl__mutmut_4, 
    'x__get_functions_impl__mutmut_5': x__get_functions_impl__mutmut_5, 
    'x__get_functions_impl__mutmut_6': x__get_functions_impl__mutmut_6, 
    'x__get_functions_impl__mutmut_7': x__get_functions_impl__mutmut_7, 
    'x__get_functions_impl__mutmut_8': x__get_functions_impl__mutmut_8, 
    'x__get_functions_impl__mutmut_9': x__get_functions_impl__mutmut_9, 
    'x__get_functions_impl__mutmut_10': x__get_functions_impl__mutmut_10, 
    'x__get_functions_impl__mutmut_11': x__get_functions_impl__mutmut_11, 
    'x__get_functions_impl__mutmut_12': x__get_functions_impl__mutmut_12, 
    'x__get_functions_impl__mutmut_13': x__get_functions_impl__mutmut_13, 
    'x__get_functions_impl__mutmut_14': x__get_functions_impl__mutmut_14, 
    'x__get_functions_impl__mutmut_15': x__get_functions_impl__mutmut_15, 
    'x__get_functions_impl__mutmut_16': x__get_functions_impl__mutmut_16, 
    'x__get_functions_impl__mutmut_17': x__get_functions_impl__mutmut_17, 
    'x__get_functions_impl__mutmut_18': x__get_functions_impl__mutmut_18, 
    'x__get_functions_impl__mutmut_19': x__get_functions_impl__mutmut_19, 
    'x__get_functions_impl__mutmut_20': x__get_functions_impl__mutmut_20
}

def _get_functions_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__get_functions_impl__mutmut_orig, x__get_functions_impl__mutmut_mutants, args, kwargs)
    return result 

_get_functions_impl.__signature__ = _mutmut_signature(x__get_functions_impl__mutmut_orig)
x__get_functions_impl__mutmut_orig.__name__ = 'x__get_functions_impl'
