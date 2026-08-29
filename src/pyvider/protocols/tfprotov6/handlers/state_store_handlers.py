#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform pluggable state-store RPC handlers.

These handlers own no storage of their own. Every read, write, and lock is
delegated to the backend that :mod:`pyvider.state_stores` resolves for the
requested store type, so swapping the durable backend never touches protocol
code.
"""

from __future__ import annotations

from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._diagnostics import error_diagnostic
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.state_stores import (
    BaseStateStore,
    StateLockConflictError,
    StateStoreError,
    default_lock_ttl_seconds,
    state_store_manager,
)


def _backend(type_name: str) -> BaseStateStore:
    """Resolve the backend serving a store type."""
    return state_store_manager.resolve(type_name)


async def read_state_bytes(type_name: str, state_id: str) -> bytes | None:
    """Return the stored payload for a state, or None when it is absent."""
    return await _backend(type_name).read_state(type_name, state_id)


async def write_state_bytes(type_name: str, state_id: str, payload: bytes) -> None:
    """Durably store a state payload."""
    await _backend(type_name).write_state(type_name, state_id, payload)


async def delete_state_bytes(type_name: str, state_id: str) -> None:
    """Remove a state payload."""
    await _backend(type_name).delete_state(type_name, state_id)


async def list_state_ids(type_name: str) -> list[str]:
    """Return every state id held for a store type."""
    return await _backend(type_name).list_states(type_name)


def state_store_chunk_size(type_name: str) -> int:
    """Return the chunk size negotiated for a store type."""
    return state_store_manager.chunk_size(type_name)


def reset_state_stores() -> None:
    """Drop every resolved backend and negotiated chunk size (test support)."""
    state_store_manager.reset()


@rpc_handler("ValidateStateStoreConfig")
async def ValidateStateStoreConfigHandler(
    request: pb.ValidateStateStore.Request, context: Any
) -> pb.ValidateStateStore.Response:
    """Validate a state-store configuration against its backend."""
    try:
        backend = _backend(request.type_name)
        config = decode_config(backend, request.config)
        errors = await backend.validate(config)
    except Exception as exc:
        logger.error(
            "State store configuration validation failed",
            operation="validate_state_store_config",
            state_store_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return pb.ValidateStateStore.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="State store configuration is invalid",
                    detail=str(exc),
                )
            ]
        )

    return pb.ValidateStateStore.Response(diagnostics=[error_diagnostic(message) for message in errors])


@rpc_handler("ConfigureStateStore")
async def ConfigureStateStoreHandler(
    request: pb.ConfigureStateStore.Request, context: Any
) -> pb.ConfigureStateStore.Response:
    """Configure the backend for a store type and report server capabilities."""
    chunk_size = state_store_manager.set_chunk_size(request.type_name, request.capabilities.chunk_size)
    try:
        backend = _backend(request.type_name)
        config = decode_config(backend, request.config)
        await backend.configure(config, chunk_size)
    except Exception as exc:
        logger.error(
            "State store configuration failed",
            operation="configure_state_store",
            state_store_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return pb.ConfigureStateStore.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="State store could not be configured",
                    detail=str(exc),
                )
            ],
            capabilities=pb.StateStoreServerCapabilities(chunk_size=chunk_size),
        )

    logger.debug(
        "State store configured",
        operation="configure_state_store",
        state_store_type=request.type_name,
        backend=type(backend).__name__,
        durable=backend.durable,
        chunk_size=chunk_size,
    )
    return pb.ConfigureStateStore.Response(
        diagnostics=[],
        capabilities=pb.StateStoreServerCapabilities(chunk_size=chunk_size),
    )


@rpc_handler("LockState")
async def LockStateHandler(request: pb.LockState.Request, context: Any) -> pb.LockState.Response:
    """Acquire a lease over a state, refusing when another lease is live."""
    try:
        lock = await _backend(request.type_name).lock_state(
            request.type_name,
            request.state_id,
            request.operation,
            default_lock_ttl_seconds(),
        )
    except StateLockConflictError as conflict:
        logger.warning(
            "State lock request denied; state already locked",
            operation="lock_state",
            state_store_type=request.type_name,
            state_id=request.state_id,
            holder=conflict.existing.holder,
        )
        return pb.LockState.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="State is already locked",
                    detail=str(conflict),
                )
            ]
        )
    except StateStoreError as exc:
        return pb.LockState.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="State lock could not be acquired",
                    detail=str(exc),
                )
            ]
        )

    logger.debug(
        "State lock acquired",
        operation="lock_state",
        state_store_type=request.type_name,
        state_id=request.state_id,
        lock_id=lock.lock_id,
    )
    return pb.LockState.Response(lock_id=lock.lock_id, diagnostics=[])


@rpc_handler("UnlockState")
async def UnlockStateHandler(request: pb.UnlockState.Request, context: Any) -> pb.UnlockState.Response:
    """Release a lease, warning when the supplied lock id does not hold it."""
    released = await _backend(request.type_name).unlock_state(
        request.type_name, request.state_id, request.lock_id
    )
    if released:
        return pb.UnlockState.Response(diagnostics=[])
    return pb.UnlockState.Response(
        diagnostics=[
            pb.Diagnostic(
                severity=pb.Diagnostic.WARNING,
                summary="UnlockState lock not held",
                detail="The provided lock ID does not match an active lock.",
            )
        ]
    )


@rpc_handler("GetStates")
async def GetStatesHandler(request: pb.GetStates.Request, context: Any) -> pb.GetStates.Response:
    """Enumerate the state ids held by a store type."""
    return pb.GetStates.Response(state_id=await list_state_ids(request.type_name), diagnostics=[])


@rpc_handler("DeleteState")
async def DeleteStateHandler(request: pb.DeleteState.Request, context: Any) -> pb.DeleteState.Response:
    """Delete a stored state."""
    try:
        await delete_state_bytes(request.type_name, request.state_id)
    except StateStoreError as exc:
        return pb.DeleteState.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="State could not be deleted",
                    detail=str(exc),
                )
            ]
        )
    return pb.DeleteState.Response(diagnostics=[])


# 🐍🏗️🔚
