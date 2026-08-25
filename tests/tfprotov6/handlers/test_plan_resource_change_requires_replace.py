#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for requires_replace handling in the PlanResourceChange handler."""

from typing import Any

from attrs import define
from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.conversion import marshal
from pyvider.cty import CtyNumber, CtyString, CtyValue
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import (
    _attribute_changed,
    _collect_requires_replace_paths,
    _plan_resource_change_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_num, a_str, s_resource

MODULE = "pyvider.protocols.tfprotov6.handlers.plan_resource_change"

RESOURCE_SCHEMA = s_resource(
    {
        "name": a_str(required=True, requires_replace=True),
        "size_gb": a_num(optional=True),
    }
)


@define(frozen=True)
class DemoConfig:
    name: str | None = None
    size_gb: int | None = None


@define(frozen=True)
class DemoState:
    name: str | None = None
    size_gb: int | None = None


class DemoResource(BaseResource[Any, DemoState, DemoConfig]):
    config_class = DemoConfig
    state_class = DemoState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return RESOURCE_SCHEMA

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, None]:
        return base_plan, None

    async def _update(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, None]:
        return base_plan, None

    async def read(self, ctx: ResourceContext) -> DemoState | None:
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


class ShrinkRequiresReplaceResource(DemoResource):
    """A resource whose replacement depends on the values, not on the mere fact of change."""

    async def _update(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, None]:
        if ctx.config.size_gb is not None and ctx.state.size_gb is not None:  # type: ignore[union-attr]
            if ctx.config.size_gb < ctx.state.size_gb:  # type: ignore[union-attr]
                ctx.require_replace("size_gb")
        return base_plan, None


def _request(
    config: dict[str, Any],
    prior_state: dict[str, Any] | None = None,
) -> pb.PlanResourceChange.Request:
    request = pb.PlanResourceChange.Request(
        type_name="demo",
        config=marshal(config, schema=RESOURCE_SCHEMA.block),
        proposed_new_state=marshal(config, schema=RESOURCE_SCHEMA.block),
        prior_private=b"",
    )
    if prior_state is not None:
        request.prior_state.CopyFrom(marshal(prior_state, schema=RESOURCE_SCHEMA.block))
    return request


def _patched(resource_class: Any) -> Any:
    provider = MagicMock()
    provider.metadata.capabilities = {}
    return patch(
        f"{MODULE}.hub.get_component",
        side_effect=lambda kind, name: resource_class if kind == "resource" else provider,
    )


def _replaced_attribute_names(response: pb.PlanResourceChange.Response) -> list[str]:
    return [step.attribute_name for path in response.requires_replace for step in path.steps]


class TestAttributeChanged:
    """Tests for the prior-vs-planned comparison used by requires_replace."""

    def test_identical_values_are_not_a_change(self) -> None:
        prior = CtyValue(CtyString(), "a")
        planned = CtyValue(CtyString(), "a")

        assert _attribute_changed(prior, planned) is False

    def test_differing_values_are_a_change(self) -> None:
        assert _attribute_changed(CtyValue(CtyString(), "a"), CtyValue(CtyString(), "b")) is True

    def test_unknown_planned_value_is_a_change(self) -> None:
        """An unknown may resolve to the prior value, but the plan must be decided now."""
        prior = CtyValue(CtyString(), "a")

        assert _attribute_changed(prior, CtyValue.unknown(CtyString())) is True

    def test_both_null_is_not_a_change(self) -> None:
        assert _attribute_changed(CtyValue.null(CtyString()), CtyValue.null(CtyString())) is False

    def test_null_prior_and_known_planned_is_a_change(self) -> None:
        assert _attribute_changed(CtyValue.null(CtyNumber()), CtyValue(CtyNumber(), 4)) is True

    def test_native_values_compare_without_cty_wrappers(self) -> None:
        assert _attribute_changed("a", "b") is True
        assert _attribute_changed("a", "a") is False


