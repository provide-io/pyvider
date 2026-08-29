#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Action RPC handlers: validate, plan, and invoke provider-defined actions."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from provide.foundation import logger

from pyvider.actions import ActionContext, BaseAction
from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._diagnostics import (
    error_diagnostic,
    unknown_type_diagnostic,
    warning_diagnostic,
)
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import get_filtered_components
import pyvider.protocols.tfprotov6.protobuf as pb


def _unknown_action_diagnostic(action_type: str) -> pb.Diagnostic:
    return unknown_type_diagnostic(
        "action", action_type, get_filtered_components("action"), "@register_action"
    )


def _resolve_action(action_type: str) -> type[BaseAction] | None:
    action_class: type[BaseAction] | None = get_filtered_components("action").get(action_type)
    return action_class


@rpc_handler("ValidateActionConfig")
async def ValidateActionConfigHandler(
    request: pb.ValidateActionConfig.Request, context: Any
) -> pb.ValidateActionConfig.Response:
    """Validate an action's configuration through the action's own hook."""
    action_class = _resolve_action(request.type_name)
    if action_class is None:
        return pb.ValidateActionConfig.Response(diagnostics=[_unknown_action_diagnostic(request.type_name)])

    try:
        config = decode_config(action_class, request.config)
        errors = await action_class().validate(config)
    except Exception as exc:
        logger.error(
            "Action configuration validation failed",
            operation="validate_action_config",
            action_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return pb.ValidateActionConfig.Response(
            diagnostics=[error_diagnostic(f"Invalid configuration for action '{request.type_name}'", str(exc))]
        )

    return pb.ValidateActionConfig.Response(diagnostics=[error_diagnostic(message) for message in errors])


@rpc_handler("PlanAction")
async def PlanActionHandler(request: pb.PlanAction.Request, context: Any) -> pb.PlanAction.Response:
    """Plan an action through the action's own hook."""
    action_class = _resolve_action(request.action_type)
    if action_class is None:
        return pb.PlanAction.Response(diagnostics=[_unknown_action_diagnostic(request.action_type)])

    try:
        config = decode_config(action_class, request.config)
        ctx: ActionContext[Any] = ActionContext(
            action_type=request.action_type,
            config=config,
            deferral_allowed=request.client_capabilities.deferral_allowed,
        )
        plan = await action_class().plan(ctx)
    except Exception as exc:
        logger.error(
            "Action planning failed",
            operation="plan_action",
            action_type=request.action_type,
            error_type=type(exc).__name__,
            error_message=str(exc),
            exc_info=True,
        )
        return pb.PlanAction.Response(
            diagnostics=[error_diagnostic(f"Action '{request.action_type}' could not be planned", str(exc))]
        )

    response = pb.PlanAction.Response(diagnostics=[warning_diagnostic(warning) for warning in plan.warnings])

    if plan.defer is not None:
        if not ctx.deferral_allowed:
            # Terraform rejects a deferral it did not offer to accept, so an
            # action that defers anyway is reported as an error the practitioner
            # can act on rather than a response Terraform will refuse.
            response.diagnostics.append(
                error_diagnostic(
                    f"Action '{request.action_type}' deferred but the client does not allow deferrals",
                    "Terraform did not set deferral_allowed for this request.",
                )
            )
        else:
            # Resolved by name rather than by number so the framework enum and
            # the proto enum cannot silently drift apart.
            reason: Any = pb.Deferred.Reason.Value(plan.defer.name)
            response.deferred.reason = reason

    return response


def _completed(diagnostics: list[pb.Diagnostic] | None = None) -> pb.InvokeAction.Event:
    return pb.InvokeAction.Event(completed=pb.InvokeAction.Event.Completed(diagnostics=diagnostics or []))


async def stream_invoke_action(
    request: pb.InvokeAction.Request, context: Any
) -> AsyncIterator[pb.InvokeAction.Event]:
    """Run an action, forwarding its progress and then a completion event.

    Every path ends with exactly one completed event, including failures:
    Terraform treats the completed event as the end of the action, so omitting
    it on error would leave the operation hanging rather than failing.
    """
    action_class = _resolve_action(request.action_type)
    if action_class is None:
        logger.error(
            "InvokeAction requested an unregistered action type",
            operation="invoke_action",
            action_type=request.action_type,
        )
        yield _completed([_unknown_action_diagnostic(request.action_type)])
        return

    try:
        config = decode_config(action_class, request.config)
        instance = action_class()
    except Exception as exc:
        logger.error(
            "Action configuration could not be prepared",
            operation="invoke_action",
            action_type=request.action_type,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        yield _completed(
            [error_diagnostic(f"Invalid configuration for action '{request.action_type}'", str(exc))]
        )
        return

    ctx: ActionContext[Any] = ActionContext(
        action_type=request.action_type,
        config=config,
        deferral_allowed=request.client_capabilities.deferral_allowed,
    )

    emitted = 0
    try:
        async for progress in instance.invoke(ctx):
            yield pb.InvokeAction.Event(progress=pb.InvokeAction.Event.Progress(message=progress.message))
            emitted += 1
    except Exception as exc:
        logger.error(
            "Action invocation failed",
            operation="invoke_action",
            action_type=request.action_type,
            progress_events=emitted,
            error_type=type(exc).__name__,
            error_message=str(exc),
            exc_info=True,
        )
        yield _completed([error_diagnostic(f"Action '{request.action_type}' failed", str(exc))])
        return

    logger.info(
        "InvokeAction completed",
        operation="invoke_action",
        action_type=request.action_type,
        progress_events=emitted,
    )
    yield _completed()


# 🐍🏗️🔚
