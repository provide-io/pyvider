#
# pyvider/protocols/tfprotov6/handlers/validate_provider_config.py
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
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
)


@resilient()
async def ValidateProviderConfigHandler(
    request: pb.ValidateProviderConfig.Request, context: Any
) -> pb.ValidateProviderConfig.Response:
    """Handle ValidateProviderConfig requests."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ValidateProviderConfig")

    try:
        return await _validate_provider_config_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ValidateProviderConfig")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ValidateProviderConfig")


async def _validate_provider_config_impl(
    request: pb.ValidateProviderConfig.Request, context: Any
) -> pb.ValidateProviderConfig.Response:
    """Implementation of ValidateProviderConfig handler."""
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
