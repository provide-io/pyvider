#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive lifecycle tests for resources/base.py (44% → 90%+)."""

from typing import Any

import attrs
import pytest

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_num, a_str, s_resource


# Test fixtures
@attrs.define
class SampleConfig:
    name: str
    count: int = 0


@attrs.define
class SampleState:
    id: str
    name: str
    count: int = 0


@attrs.define
class SamplePrivateState(PrivateState):
    secret: str = ""


class SampleResource(BaseResource[Any, SampleState, SampleConfig]):
    """Concrete test resource for testing."""

    config_class = SampleConfig
    state_class = SampleState
    private_state_class = SamplePrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "id": a_str(computed=True),
                "name": a_str(required=True),
                "count": a_num(optional=True),
            }
        )

    async def _validate_config(self, config: SampleConfig) -> list[str]:
        errors = []
        if config.name == "invalid":
            errors.append("Name cannot be 'invalid'")
        return errors

    async def read(self, ctx: ResourceContext) -> SampleState | None:
        if ctx.state and ctx.state.id == "deleted":
            return None
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass  # Deletion logic


class TestBaseResourceLifecycle:
    """Tests for BaseResource lifecycle methods."""

    @pytest.mark.asyncio
    async def test_validate_with_valid_config(self) -> None:
        """Test validation passes for valid config."""
        resource = SampleResource()
        config = SampleConfig(name="valid", count=10)

        errors = await resource.validate(config)

        assert len(errors) == 0

    @pytest.mark.asyncio
    async def test_validate_with_invalid_config(self) -> None:
        """Test validation fails for invalid config."""
        resource = SampleResource()
        config = SampleConfig(name="invalid", count=10)

        errors = await resource.validate(config)

        assert len(errors) == 1
        assert "cannot be 'invalid'" in errors[0]

    @pytest.mark.asyncio
    async def test_validate_with_none_config_returns_empty_list(self) -> None:
        """Test validation with None config returns empty list."""
        resource = SampleResource()

        errors = await resource.validate(None)

        assert errors == []

    @pytest.mark.asyncio
    async def test_plan_create_operation(self) -> None:
        """Test plan for create operation (state is None)."""
        resource = SampleResource()
        schema = SampleResource.get_schema()
        cty_type = schema.block.to_cty_type()

        # Create operation: state is None
        config = SampleConfig(name="new-resource", count=5)
        config_cty = cty_type.validate({"name": "new-resource", "count": 5})
        planned_state_cty = cty_type.validate({"name": "new-resource", "count": 5, "id": "computed"})

        ctx = ResourceContext(
            config=config,
            state=None,  # Create operation
            private_state=None,
            capabilities={},
            config_cty=config_cty,
            planned_state_cty=planned_state_cty,
        )

        planned_state, _private_state = await resource.plan(ctx)

        assert planned_state is not None
        assert "name" in planned_state
        assert planned_state["name"] == "new-resource"

    @pytest.mark.asyncio
    async def test_plan_update_operation(self) -> None:
        """Test plan for update operation (state exists)."""
        resource = SampleResource()
        schema = SampleResource.get_schema()
        cty_type = schema.block.to_cty_type()

        # Update operation: state exists
        config = SampleConfig(name="updated-resource", count=10)
        state = SampleState(id="res-123", name="old-name", count=5)
        config_cty = cty_type.validate({"id": "res-123", "name": "updated-resource", "count": 10})
        planned_state_cty = cty_type.validate({"id": "res-123", "name": "updated-resource", "count": 10})

        ctx = ResourceContext(
            config=config,
            state=state,  # Update operation
            private_state=None,
            capabilities={},
            config_cty=config_cty,
            planned_state_cty=planned_state_cty,
        )

        planned_state, _private_state = await resource.plan(ctx)

        assert planned_state is not None
        assert planned_state["name"] == "updated-resource"

    @pytest.mark.asyncio
    async def test_plan_delete_operation(self) -> None:
        """Test plan for delete operation (config is None, planned_state is None)."""
        resource = SampleResource()
        state = SampleState(id="res-to-delete", name="old", count=0)

        ctx = ResourceContext(
            config=None,  # Delete operation
            state=state,
            private_state=None,
            capabilities={},
            planned_state=None,
        )

        planned_state, private_state = await resource.plan(ctx)

        # Delete plan should return None, None
        assert planned_state is None
        assert private_state is None

    @pytest.mark.asyncio
    async def test_plan_with_validation_errors(self) -> None:
        """Test that plan adds validation errors to context."""
        resource = SampleResource()
        schema = SampleResource.get_schema()
        cty_type = schema.block.to_cty_type()

        config = SampleConfig(name="invalid", count=5)
        config_cty = cty_type.validate({"name": "invalid", "count": 5})

        ctx = ResourceContext(
            config=config,
            state=None,
            private_state=None,
            capabilities={},
            config_cty=config_cty,
            planned_state_cty=config_cty,
        )

        planned_state, private_state = await resource.plan(ctx)

        # Plan should return None, None when validation fails
        assert planned_state is None
        assert private_state is None
        assert len(ctx.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_apply_create_operation(self) -> None:
        """Test apply for create operation."""
        resource = SampleResource()

        planned_state = SampleState(id="new-id", name="created", count=1)
        ctx = ResourceContext(
            config=None,
            state=None,  # Create operation
            private_state=None,
            capabilities={},
            planned_state=planned_state,
        )

        new_state, _private_state = await resource.apply(ctx)

        assert new_state is not None
        assert new_state.id == "new-id"
        assert new_state.name == "created"

    @pytest.mark.asyncio
    async def test_apply_update_operation(self) -> None:
        """Test apply for update operation."""
        resource = SampleResource()

        old_state = SampleState(id="res-123", name="old", count=1)
        planned_state = SampleState(id="res-123", name="updated", count=2)

        ctx = ResourceContext(
            config=None,
            state=old_state,  # Update operation
            private_state=None,
            capabilities={},
            planned_state=planned_state,
        )

        new_state, _private_state = await resource.apply(ctx)

        assert new_state is not None
        assert new_state.name == "updated"
        assert new_state.count == 2

    @pytest.mark.asyncio
    async def test_apply_delete_operation(self) -> None:
        """Test apply for delete operation."""
        resource = SampleResource()

        old_state = SampleState(id="res-to-delete", name="deleted", count=0)
        ctx = ResourceContext(
            config=None,
            state=old_state,
            private_state=None,
            capabilities={},
            planned_state=None,  # Delete operation
        )

        new_state, private_state = await resource.apply(ctx)

        # Delete should return None, None
        assert new_state is None
        assert private_state is None

    @pytest.mark.asyncio
    async def test_read_returns_state(self) -> None:
        """Test read method returns state."""
        resource = SampleResource()
        state = SampleState(id="res-123", name="test", count=5)

        ctx = ResourceContext(
            config=None,
            state=state,
            private_state=None,
            capabilities={},
        )

        result = await resource.read(ctx)

        assert result is not None
        assert result.id == "res-123"
        assert result.name == "test"

    @pytest.mark.asyncio
    async def test_read_returns_none_for_deleted_resource(self) -> None:
        """Test read returns None for deleted resource."""
        resource = SampleResource()
        state = SampleState(id="deleted", name="gone", count=0)

        ctx = ResourceContext(
            config=None,
            state=state,
            private_state=None,
            capabilities={},
        )

        result = await resource.read(ctx)

        assert result is None


# 🐍🏗️🔚
