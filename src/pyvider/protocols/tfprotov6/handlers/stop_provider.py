#
# pyvider/protocols/tfprotov6/handlers/stop_provider.py
#
# pyvider/protocols/tfprotov6/handlers/stop_provider.py
#
# pyvider/protocols/tfprotov6/handlers/stop_provider.py
#

from typing import Any

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.rpcplugin.server import RPCPluginServer
from pyvider.telemetry import logger


async def StopProviderHandler(
    request: pb.StopProvider.Request, context: Any
) -> pb.StopProvider.Response:
    """
    Handles the StopProvider RPC call from Terraform Core.
    This is the primary mechanism for Terraform to request a graceful plugin exit.
    """
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
        logger.info(
            "🛎️🔒✅ StopProvider handler finished. Returning response to Terraform."
        )
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


# 🐍🏗⛮️


# 🐍🏗️📄🪄
