#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Action RPCs delegate to the registered action's hooks."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import pytest

from pyvider.actions import ActionContext, ActionPlan, ActionProgress, DeferralReason
from pyvider.conversion import marshal
from pyvider.handler import ProviderHandler
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.action_handlers import (
    PlanActionHandler,
    ValidateActionConfigHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb

from .conftest import ACTION_TYPE, DemoRebootAction


def _config() -> pb.DynamicValue:
    return marshal({"target": "web-1", "attempts": 3}, schema=DemoRebootAction.get_schema().block)


async def _invoke(
    action_type: str = ACTION_TYPE,
    *,
    config: pb.DynamicValue | None = None,
    deferral_allowed: bool = False,
) -> list[pb.InvokeAction.Event]:
    request = pb.InvokeAction.Request(action_type=action_type)
    request.client_capabilities.deferral_allowed = deferral_allowed
    if config is not None:
        request.config.CopyFrom(config)

    handler = ProviderHandler()
    return [event async for event in handler.InvokeAction(request, context=None)]


def _errors(diagnostics: Any) -> list[pb.Diagnostic]:
    return [d for d in diagnostics if d.severity == pb.Diagnostic.ERROR]


# --- ValidateActionConfig --------------------------------------------------


@pytest.mark.asyncio
async def test_validate_accepts_a_valid_config(demo_action: type[DemoRebootAction]) -> None:
    request = pb.ValidateActionConfig.Request(type_name=ACTION_TYPE, config=_config())

    response = await ValidateActionConfigHandler(request, context=None)

    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_validate_surfaces_hook_errors(demo_action: type[DemoRebootAction]) -> None:
    demo_action.validation_errors = ["target is required", "attempts must be positive"]
    request = pb.ValidateActionConfig.Request(type_name=ACTION_TYPE, config=_config())

    response = await ValidateActionConfigHandler(request, context=None)

    assert [d.summary for d in response.diagnostics] == demo_action.validation_errors
    assert all(d.severity == pb.Diagnostic.ERROR for d in response.diagnostics)


@pytest.mark.asyncio
async def test_validate_reports_an_unregistered_action(demo_action: type[DemoRebootAction]) -> None:
    request = pb.ValidateActionConfig.Request(type_name="nope")

    response = await ValidateActionConfigHandler(request, context=None)

    assert _errors(response.diagnostics)[0].summary == "Unknown action type 'nope'"
    assert ACTION_TYPE in response.diagnostics[0].detail


@pytest.mark.asyncio
async def test_validate_reports_an_undecodable_config(demo_action: type[DemoRebootAction]) -> None:
    request = pb.ValidateActionConfig.Request(type_name=ACTION_TYPE)
    request.config.msgpack = b"\xc1not-msgpack"

    response = await ValidateActionConfigHandler(request, context=None)

    assert "Invalid configuration" in _errors(response.diagnostics)[0].summary


@pytest.mark.asyncio
async def test_validate_reports_a_failing_hook(demo_action: type[DemoRebootAction]) -> None:
    class Exploding(DemoRebootAction):
        async def validate(self, config: Any) -> list[str]:
            raise RuntimeError("validator blew up")

    hub.register("action", ACTION_TYPE, Exploding)
    request = pb.ValidateActionConfig.Request(type_name=ACTION_TYPE, config=_config())

    response = await ValidateActionConfigHandler(request, context=None)

    assert "validator blew up" in _errors(response.diagnostics)[0].detail


# --- PlanAction ------------------------------------------------------------


@pytest.mark.asyncio
async def test_plan_receives_the_decoded_config(demo_action: type[DemoRebootAction]) -> None:
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())

    response = await PlanActionHandler(request, context=None)

    assert list(response.diagnostics) == []
    ctx = demo_action.plan_contexts[0]
    assert ctx.action_type == ACTION_TYPE
    assert ctx.config is not None
    assert ctx.config.target == "web-1"
    assert ctx.config.attempts == 3


@pytest.mark.asyncio
async def test_plan_warnings_become_warning_diagnostics(demo_action: type[DemoRebootAction]) -> None:
    demo_action.planned = ActionPlan(warnings=("host is already rebooting",))
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())

    response = await PlanActionHandler(request, context=None)

    assert len(response.diagnostics) == 1
    assert response.diagnostics[0].severity == pb.Diagnostic.WARNING
    assert response.diagnostics[0].summary == "host is already rebooting"


@pytest.mark.asyncio
async def test_plan_deferral_is_forwarded_when_the_client_allows_it(
    demo_action: type[DemoRebootAction],
) -> None:
    demo_action.planned = ActionPlan(defer=DeferralReason.PROVIDER_CONFIG_UNKNOWN)
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())
    request.client_capabilities.deferral_allowed = True

    response = await PlanActionHandler(request, context=None)

    assert response.HasField("deferred")
    assert response.deferred.reason == pb.Deferred.PROVIDER_CONFIG_UNKNOWN
    assert list(response.diagnostics) == []


