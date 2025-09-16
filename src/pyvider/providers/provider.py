from typing import ClassVar

from provide.foundation import logger

from pyvider.capabilities import BaseCapability
from pyvider.common.utils.attrs_factory import create_attrs_class_from_schema
from pyvider.exceptions import FrameworkConfigurationError
from pyvider.hub import hub
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.providers.decorators import register_provider
from pyvider.schema import s_provider


@register_provider("pyvider")
class PyviderProvider(BaseProvider):
    capabilities: ClassVar[dict[str, BaseCapability]] = {}

    def __init__(self) -> None:
        provider_metadata = ProviderMetadata(name="pyvider", version="0.1.0")
        super().__init__(metadata=provider_metadata)
        logger.info("PyviderProvider orchestrator initialized.")

    async def setup(self) -> None:
        final_attributes = {}
        capability_classes = hub.get_components("capability")

        provider_ctx = hub.get_component("singleton", "provider_context")
        provider_config = provider_ctx.config if provider_ctx else None

        for name, cap_class in capability_classes.items():
            cap_instance = cap_class(config=provider_config)
            self.capabilities[name] = cap_instance
            if hasattr(cap_instance, "get_schema_contribution"):
                final_attributes.update(cap_instance.get_schema_contribution())

        self.capabilities["provider"] = self

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
            if parent_cap_name not in self.capabilities:
                raise FrameworkConfigurationError(
                    f"Component '{name}' is associated with capability '{parent_cap_name}', but that capability is not registered."
                )
