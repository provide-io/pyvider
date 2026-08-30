#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger

from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._component_config import (
    config_to_attrs_instance,
    unmarshal_config,
)
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
)
from pyvider.schema.required import check_required_attributes


@rpc_handler("ValidateProviderConfig")
async def ValidateProviderConfigHandler(
    request: pb.ValidateProviderConfig.Request, context: Any
) -> pb.ValidateProviderConfig.Response:
    """Handle ValidateProviderConfig requests."""
    return await _validate_provider_config_impl(request, context)


def _log_declared_test_mode(provider_instance: Any, config_cty: Any) -> None:
    """Say whether the configuration asks for test mode. Logging only, never fatal.

    A configuration that cannot be parsed here is not a validation failure: the
    required-attribute and schema checks have already run, and this is only
    reporting what the practitioner asked for.
    """
    try:
        if config_cty.is_unknown:
            return
        config_instance = config_to_attrs_instance(config_cty, provider_instance.config_class)
        if not config_instance:
            return
        if getattr(config_instance, "pyvider_testmode", False):
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
            # Deliberately outside the `except Exception` below that tolerates
            # a config we can't parse: `.schema` raising means the provider
            # itself is broken, not that this particular config is
            # unparsable, and that must fail validation loudly rather than
            # be swallowed alongside a benign parse failure.
            provider_schema = provider_instance.schema
            config_cty = None
            try:
                config_cty = unmarshal_config(request.config, provider_schema.block)
            except Exception as e:
                # Don't fail validation if we can't parse config for logging
                logger.debug(
                    "Could not parse config for test mode check",
                    operation="validate_provider_config",
                    error=str(e),
                )

            if config_cty is not None:
                # cty 0.5 no longer refuses a present-but-null value for a
                # required attribute (see pyvider.schema.required), so the
                # schema layer's own check is called explicitly here.
                # Deliberately outside the swallow-all block above: a
                # genuinely missing required argument must fail validation,
                # not just skip the test-mode log line below. It raises
                # CtyAttributeValidationError, caught below by the
                # `(CtyValidationError, PyviderError)` clause -- the same
                # route validate_resource_config.py and
                # validate_data_resource_config.py use -- so the diagnostic
                # Terraform receives carries an attribute path, not just a
                # message string.
                check_required_attributes(provider_schema.block, config_cty.value)

                _log_declared_test_mode(provider_instance, config_cty)

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

    except (CtyValidationError, PyviderError) as e:
        # Same routing as validate_resource_config.py and
        # validate_data_resource_config.py: create_diagnostic_from_exception
        # knows how to turn a CtyAttributeValidationError's `.path` into a
        # populated `Diagnostic.attribute`, so Terraform can point the
        # practitioner at the offending argument instead of just printing a
        # message string.
        logger.error(
            "ValidateProviderConfig failed with framework error",
            operation="validate_provider_config",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        return pb.ValidateProviderConfig.Response(diagnostics=[diag])

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
