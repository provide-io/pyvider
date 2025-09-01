from typing import Any

from pyvider.conversion import unmarshal
from pyvider.exceptions import ProviderConfigurationError, PyviderError
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.context import ProviderContext
from pyvider.resources.base import BaseResource
from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception


async def ConfigureProviderHandler(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """
    Handles the ConfigureProvider RPC request.

    This handler validates the provider configuration sent by Terraform
    and initializes the provider context, making it available for all
    subsequent component operations.
    """
    response = pb.ConfigureProvider.Response()
    logger.debug("Received ConfigureProvider request")
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise ProviderConfigurationError("Provider instance not found in hub.")

        provider_schema = provider_instance.schema
        config_cty = unmarshal(request.config, schema=provider_schema.block)

        if config_cty.is_unknown:
            logger.warning(
                "Provider configuration is unknown. Deferring configuration."
            )
            return response

        config_instance = BaseResource.from_cty(
            config_cty, provider_instance.config_class
        )

        if config_instance is None:
            raise ProviderConfigurationError(
                "Failed to instantiate provider configuration."
            )

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
