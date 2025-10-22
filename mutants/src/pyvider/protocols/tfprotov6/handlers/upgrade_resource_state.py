#
# pyvider/protocols/tfprotov6/handlers/upgrade_resource_state.py
#

import json
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
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    DynamicValue,
)
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
async def UpgradeResourceStateHandler(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """
    Handle UpgradeResourceState requests. For now, this is a pass-through
    as we are not implementing schema versioning. It must return the state
    it was given, unmodified.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="UpgradeResourceState")

    try:
        return await _upgrade_resource_state_impl(request, context)
    except Exception:
        handler_errors.inc(handler="UpgradeResourceState")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="UpgradeResourceState")


async def x__upgrade_resource_state_impl__mutmut_orig(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_1(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug(None)
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_2(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("XXUpgradeResourceState calledXX")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_3(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("upgraderesourcestate called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_4(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UPGRADERESOURCESTATE CALLED")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_5(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(None)

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_6(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state or request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_7(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = None
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_8(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = None

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_9(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode(None)

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_10(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps(None).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_11(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("XXutf-8XX")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_12(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("UTF-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_13(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = None

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_14(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=None, diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_15(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=None
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_16(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_17(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_18(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=None), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_19(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(None)
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_20(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(None, exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_21(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=None)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_22(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_23(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", )
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_24(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=False)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_25(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=None
        )


async def x__upgrade_resource_state_impl__mutmut_26(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=None,
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_27(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary=None,
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_28(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=None,
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_29(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    summary="State upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_30(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_31(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_32(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="XXState upgrade failedXX",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_33(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="state upgrade failed",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_34(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="STATE UPGRADE FAILED",
                    detail=str(e),
                )
            ]
        )


async def x__upgrade_resource_state_impl__mutmut_35(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Implementation of UpgradeResourceState handler."""
    logger.debug("UpgradeResourceState called")
    try:
        logger.debug(f"Upgrade request: {request}")

        # FIX: The handler must return the exact state it received if no upgrade
        # logic is being performed. Stripping attributes causes inconsistencies.
        if request.raw_state and request.raw_state.json:
            upgraded_state_json = request.raw_state.json
        else:
            # If there's no state, return an empty object.
            upgraded_state_json = json.dumps({}).encode("utf-8")

        response = pb.UpgradeResourceState.Response(
            upgraded_state=DynamicValue(json=upgraded_state_json), diagnostics=[]
        )

        logger.debug(f"UpgradeResourceState response (pass-through): {response}")
        return response

    except Exception as e:
        logger.error(f"Error in UpgradeResourceState: {e!s}", exc_info=True)
        return pb.UpgradeResourceState.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="State upgrade failed",
                    detail=str(None),
                )
            ]
        )

x__upgrade_resource_state_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__upgrade_resource_state_impl__mutmut_1': x__upgrade_resource_state_impl__mutmut_1, 
    'x__upgrade_resource_state_impl__mutmut_2': x__upgrade_resource_state_impl__mutmut_2, 
    'x__upgrade_resource_state_impl__mutmut_3': x__upgrade_resource_state_impl__mutmut_3, 
    'x__upgrade_resource_state_impl__mutmut_4': x__upgrade_resource_state_impl__mutmut_4, 
    'x__upgrade_resource_state_impl__mutmut_5': x__upgrade_resource_state_impl__mutmut_5, 
    'x__upgrade_resource_state_impl__mutmut_6': x__upgrade_resource_state_impl__mutmut_6, 
    'x__upgrade_resource_state_impl__mutmut_7': x__upgrade_resource_state_impl__mutmut_7, 
    'x__upgrade_resource_state_impl__mutmut_8': x__upgrade_resource_state_impl__mutmut_8, 
    'x__upgrade_resource_state_impl__mutmut_9': x__upgrade_resource_state_impl__mutmut_9, 
    'x__upgrade_resource_state_impl__mutmut_10': x__upgrade_resource_state_impl__mutmut_10, 
    'x__upgrade_resource_state_impl__mutmut_11': x__upgrade_resource_state_impl__mutmut_11, 
    'x__upgrade_resource_state_impl__mutmut_12': x__upgrade_resource_state_impl__mutmut_12, 
    'x__upgrade_resource_state_impl__mutmut_13': x__upgrade_resource_state_impl__mutmut_13, 
    'x__upgrade_resource_state_impl__mutmut_14': x__upgrade_resource_state_impl__mutmut_14, 
    'x__upgrade_resource_state_impl__mutmut_15': x__upgrade_resource_state_impl__mutmut_15, 
    'x__upgrade_resource_state_impl__mutmut_16': x__upgrade_resource_state_impl__mutmut_16, 
    'x__upgrade_resource_state_impl__mutmut_17': x__upgrade_resource_state_impl__mutmut_17, 
    'x__upgrade_resource_state_impl__mutmut_18': x__upgrade_resource_state_impl__mutmut_18, 
    'x__upgrade_resource_state_impl__mutmut_19': x__upgrade_resource_state_impl__mutmut_19, 
    'x__upgrade_resource_state_impl__mutmut_20': x__upgrade_resource_state_impl__mutmut_20, 
    'x__upgrade_resource_state_impl__mutmut_21': x__upgrade_resource_state_impl__mutmut_21, 
    'x__upgrade_resource_state_impl__mutmut_22': x__upgrade_resource_state_impl__mutmut_22, 
    'x__upgrade_resource_state_impl__mutmut_23': x__upgrade_resource_state_impl__mutmut_23, 
    'x__upgrade_resource_state_impl__mutmut_24': x__upgrade_resource_state_impl__mutmut_24, 
    'x__upgrade_resource_state_impl__mutmut_25': x__upgrade_resource_state_impl__mutmut_25, 
    'x__upgrade_resource_state_impl__mutmut_26': x__upgrade_resource_state_impl__mutmut_26, 
    'x__upgrade_resource_state_impl__mutmut_27': x__upgrade_resource_state_impl__mutmut_27, 
    'x__upgrade_resource_state_impl__mutmut_28': x__upgrade_resource_state_impl__mutmut_28, 
    'x__upgrade_resource_state_impl__mutmut_29': x__upgrade_resource_state_impl__mutmut_29, 
    'x__upgrade_resource_state_impl__mutmut_30': x__upgrade_resource_state_impl__mutmut_30, 
    'x__upgrade_resource_state_impl__mutmut_31': x__upgrade_resource_state_impl__mutmut_31, 
    'x__upgrade_resource_state_impl__mutmut_32': x__upgrade_resource_state_impl__mutmut_32, 
    'x__upgrade_resource_state_impl__mutmut_33': x__upgrade_resource_state_impl__mutmut_33, 
    'x__upgrade_resource_state_impl__mutmut_34': x__upgrade_resource_state_impl__mutmut_34, 
    'x__upgrade_resource_state_impl__mutmut_35': x__upgrade_resource_state_impl__mutmut_35
}

def _upgrade_resource_state_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__upgrade_resource_state_impl__mutmut_orig, x__upgrade_resource_state_impl__mutmut_mutants, args, kwargs)
    return result 

_upgrade_resource_state_impl.__signature__ = _mutmut_signature(x__upgrade_resource_state_impl__mutmut_orig)
x__upgrade_resource_state_impl__mutmut_orig.__name__ = 'x__upgrade_resource_state_impl'
