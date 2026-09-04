#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A state lock is held until it is unlocked, not until a timer runs out.

Terraform acquires a state lock once per operation and releases it with
UnlockState when the operation ends. Nothing renews it in between: the pluggable
state store client sends `Lock` and `Unlock` and no third thing
(terraform/internal/states/remote/remote_grpc.go:122-130), and there is no TTL
anywhere under `internal/states` or `internal/backend/pluggable`.

So a lease that expires on its own is a lock that can be taken from underneath a
running apply. With the default of five minutes, any apply slower than that --
an ordinary size of infrastructure -- could be joined by a second writer, and
the first writer's UnlockState would then be refused because the lock id no
longer matches.

The stale-lock problem this was meant to solve is the one every Terraform
backend has, and it has a standard answer: `terraform force-unlock <ID>`, which
arrives here as UnlockState with that id. Expiry is now opt-in, and off.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from pyvider.exceptions import PyviderError
from pyvider.state_stores.filesystem import FileSystemStateStore
from pyvider.state_stores.manager import default_lock_ttl_seconds
from pyvider.state_stores.memory import InMemoryStateStore

TYPE_NAME = "test_store"
STATE_ID = "main"


def _backends(tmp_path) -> list[object]:
    return [InMemoryStateStore(), FileSystemStateStore(root=str(tmp_path))]


@pytest.mark.asyncio
async def test_a_lock_taken_with_the_default_never_expires(tmp_path) -> None:
    """The default must not hand the lock to a second writer while one holds it."""
    for backend in _backends(tmp_path):
        lock = await backend.lock_state(TYPE_NAME, STATE_ID, "apply")

        assert lock.expires_at == 0.0, (
            f"{type(backend).__name__} gave the lock an expiry by default, so an "
            "apply that runs longer than it can be joined by a second writer"
        )
        assert not lock.is_expired(now=time.time() + 86_400)


@pytest.mark.asyncio
async def test_the_default_ttl_is_no_expiry() -> None:
    assert default_lock_ttl_seconds() == 0.0


@pytest.mark.asyncio
async def test_an_explicit_ttl_is_still_honoured(tmp_path) -> None:
    """Expiry stays available for an operator who has decided they want it."""
    for backend in _backends(tmp_path):
        lock = await backend.lock_state(TYPE_NAME, STATE_ID, "apply", ttl_seconds=60)

        assert lock.expires_at > time.time()
        assert lock.is_expired(now=time.time() + 120)


@pytest.mark.asyncio
async def test_a_held_lock_is_not_reclaimable(tmp_path) -> None:
    """A second acquisition is refused for as long as the first is held."""
    for backend in _backends(tmp_path):
        await backend.lock_state(TYPE_NAME, STATE_ID, "apply")

        with pytest.raises(PyviderError):
            await backend.lock_state(TYPE_NAME, STATE_ID, "apply")


@pytest.mark.asyncio
async def test_a_lock_is_released_by_its_id(tmp_path) -> None:
    """The recovery path for a stale lock: `terraform force-unlock <ID>`."""
    for backend in _backends(tmp_path):
        lock = await backend.lock_state(TYPE_NAME, STATE_ID, "apply")

        assert await backend.unlock_state(TYPE_NAME, STATE_ID, lock.lock_id) is True

        # And the state is lockable again afterwards.
        again = await backend.lock_state(TYPE_NAME, STATE_ID, "apply")
        assert again.lock_id != lock.lock_id


@pytest.mark.asyncio
async def test_an_expired_lease_is_still_reclaimable_when_opted_in(tmp_path) -> None:
    """Opting in keeps the old behaviour, so the escape hatch still works."""
    for backend in _backends(tmp_path):
        first = await backend.lock_state(TYPE_NAME, STATE_ID, "apply", ttl_seconds=0.01)
        await asyncio.sleep(0.05)

        second = await backend.lock_state(TYPE_NAME, STATE_ID, "apply", ttl_seconds=0.01)

        assert second.lock_id != first.lock_id


# 🐍🏗️🔚


@pytest.mark.asyncio
async def test_a_lease_with_an_unreadable_timestamp_does_not_wedge_the_lock(tmp_path) -> None:
    """A lease nobody can interpret is discarded, not raised on forever.

    Corrupt JSON was already treated as "no lease", on the reasoning that
    refusing to ever lock again is worse than reclaiming a record nobody can
    read. A lease that parses as JSON but carries a malformed timestamp took a
    different path: `StateLock.from_dict` raised `ValueError` out of `float()`,
    and it raised on every subsequent attempt, so the state could never be
    locked again without deleting the file by hand.
    """
    import json

    store = FileSystemStateStore(root=str(tmp_path))
    lock = await store.lock_state(TYPE_NAME, STATE_ID, "apply")
    await store.unlock_state(TYPE_NAME, STATE_ID, lock.lock_id)

    lock_path = store._lock_path(TYPE_NAME, STATE_ID)
    lock_path.write_text(json.dumps({"lock_id": "stale", "expires_at": "not-a-number"}))

    # Must not raise, and must be lockable again.
    reacquired = await store.lock_state(TYPE_NAME, STATE_ID, "apply")

    assert reacquired.lock_id != "stale"


@pytest.mark.asyncio
async def test_a_lease_holding_a_null_timestamp_is_also_discarded(tmp_path) -> None:
    """The same shape, reached through TypeError rather than ValueError."""
    import json

    store = FileSystemStateStore(root=str(tmp_path))
    lock = await store.lock_state(TYPE_NAME, STATE_ID, "apply")
    await store.unlock_state(TYPE_NAME, STATE_ID, lock.lock_id)

    lock_path = store._lock_path(TYPE_NAME, STATE_ID)
    lock_path.write_text(json.dumps({"lock_id": "stale", "acquired_at": None}))

    reacquired = await store.lock_state(TYPE_NAME, STATE_ID, "apply")

    assert reacquired.lock_id != "stale"
