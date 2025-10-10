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
    logger.debug("Received ConfigureProvider request")
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            err = ProviderConfigurationError("Provider instance not found in hub.")
            err.add_context("hub.dimension", "singleton")
            err.add_context("hub.component_type", "provider")
            err.add_context("terraform.summary", "Provider not registered")
            err.add_context(
                "terraform.detail", "The provider has not been properly registered with the framework."
            )
            raise err

        provider_schema = provider_instance.schema
        config_cty = unmarshal(request.config, schema=provider_schema.block)

        if config_cty.is_unknown:
            logger.warning("Provider configuration is unknown. Deferring configuration.")
            return response

        config_instance = BaseResource.from_cty(config_cty, provider_instance.config_class)

        if config_instance is None:
            err = ProviderConfigurationError("Failed to instantiate provider configuration.")
            err.add_context("config.schema", str(provider_schema.block) if provider_schema else "None")
            err.add_context("terraform.summary", "Invalid provider configuration")
            err.add_context(
                "terraform.detail", "The provider configuration could not be parsed into the expected format."
            )
            raise err

        provider_context = ProviderContext(config=config_instance)
        hub.register("singleton", "provider_context", provider_context)

        logger.info("Provider successfully configured and context stored in hub.")

    except PyviderError as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error("Unhandled error in ConfigureProviderHandler", exc_info=True)
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
