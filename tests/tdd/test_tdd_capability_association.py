#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import pytest

from pyvider.exceptions import FrameworkConfigurationError
from pyvider.hub import hub
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.decorators import register_resource
from pyvider.schema import PvsSchema, a_str, s_resource


@register_resource("orphan_resource")
class OrphanResource(BaseResource):
    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str()})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: Any) -> None:
        pass

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict, None]:
        return base_plan, None

    async def _delete_apply(self, ctx: Any) -> None:
        pass


@pytest.mark.asyncio
class TestTddCapabilityAssociation:
    @pytest.fixture(autouse=True)
    def clean_hub(self) -> None:
        hub.registry = {}
        yield
        hub.registry = {}

    async def test_provider_setup_succeeds_for_provider_component(self) -> None:
        """A component without `component_of` is a provider component and should succeed."""
        hub.register("resource", "orphan_resource", OrphanResource)
        provider = BaseProvider(metadata=ProviderMetadata(name="test", version="0.0.1"))
        try:
            await provider.setup()
        except FrameworkConfigurationError:
            pytest.fail("Provider setup failed for a valid provider component.")


# 🐍🏗️🔚
