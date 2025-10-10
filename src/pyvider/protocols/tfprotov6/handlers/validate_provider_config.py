#
# pyvider/protocols/tfprotov6/handlers/validate_provider_config.py
#

from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
)


@resilient()
async def ValidateProviderConfigHandler(
    request: pb.ValidateProviderConfig.Request, context: Any
) -> pb.ValidateProviderConfig.Response:
    """Handle ValidateProviderConfig requests."""

    logger.debug("6️⃣️ 📋 ValidateProviderConfigHandler called")
    try:
        logger.trace(99, f"6️⃣️ ←️ 📋 ValidateProviderConfig request: {request}")
        response = pb.ValidateProviderConfig.Response(
            diagnostics=[]  # Empty diagnostics means validation passed
        )
        logger.trace(99, f"6️⃣️ →️ 📋 ValidateProviderConfig response: {response}")
        return response
    except Exception as e:
        logger.error(f"6️⃣️ ⛔️ 📋 Error in ValidateProviderConfig: {e!s}", exc_info=True)
        return pb.ValidateProviderConfig.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="Provider configuration validation failed",
                    detail=str(e),
                )
            ]
        )


# 🐍🏗⛮️
