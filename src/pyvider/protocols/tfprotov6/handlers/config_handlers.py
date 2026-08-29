#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform protocol v6.11 configuration RPC handlers.

Each handler here resolves the registered component that owns the request and
calls its hook. The action RPCs live in
:mod:`pyvider.protocols.tfprotov6.handlers.action_handlers` and the state-store
RPCs in :mod:`pyvider.protocols.tfprotov6.handlers.state_store_handlers`; both
are re-exported below so existing import sites keep working.
"""

from __future__ import annotations

from typing import Any

from provide.foundation import logger

from pyvider.conversion import marshal, unmarshal
from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._diagnostics import (
    error_diagnostic,
    unknown_type_diagnostic,
)
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.action_handlers import (
    PlanActionHandler,
    ValidateActionConfigHandler,
    stream_invoke_action,
)
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import (
    ConfigureStateStoreHandler,
    DeleteStateHandler,
    GetStatesHandler,
    LockStateHandler,
    UnlockStateHandler,
    ValidateStateStoreConfigHandler,
    delete_state_bytes,
    list_state_ids,
    read_state_bytes,
    reset_state_stores,
    state_store_chunk_size,
    write_state_bytes,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    cty_to_attrs_instance,
    get_filtered_components,
)
import pyvider.protocols.tfprotov6.protobuf as pb

__all__ = [
    "ConfigureStateStoreHandler",
    "DeleteStateHandler",
    "GenerateResourceConfigHandler",
    "GetStatesHandler",
    "LockStateHandler",
    "PlanActionHandler",
    "UnlockStateHandler",
    "ValidateActionConfigHandler",
    "ValidateListResourceConfigHandler",
    "ValidateStateStoreConfigHandler",
    "delete_state_bytes",
    "list_state_ids",
    "read_state_bytes",
    "reset_state_stores",
    "state_store_chunk_size",
    "stream_invoke_action",
    "write_state_bytes",
]


@rpc_handler("GenerateResourceConfig")
async def GenerateResourceConfigHandler(
    request: pb.GenerateResourceConfig.Request, context: Any
) -> pb.GenerateResourceConfig.Response:
    """Turn a resource's state into a valid configuration via its own hook."""
    resources = get_filtered_components("resource")
    resource_class = resources.get(request.type_name)
    if resource_class is None:
        return pb.GenerateResourceConfig.Response(
            diagnostics=[
                unknown_type_diagnostic("resource", request.type_name, list(resources), "@register_resource")
            ]
        )

    generate = getattr(resource_class, "generate_config", None)
    if generate is None:
        # A duck-typed resource that predates the hook has nothing to say about
        # config generation, and its state is the best answer available.
        return pb.GenerateResourceConfig.Response(config=request.state, diagnostics=[])

    try:
        schema = resource_class.get_schema()
        state_cty = unmarshal(request.state, schema=schema.block) if request.state.ByteSize() else None
        state_value: Any = state_cty
        if resource_class.state_class is not None and state_cty is not None:
            state_value = cty_to_attrs_instance(state_cty, resource_class.state_class)

        generated = await resource_class().generate_config(state_value)
    except Exception as exc:
        logger.error(
            "Resource config generation failed",
            operation="generate_resource_config",
            resource_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
            exc_info=True,
        )
        return pb.GenerateResourceConfig.Response(
            diagnostics=[
                error_diagnostic(
                    f"Could not generate configuration for resource '{request.type_name}'", str(exc)
                )
            ]
        )

    if generated is None:
        # The hook declined to rewrite anything. Forwarding the original wire
        # value avoids a decode/encode round trip that could only lose fidelity.
        return pb.GenerateResourceConfig.Response(config=request.state, diagnostics=[])

    try:
        config = marshal(generated, schema=schema.block)
    except Exception as exc:
        logger.error(
            "Generated resource config could not be encoded",
            operation="generate_resource_config",
            resource_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return pb.GenerateResourceConfig.Response(
            diagnostics=[
                error_diagnostic(
                    f"Generated configuration for resource '{request.type_name}' is not valid",
                    str(exc),
                )
            ]
        )

    logger.debug(
        "Resource config generated",
        operation="generate_resource_config",
        resource_type=request.type_name,
    )
    return pb.GenerateResourceConfig.Response(config=config, diagnostics=[])


@rpc_handler("ValidateListResourceConfig")
async def ValidateListResourceConfigHandler(
    request: pb.ValidateListResourceConfig.Request, context: Any
) -> pb.ValidateListResourceConfig.Response:
    """Validate a list block through the list resource's own hook."""
    registered = get_filtered_components("list_resource")
    if not registered:
        # Matching ListResource: a provider with no list resources is not in
        # error, it simply has nothing to validate against.
        return pb.ValidateListResourceConfig.Response(diagnostics=[])

    list_resource_class = registered.get(request.type_name)
    if list_resource_class is None:
        return pb.ValidateListResourceConfig.Response(
            diagnostics=[
                unknown_type_diagnostic(
                    "list resource", request.type_name, list(registered), "@register_list_resource"
                )
            ]
        )

    try:
        config = decode_config(list_resource_class, request.config)
        errors = await list_resource_class().validate(config)
    except Exception as exc:
        logger.error(
            "List resource configuration validation failed",
            operation="validate_list_resource_config",
            request_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return pb.ValidateListResourceConfig.Response(
            diagnostics=[
                error_diagnostic(f"Invalid configuration for list resource '{request.type_name}'", str(exc))
            ]
        )

    return pb.ValidateListResourceConfig.Response(
        diagnostics=[error_diagnostic(message) for message in errors]
    )


# 🐍🏗️🔚
