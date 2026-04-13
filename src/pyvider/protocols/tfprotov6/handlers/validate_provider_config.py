#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.conversion import unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
)
from pyvider.resources.base import BaseResource


@rpc_handler("ValidateProviderConfig")
async def ValidateProviderConfigHandler(
    request: pb.ValidateProviderConfig.Request, context: Any
) -> pb.ValidateProviderConfig.Response:
    """Handle ValidateProviderConfig requests."""
    return await _validate_provider_config_impl(request, context)


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

        # Get provider instance and parse config to check test mode
        provider_instance = hub.get_component("singleton", "provider")
        if provider_instance and request.config.msgpack:
            try:
                provider_schema = provider_instance.schema
                config_cty = unmarshal(request.config, schema=provider_schema.block)

                if not config_cty.is_unknown:
                    config_instance = BaseResource.from_cty(config_cty, provider_instance.config_class)  # type: ignore[arg-type]
                    if config_instance:
                        test_mode_enabled = getattr(config_instance, "pyvider_testmode", False)

                        if test_mode_enabled:
                            logger.warning(
                                "⚠️  Provider test mode ENABLED - test-only components will be accessible",
                                operation="validate_provider_config",
                            )
                        else:
                            logger.debug(
                                "Provider test mode NOT enabled - test-only components will be filtered out",
                                operation="validate_provider_config",
                            )
            except Exception as e:
                # Don't fail validation if we can't parse config for logging
                logger.debug(
                    "Could not parse config for test mode check",
                    operation="validate_provider_config",
                    error=str(e),
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


# 🐍🏗️🔚
