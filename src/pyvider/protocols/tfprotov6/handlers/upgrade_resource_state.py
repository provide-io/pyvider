#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import json
from typing import Any

from provide.foundation import logger

from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import (
    Diagnostic,
    DynamicValue,
)


@rpc_handler("UpgradeResourceState")
async def UpgradeResourceStateHandler(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Handle the UpgradeResourceState RPC."""
    return await _upgrade_resource_state_impl(request, context)


def _error_response(summary: str, detail: str) -> pb.UpgradeResourceState.Response:
    """Build a single-ERROR-diagnostic response.

    Returning no `upgraded_state` alongside the diagnostic is deliberate: this
    RPC decides what gets written back to state, so a failure must leave the
    stored state alone rather than replace it with something unusable.
    """
    return pb.UpgradeResourceState.Response(
        diagnostics=[Diagnostic(severity=Diagnostic.ERROR, summary=summary, detail=detail)]
    )


def _upgraded_state_value(
    upgraded: dict[str, Any], schema: Any, type_name: str, from_version: int
) -> DynamicValue:
    """Validate the hook's result against the current schema and encode it.

    The validation is the point. An upgrade hook returns plain Python, and
    nothing else checks it before Terraform writes it to state, so a hook that
    drops a required attribute or changes a type would persist state the
    provider cannot read back -- the very failure the version bump exists to
    prevent.
    """
    try:
        state_cty = schema.block.to_cty_type().validate(upgraded)
    except Exception as exc:
        raise _UpgradeRejected(
            f"Upgraded state for '{type_name}' does not match schema version {schema.version}",
            f"upgrade_state() migrated state from version {from_version} to version "
            f"{schema.version}, but the result is not valid against the current schema:\n\n"
            f"{exc}\n\n"
            "Nothing was written: storing state the schema rejects would leave the "
            "resource unreadable.\n\n"
            "Suggestion: check that upgrade_state() returns every attribute the "
            "current schema requires, with the types it declares.",
        ) from exc

    return DynamicValue(msgpack=marshal(state_cty, schema=schema.block).msgpack)


class _UpgradeRejected(Exception):
    """An upgrade result the current schema will not accept."""

    def __init__(self, summary: str, detail: str) -> None:
        super().__init__(summary)
        self.summary = summary
        self.detail = detail


async def _upgrade_resource_state_impl(
    request: pb.UpgradeResourceState.Request, context: Any
) -> pb.UpgradeResourceState.Response:
    """Upgrade stored state to the resource's current schema version.

    Terraform records a resource's schema version in state and calls this
    whenever it differs from the one the provider now advertises. When the
    versions agree there is nothing to migrate and the stored bytes pass
    through untouched -- which is every call for a resource that has never
    bumped its version, and so must stay exactly as cheap and as lossless as
    the pass-through this replaced.
    """
    logger.debug(
        "Starting resource state upgrade operation",
        operation="upgrade_resource_state",
        resource_type=request.type_name,
        version=request.version,
    )

    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            return _error_response(
                f"Unknown resource type '{request.type_name}'",
                f"Terraform asked to upgrade state for '{request.type_name}', which is "
                "not registered with this provider.\n\n"
                "Suggestion: Ensure the resource is registered using the "
                "@register_resource decorator and that component discovery has "
                "completed successfully.",
            )

        if not (request.raw_state and request.raw_state.json):
            logger.debug(
                "No state to upgrade, returning empty state",
                operation="upgrade_resource_state",
                resource_type=request.type_name,
            )
            return pb.UpgradeResourceState.Response(
                upgraded_state=DynamicValue(json=json.dumps({}).encode("utf-8")), diagnostics=[]
            )

        schema = resource_class.get_schema()

        if request.version == schema.version:
            # The stored bytes are returned verbatim rather than decoded and
            # re-encoded: there is nothing to migrate, and a round trip could
            # only lose something.
            logger.debug(
                "State version matches, passing through",
                operation="upgrade_resource_state",
                resource_type=request.type_name,
                version=request.version,
                state_size=len(request.raw_state.json),
            )
            upgraded_state = DynamicValue(json=request.raw_state.json)
        else:
            logger.info(
                "Upgrading resource state",
                operation="upgrade_resource_state",
                resource_type=request.type_name,
                from_version=request.version,
                to_version=schema.version,
            )
            raw_state = json.loads(request.raw_state.json)
            upgraded = await resource_class.upgrade_state(request.version, raw_state)
            upgraded_state = _upgraded_state_value(upgraded, schema, request.type_name, request.version)

        logger.info(
            "Resource state upgrade completed successfully",
            operation="upgrade_resource_state",
            resource_type=request.type_name,
            from_version=request.version,
            to_version=schema.version,
        )
        return pb.UpgradeResourceState.Response(upgraded_state=upgraded_state, diagnostics=[])

    except _UpgradeRejected as e:
        logger.error(
            "Upgraded state does not match the current schema",
            operation="upgrade_resource_state",
            resource_type=request.type_name,
            from_version=request.version,
            error_message=e.detail,
        )
        return _error_response(e.summary, e.detail)

    except Exception as e:
        logger.error(
            "Resource state upgrade failed",
            operation="upgrade_resource_state",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        return _error_response(
            "State upgrade failed",
            f"Failed to upgrade resource state: {e}\n\n"
            "Suggestion: This may indicate a state format incompatibility.\n\n"
            "Troubleshooting:\n"
            "  1. Check the resource state version matches provider expectations\n"
            "  2. Review provider logs for state parsing errors\n"
            "  3. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG",
        )


# 🐍🏗️🔚
