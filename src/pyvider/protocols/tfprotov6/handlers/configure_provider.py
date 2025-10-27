import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import unmarshal
from pyvider.exceptions import ProviderConfigurationError, PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.context import ProviderContext
from pyvider.resources.base import BaseResource


@resilient()
async def ConfigureProviderHandler(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """
    Handles the ConfigureProvider RPC request.

    This handler validates the provider configuration sent by Terraform
    and initializes the provider context, making it available for all
    subsequent component operations.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="ConfigureProvider")

    try:
        return await _configure_provider_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ConfigureProvider")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ConfigureProvider")


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
        config_cty = unmarshal(request.config, schema=provider_schema.block)

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

        config_instance = BaseResource.from_cty(config_cty, provider_instance.config_class)

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

        test_mode_enabled = getattr(config_instance, "provider_testmode", False)
        provider_context = ProviderContext(config=config_instance, test_mode_enabled=test_mode_enabled)
        hub.register("singleton", "provider_context", provider_context)

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
