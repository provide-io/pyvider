#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The state-store backend contract.

A state store is the durable side of Terraform's pluggable state RPCs
(``ReadStateBytes`` / ``WriteStateBytes`` / ``LockState`` / ``UnlockState`` /
``GetStates`` / ``DeleteState``). Backends implement this interface; the
protocol handlers never touch storage directly.

Every method takes the store ``type_name`` explicitly rather than binding it at
construction. The RPCs all carry a type name, and keeping it in the signature
means one backend instance can serve several store types without the manager
having to thread identity through a constructor it does not control.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pyvider.schema import PvsSchema
from pyvider.state_stores.defaults import DEFAULT_LOCK_TTL_SECONDS
from pyvider.state_stores.types import StateLock


class BaseStateStore(ABC):
    """Abstract durable backend for Terraform pluggable state stores."""

    #: attrs class describing the store's configuration block, if it has one.
    config_class: type | None = None

    #: Whether state written to this backend survives the provider process.
    #: The manager surfaces this so a non-durable backend cannot be mistaken
    #: for a production one in logs or diagnostics.
    durable: bool = True

    @classmethod
    def get_schema(cls) -> PvsSchema | None:
        """Return the store's configuration schema, or None if it takes none."""
        return None

    async def validate(self, config: Any) -> list[str]:
        """Validate backend configuration.

        Returns a list of human-readable error messages; empty means valid.
        The default accepts any configuration, which is correct for backends
        that have no configuration to reject.
        """
        return []

    async def configure(self, config: Any, chunk_size: int) -> None:
        """Apply backend configuration before any state operation runs.

        ``chunk_size`` is the value negotiated with Terraform, already
        normalized by the manager.
        """
        return

    @abstractmethod
    async def read_state(self, type_name: str, state_id: str) -> bytes | None:
        """Return the stored payload, or None when the state does not exist."""

    @abstractmethod
    async def write_state(self, type_name: str, state_id: str, payload: bytes) -> None:
        """Durably store a payload, replacing any previous value atomically."""

    @abstractmethod
    async def delete_state(self, type_name: str, state_id: str) -> None:
        """Remove a state. Deleting a state that does not exist is a no-op."""

    @abstractmethod
    async def list_states(self, type_name: str) -> list[str]:
        """Return every state id held for a store type."""

    @abstractmethod
    async def lock_state(
        self,
        type_name: str,
        state_id: str,
        operation: str = "",
        ttl_seconds: float = DEFAULT_LOCK_TTL_SECONDS,
    ) -> StateLock:
        """Atomically acquire a lease over a state.

        Raises:
            StateLockConflictError: another live lease already holds the state.
        """

    @abstractmethod
    async def unlock_state(self, type_name: str, state_id: str, lock_id: str) -> bool:
        """Release a lease.

        Returns True when ``lock_id`` matched the live lease and it was
        released, False when no such lease was held.
        """

    @abstractmethod
    async def get_lock(self, type_name: str, state_id: str) -> StateLock | None:
        """Return the live lease over a state, or None when unlocked."""


# 🐍🏗️🔚
