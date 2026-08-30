#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Resolution and lifecycle for state-store backends.

The protocol handlers know a store only by its Terraform ``type_name``. This
module turns that name into a live backend instance, remembers the chunk size
negotiated for it, and keeps one instance per store type so a lock taken during
``LockState`` is visible to the ``UnlockState`` that follows.
"""

from __future__ import annotations

from collections.abc import Callable
import os
import threading
from typing import Any

from provide.foundation import logger

from pyvider.state_stores.base import BaseStateStore
from pyvider.state_stores.defaults import (
    BACKEND_FILESYSTEM,
    BACKEND_MEMORY,
    DEFAULT_BACKEND,
    DEFAULT_LOCK_TTL_SECONDS,
    DEFAULT_STATE_STORE_CHUNK_SIZE,
    ENV_BACKEND,
    ENV_LOCK_TTL,
    ENV_PATH,
    MAX_STATE_STORE_CHUNK_SIZE,
)
from pyvider.state_stores.filesystem import FileSystemStateStore
from pyvider.state_stores.memory import InMemoryStateStore
from pyvider.state_stores.types import StateStoreConfigurationError

BackendFactory = Callable[[], BaseStateStore]

_BUILTIN_BACKENDS: dict[str, BackendFactory] = {
    BACKEND_MEMORY: InMemoryStateStore,
    BACKEND_FILESYSTEM: FileSystemStateStore,
}


def default_backend_name() -> str:
    """Choose the backend used for store types with no explicit registration.

    An explicit ``PYVIDER_STATE_STORE_BACKEND`` wins. Otherwise, setting
    ``PYVIDER_STATE_STORE_PATH`` is read as intent to use durable storage --
    naming a directory and still getting an in-memory store would be a silent
    trap. With neither set the non-durable backend is used, which keeps unit
    tests and local runs from writing to disk.
    """
    configured = os.environ.get(ENV_BACKEND, "").strip().lower()
    if configured:
        return configured
    if os.environ.get(ENV_PATH, "").strip():
        return BACKEND_FILESYSTEM
    return DEFAULT_BACKEND


def default_lock_ttl_seconds() -> float:
    """Lease duration applied when a caller does not specify one."""
    raw = os.environ.get(ENV_LOCK_TTL, "").strip()
    if not raw:
        return DEFAULT_LOCK_TTL_SECONDS
    try:
        value = float(raw)
    except ValueError:
        logger.warning(
            "Ignoring non-numeric state lock TTL override",
            operation="state_store_config",
            env_var=ENV_LOCK_TTL,
            value=raw,
        )
        return DEFAULT_LOCK_TTL_SECONDS
    return value if value > 0 else DEFAULT_LOCK_TTL_SECONDS


def normalize_chunk_size(chunk_size: int) -> int:
    """Clamp a client-supplied chunk size to a value Core will accept.

    The upper bound matters as much as the lower one. Core checks the size a
    provider answers with against its own maximum and fails configuration if it
    is exceeded, so echoing back an oversized proposal turns a client's mistake
    into this provider's error.
    """
    if chunk_size <= 0:
        return DEFAULT_STATE_STORE_CHUNK_SIZE
    return min(chunk_size, MAX_STATE_STORE_CHUNK_SIZE)


class StateStoreManager:
    """Owns the live backend instance for every state-store type."""

    def __init__(self) -> None:
        self._mutex = threading.Lock()
        self._instances: dict[str, BaseStateStore] = {}
        self._chunk_sizes: dict[str, int] = {}
        self._override_factory: BackendFactory | None = None

    # ------------------------------------------------------------------
    # Backend resolution
    # ------------------------------------------------------------------

    def resolve(self, type_name: str) -> BaseStateStore:
        """Return the backend serving ``type_name``, creating it on first use."""
        with self._mutex:
            existing = self._instances.get(type_name)
            if existing is not None:
                return existing

        # Instantiation happens outside the mutex so that a provider-supplied
        # constructor cannot deadlock the manager, then the result is published
        # under the mutex with a double-check.
        instance = self._build_backend(type_name)
        with self._mutex:
            return self._instances.setdefault(type_name, instance)

    def register_instance(self, type_name: str, backend: BaseStateStore) -> None:
        """Bind an already-constructed backend to a store type."""
        with self._mutex:
            self._instances[type_name] = backend

    def set_default_backend_factory(self, factory: BackendFactory | None) -> None:
        """Override how unregistered store types get their backend."""
        with self._mutex:
            self._override_factory = factory

    def _build_backend(self, type_name: str) -> BaseStateStore:
        registered = self._registered_class(type_name)
        if registered is not None:
            return self._instantiate(registered, type_name)

        with self._mutex:
            override = self._override_factory
        if override is not None:
            return override()

        name = default_backend_name()
        factory = _BUILTIN_BACKENDS.get(name)
        if factory is None:
            raise StateStoreConfigurationError(
                f"Unknown state store backend '{name}'. "
                f"Valid values for {ENV_BACKEND} are: {', '.join(sorted(_BUILTIN_BACKENDS))}."
            )
        backend = factory()
        if not backend.durable:
            logger.debug(
                "Using non-durable state store backend",
                operation="state_store_resolve",
                state_store_type=type_name,
                backend=name,
            )
        return backend

    @staticmethod
    def _registered_class(type_name: str) -> type[BaseStateStore] | None:
        from pyvider.hub import hub

        component = hub.get_component("state_store", type_name)
        if component is None:
            return None
        if not (isinstance(component, type) and issubclass(component, BaseStateStore)):
            raise StateStoreConfigurationError(
                f"Registered state store '{type_name}' is not a BaseStateStore subclass."
            )
        return component

    @staticmethod
    def _instantiate(store_cls: type[BaseStateStore], type_name: str) -> BaseStateStore:
        try:
            return store_cls()
        except Exception as exc:
            raise StateStoreConfigurationError(
                f"Failed to instantiate state store '{type_name}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Chunk-size negotiation
    # ------------------------------------------------------------------

    def set_chunk_size(self, type_name: str, chunk_size: int) -> int:
        """Record the negotiated chunk size and return the normalized value."""
        normalized = normalize_chunk_size(chunk_size)
        with self._mutex:
            self._chunk_sizes[type_name] = normalized
        return normalized

    def chunk_size(self, type_name: str) -> int:
        """Return the chunk size negotiated for a store type."""
        with self._mutex:
            return self._chunk_sizes.get(type_name, DEFAULT_STATE_STORE_CHUNK_SIZE)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Drop every cached backend, chunk size, and override.

        In-memory backends are cleared explicitly so a test that holds a
        reference to one still sees it emptied.
        """
        with self._mutex:
            instances = list(self._instances.values())
            self._instances.clear()
            self._chunk_sizes.clear()
            self._override_factory = None
        for instance in instances:
            clear = getattr(instance, "clear", None)
            if callable(clear):
                clear()

    def describe(self) -> dict[str, Any]:
        """Summarize resolved backends. Used by diagnostics and tests."""
        with self._mutex:
            return {
                type_name: {
                    "backend": type(backend).__name__,
                    "durable": backend.durable,
                    "chunk_size": self._chunk_sizes.get(type_name, DEFAULT_STATE_STORE_CHUNK_SIZE),
                }
                for type_name, backend in self._instances.items()
            }


#: Process-wide manager used by the protocol handlers.
state_store_manager = StateStoreManager()

__all__ = [
    "DEFAULT_LOCK_TTL_SECONDS",
    "BackendFactory",
    "StateStoreManager",
    "default_backend_name",
    "default_lock_ttl_seconds",
    "normalize_chunk_size",
    "state_store_manager",
]

# 🐍🏗️🔚
