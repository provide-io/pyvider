#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest

from pyvider.exceptions import ResourceError
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource


# 1. Define a structured class for the resource's private state.
#    This inherits from the PrivateState marker class.
@attrs.define(frozen=True)
class StatefulPrivateState(PrivateState):
    """A structured object to hold internal metadata for the resource."""

    internal_id: str
    version: int
    transient_token: str


# 2. Define a simple attrs class for the resource's main state.
@attrs.define(frozen=True)
class StatefulResourceState:
    name: str
    internal_id: str


# 3. Implement the test resource.
class StatefulResource(BaseResource):
    """
    A test resource designed to validate the private state lifecycle.
    - `_create` creates a private state object.
    - `_create_apply` expects to receive that exact object back.
    """

    state_class = StatefulResourceState
    private_state_class = StatefulPrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "internal_id": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, StatefulPrivateState | None]:
        """
        On plan, create a new state and a new private state object containing
        a unique token.
        """
        base_plan["internal_id"] = "id-planned"
        private_state = StatefulPrivateState(
            internal_id="id-planned", version=1, transient_token="secret-plan-token"
        )
        return base_plan, private_state

    async def _create_apply(
        self, ctx: ResourceContext
    ) -> tuple[StatefulResourceState | None, StatefulPrivateState | None]:
        """
        On apply, validate that the private state received from the framework
        is exactly what was generated during the plan phase.
        """
        # This is the core assertion of the contract.
        if not ctx.private_state:
            raise ResourceError("Apply phase received no private state, but one was expected.")

        if not isinstance(ctx.private_state, StatefulPrivateState):
            raise ResourceError(f"Private state has incorrect type: got {type(ctx.private_state).__name__}")

        if ctx.private_state.transient_token != "secret-plan-token":
            raise ResourceError("The private state received by apply was tampered with or lost.")

        # If validation passes, return the final state.
        final_state = StatefulResourceState(
            name=ctx.planned_state.name, internal_id=ctx.private_state.internal_id
        )
        # The private state is typically not persisted after apply.
        return final_state, None

    # Dummy implementations for other abstract methods
    async def read(self, ctx: ResourceContext) -> StatefulResourceState | None:
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@pytest.mark.asyncio
async def test_private_state_is_passed_from_plan_to_apply() -> None:
    """
    TDD: Verifies that the private state object returned by `_create` is
    correctly passed to the `_create_apply` method within the ResourceContext.
    """
    resource = StatefulResource()

    # --- Simulate the Plan Phase ---
    # The config is a simple object, not an attrs class, for this test.
    config_obj = type("Config", (), {"name": "test-resource"})()
    plan_context = ResourceContext(config=config_obj)
    base_plan = {"name": "test-resource"}

    planned_state_dict, planned_private_state = await resource._create(plan_context, base_plan)
    planned_state = resource.state_class(**planned_state_dict)

    assert planned_private_state is not None
    assert planned_private_state.transient_token == "secret-plan-token"

    # --- Simulate the Apply Phase ---
    # The framework would pass the planned_state and planned_private_state
    # into the context for the apply call.
    apply_context = ResourceContext(
        config=config_obj,
        planned_state=planned_state,
        private_state=planned_private_state,
    )

    # The `_create_apply` method contains the assertions. If it runs without
    # raising an error, the contract is fulfilled.
    final_state, final_private_state = await resource._create_apply(apply_context)

    assert final_state is not None
    assert final_state.internal_id == "id-planned"
    assert final_private_state is None


# 🐍🏗️🔚
