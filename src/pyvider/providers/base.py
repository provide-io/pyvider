#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
from collections.abc import Sequence
from typing import Any

import attrs
from attrs import define, field
from provide.foundation import logger

from pyvider.exceptions import FrameworkConfigurationError, ProviderAlreadyConfiguredError
from pyvider.lint import LintContext, LintFinding
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


def _config_keys(config: Any) -> list[str]:
    """Field names of a provider config, whatever it is.

    The configure hook receives what the protocol layer produced: an attrs instance
    for a populated config, None for an empty one, and a dict when called directly.
    """
    if config is None:
        return []
    if isinstance(config, dict):
        return list(config.keys())
    if attrs.has(type(config)):
        return [f.name for f in attrs.fields(type(config))]
    return []


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
    capabilities: dict[str, Any] = field(factory=dict, init=False)
    _setup_done: bool = field(default=False, init=False)
    _setup_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _configure_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)

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

        async with self._setup_lock:
            if self._setup_done:
                return

            logger.debug(
                "Provider setup started",
                operation="setup",
                provider_name=self.metadata.name,
                provider_version=self.metadata.version,
                protocol_version=self.metadata.protocol_version,
            )

            final_attributes: dict[str, Any] = {}
            capability_classes = hub.get_components("capability")

            provider_ctx_factory = hub.get_component("singleton", "provider_context")
            if provider_ctx_factory:
                provider_ctx = cast(
                    PyviderContext,
                    provider_ctx_factory() if callable(provider_ctx_factory) else provider_ctx_factory,
                )
            else:
                provider_ctx = None
            provider_config = provider_ctx.config if provider_ctx else None

            new_capabilities: dict[str, Any] = {}
            for name, cap_class in capability_classes.items():
                cap_instance = cap_class(config=provider_config)
                new_capabilities[name] = cap_instance
                if hasattr(cap_instance, "get_schema_contribution"):
                    final_attributes.update(cap_instance.get_schema_contribution())

            new_capabilities["provider"] = self

            self._final_schema = s_provider(attributes=final_attributes)
            self.config_class = create_attrs_class_from_schema(
                "ProviderConfig", self._final_schema.block.attributes
            )

            all_components = {
                **hub.get_components("resource"),
                **hub.get_components("data_source"),
                **hub.get_components("function"),
            }
            for name, comp in all_components.items():
                parent_cap_name = getattr(comp, "_parent_capability", "provider")
                if parent_cap_name not in new_capabilities:
                    raise FrameworkConfigurationError(
                        f"Component '{name}' is associated with capability '{parent_cap_name}', "
                        f"but that capability is not registered."
                    )

            # Atomic publish — capabilities is only observed in a completed state.
            self.capabilities = new_capabilities
            self._setup_done = True

            logger.info(
                "Provider setup completed",
                operation="setup",
                provider_name=self.metadata.name,
                capabilities=list(self.capabilities.keys()),
            )

    async def configure(self, config: Any) -> None:
        """Configure the provider with the given configuration.

        The ``config`` parameter is an attrs instance produced by the framework's
        configuration parsing (via ``BaseResource.from_cty()``).  It is not a
        plain ``dict``; use attribute access (``config.api_key``) rather than
        mapping access (``config["api_key"]`` or ``config.get("api_key")``).
        """
        async with self._configure_lock:
            if self._configured:
                logger.warning(
                    "Attempted to configure provider that is already configured",
                    operation="configure",
                    provider_name=self.metadata.name,
                    provider_version=self.metadata.version,
                )
                raise ProviderAlreadyConfiguredError(
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
                config_keys=_config_keys(config),
            )
            self._configured = True
            logger.info(
                "Provider configured successfully",
                operation="configure",
                provider_name=self.metadata.name,
            )

    async def lint(self, ctx: LintContext[Any]) -> Sequence[LintFinding]:
        """Return opt-in advisory findings for a semantically valid configuration."""
        return ()

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

    @classmethod
    def get_provider_meta_schema(cls) -> PvsSchema | None:
        """Get the provider_meta schema. Defaults to None."""
        return None


# 🐍🏗️🔚
