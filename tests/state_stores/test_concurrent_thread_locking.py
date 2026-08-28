#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Two threads of one provider cannot both hold the same state lock.

`test_cross_process_locking.py` covers separate processes, which is the case
POSIX record locks handle correctly. Every state-store handler reaches the
backend through `asyncio.to_thread`, so concurrent *threads* of one process are
the ordinary case -- and `fcntl.lockf` does not separate them: a second lock
from the same process replaces the first rather than waiting.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from pyvider.state_stores import FileSystemStateStore
from pyvider.state_stores.types import StateLockConflictError

TYPE_NAME = "threaded"
STATE_ID = "default"
TRIALS = 60


@pytest.fixture
def store(tmp_path: Path) -> FileSystemStateStore:
    return FileSystemStateStore(root=tmp_path / "state")


async def _try_lock(store: FileSystemStateStore) -> str | None:
    try:
        lock = await store.lock_state(TYPE_NAME, STATE_ID, operation="plan", ttl_seconds=60)
    except StateLockConflictError:
        return None
    return lock.lock_id


async def test_only_one_of_two_concurrent_threads_acquires(store: FileSystemStateStore) -> None:
    """Repeated because the losing interleaving is timing-dependent."""
    for trial in range(TRIALS):
        state_id = f"{STATE_ID}-{trial}"

        async def _attempt(sid: str = state_id) -> str | None:
            try:
                lock = await store.lock_state(TYPE_NAME, sid, operation="plan", ttl_seconds=60)
            except StateLockConflictError:
                return None
            return lock.lock_id

        winners = [r for r in await asyncio.gather(_attempt(), _attempt()) if r is not None]
        assert len(winners) == 1, f"trial {trial}: {len(winners)} threads acquired the same lock"

        held = await store.get_lock(TYPE_NAME, state_id)
        assert held is not None
        assert held.lock_id == winners[0], "the recorded lease belongs to a caller that was told it lost"


async def test_the_winner_can_unlock_and_the_loser_cannot(store: FileSystemStateStore) -> None:
    first = await _try_lock(store)
    assert first is not None
    assert await _try_lock(store) is None, "a second acquire succeeded against a live lease"

    assert await store.unlock_state(TYPE_NAME, STATE_ID, "not-the-holder") is False
    assert await store.unlock_state(TYPE_NAME, STATE_ID, first) is True


async def test_a_read_modify_write_under_the_lock_loses_no_updates(
    store: FileSystemStateStore,
) -> None:
    """The mutex guards the lease record; concurrent threads must serialise on it."""
    await store.write_state(TYPE_NAME, STATE_ID, b"0")

    async def bump() -> None:
        lock = await store.lock_state(TYPE_NAME, STATE_ID, ttl_seconds=60)
        current = int((await store.read_state(TYPE_NAME, STATE_ID) or b"0").decode())
        await asyncio.sleep(0)
        await store.write_state(TYPE_NAME, STATE_ID, str(current + 1).encode())
        await store.unlock_state(TYPE_NAME, STATE_ID, lock.lock_id)

    results = await asyncio.gather(*(bump() for _ in range(4)), return_exceptions=True)
    conflicts = [r for r in results if isinstance(r, StateLockConflictError)]
    applied = int((await store.read_state(TYPE_NAME, STATE_ID)).decode())

    # Whoever was refused the lock did not write; whoever held it did.
    assert applied == 4 - len(conflicts)


# 🌊🪢🔚
