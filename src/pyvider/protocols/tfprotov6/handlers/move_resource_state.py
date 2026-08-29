#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import json
from typing import Any

from provide.foundation import logger

from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@rpc_handler("MoveResourceState")
async def MoveResourceStateHandler(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    """Handle move resource state request."""
    return await _move_resource_state_impl(request, context)


def _refuse(
    response: pb.MoveResourceState.Response, summary: str, detail: str
) -> pb.MoveResourceState.Response:
    """Refuse the move, carrying nothing of the source into the response.

    Terraform reads target_state and target_private whether or not diagnostics
    are present, so a refusal that leaves them populated is not a refusal.
    """
    response.diagnostics.append(pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=summary, detail=detail))
    return response


def _pass_through(
    request: pb.MoveResourceState.Request, response: pb.MoveResourceState.Response
) -> pb.MoveResourceState.Response:
    """A move that changed only the provider address, not the resource type.

    The state was written by this same type against this same schema, so it needs
    no translation and everything recorded alongside it stays attached.
    """
    response.target_state.CopyFrom(pb.DynamicValue(json=request.source_state.json or b"{}"))
    response.target_private = request.source_private
    response.target_identity.CopyFrom(
        pb.ResourceIdentityData(identity_data=pb.DynamicValue(json=request.source_identity.json or b"{}"))
    )
    return response


async def _move_resource_state_impl(
    request: pb.MoveResourceState.Request, context: Any
) -> pb.MoveResourceState.Response:
    """
    Decide whether the target resource accepts a resource moved from elsewhere.

    Terraform asks the *target* provider this question, and the answer belongs to
    the target resource. This used to answer yes for every pair and copy
    `source_state.json` straight into `target_state` with empty diagnostics -- so
    a `moved` block between two unrelated types wrote one type's state into the
    other's slot and reported success. Nothing downstream re-validates a moved
    state against the target schema, so the practitioner met it on the next plan
    as an unexplained diff, or on the next apply as a failure inside a resource
    they had not touched.

    terraform-plugin-framework draws the same line: a resource that implements no
    `MoveState` refuses, and one that does matches on the source provider address
    and type name and refuses anything it does not recognise.

    Three outcomes:

    * the type name did not change -- only the provider address did -- so the
      state needs no translation and passes through whole;
    * the target resource declares `move_state` and accepts this source, so what
      it returns is the target state;
    * anything else is refused with a diagnostic naming both types.
    """
    response = pb.MoveResourceState.Response()

    logger.debug(
        "MoveResourceState requested",
        operation="move_resource_state",
        source_type_name=request.source_type_name,
        target_type_name=request.target_type_name,
        source_state_has_json=bool(request.source_state.json),
    )

    try:
        if request.source_type_name == request.target_type_name:
            logger.info(
                "MoveResourceState completed (same type, state passed through)",
                operation="move_resource_state",
                target_type_name=request.target_type_name,
            )
            return _pass_through(request, response)

        resource_class = hub.get_component("resource", request.target_type_name)
        if not resource_class:
            logger.info(
                "Move target is not a registered resource type",
                operation="move_resource_state",
                source_type_name=request.source_type_name,
                target_type_name=request.target_type_name,
            )
            return _refuse(
                response,
                f"Cannot move to {request.target_type_name}",
                f"The resource type '{request.target_type_name}' is not registered with this "
                f"provider, so it cannot accept a resource moved from "
                f"'{request.source_type_name}'.\n\n"
                f"Suggestion: check the target address in the `moved` block, and run "
                f"'pyvider components list' to see what was registered.",
            )

        check_test_only_access(resource_class, request.target_type_name, "resource")

        move_state = getattr(resource_class(), "move_state", None)
        if move_state is None:
            # A resource that cannot be moved into is a normal thing to be, so this
            # reports the resource rather than the framework.
            logger.info(
                "Resource does not implement move_state",
                operation="move_resource_state",
                source_type_name=request.source_type_name,
                target_type_name=request.target_type_name,
            )
            return _refuse(
                response,
                f"{request.target_type_name} does not support move",
                f"The resource type '{request.target_type_name}' does not implement "
                f"`move_state`, so it cannot accept a resource moved from "
                f"'{request.source_type_name}'. Its state was written against a different "
                f"schema and copying it across would not be a translation.\n\n"
                f"Suggestion: implement `async def move_state(self, source_provider_address, "
                f"source_type_name, source_state, source_schema_version)` on "
                f"'{request.target_type_name}', returning the target state — or remove the "
                f"resource and declare the new one, which recreates the object.",
            )

        source_state = json.loads(request.source_state.json or b"{}")
        moved = await move_state(
            request.source_provider_address,
            request.source_type_name,
            source_state,
            request.source_schema_version,
        )

        if moved is None:
            return _refuse(
                response,
                f"{request.target_type_name} does not support this move",
                f"The resource type '{request.target_type_name}' implements `move_state` but "
                f"declined a move from '{request.source_type_name}' at "
                f"'{request.source_provider_address}'.\n\n"
                f"Suggestion: check the source address in the `moved` block against the "
                f"sources '{request.target_type_name}' accepts.",
            )

        # The source's private state was written by the source's type and means
        # nothing to the target's, so it is not carried across a type change. A
        # resource that wants private state after a move returns it, the same
        # (state, private) shape the plan, apply and import hooks use.
        target_private = b""
        if isinstance(moved, tuple):
            moved, target_private = moved

        response.target_state.CopyFrom(pb.DynamicValue(json=json.dumps(moved).encode("utf-8")))
        response.target_private = target_private

        logger.info(
            "MoveResourceState completed",
            operation="move_resource_state",
            source_type_name=request.source_type_name,
            target_type_name=request.target_type_name,
            target_state_bytes=len(response.target_state.json),
        )
        return response

    except Exception as e:
        logger.error(
            "Resource move failed",
            operation="move_resource_state",
            source_type_name=request.source_type_name,
            target_type_name=request.target_type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        # A partial state is worse than none: reset whatever was written before the
        # failure so a refused move cannot leave Terraform something to record.
        response = pb.MoveResourceState.Response()
        response.diagnostics.append(await create_diagnostic_from_exception(e))
        return response


# 🐍🏗️🔚
