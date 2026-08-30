#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Contract tests every state-store backend must satisfy.

Both backends are driven through the same cases so a durable backend cannot
quietly diverge from the in-memory one the tests were written against.
"""

import asyncio
from collections.abc import Iterator
from pathlib import Path
import time

import pytest

from pyvider.state_stores import (
    BaseStateStore,
    FileSystemStateStore,
    InMemoryStateStore,
    StateLockConflictError,
)

TYPE_NAME = "demo_store"


@pytest.fixture(params=["memory", "filesystem"])
def backend(request, tmp_path: Path) -> Iterator[BaseStateStore]:
    if request.param == "memory":
        yield InMemoryStateStore()
    else:
        yield FileSystemStateStore(root=tmp_path / "state")


@pytest.mark.asyncio
async def test_read_missing_state_returns_none(backend: BaseStateStore) -> None:
    assert await backend.read_state(TYPE_NAME, "absent") is None


@pytest.mark.asyncio
async def test_write_then_read_roundtrips_payload(backend: BaseStateStore) -> None:
    await backend.write_state(TYPE_NAME, "main", b"payload-bytes")

    assert await backend.read_state(TYPE_NAME, "main") == b"payload-bytes"


@pytest.mark.asyncio
async def test_write_replaces_previous_payload(backend: BaseStateStore) -> None:
    await backend.write_state(TYPE_NAME, "main", b"first")
    await backend.write_state(TYPE_NAME, "main", b"second-and-longer")

    assert await backend.read_state(TYPE_NAME, "main") == b"second-and-longer"


@pytest.mark.asyncio
async def test_list_states_is_scoped_to_type_name(backend: BaseStateStore) -> None:
    await backend.write_state(TYPE_NAME, "alpha", b"a")
    await backend.write_state(TYPE_NAME, "beta", b"b")
    await backend.write_state("other_store", "gamma", b"g")

    assert sorted(await backend.list_states(TYPE_NAME)) == ["alpha", "beta"]
    assert await backend.list_states("other_store") == ["gamma"]


@pytest.mark.asyncio
async def test_list_states_for_unknown_type_is_empty(backend: BaseStateStore) -> None:
    assert await backend.list_states("never_used") == []


@pytest.mark.asyncio
async def test_delete_removes_state(backend: BaseStateStore) -> None:
    await backend.write_state(TYPE_NAME, "main", b"payload")

    await backend.delete_state(TYPE_NAME, "main")

    assert await backend.read_state(TYPE_NAME, "main") is None
    assert await backend.list_states(TYPE_NAME) == []


@pytest.mark.asyncio
async def test_delete_missing_state_is_a_noop(backend: BaseStateStore) -> None:
    await backend.delete_state(TYPE_NAME, "absent")


@pytest.mark.asyncio
async def test_lock_returns_a_lease_with_expiry(backend: BaseStateStore) -> None:
    lock = await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=60)

    assert lock.lock_id
    assert lock.type_name == TYPE_NAME
    assert lock.state_id == "main"
    assert lock.operation == "plan"
    assert lock.expires_at > time.time()
    assert not lock.is_expired()


@pytest.mark.asyncio
async def test_second_lock_on_live_lease_conflicts(backend: BaseStateStore) -> None:
    first = await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=60)

    with pytest.raises(StateLockConflictError) as excinfo:
        await backend.lock_state(TYPE_NAME, "main", "apply", ttl_seconds=60)

    assert excinfo.value.existing.lock_id == first.lock_id


@pytest.mark.asyncio
async def test_locks_on_distinct_states_do_not_conflict(backend: BaseStateStore) -> None:
    await backend.lock_state(TYPE_NAME, "one", "plan", ttl_seconds=60)
    await backend.lock_state(TYPE_NAME, "two", "plan", ttl_seconds=60)


@pytest.mark.asyncio
async def test_expired_lease_is_reclaimable(backend: BaseStateStore) -> None:
    stale = await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=0.01)
    await asyncio.sleep(0.05)

    fresh = await backend.lock_state(TYPE_NAME, "main", "apply", ttl_seconds=60)

    assert fresh.lock_id != stale.lock_id


@pytest.mark.asyncio
async def test_unlock_with_matching_id_releases(backend: BaseStateStore) -> None:
    lock = await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=60)

    assert await backend.unlock_state(TYPE_NAME, "main", lock.lock_id) is True
    assert await backend.get_lock(TYPE_NAME, "main") is None


@pytest.mark.asyncio
async def test_unlock_with_wrong_id_is_refused(backend: BaseStateStore) -> None:
    lock = await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=60)

    assert await backend.unlock_state(TYPE_NAME, "main", "not-the-lock-id") is False

    held = await backend.get_lock(TYPE_NAME, "main")
    assert held is not None
    assert held.lock_id == lock.lock_id


@pytest.mark.asyncio
async def test_unlock_when_unlocked_is_refused(backend: BaseStateStore) -> None:
    assert await backend.unlock_state(TYPE_NAME, "main", "any-id") is False


@pytest.mark.asyncio
async def test_get_lock_reports_expired_lease_as_unlocked(backend: BaseStateStore) -> None:
    await backend.lock_state(TYPE_NAME, "main", "plan", ttl_seconds=0.01)
    await asyncio.sleep(0.05)

    assert await backend.get_lock(TYPE_NAME, "main") is None


@pytest.mark.asyncio
async def test_locking_does_not_disturb_stored_payload(backend: BaseStateStore) -> None:
    await backend.write_state(TYPE_NAME, "main", b"payload")
    lock = await backend.lock_state(TYPE_NAME, "main", "apply", ttl_seconds=60)
    await backend.unlock_state(TYPE_NAME, "main", lock.lock_id)

    assert await backend.read_state(TYPE_NAME, "main") == b"payload"
    assert await backend.list_states(TYPE_NAME) == ["main"]


# 🐍🏗️🔚
