#
# pyvider/src/pyvider/protocols/tfprotov6/handlers/stop_provider.py
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
from pyvider.rpcplugin.server import RPCPluginServer
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
async def StopProviderHandler(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """
    Handles the StopProvider RPC call from Terraform Core.
    This is the primary mechanism for Terraform to request a graceful plugin exit.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="StopProvider")

    try:
        return await _stop_provider_impl(request, context)
    except Exception:
        handler_errors.inc(handler="StopProvider")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="StopProvider")


async def x__stop_provider_impl__mutmut_orig(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_1(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info(None)

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_2(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("XX🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...XX")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_3(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ stopprovider rpc received. initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_4(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ STOPPROVIDER RPC RECEIVED. INITIATING PROVIDER SHUTDOWN...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_5(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = None

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_6(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug(None)
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_7(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("XX🛎️🔧 Calling server_instance.stop() for graceful shutdown...XX")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_8(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_9(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 CALLING SERVER_INSTANCE.STOP() FOR GRACEFUL SHUTDOWN...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_10(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info(None)
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_11(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("XX🛎️🔧✅ Provider server_instance.stop() completed.XX")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_12(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_13(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ PROVIDER SERVER_INSTANCE.STOP() COMPLETED.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_14(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                None
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_15(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "XX🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly.XX"
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_16(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ no active rpcpluginserver instance found during stopprovider. plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_17(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ NO ACTIVE RPCPLUGINSERVER INSTANCE FOUND DURING STOPPROVIDER. PLUGIN MIGHT NOT HAVE STARTED CORRECTLY."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_18(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info(None)
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_19(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("XX🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.XX")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_20(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ stopprovider handler finished. returning response to terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_21(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ STOPPROVIDER HANDLER FINISHED. RETURNING RESPONSE TO TERRAFORM.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_22(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = None
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_23(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(None, exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_24(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=None)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_25(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(exc_info=True)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_26(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", )
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


async def x__stop_provider_impl__mutmut_27(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("🛎️🔒✅ StopProvider RPC received. Initiating provider shutdown...")

        server_instance = RPCPluginServer.get_instance()

        if server_instance:
            logger.debug("🛎️🔧 Calling server_instance.stop() for graceful shutdown...")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("🛎️🔧✅ Provider server_instance.stop() completed.")
        else:
            logger.warning(
                "🛎️⚠️ No active RPCPluginServer instance found during StopProvider. Plugin might not have started correctly."
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        # Terraform doesn't typically expect a message on stderr for successful StopProvider,
        # but logging is good.
        logger.info("🛎️🔒✅ StopProvider handler finished. Returning response to Terraform.")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        error_msg = f"Unexpected error during StopProvider handling: {e}"
        logger.error(f"🛎️❗❌ {error_msg}", exc_info=False)
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure

x__stop_provider_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__stop_provider_impl__mutmut_1': x__stop_provider_impl__mutmut_1, 
    'x__stop_provider_impl__mutmut_2': x__stop_provider_impl__mutmut_2, 
    'x__stop_provider_impl__mutmut_3': x__stop_provider_impl__mutmut_3, 
    'x__stop_provider_impl__mutmut_4': x__stop_provider_impl__mutmut_4, 
    'x__stop_provider_impl__mutmut_5': x__stop_provider_impl__mutmut_5, 
    'x__stop_provider_impl__mutmut_6': x__stop_provider_impl__mutmut_6, 
    'x__stop_provider_impl__mutmut_7': x__stop_provider_impl__mutmut_7, 
    'x__stop_provider_impl__mutmut_8': x__stop_provider_impl__mutmut_8, 
    'x__stop_provider_impl__mutmut_9': x__stop_provider_impl__mutmut_9, 
    'x__stop_provider_impl__mutmut_10': x__stop_provider_impl__mutmut_10, 
    'x__stop_provider_impl__mutmut_11': x__stop_provider_impl__mutmut_11, 
    'x__stop_provider_impl__mutmut_12': x__stop_provider_impl__mutmut_12, 
    'x__stop_provider_impl__mutmut_13': x__stop_provider_impl__mutmut_13, 
    'x__stop_provider_impl__mutmut_14': x__stop_provider_impl__mutmut_14, 
    'x__stop_provider_impl__mutmut_15': x__stop_provider_impl__mutmut_15, 
    'x__stop_provider_impl__mutmut_16': x__stop_provider_impl__mutmut_16, 
    'x__stop_provider_impl__mutmut_17': x__stop_provider_impl__mutmut_17, 
    'x__stop_provider_impl__mutmut_18': x__stop_provider_impl__mutmut_18, 
    'x__stop_provider_impl__mutmut_19': x__stop_provider_impl__mutmut_19, 
    'x__stop_provider_impl__mutmut_20': x__stop_provider_impl__mutmut_20, 
    'x__stop_provider_impl__mutmut_21': x__stop_provider_impl__mutmut_21, 
    'x__stop_provider_impl__mutmut_22': x__stop_provider_impl__mutmut_22, 
    'x__stop_provider_impl__mutmut_23': x__stop_provider_impl__mutmut_23, 
    'x__stop_provider_impl__mutmut_24': x__stop_provider_impl__mutmut_24, 
    'x__stop_provider_impl__mutmut_25': x__stop_provider_impl__mutmut_25, 
    'x__stop_provider_impl__mutmut_26': x__stop_provider_impl__mutmut_26, 
    'x__stop_provider_impl__mutmut_27': x__stop_provider_impl__mutmut_27
}

def _stop_provider_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__stop_provider_impl__mutmut_orig, x__stop_provider_impl__mutmut_mutants, args, kwargs)
    return result 

_stop_provider_impl.__signature__ = _mutmut_signature(x__stop_provider_impl__mutmut_orig)
x__stop_provider_impl__mutmut_orig.__name__ = 'x__stop_provider_impl'


# 🐍🏗⛮️
