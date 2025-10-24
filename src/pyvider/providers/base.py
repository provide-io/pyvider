import asyncio
from typing import Any

from attrs import define, field
from provide.foundation import logger

from pyvider.cty import CtyType
from pyvider.exceptions import FrameworkConfigurationError, ProviderError
from pyvider.schema import PvsSchema


@define
class ProviderCapabilities:
    """Provider capability configuration."""

    plan_destroy: bool = True
    get_provider_schema_optional: bool = False
    move_resource_state: bool = True


@define
class ProviderMetadata:
    """Provider metadata configuration."""

    name: str
    version: str
    protocol_version: str = "6"
    capabilities: ProviderCapabilities = field(factory=ProviderCapabilities)


@define
class BaseProvider:
    """
    Base provider implementation that handles gRPC service initialization
    and provider lifecycle management.
    """

    metadata: ProviderMetadata
    config_class: Any | None = None  # Add config_class attribute
    _configured: bool = field(default=False, init=False)
    _final_schema: PvsSchema | None = field(default=None, init=False)

    async def setup(self) -> None:
        """
        An initialization hook called by the framework after component
        discovery but before serving requests. This is the ideal place
        to assemble the final schema by integrating capabilities.
        """
        logger.debug(
            "Provider setup hook called",
            operation="setup",
            provider_name=self.metadata.name,
            provider_version=self.metadata.version,
            protocol_version=self.metadata.protocol_version,
        )
        pass  # pragma: no cover

    async def configure(self, config: dict[str, CtyType]) -> None:
        """Configure the provider with the given configuration."""
        async with asyncio.Lock():
            if self._configured:
                logger.warning(
                    "Attempted to configure provider that is already configured",
                    operation="configure",
                    provider_name=self.metadata.name,
                    provider_version=self.metadata.version,
                )
                raise ProviderError(
                    f"Provider '{self.metadata.name}' has already been configured. "
                    f"Terraform providers can only be configured once per execution.\n\n"
                    f"Suggestion: Ensure your Terraform configuration has only one 'provider' block "
                    f"for this provider. Multiple 'provider' blocks with the same name require "
                    f"the 'alias' parameter.\n\n"
                    f"Example:\n"
                    f'  provider "{self.metadata.name}" {{\n'
                    f"    # Configuration here\n"
                    f"  }}\n\n"
                    f"For multiple configurations:\n"
                    f'  provider "{self.metadata.name}" {{\n'
                    f'    alias = "west"\n'
                    f"  }}"
                )

            logger.info(
                "Provider configuration started",
                operation="configure",
                provider_name=self.metadata.name,
                provider_version=self.metadata.version,
                config_keys=list(config.keys()),
            )
            self._configured = True
            logger.info(
                "Provider configured successfully",
                operation="configure",
                provider_name=self.metadata.name,
            )

    @property
    def schema(self) -> PvsSchema:
        """Get the provider schema."""
        if self._final_schema is None:
            logger.error(
                "Provider schema accessed before initialization",
                operation="get_schema",
                provider_name=self.metadata.name,
                setup_completed=False,
            )
            raise FrameworkConfigurationError(
                f"Provider schema for '{self.metadata.name}' was requested before initialization.\n\n"
                f"Error: The setup() hook must be called before accessing the provider schema. "
                f"This is typically handled automatically by the framework during provider startup.\n\n"
                f"Suggestion: This usually indicates an internal framework issue. If you're seeing this error:\n"
                f"  1. Ensure the provider is being started through the standard 'pyvider provide' command\n"
                f"  2. Check that the provider's setup() hook is implemented correctly\n"
                f"  3. Verify that schema access happens after provider initialization\n\n"
                f"If the issue persists, this may be a framework bug. Please report it with:\n"
                f"  - Provider name: {self.metadata.name}\n"
                f"  - Provider version: {self.metadata.version}\n"
                f"  - How the provider was started (command line, tests, etc.)"
            )
        return self._final_schema
