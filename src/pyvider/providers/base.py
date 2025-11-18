#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import asyncio
from typing import Any, ClassVar

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

    Automatically discovers and integrates capabilities during setup().
    Component packages can override setup() for custom initialization.
    """

    metadata: ProviderMetadata
    config_class: Any | None = None  # Add config_class attribute
    _configured: bool = field(default=False, init=False)
    _final_schema: PvsSchema | None = field(default=None, init=False)
    capabilities: ClassVar[dict[str, Any]] = {}

    async def setup(self) -> None:
        """
        Initialization hook called by the framework after component
        discovery but before serving requests.

        Automatically:
        - Discovers capabilities from the hub
        - Instantiates capability classes
        - Composes provider schema from capability contributions
        - Creates config_class for configuration parsing

        Override this method for custom provider initialization.
        """
        from typing import cast

        from pyvider.cli.context import PyviderContext
        from pyvider.common.utils.attrs_factory import create_attrs_class_from_schema
        from pyvider.hub import hub
        from pyvider.schema import s_provider

        logger.debug(
            "Provider setup started",
            operation="setup",
            provider_name=self.metadata.name,
            provider_version=self.metadata.version,
            protocol_version=self.metadata.protocol_version,
        )

        # Auto-discover and instantiate capabilities
        final_attributes = {}
        capability_classes = hub.get_components("capability")

        provider_ctx_factory = hub.get_component("singleton", "provider_context")
        if provider_ctx_factory:
            # Handle both factory functions and direct instances
            provider_ctx = cast(
                PyviderContext,
                provider_ctx_factory() if callable(provider_ctx_factory) else provider_ctx_factory,
            )
        else:
            provider_ctx = None
        provider_config = provider_ctx.config if provider_ctx else None

        for name, cap_class in capability_classes.items():
            cap_instance = cap_class(config=provider_config)
            self.capabilities[name] = cap_instance
            if hasattr(cap_instance, "get_schema_contribution"):
                final_attributes.update(cap_instance.get_schema_contribution())

        self.capabilities["provider"] = self

        # Build final provider schema
        self._final_schema = s_provider(attributes=final_attributes)
        self.config_class = create_attrs_class_from_schema(
            "ProviderConfig", self._final_schema.block.attributes
        )

        # Validate component-capability associations
        all_components = {
            **hub.get_components("resource"),
            **hub.get_components("data_source"),
            **hub.get_components("function"),
        }
        for name, comp in all_components.items():
            parent_cap_name = getattr(comp, "_parent_capability", "provider")
            if parent_cap_name not in self.capabilities:
                raise FrameworkConfigurationError(
                    f"Component '{name}' is associated with capability '{parent_cap_name}', "
                    f"but that capability is not registered."
                )

        logger.info(
            "Provider setup completed",
            operation="setup",
            provider_name=self.metadata.name,
            capabilities=list(self.capabilities.keys()),
        )

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


# 🐍🏗️🔚
