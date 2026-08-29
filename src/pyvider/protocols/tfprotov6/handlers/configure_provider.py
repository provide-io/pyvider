#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation import logger
from provide.foundation.config import get_env, parse_bool_extended

from pyvider.exceptions import (
    ProviderAlreadyConfiguredError,
    ProviderConfigurationError,
    PyviderError,
)
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._component_config import (
    config_to_attrs_instance,
    unmarshal_config,
)
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.context import ProviderContext


@rpc_handler("ConfigureProvider")
async def ConfigureProviderHandler(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """
    Handles the ConfigureProvider RPC request.

    This handler validates the provider configuration sent by Terraform
    and initializes the provider context, making it available for all
    subsequent component operations.
    """
    return await _configure_provider_impl(request, context)


def _resolve_test_mode(config_instance: Any) -> tuple[bool, str]:
    """Resolve pyvider_testmode: env var beats HCL config beats default."""
    env_testmode_str = get_env("PYVIDER_TESTMODE", default=None)
    env_testmode = parse_bool_extended(env_testmode_str) if env_testmode_str else None
    config_testmode = getattr(config_instance, "pyvider_testmode", None)

    if env_testmode is not None:
        return env_testmode, "PYVIDER_TESTMODE environment variable"
    if config_testmode is not None:
        return config_testmode, "provider configuration (HCL)"
    return False, "default"


async def _configure_provider_impl(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """Implementation of ConfigureProvider handler."""
    response = pb.ConfigureProvider.Response()

    logger.debug(
        "ConfigureProvider handler called",
        operation="configure_provider",
        has_config=bool(request.config.msgpack),
        terraform_version=request.terraform_version if hasattr(request, "terraform_version") else "unknown",
    )

    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            logger.error(
                "Provider instance not found in hub during configuration",
                operation="configure_provider",
            )

            err = ProviderConfigurationError(
                "Provider instance not found in hub.\n\n"
                "This is an internal framework error. The provider should be registered "
                "during server initialization before ConfigureProvider is called.\n\n"
                "Suggestion: Report this issue - it indicates a provider initialization problem.\n\n"
                "Troubleshooting:\n"
                "  1. Ensure the provider class has the @provider decorator\n"
                "  2. Verify the provider's setup() method completed successfully\n"
                "  3. Check provider logs for initialization errors\n"
                "  4. Verify component discovery completed without errors"
            )
            err.add_context("hub.dimension", "singleton")
            err.add_context("hub.component_type", "provider")
            err.add_context("terraform.summary", "Provider not registered")
            err.add_context(
                "terraform.detail", "The provider has not been properly registered with the framework."
            )
            raise err

        logger.debug(
            "Provider instance retrieved for configuration",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
            provider_version=provider_instance.metadata.version,
        )

        provider_schema = provider_instance.schema
        config_cty = unmarshal_config(request.config, provider_schema.block)

        if config_cty.is_unknown:
            logger.warning(
                "Provider configuration contains unknown values, deferring configuration",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )
            return response

        logger.debug(
            "Parsing provider configuration",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
        )

        config_instance = config_to_attrs_instance(config_cty, provider_instance.config_class)

        if config_instance is None:
            logger.error(
                "Failed to parse provider configuration into attrs instance",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )

            err = ProviderConfigurationError(
                f"Failed to instantiate provider configuration for '{provider_instance.metadata.name}'.\n\n"
                f"Suggestion: Ensure all required provider configuration fields are provided with valid types.\n\n"
                f"Troubleshooting:\n"
                f"  1. Review the provider schema for required vs optional fields\n"
                f"  2. Check that all field values have the correct type\n"
                f"  3. Ensure no required fields are unknown/computed during configuration\n"
                f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
            err.add_context("config.schema", str(provider_schema.block) if provider_schema else "None")
            err.add_context("provider.name", provider_instance.metadata.name)
            err.add_context("terraform.summary", "Invalid provider configuration")
            err.add_context(
                "terraform.detail", "The provider configuration could not be parsed into the expected format."
            )
            raise err

        logger.debug(
            "Creating provider context",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
        )

        # Check PYVIDER_TESTMODE environment variable (highest priority),
        # then HCL configuration, then default.
        test_mode_enabled, test_mode_source = _resolve_test_mode(config_instance)

        logger.debug(
            "Resolved pyvider_testmode",
            config_instance_type=type(config_instance).__name__,
            final_value=test_mode_enabled,
            source=test_mode_source,
        )

        # The provider's own configure() hook: where a provider turns configuration
        # into whatever it needs to serve requests — an API client, credentials, a
        # working directory. Registering the context after the hook fully succeeds
        # ensures the published context always matches the live provider object's
        # state, and a failed hook does not leave _configured stuck True with no client.
        try:
            await provider_instance.configure(config_instance)
            # Hook succeeded — now safe to mark configured and publish context.
            provider_instance._configured = True
            provider_context = ProviderContext(config=config_instance, test_mode_enabled=test_mode_enabled)
            hub.register("singleton", "provider_context", provider_context)
        except ProviderAlreadyConfiguredError:
            # A repeated ConfigureProvider RPC, which is normal and must succeed:
            # the "configure once" rule concerns multiple provider BLOCKS, not
            # repeated RPCs against the same object. The context published by the
            # first call still describes the live provider, so it is left alone.
            #
            # This is matched on the exception TYPE deliberately. Checking
            # provider_instance._configured instead cannot distinguish the two
            # cases: BaseProvider.configure() sets that flag before a subclass's
            # own body has run, so the ordinary `await super().configure(...)`
            # then build-a-client shape reports a failed hook as success.
            logger.debug(
                "Provider was already configured",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )
        except Exception as e:
            logger.error(
                "Provider configure() hook failed",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
                error_type=type(e).__name__,
                error_message=str(e),
                exc_info=True,
            )
            response.diagnostics.append(await create_diagnostic_from_exception(e))
            return response

        if test_mode_enabled:
            logger.warning(
                "⚠️  Provider test mode enabled - test-only components are now accessible",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
                source=test_mode_source,
            )
        else:
            logger.debug(
                "Test mode is not enabled - test-only components will be filtered out",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )

        logger.info(
            "Provider configured successfully",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
            provider_version=provider_instance.metadata.version,
            test_mode_enabled=test_mode_enabled,
        )

    except PyviderError as e:
        logger.error(
            "ConfigureProvider failed with framework error",
            operation="configure_provider",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "ConfigureProvider failed with unexpected error",
            operation="configure_provider",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
