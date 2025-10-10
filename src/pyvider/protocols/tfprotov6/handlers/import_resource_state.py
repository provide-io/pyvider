#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
#

from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


# 🐍🏗⛮️
