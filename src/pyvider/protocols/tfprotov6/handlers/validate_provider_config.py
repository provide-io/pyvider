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
    try:
        logger.debug(
            "ValidateProviderConfig handler called",
            operation="validate_provider_config",
            has_config=bool(request.config.msgpack),
        )
        # Provider configuration validation is typically minimal
        # Most validation happens in the provider's configure() method
        response = pb.ValidateProviderConfig.Response(
            diagnostics=[]  # Empty diagnostics means validation passed
        )

        logger.info(
            "Provider configuration validation passed",
            operation="validate_provider_config",
        )

        return response

    except Exception as e:
        logger.error(
            "ValidateProviderConfig failed with unexpected error",
            operation="validate_provider_config",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Provider configuration validation failed: {e}\n\n"
            f"Suggestion: Check that your provider configuration is valid and matches "
            f"the provider schema.\n\n"
            f"Troubleshooting:\n"
            f"  1. Review the provider documentation for required configuration fields\n"
            f"  2. Ensure all required fields are provided\n"
            f"  3. Check that field values are of the correct type\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {e}"
        )

        return pb.ValidateProviderConfig.Response(
            diagnostics=[
                Diagnostic(
                    severity=Diagnostic.ERROR,
                    summary="Provider configuration validation failed",
                    detail=error_detail,
                )
            ]
        )


# 🐍🏗⛮️
