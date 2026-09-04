#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""GenerateResourceConfig and ValidateListResourceConfig call provider hooks."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, ClassVar

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.list_resources import BaseListResource, ListResourceContext, ListResult
from pyvider.protocols.tfprotov6.handlers.config_handlers import (
    GenerateResourceConfigHandler,
    ValidateListResourceConfigHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_bool, a_str, s_resource

RESOURCE_TYPE = "hookable_widget"
LIST_TYPE = "hookable_widget_list"


@attrs.define
class WidgetState:
    id: str | None = None
    name: str | None = None
    computed_arn: str | None = None


class HookableWidget(BaseResource[Any, WidgetState, WidgetState]):
    """A resource whose generate_config hook each test dictates."""

    config_class = WidgetState
    state_class = WidgetState

    #: What generate_config() returns; None means "pass the state through".
    generated: ClassVar[Any] = None
    #: Raised by generate_config() when set.
    failure: ClassVar[Exception | None] = None
    #: States the hook was handed.
    seen: ClassVar[list[Any]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "id": a_str(),
                "name": a_str(),
                "computed_arn": a_str(computed=True),
            }
        )

    async def generate_config(self, state: Any) -> Any:
        type(self).seen.append(state)
        if type(self).failure is not None:
            raise type(self).failure
        return type(self).generated

    async def _validate_config(self, config: WidgetState) -> list[str]:  # pragma: no cover - unused
        return []

    async def read(self, ctx: ResourceContext) -> WidgetState | None:  # pragma: no cover - unused
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:  # pragma: no cover - unused
        return None


@attrs.define
class WidgetListConfig:
    region: str | None = None
    include_archived: bool | None = None


class HookableWidgetList(BaseListResource[WidgetListConfig]):
    config_class = WidgetListConfig
    resource_type = RESOURCE_TYPE

    validation_errors: ClassVar[list[str]] = []
    failure: ClassVar[Exception | None] = None
    seen: ClassVar[list[Any]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"region": a_str(), "include_archived": a_bool()})

    async def validate(self, config: WidgetListConfig | None) -> list[str]:
        type(self).seen.append(config)
        if type(self).failure is not None:
            raise type(self).failure
        return list(type(self).validation_errors)

    async def list(
        self, ctx: ListResourceContext[WidgetListConfig]
    ) -> AsyncIterator[ListResult]:  # pragma: no cover - unused
        yield ListResult(identity={"id": "unused"})


@pytest.fixture
def hookable_resource() -> Iterator[type[HookableWidget]]:
    HookableWidget.generated = None
    HookableWidget.failure = None
    HookableWidget.seen = []
    hub.register("resource", RESOURCE_TYPE, HookableWidget)
    yield HookableWidget
    hub.unregister("resource", RESOURCE_TYPE)


@pytest.fixture
def hookable_list() -> Iterator[type[HookableWidgetList]]:
    HookableWidgetList.validation_errors = []
    HookableWidgetList.failure = None
    HookableWidgetList.seen = []
    hub.register("list_resource", LIST_TYPE, HookableWidgetList)
    yield HookableWidgetList
    hub.unregister("list_resource", LIST_TYPE)


def _state() -> pb.DynamicValue:
    return marshal(
        {"id": "w-1", "name": "widget one", "computed_arn": "arn:widget:1"},
        schema=HookableWidget.get_schema().block,
    )


def _errors(diagnostics: Any) -> list[pb.Diagnostic]:
    return [d for d in diagnostics if d.severity == pb.Diagnostic.ERROR]


# --- GenerateResourceConfig -----------------------------------------------


@pytest.mark.asyncio
async def test_hook_receives_the_decoded_state(hookable_resource: type[HookableWidget]) -> None:
    request = pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=_state())

    await GenerateResourceConfigHandler(request, context=None)

    seen = hookable_resource.seen[0]
    assert isinstance(seen, WidgetState)
    assert seen.id == "w-1"
    assert seen.computed_arn == "arn:widget:1"


@pytest.mark.asyncio
async def test_a_hook_returning_none_reduces_the_state_to_a_configuration(
    hookable_resource: type[HookableWidget],
) -> None:
    """State stands in for the answer, minus what a configuration cannot set.

    This used to forward the state bytes verbatim, which put computed-only
    attributes into the generated file; Terraform then rejects it on the next
    plan. Terraform's own fallback for a provider without this capability does
    the same reduction (node_resource_plan_instance.go:1192-1208), and pyvider
    advertises the capability unconditionally so that fallback never runs.
    """
    from pyvider.conversion import unmarshal

    request = pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=_state())

    response = await GenerateResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []
    config = unmarshal(response.config, schema=hookable_resource.get_schema().block)
    assert config["id"].value == "w-1", "a configurable attribute was dropped"
    assert config["computed_arn"].is_null, "a computed-only attribute reached the configuration"


@pytest.mark.asyncio
async def test_a_generated_config_replaces_the_state(hookable_resource: type[HookableWidget]) -> None:
    hookable_resource.generated = WidgetState(id="w-1", name="widget one", computed_arn=None)
    request = pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=_state())

    response = await GenerateResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []
    decoded = unmarshal(response.config, schema=HookableWidget.get_schema().block)
    assert decoded["name"].value == "widget one"
    assert decoded["computed_arn"].is_null


