#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TDD Contract for the CRUD Resource Lifecycle.

This test suite defines the expected behavior of the BaseResource dispatcher
and the contracts for the _create, _update, _create_apply, and _update_apply hooks."""

from typing import Any

import attrs
from provide.testkit.mocking import AsyncMock
import pytest
from pytest_mock import MockerFixture

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_resource


@attrs.define(frozen=True)
class ContractConfig:
    name: str
    location: str


@attrs.define(frozen=True)
class ContractState:
    name: str
    location: str
    id: str


class ContractTestResource(BaseResource):
    """A mockable resource to spy on lifecycle method calls."""

    config_class = ContractConfig
    state_class = ContractState

    def __init__(self, mocker: MockerFixture) -> None:
        self._mocker = mocker
        # Spy on the methods we want to test
        self._create = AsyncMock(return_value=({}, None))
        self._update = AsyncMock(return_value=({}, None))
        self._delete_plan = AsyncMock(return_value=(None, None))
        self._create_apply = AsyncMock(return_value=(None, None))
        self._update_apply = AsyncMock(return_value=(None, None))
        self._delete_apply = AsyncMock()

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(),
                "location": a_str(),
                "id": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> None:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        # This method makes the class concrete. The __init__ overwrites it
        # with the mock for spying.
        await self._delete_apply(ctx)


@pytest.mark.asyncio
class TestResourceContracts:
    async def test_tdd1_create_plan_contract(self, mocker: MockerFixture) -> None:
        """
        TDD 1: Verifies the `base_plan` passed to `_create` contains all config values.
        """
        resource = ContractTestResource(mocker)
        config = ContractConfig(name="new-server", location="us-west-1")

        # Simulate the proposed new state that Terraform provides during a create plan.
        schema = resource.get_schema()
        proposed_new_state_cty = schema.block.to_cty_type().validate(
            {
                "name": config.name,
                "location": config.location,
            }
        )

        ctx = ResourceContext(config=config, state=None, planned_state_cty=proposed_new_state_cty)

        await resource.plan(ctx)

        resource._create.assert_called_once()
        call_args = resource._create.call_args[0]
        base_plan_arg = call_args[1]

        assert base_plan_arg["name"] == "new-server"
        assert base_plan_arg["location"] == "us-west-1"

    async def test_tdd2_update_context_contract(self, mocker: MockerFixture) -> None:
        """
        TDD 2: Verifies `_update` receives a context with both prior state and new config.
        """
        resource = ContractTestResource(mocker)
        prior_state = ContractState(name="old-name", location="us-east-1", id="server-123")
        new_config = ContractConfig(name="new-name", location="us-west-2")

        # Simulate the proposed new state for an update.
        schema = resource.get_schema()
        proposed_new_state_cty = schema.block.to_cty_type().validate(
            {
                "name": new_config.name,
                "location": new_config.location,
                "id": prior_state.id,  # ID is carried over from prior state
            }
        )

        # The `planned_state` (attrs object) is also needed for the context.
        planned_state = ContractState(name="new-name", location="us-west-2", id="server-123")

        ctx = ResourceContext(
            config=new_config,
            state=prior_state,
            planned_state=planned_state,
            planned_state_cty=proposed_new_state_cty,
        )

        await resource.plan(ctx)

        resource._update.assert_called_once()
        call_args = resource._update.call_args[0]
        ctx_arg: ResourceContext = call_args[0]
        base_plan_arg = call_args[1]

        assert ctx_arg.state is prior_state
        assert ctx_arg.config is new_config
        # Also verify the base_plan is now correctly populated
        assert base_plan_arg["name"] == "new-name"
        assert base_plan_arg["location"] == "us-west-2"

    async def test_tdd3_apply_consistency_contract(self, mocker: MockerFixture) -> None:
        """
        TDD 3: Verifies `_update_apply` receives the correct planned state.
        """
        resource = ContractTestResource(mocker)
        prior_state = ContractState(name="old-name", location="us-east-1", id="server-123")
        # This is the state that came out of the `plan` phase.
        planned_state_from_plan = ContractState(name="new-name", location="us-west-2", id="server-123")

        ctx = ResourceContext(state=prior_state, planned_state=planned_state_from_plan)

        await resource.apply(ctx)

        resource._update_apply.assert_called_once()
        call_args = resource._update_apply.call_args[0]
        ctx_arg: ResourceContext = call_args[0]

        assert ctx_arg.planned_state is planned_state_from_plan
        assert ctx_arg.state is prior_state


# 🐍🏗️🔚
