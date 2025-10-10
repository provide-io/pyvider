#
# pyvider/protocols/tfprotov6/handlers/move_resource_state.py
#

from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def MoveResourceStateHandler(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    logger.warning("👋🫴🤝 Unimplemented: MoveResourceState was called.")
    return pb.MoveResourceState.Response(diagnostics=[])


# 🐍🏗⛮️
