#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any, cast

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.rpcplugin.server import RPCPluginServer


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


async def _stop_provider_impl(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler."""
    try:
        logger.info("StopProvider RPC received, initiating graceful shutdown", operation="stop_provider")

        server_factory = hub.get_component("singleton", "rpc_plugin_server")
        if server_factory:
            # Handle both factory functions and direct instances
            server_instance = cast(
                RPCPluginServer, server_factory() if callable(server_factory) else server_factory
            )
        else:
            server_instance = None

        if server_instance:
            logger.debug("Calling server stop for graceful shutdown", operation="stop_provider")
            # The stop() method is now responsible for the full shutdown sequence,
            # including resolving _serving_future.
            await server_instance.stop()
            logger.info("Provider server stop completed successfully", operation="stop_provider")
        else:
            logger.warning(
                "No active RPCPluginServer instance found during stop",
                operation="stop_provider",
            )

        # The plugin process should exit naturally after asyncio.run() in __main__.py completes,
        # which happens when server.serve() (and thus server.stop()) finishes.
        # No need for explicit sys.exit() here, as that can be too abrupt.

        logger.info("StopProvider handler completed successfully", operation="stop_provider")
        return pb.StopProvider.Response()

    except Exception as e:
        # Log any error during the StopProvider handling itself
        logger.error(
            "Unexpected error during provider stop",
            operation="stop_provider",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        # Return an error diagnostic if possible, though Terraform might just kill the plugin
        # if this handler itself fails badly or times out.
        # Since StopProvider.Response has no diagnostics field, we can only log.
        # Terraform will see the RPC error.
        raise  # Re-raise to ensure gRPC layer handles it as an RPC failure


# 🐍🏗️🔚
