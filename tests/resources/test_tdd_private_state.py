#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import msgpack
import pytest

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource


# GIVEN a resource that uses a structured private state object
@attrs.define(frozen=True)
class MyPrivateState(PrivateState):
    internal_id: str
    version: int


class ResourceWithPrivateState(BaseResource):
    private_state_class = MyPrivateState

    # Other required abstract methods...
    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str()})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> None:
        pass

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any], MyPrivateState]:
        # WHEN the plan operation returns a private state object
        private_state = MyPrivateState(internal_id="uuid-1234", version=1)
        return base_plan, private_state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@pytest.mark.asyncio
async def test_private_state_roundtrip() -> None:
    """
    TDD Contract: Verifies that a structured private state object can be
    serialized to bytes by one handler and correctly deserialized back
    into a typed object by another.
    """
    resource = ResourceWithPrivateState()
    ctx = ResourceContext()  # Dummy context for plan

    # 1. Simulate the Plan handler's work
    _, planned_private_state_obj = await resource._create(ctx, {})

    # This is what the handler would do
    serialized_private_bytes = msgpack.packb(attrs.asdict(planned_private_state_obj))

    # 2. Simulate the Apply handler's work
    # This is what the next handler would do upon receiving the bytes
    deserialized_data = msgpack.unpackb(serialized_private_bytes)
    rehydrated_private_state_obj = MyPrivateState(**deserialized_data)

    # THEN the rehydrated object is identical to the original
    assert rehydrated_private_state_obj == planned_private_state_obj


# 🐍🏗️🔚