class TestCollectRequiresReplacePaths:
    """Tests for _collect_requires_replace_paths' own contract."""

    def test_no_paths_without_prior_state(self) -> None:
        """A resource being created cannot be replaced."""
        planned = RESOURCE_SCHEMA.block.to_cty_type().validate({"name": "b", "size_gb": 1})

        paths = _collect_requires_replace_paths(RESOURCE_SCHEMA, None, planned, ["name"], "demo")

        assert paths == []

    def test_no_paths_when_prior_state_is_null(self) -> None:
        prior = CtyValue.null(RESOURCE_SCHEMA.block.to_cty_type())
        planned = RESOURCE_SCHEMA.block.to_cty_type().validate({"name": "b", "size_gb": 1})

        paths = _collect_requires_replace_paths(RESOURCE_SCHEMA, prior, planned, ["name"], "demo")

        assert paths == []

    def test_no_paths_without_planned_state(self) -> None:
        """A resource being destroyed cannot be replaced."""
        prior = RESOURCE_SCHEMA.block.to_cty_type().validate({"name": "a", "size_gb": 1})

        paths = _collect_requires_replace_paths(RESOURCE_SCHEMA, prior, None, ["name"], "demo")

        assert paths == []

    def test_context_and_schema_paths_are_deduplicated(self) -> None:
        prior = RESOURCE_SCHEMA.block.to_cty_type().validate({"name": "a", "size_gb": 1})
        planned = RESOURCE_SCHEMA.block.to_cty_type().validate({"name": "b", "size_gb": 1})

        paths = _collect_requires_replace_paths(RESOURCE_SCHEMA, prior, planned, ["name", "size_gb"], "demo")

        assert [step.attribute_name for p in paths for step in p.steps] == ["name", "size_gb"]


class TestPlanRequiresReplace:
    """Integration-level coverage through the real handler."""

    @pytest.mark.asyncio
    async def test_emits_requires_replace_when_flagged_attribute_changes(self) -> None:
        request = _request({"name": "b", "size_gb": 1}, prior_state={"name": "a", "size_gb": 1})

        with _patched(DemoResource):
            response = await _plan_resource_change_impl(request, context=None)

        assert not response.diagnostics
        assert _replaced_attribute_names(response) == ["name"]

    @pytest.mark.asyncio
    async def test_omits_requires_replace_when_flagged_attribute_is_unchanged(self) -> None:
        request = _request({"name": "a", "size_gb": 2}, prior_state={"name": "a", "size_gb": 1})

        with _patched(DemoResource):
            response = await _plan_resource_change_impl(request, context=None)

        assert not response.diagnostics
        assert list(response.requires_replace) == []

    @pytest.mark.asyncio
    async def test_omits_requires_replace_on_create(self) -> None:
        """Terraform rejects requires_replace paths on a resource that has no prior state."""
        request = _request({"name": "a", "size_gb": 1})

        with _patched(DemoResource):
            response = await _plan_resource_change_impl(request, context=None)

        assert not response.diagnostics
        assert list(response.requires_replace) == []

    @pytest.mark.asyncio
    async def test_emits_requires_replace_from_context_call(self) -> None:
        request = _request({"name": "a", "size_gb": 1}, prior_state={"name": "a", "size_gb": 5})

        with _patched(ShrinkRequiresReplaceResource):
            response = await _plan_resource_change_impl(request, context=None)

        assert not response.diagnostics
        assert _replaced_attribute_names(response) == ["size_gb"]

    @pytest.mark.asyncio
    async def test_omits_context_path_when_condition_does_not_hold(self) -> None:
        request = _request({"name": "a", "size_gb": 9}, prior_state={"name": "a", "size_gb": 5})

        with _patched(ShrinkRequiresReplaceResource):
            response = await _plan_resource_change_impl(request, context=None)

        assert not response.diagnostics
        assert list(response.requires_replace) == []


# 🐍🏗️🔚
