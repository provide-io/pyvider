#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Durable filesystem state-store backend.

State survives provider restarts and is shared by every process pointed at the
same root directory, including one on a network share. Two properties make that
safe:

* **Atomic writes.** A payload is written to a temporary file in the same
  directory, fsynced, then ``os.replace``-d over the target. A reader therefore
  observes either the whole previous payload or the whole new one -- never a
  partially written file, which is what a plain ``open(...).write()`` would
  expose after a crash mid-write.

* **Lease-aware locks.** A lock is a JSON lease stored beside the state and
  mutated only inside a kernel-level file mutex, so "is it locked? then claim
  it" is a single atomic step across processes. The lease carries an absolute
  expiry, so a provider that dies holding a lock does not wedge the state
  permanently.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
from pathlib import Path
import tempfile
import time
from typing import IO, Any
import urllib.parse
import uuid

from provide.foundation import logger

from pyvider.state_stores._filelock import exclusive_file_mutex
from pyvider.state_stores.base import BaseStateStore
from pyvider.state_stores.defaults import (
    DEFAULT_LOCK_TTL_SECONDS,
    DEFAULT_STATE_ROOT_DIRNAME,
    DEFAULT_STATE_SUBDIRNAME,
    ENV_PATH,
    LOCK_FILE_SUFFIX,
    STATE_DIR_MODE,
    STATE_FILE_MODE,
    STATE_FILE_SUFFIX,
    TEMP_FILE_SUFFIX,
)
from pyvider.state_stores.types import StateLock, StateLockConflictError, StateStoreError


def default_state_root() -> Path:
    """Resolve the root directory for filesystem-backed state."""
    configured = os.environ.get(ENV_PATH)
    if configured:
        return Path(configured).expanduser()
    return Path.cwd() / DEFAULT_STATE_ROOT_DIRNAME / DEFAULT_STATE_SUBDIRNAME


def _encode_segment(value: str) -> str:
    """Make a Terraform-supplied name safe to use as a single path segment.

    Type names and state ids arrive over the wire and may contain slashes,
    ``..``, or characters the host filesystem rejects. Percent-encoding keeps
    the mapping reversible (``list_states`` decodes it back) while confining
    every state to exactly one file inside the store root.
    """
    encoded = urllib.parse.quote(value, safe="")
    # `quote` does not escape `.` -- it is in the always-safe set, whatever
    # `safe=""` says -- so `..` came through intact and walked out of the root
    # this function's docstring promises to confine it to.
    #
    # Trailing dots are escaped as well, not only an all-dots segment. Windows
    # drops trailing dots and spaces from a path component, so a name encoding to
    # one ending in a dot names a *different* directory on disk than the encoder
    # meant, and the mapping `list_states` reverses stops being reversible --
    # silently, since nothing errors at encode time. `../..` encodes to `..%2F..`,
    # which Windows resolved against `..%2F`:
    #
    #     [WinError 3] The system cannot find the path specified:
    #     '...\\store\\state\\..%2F\\tmphiaxm3tu.tmp' ->
    #     '...\\store\\state\\..%2F..\\victim.tfstate'
    #
    # `quote` already escapes a space, so only dots can reach the strip; the
    # space is kept in the set because what is being ruled out is the class of
    # characters Windows discards, not the two that happen to occur today.
    # `unquote` reverses the escapes unchanged, so the mapping stays exact.
    kept = encoded.rstrip(". ")
    if len(kept) != len(encoded):
        encoded = kept + "".join(f"%{ord(c):02X}" for c in encoded[len(kept) :])
    return encoded


def _decode_segment(value: str) -> str:
    return urllib.parse.unquote(value)


