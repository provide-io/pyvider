#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
#
# pyvider/protocols/tfprotov6/handlers/import_resource_state.py
#

from typing import Any

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.telemetry import logger


async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    logger.warning("👋🫴🤝 Unimplemented: ImportResourceState was called.")
    return pb.ImportResourceState.Response(diagnostics=[])


# 🐍🏗⛮️


# 🐍🏗️📄🪄
