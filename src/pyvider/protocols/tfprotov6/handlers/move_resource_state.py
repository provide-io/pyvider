#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from decimal import Decimal
import json
from typing import Any

from provide.foundation import logger

from pyvider.conversion import marshal_identity
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    derive_identity_values,
    null_write_only_attributes,
    resolve_identity_schema,
)
import pyvider.protocols.tfprotov6.protobuf as pb


def _load_state_json(raw: bytes) -> Any:
    """Decode state JSON without losing number precision.

    Terraform's numbers are arbitrary precision: go-cty parses them through
    `ParseNumberVal`, which is backed by a 512-bit big.Float
    (go-cty/cty/json/unmarshal.go:75). Python's `json.loads` turns them into
    binary floats, so a value that arrived exact goes back out rounded --
    encoded as a float64 rather than the string form the codec uses for a
    number it cannot represent exactly. The result is a diff on an attribute
    nobody touched, on the first plan after an upgrade or a move.
    """
    return json.loads(raw, parse_float=Decimal, parse_int=Decimal)


def _set_target_identity(
    response: pb.MoveResourceState.Response,
    resource_class: Any,
    target_schema: Any,
    moved: dict[str, Any],
    target_type_name: str,
) -> None:
    """Give the moved resource the identity its new type derives from state.

    Identity used to be carried only by the same-type pass-through, so a
    resource that declares an identity schema arrived at its new type without
    one, and a later import or list could not tie the object back to it.
    Deriving it here is what apply and read already do, so no hook signature has
    to change to get it.
    """
    identity_schema = resolve_identity_schema(resource_class)
    if identity_schema is None:
        return

    state_value: Any = moved
    if resource_class.state_class is not None:
        state_value = cty_to_attrs_instance(
            target_schema.block.to_cty_type().validate(moved), resource_class.state_class
        )

    identity_values = derive_identity_values(
        resource_class, state_value, target_type_name, "move_resource_state"
    )
    if identity_values is not None:
        response.target_identity.CopyFrom(marshal_identity(identity_values, identity_schema))


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

        source_state = _load_state_json(request.source_state.json or b"{}")
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

        # Terraform rejects a non-null write-only attribute in a moved state
        # (refactoring/cross_provider_move.go:159-176). The source type's state
        # may well have carried one; the target's must not.
        target_schema = resource_class.get_schema()
        null_write_only_attributes(moved, target_schema.block)

        # The moved state is a hook's plain Python and nothing else checks it
        # before Terraform writes it to state. Core rejects a value that does not
        # conform (refactoring/cross_provider_move.go:202-219), but by then the
        # message is about the provider rather than about the hook that produced
        # it. This is what UpgradeResourceState already does with its own hook's
        # output, for the same reason.
        try:
            target_schema.block.to_cty_type().validate(moved)
        except Exception as exc:
            return _refuse(
                response,
                f"Moved state is not valid for {request.target_type_name}",
                f"`move_state` on '{request.target_type_name}' returned a state that does "
                f"not match its own schema:\n\n{exc}\n\n"
                f"Suggestion: the hook must return a value of the *target* resource's "
                f"schema, translated from the source's, not the source state as it stands.",
            )

        _set_target_identity(response, resource_class, target_schema, moved, request.target_type_name)

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