class FileSystemStateStore(BaseStateStore):
    """Durable state store backed by a directory tree."""

    durable = True

    def __init__(self, root: Path | None = None) -> None:
        self._root = Path(root) if root is not None else default_state_root()

    @property
    def root(self) -> Path:
        """The directory tree holding every state served by this backend."""
        return self._root

    async def validate(self, config: Any) -> list[str]:
        """Reject configurations whose root cannot be used."""
        root = _config_root(config)
        if root is None:
            return []
        candidate, occupied = await asyncio.to_thread(_probe_root, root)
        if occupied:
            return [f"State store path '{candidate}' exists and is not a directory."]
        return []

    async def configure(self, config: Any, chunk_size: int) -> None:
        root = _config_root(config)
        if root is not None:
            self._root = await asyncio.to_thread(_expand_root, root)
        await asyncio.to_thread(self._ensure_root)
        logger.debug(
            "Filesystem state store configured",
            operation="configure_state_store",
            state_store_root=str(self._root),
            chunk_size=chunk_size,
        )

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def _type_dir(self, type_name: str) -> Path:
        return self._root / _encode_segment(type_name)

    def _state_path(self, type_name: str, state_id: str) -> Path:
        return self._type_dir(type_name) / f"{_encode_segment(state_id)}{STATE_FILE_SUFFIX}"

    def _lock_path(self, type_name: str, state_id: str) -> Path:
        return self._type_dir(type_name) / f"{_encode_segment(state_id)}{LOCK_FILE_SUFFIX}"

    def _ensure_root(self) -> None:
        self._root.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            self._root.chmod(STATE_DIR_MODE)

    # ------------------------------------------------------------------
    # State data plane
    # ------------------------------------------------------------------

    async def read_state(self, type_name: str, state_id: str) -> bytes | None:
        return await asyncio.to_thread(self._read_state_sync, type_name, state_id)

    def _read_state_sync(self, type_name: str, state_id: str) -> bytes | None:
        path = self._state_path(type_name, state_id)
        try:
            return path.read_bytes()
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise StateStoreError(f"Failed to read state from '{path}': {exc}") from exc

    async def write_state(self, type_name: str, state_id: str, payload: bytes) -> None:
        await asyncio.to_thread(self._write_state_sync, type_name, state_id, bytes(payload))

    def _write_state_sync(self, type_name: str, state_id: str, payload: bytes) -> None:
        target = self._state_path(type_name, state_id)
        directory = target.parent
        directory.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            directory.chmod(STATE_DIR_MODE)

        fd, tmp_name = tempfile.mkstemp(dir=directory, suffix=TEMP_FILE_SUFFIX)
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            tmp_path.chmod(STATE_FILE_MODE)
            # Atomic on POSIX: readers see the old inode or the new one, never
            # a half-written file.
            tmp_path.replace(target)
        except OSError as exc:
            tmp_path.unlink(missing_ok=True)
            raise StateStoreError(f"Failed to write state to '{target}': {exc}") from exc

        _fsync_directory(directory)

    async def delete_state(self, type_name: str, state_id: str) -> None:
        await asyncio.to_thread(self._delete_state_sync, type_name, state_id)

    def _delete_state_sync(self, type_name: str, state_id: str) -> None:
        path = self._state_path(type_name, state_id)
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            raise StateStoreError(f"Failed to delete state at '{path}': {exc}") from exc
        _fsync_directory(path.parent)

    async def list_states(self, type_name: str) -> list[str]:
        return await asyncio.to_thread(self._list_states_sync, type_name)

    def _list_states_sync(self, type_name: str) -> list[str]:
        directory = self._type_dir(type_name)
        if not directory.is_dir():
            return []
        return sorted(
            _decode_segment(entry.name[: -len(STATE_FILE_SUFFIX)])
            for entry in directory.iterdir()
            if entry.is_file() and entry.name.endswith(STATE_FILE_SUFFIX)
        )

    # ------------------------------------------------------------------
    # Lease-aware locking
    # ------------------------------------------------------------------

    async def lock_state(
        self,
        type_name: str,
        state_id: str,
        operation: str = "",
        ttl_seconds: float = DEFAULT_LOCK_TTL_SECONDS,
    ) -> StateLock:
        return await asyncio.to_thread(self._lock_state_sync, type_name, state_id, operation, ttl_seconds)

    def _lock_state_sync(self, type_name: str, state_id: str, operation: str, ttl_seconds: float) -> StateLock:
        path = self._lock_path(type_name, state_id)
        now = time.time()
        with exclusive_file_mutex(path, file_mode=STATE_FILE_MODE) as handle:
            existing = _read_lease(handle)
            if existing is not None and not existing.is_expired(now):
                raise StateLockConflictError(existing)
            if existing is not None:
                logger.warning(
                    "Reclaiming expired state lock lease",
                    operation="lock_state",
                    state_store_type=type_name,
                    state_id=state_id,
                    previous_holder=existing.holder,
                    previous_lock_id=existing.lock_id,
                )
            lock = StateLock(
                lock_id=str(uuid.uuid4()),
                type_name=type_name,
                state_id=state_id,
                operation=operation,
                acquired_at=now,
                expires_at=now + ttl_seconds if ttl_seconds > 0 else 0.0,
            )
            _write_lease(handle, lock)
            return lock

    async def unlock_state(self, type_name: str, state_id: str, lock_id: str) -> bool:
        return await asyncio.to_thread(self._unlock_state_sync, type_name, state_id, lock_id)

    def _unlock_state_sync(self, type_name: str, state_id: str, lock_id: str) -> bool:
        path = self._lock_path(type_name, state_id)
        with exclusive_file_mutex(path, file_mode=STATE_FILE_MODE) as handle:
            existing = _read_lease(handle)
            if existing is None or existing.lock_id != lock_id:
                return False
            _write_lease(handle, None)
            return True

    async def get_lock(self, type_name: str, state_id: str) -> StateLock | None:
        return await asyncio.to_thread(self._get_lock_sync, type_name, state_id)

    def _get_lock_sync(self, type_name: str, state_id: str) -> StateLock | None:
        path = self._lock_path(type_name, state_id)
        if not path.exists():
            return None
        with exclusive_file_mutex(path, file_mode=STATE_FILE_MODE) as handle:
            existing = _read_lease(handle)
        if existing is None or existing.is_expired():
            return None
        return existing


