#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
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
async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Handle import resource state request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ImportResourceState")

    try:
        return await _import_resource_state_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ImportResourceState")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ImportResourceState")


async def x__import_resource_state_impl__mutmut_orig(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


async def x__import_resource_state_impl__mutmut_1(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning(None)
    return pb.ImportResourceState.Response(diagnostics=[])


async def x__import_resource_state_impl__mutmut_2(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("XX👋🫴🤝 Unimplemented: ImportResourceState was called.XX")
    return pb.ImportResourceState.Response(diagnostics=[])


async def x__import_resource_state_impl__mutmut_3(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("👋🫴🤝 unimplemented: importresourcestate was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


async def x__import_resource_state_impl__mutmut_4(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("👋🫴🤝 UNIMPLEMENTED: IMPORTRESOURCESTATE WAS CALLED.")
    return pb.ImportResourceState.Response(diagnostics=[])


async def x__import_resource_state_impl__mutmut_5(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Implementation of ImportResourceState handler."""
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=None)

x__import_resource_state_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__import_resource_state_impl__mutmut_1': x__import_resource_state_impl__mutmut_1, 
    'x__import_resource_state_impl__mutmut_2': x__import_resource_state_impl__mutmut_2, 
    'x__import_resource_state_impl__mutmut_3': x__import_resource_state_impl__mutmut_3, 
    'x__import_resource_state_impl__mutmut_4': x__import_resource_state_impl__mutmut_4, 
    'x__import_resource_state_impl__mutmut_5': x__import_resource_state_impl__mutmut_5
}

def _import_resource_state_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__import_resource_state_impl__mutmut_orig, x__import_resource_state_impl__mutmut_mutants, args, kwargs)
    return result 

_import_resource_state_impl.__signature__ = _mutmut_signature(x__import_resource_state_impl__mutmut_orig)
x__import_resource_state_impl__mutmut_orig.__name__ = 'x__import_resource_state_impl'


# 🐍🏗⛮️
