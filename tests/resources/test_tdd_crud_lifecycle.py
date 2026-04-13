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
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource


@attrs.define(frozen=True)
class CrudConfig:
    name: str


@attrs.define(frozen=True)
class CrudState:
    name: str
    id: str


@attrs.define(frozen=True)
class CrudPrivateState(PrivateState):
    version: int


class CrudTestResource(BaseResource):
    """A mockable resource to spy on lifecycle method calls."""

    config_class = CrudConfig
    state_class = CrudState
    private_state_class = CrudPrivateState

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
        return s_resource({"name": a_str(), "id": a_str(computed=True)})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> None:
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        # This method makes the class concrete. The __init__ overwrites it
        # with the mock for spying.
        await self._delete_apply(ctx)


@pytest.mark.asyncio
class TestCrudLifecycleDispatcher:
    async def test_plan_dispatches_to_create(self, mocker: MockerFixture) -> None:
        """TDD Contract: plan() must call _create() when state is None."""
        resource = CrudTestResource(mocker)
        config = CrudConfig(name="new-resource")
        ctx = ResourceContext(config=config, state=None)

        await resource.plan(ctx)

        resource._create.assert_called_once()
        resource._update.assert_not_called()
        resource._delete_plan.assert_not_called()

    async def test_plan_dispatches_to_update(self, mocker: MockerFixture) -> None:
        """TDD Contract: plan() must call _update() when state is present."""
        resource = CrudTestResource(mocker)
        config = CrudConfig(name="updated-resource")
        state = CrudState(name="old-resource", id="123")
        planned_state = CrudState(name="updated-resource", id="123")
        ctx = ResourceContext(config=config, state=state, planned_state=planned_state)

        await resource.plan(ctx)

        resource._update.assert_called_once()
        resource._create.assert_not_called()
        resource._delete_plan.assert_not_called()

    async def test_plan_dispatches_to_delete_plan(self, mocker: MockerFixture) -> None:
        """TDD Contract: plan() must call _delete_plan() for a delete operation."""
        resource = CrudTestResource(mocker)
        state = CrudState(name="old-resource", id="123")
        ctx = ResourceContext(config=None, state=state, planned_state=None)

        await resource.plan(ctx)

        resource._delete_plan.assert_called_once()
        resource._create.assert_not_called()
        resource._update.assert_not_called()

    async def test_apply_dispatches_to_create_apply(self, mocker: MockerFixture) -> None:
        """TDD Contract: apply() must call _create_apply() when state is None."""
        resource = CrudTestResource(mocker)
        planned_state = CrudState(name="new-resource", id="123")
        ctx = ResourceContext(state=None, planned_state=planned_state)

        await resource.apply(ctx)

        resource._create_apply.assert_called_once()
        resource._update_apply.assert_not_called()
        resource._delete_apply.assert_not_called()

    async def test_apply_dispatches_to_update_apply(self, mocker: MockerFixture) -> None:
        """TDD Contract: apply() must call _update_apply() when state is present."""
        resource = CrudTestResource(mocker)
        state = CrudState(name="old-resource", id="123")
        planned_state = CrudState(name="updated-resource", id="123")
        ctx = ResourceContext(state=state, planned_state=planned_state)

        await resource.apply(ctx)

        resource._update_apply.assert_called_once()
        resource._create_apply.assert_not_called()
        resource._delete_apply.assert_not_called()

    async def test_apply_dispatches_to_delete_apply(self, mocker: MockerFixture) -> None:
        """TDD Contract: apply() must call _delete_apply() when planned_state is None."""
        resource = CrudTestResource(mocker)
        state = CrudState(name="old-resource", id="123")
        ctx = ResourceContext(state=state, planned_state=None)

        await resource.apply(ctx)

        resource._delete_apply.assert_called_once()
        resource._create_apply.assert_not_called()
        resource._update_apply.assert_not_called()


# 🐍🏗️🔚