def _expand_root(root: str) -> Path:
    """Expand a configured root. Touches the filesystem, so callers use a thread."""
    return Path(root).expanduser()


def _probe_root(root: str) -> tuple[Path, bool]:
    """Expand a candidate root and report whether something else already occupies it."""
    candidate = _expand_root(root)
    return candidate, candidate.exists() and not candidate.is_dir()


def _config_root(config: Any) -> str | None:
    """Pull a ``path`` setting out of whatever shape the config arrived in."""
    if config is None:
        return None
    value = config.get("path") if isinstance(config, dict) else getattr(config, "path", None)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _read_lease(handle: IO[bytes]) -> StateLock | None:
    """Read the lease record from an already-mutexed handle."""
    handle.seek(0)
    raw = handle.read()
    if not raw.strip():
        return None
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # A corrupt lease is treated as no lease rather than a hard failure:
        # refusing to ever lock again would be a worse outcome than reclaiming
        # a record nobody can interpret.
        logger.warning("Discarding unreadable state lock lease", operation="lock_state")
        return None
    if not isinstance(payload, dict) or "lock_id" not in payload:
        return None
    return StateLock.from_dict(payload)


def _write_lease(handle: IO[bytes], lock: StateLock | None) -> None:
    """Replace the lease record on an already-mutexed handle."""
    handle.seek(0)
    handle.truncate()
    if lock is not None:
        handle.write(json.dumps(lock.to_dict()).encode("utf-8"))
    handle.flush()
    os.fsync(handle.fileno())


def _fsync_directory(directory: Path) -> None:
    """Persist a directory entry change so a rename survives a power loss."""
    try:
        fd = os.open(directory, os.O_RDONLY)
    except OSError:  # pragma: no cover - platforms that disallow directory fds
        return
    try:
        os.fsync(fd)
    except OSError:  # pragma: no cover - not all filesystems support this
        pass
    finally:
        os.close(fd)


# 🐍🏗️🔚
