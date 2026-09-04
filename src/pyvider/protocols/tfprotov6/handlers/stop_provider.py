#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.common.stop_signal import request_stop
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("StopProvider")
async def StopProviderHandler(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """
    Handles the StopProvider RPC call from Terraform Core.
    Asks in-flight work to wind up; it does not stop the server.
    """
    return await _stop_provider_impl(request, context)


async def _stop_provider_impl(request: pb.StopProvider.Request, context: Any) -> pb.StopProvider.Response:
    """Implementation of StopProvider handler.

    Terraform's Stop is advisory. It asks the provider to halt what it is doing
    and expects an immediate answer; the calls already in flight are still
    expected to return on their own, and Terraform waits for them
    (terraform/internal/providers/provider.go:63-73,
    internal/terraform/context.go:340-386). Stopping the process is a separate
    step, driven by `Close()` and go-plugin's `Kill()`, which reaches this
    plugin as GRPCController.Shutdown
    (terraform/internal/plugin6/grpc_provider.go:1885-1904).

    This used to schedule `RPCPluginServer.stop()` shortly after replying, which
    tears down the gRPC server with a short grace period, unlinks the socket and
    exits the process. Any `ApplyResourceChange` still running was cut off, so an
    interrupted apply failed with UNAVAILABLE and a resource created remotely
    never reached state -- and Terraform's own teardown then found a dead socket
    and reported "plugin failed to exit gracefully". terraform-plugin-go
    implements Stop by cancelling contexts and carries on serving
    (tfprotov6/tf6server/server.go:412-454), which is what this now matches.

    StopProvider.Response carries an `Error` string, the protocol's channel for
    reporting a stop that could not be started, so a failure is returned there
    rather than raised: raising would reach Terraform as a transport error,
    indistinguishable from the plugin having crashed.
    """
    logger.info("StopProvider RPC received, signalling in-flight work to stop", operation="stop_provider")

    request_stop()

    logger.info("StopProvider handler completed successfully", operation="stop_provider")
    return pb.StopProvider.Response()


# 🐍🏗️🔚