@pytest.mark.asyncio
async def test_a_failing_hook_is_reported(hookable_resource: type[HookableWidget]) -> None:
    hookable_resource.failure = RuntimeError("cannot derive config")
    request = pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=_state())

    response = await GenerateResourceConfigHandler(request, context=None)

    assert "cannot derive config" in _errors(response.diagnostics)[0].detail


@pytest.mark.asyncio
async def test_an_unencodable_generated_config_is_reported(
    hookable_resource: type[HookableWidget],
) -> None:
    hookable_resource.generated = {"id": object()}
    request = pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=_state())

    response = await GenerateResourceConfigHandler(request, context=None)

    assert "is not valid" in _errors(response.diagnostics)[0].summary


@pytest.mark.asyncio
async def test_an_unregistered_resource_is_reported(hookable_resource: type[HookableWidget]) -> None:
    request = pb.GenerateResourceConfig.Request(type_name="nope", state=_state())

    response = await GenerateResourceConfigHandler(request, context=None)

    assert _errors(response.diagnostics)[0].summary == "Unknown resource type 'nope'"
    assert RESOURCE_TYPE in response.diagnostics[0].detail


@pytest.mark.asyncio
async def test_a_resource_without_the_hook_passes_the_state_through() -> None:
    class LegacyWidget:
        """A duck-typed resource registered before the hook existed."""

        state_class = None
        config_class = None

        @classmethod
        def get_schema(cls) -> PvsSchema:
            return s_resource(attributes={"id": a_str()})

    hub.register("resource", "legacy_widget", LegacyWidget)
    state = marshal({"id": "w-1"}, schema=LegacyWidget.get_schema().block)
    request = pb.GenerateResourceConfig.Request(type_name="legacy_widget", state=state)

    try:
        response = await GenerateResourceConfigHandler(request, context=None)
    finally:
        hub.unregister("resource", "legacy_widget")

    assert response.config == state
    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_a_resource_without_a_state_class_gets_the_raw_cty_value() -> None:
    """A resource may skip state_class and read the CtyValue directly."""
    seen: list[Any] = []

    class RawStateWidget:
        state_class = None
        config_class = None

        @classmethod
        def get_schema(cls) -> PvsSchema:
            return s_resource(attributes={"id": a_str()})

        async def generate_config(self, state: Any) -> Any:
            seen.append(state)
            return {"id": "rewritten"}

    hub.register("resource", "raw_state_widget", RawStateWidget)
    state = marshal({"id": "w-1"}, schema=RawStateWidget.get_schema().block)
    request = pb.GenerateResourceConfig.Request(type_name="raw_state_widget", state=state)

    try:
        response = await GenerateResourceConfigHandler(request, context=None)
    finally:
        hub.unregister("resource", "raw_state_widget")

    assert list(response.diagnostics) == []
    # No state_class means no attrs conversion: the hook sees the CtyValue.
    assert seen[0]["id"].value == "w-1"
    decoded = unmarshal(response.config, schema=RawStateWidget.get_schema().block)
    assert decoded["id"].value == "rewritten"


@pytest.mark.asyncio
async def test_the_base_hook_defaults_to_passing_the_state_through() -> None:
    assert await BaseResource.generate_config(object(), None) is None  # type: ignore[arg-type]


# --- ValidateListResourceConfig -------------------------------------------


@pytest.mark.asyncio
async def test_list_validation_receives_the_decoded_config(
    hookable_list: type[HookableWidgetList],
) -> None:
    config = marshal(
        {"region": "us-east-1", "include_archived": False}, schema=HookableWidgetList.get_schema().block
    )
    request = pb.ValidateListResourceConfig.Request(type_name=LIST_TYPE, config=config)

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []
    seen = hookable_list.seen[0]
    assert isinstance(seen, WidgetListConfig)
    assert seen.region == "us-east-1"


@pytest.mark.asyncio
async def test_list_validation_surfaces_hook_errors(hookable_list: type[HookableWidgetList]) -> None:
    hookable_list.validation_errors = ["region is required"]
    request = pb.ValidateListResourceConfig.Request(type_name=LIST_TYPE)

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert [d.summary for d in response.diagnostics] == ["region is required"]


@pytest.mark.asyncio
async def test_list_validation_reports_a_failing_hook(
    hookable_list: type[HookableWidgetList],
) -> None:
    hookable_list.failure = RuntimeError("validator blew up")
    request = pb.ValidateListResourceConfig.Request(type_name=LIST_TYPE)

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert "validator blew up" in _errors(response.diagnostics)[0].detail


@pytest.mark.asyncio
async def test_list_validation_reports_an_unknown_type(
    hookable_list: type[HookableWidgetList],
) -> None:
    request = pb.ValidateListResourceConfig.Request(type_name="nope")

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert _errors(response.diagnostics)[0].summary == "Unknown list resource type 'nope'"


@pytest.mark.asyncio
async def test_list_validation_accepts_when_no_list_resources_exist() -> None:
    request = pb.ValidateListResourceConfig.Request(type_name="anything")

    response = await ValidateListResourceConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


# 🐍🏗️🔚
