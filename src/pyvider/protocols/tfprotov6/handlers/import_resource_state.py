#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
#

from typing import Any

from provide.foundation import logger

import pyvider.protocols.tfprotov6.protobuf as pb


async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


# 🐍🏗⛮️