@pytest.mark.asyncio
async def test_an_action_may_only_defer_for_an_unknown_provider_config(
    demo_action: type[DemoRebootAction],
) -> None:
    """Terraform accepts exactly one reason from PlanAction.

    "An action can only be deferred due to an unknown provider configuration"
    (internal/plugin6/grpc_provider.go:1941-1958). Any other reason is refused
    there, so it is reported here, where the action that chose it can be named.
    """
    demo_action.planned = ActionPlan(defer=DeferralReason.ABSENT_PREREQ)
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())
    request.client_capabilities.deferral_allowed = True

    response = await PlanActionHandler(request, context=None)

    assert not response.HasField("deferred"), "a reason Terraform refuses was sent anyway"
    detail = " ".join(d.summary + " " + d.detail for d in response.diagnostics)
    assert "ABSENT_PREREQ" in detail
    assert "PROVIDER_CONFIG_UNKNOWN" in detail, "the diagnostic does not say what to use instead"


@pytest.mark.asyncio
async def test_plan_deferral_without_client_support_is_an_error(
    demo_action: type[DemoRebootAction],
) -> None:
    demo_action.planned = ActionPlan(defer=DeferralReason.RESOURCE_CONFIG_UNKNOWN)
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())
    request.client_capabilities.deferral_allowed = False

    response = await PlanActionHandler(request, context=None)

    assert not response.HasField("deferred")
    assert "does not allow deferrals" in _errors(response.diagnostics)[0].summary


@pytest.mark.asyncio
async def test_plan_context_reports_client_deferral_support(
    demo_action: type[DemoRebootAction],
) -> None:
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())
    request.client_capabilities.deferral_allowed = True

    await PlanActionHandler(request, context=None)

    assert demo_action.plan_contexts[0].deferral_allowed is True


@pytest.mark.asyncio
async def test_plan_reports_an_unregistered_action(demo_action: type[DemoRebootAction]) -> None:
    request = pb.PlanAction.Request(action_type="nope")

    response = await PlanActionHandler(request, context=None)

    assert _errors(response.diagnostics)[0].summary == "Unknown action type 'nope'"


@pytest.mark.asyncio
async def test_plan_reports_a_failing_hook(demo_action: type[DemoRebootAction]) -> None:
    class Exploding(DemoRebootAction):
        async def plan(self, ctx: ActionContext[Any]) -> ActionPlan:
            raise RuntimeError("planner blew up")

    hub.register("action", ACTION_TYPE, Exploding)
    request = pb.PlanAction.Request(action_type=ACTION_TYPE, config=_config())

    response = await PlanActionHandler(request, context=None)

    assert "planner blew up" in _errors(response.diagnostics)[0].detail


# --- InvokeAction ----------------------------------------------------------


@pytest.mark.asyncio
async def test_invoke_streams_progress_then_completes(demo_action: type[DemoRebootAction]) -> None:
    demo_action.progress = ["draining", "rebooting", "healthy"]

    events = await _invoke(config=_config())

    assert [event.WhichOneof("type") for event in events] == [
        "progress",
        "progress",
        "progress",
        "completed",
    ]
    assert [event.progress.message for event in events[:3]] == demo_action.progress
    assert list(events[-1].completed.diagnostics) == []


@pytest.mark.asyncio
async def test_invoke_completes_even_with_no_progress(demo_action: type[DemoRebootAction]) -> None:
    events = await _invoke(config=_config())

    assert len(events) == 1
    assert events[0].WhichOneof("type") == "completed"
    assert list(events[0].completed.diagnostics) == []


@pytest.mark.asyncio
async def test_invoke_receives_the_decoded_config(demo_action: type[DemoRebootAction]) -> None:
    await _invoke(config=_config(), deferral_allowed=True)

    ctx = demo_action.invoke_contexts[0]
    assert ctx.config is not None
    assert ctx.config.target == "web-1"
    assert ctx.deferral_allowed is True


@pytest.mark.asyncio
async def test_invoke_reports_a_mid_stream_failure_after_partial_progress(
    demo_action: type[DemoRebootAction],
) -> None:
    class Exploding(DemoRebootAction):
        async def invoke(self, ctx: ActionContext[Any]) -> AsyncIterator[ActionProgress]:
            yield ActionProgress(message="draining")
            raise RuntimeError("host stopped responding")

    hub.register("action", ACTION_TYPE, Exploding)
    events = await _invoke(config=_config())

    assert [event.WhichOneof("type") for event in events] == ["progress", "completed"]
    diagnostics = _errors(events[-1].completed.diagnostics)
    assert "host stopped responding" in diagnostics[0].detail


@pytest.mark.asyncio
async def test_invoke_reports_an_undecodable_config(demo_action: type[DemoRebootAction]) -> None:
    request = pb.InvokeAction.Request(action_type=ACTION_TYPE)
    request.config.msgpack = b"\xc1not-msgpack"

    handler = ProviderHandler()
    events = [event async for event in handler.InvokeAction(request, context=None)]

    assert len(events) == 1
    assert "Invalid configuration" in _errors(events[0].completed.diagnostics)[0].summary


@pytest.mark.asyncio
async def test_invoke_reports_an_unregistered_action(demo_action: type[DemoRebootAction]) -> None:
    events = await _invoke("nope")

    assert len(events) == 1
    assert _errors(events[0].completed.diagnostics)[0].summary == "Unknown action type 'nope'"


# 🐍🏗️🔚
