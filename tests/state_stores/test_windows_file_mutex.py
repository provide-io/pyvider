#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The cross-process mutex on Windows, where there is no ``fcntl``.

Windows takes the same kind of lock by a different name: ``msvcrt.locking``
locks a byte range on an open descriptor, and the range is released when the
handle closes -- which the OS does for every handle at process termination.
That is the one property this mutex depends on, and the same one
``fcntl.lockf`` provides, so both platforms get a lock a dead holder cannot
keep.

The Windows branch cannot run on the host that develops it, so these tests
force ``HAVE_FCNTL`` off and put a recording stand-in in ``msvcrt``'s place.
What they pin is the wiring: which call is made, in which mode, over which
range, at which file position, and which errnos mean a peer holds the lock.
The exclusion itself is the kernel's, and is covered for real -- on Windows in
CI as well as here -- by ``test_cross_process_locking.py``.
"""

from __future__ import annotations

from collections.abc import Callable
import errno
import os
from pathlib import Path

import pytest

from pyvider.state_stores import _filelock
from pyvider.state_stores._filelock import (
    FileMutexTimeoutError,
    FileMutexUnsupportedError,
    exclusive_file_mutex,
)

#: The CRT's own values, so the assertions read against the real API.
LK_UNLCK = 0
LK_NBLCK = 2

#: The errno the CRT reports once its internal retries are exhausted. Absent
#: from `errno` on POSIX hosts, which is where this test usually runs.
EDEADLOCK = getattr(errno, "EDEADLOCK", 36)


class RecordingCrt:
    """Stands in for the Windows CRT, recording how it was called."""

    LK_UNLCK = LK_UNLCK
    LK_NBLCK = LK_NBLCK

    def __init__(self, failures: list[int] | None = None) -> None:
        self.calls: list[tuple[int, int]] = []
        self.positions: list[int] = []
        self._failures = list(failures or [])

    def locking(self, fd: int, mode: int, nbytes: int) -> None:
        # Read the descriptor's position before recording the call: the range
        # msvcrt locks starts wherever the file happens to be pointing.
        self.positions.append(os.lseek(fd, 0, os.SEEK_CUR))
        self.calls.append((mode, nbytes))
        if self._failures:
            raise OSError(self._failures.pop(0), "simulated")


@pytest.fixture
def on_windows(monkeypatch: pytest.MonkeyPatch) -> Callable[..., RecordingCrt]:
    """Present this host as Windows, with a CRT that records what it is asked."""

    def install(failures: list[int] | None = None) -> RecordingCrt:
        crt = RecordingCrt(failures)
        monkeypatch.setattr(_filelock, "HAVE_FCNTL", False)
        monkeypatch.setattr(_filelock, "msvcrt", crt)
        return crt

    return install


@pytest.fixture
def lock_path(tmp_path: Path) -> Path:
    return tmp_path / "state.tflock"


class TestTheKernelLockIsTakenThroughTheCrt:
    def test_the_lock_and_the_release_are_both_made(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        crt = on_windows()

        with exclusive_file_mutex(lock_path, timeout=1) as handle:
            handle.write(b"lease")

        assert crt.calls == [(LK_NBLCK, 1), (LK_UNLCK, 1)], (
            "the mutex did not take and release exactly one non-blocking byte-range lock"
        )

    def test_both_calls_are_made_at_the_start_of_the_file(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        """The range is measured from the current position, so the seek matters.

        The caller's block reads and rewrites the lease record through this
        same handle, which moves the position; releasing from wherever it
        ended up would unlock a range nobody locked.
        """
        crt = on_windows()

        with exclusive_file_mutex(lock_path, timeout=1) as handle:
            handle.write(b"a lease record long enough to move the position")

        assert crt.positions == [0, 0]

    def test_no_sentinel_file_is_left_beside_the_lock(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        """The kernel owns this lock; nothing on disk represents it."""
        on_windows()

        with exclusive_file_mutex(lock_path, timeout=1):
            in_use = sorted(p.name for p in lock_path.parent.iterdir())

        assert in_use == [lock_path.name], f"an on-disk lock artifact was created: {in_use}"


class TestContention:
    def test_a_lock_a_peer_holds_is_waited_out(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        crt = on_windows([errno.EACCES, errno.EACCES])

        with exclusive_file_mutex(lock_path, timeout=2):
            pass

        assert len(crt.calls) == 4, "the refused attempts were not retried"

    def test_the_crt_deadlock_errno_is_contention_too(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        """`LK_LOCK` reports EDEADLOCK after exhausting its own retries."""
        crt = on_windows([EDEADLOCK])

        with exclusive_file_mutex(lock_path, timeout=2):
            pass

        assert len(crt.calls) == 3

    def test_a_lock_held_past_the_timeout_names_the_contended_path(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        on_windows([errno.EACCES] * 10_000)

        with pytest.raises(FileMutexTimeoutError) as excinfo:
            with exclusive_file_mutex(lock_path, timeout=0.05):
                pass  # pragma: no cover - the block must not be entered

        assert str(lock_path) in str(excinfo.value)

    def test_an_unrelated_error_is_not_mistaken_for_contention(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        """A broken descriptor is a fault, not a peer; retrying it hides it."""
        on_windows([errno.EIO])

        with pytest.raises(OSError) as excinfo:
            with exclusive_file_mutex(lock_path, timeout=5):
                pass  # pragma: no cover - the block must not be entered

        assert excinfo.value.errno == errno.EIO
        assert not isinstance(excinfo.value, FileMutexTimeoutError)


class TestAHostWithNeitherPrimitive:
    def test_it_is_refused_rather_than_given_a_weaker_lock(
        self, monkeypatch: pytest.MonkeyPatch, lock_path: Path
    ) -> None:
        """A lock that silently fails to exclude is worse than no lock.

        The caller cannot tell the difference, so it writes a lease it does not
        hold. Refusing keeps the failure where somebody can see it.
        """
        monkeypatch.setattr(_filelock, "HAVE_FCNTL", False)
        monkeypatch.setattr(_filelock, "msvcrt", None)

        with pytest.raises(FileMutexUnsupportedError):
            with exclusive_file_mutex(lock_path, timeout=1):
                pass  # pragma: no cover - the block must not be entered


class TestTheHandleIsAlwaysClosed:
    def test_a_release_that_fails_still_closes_the_handle(
        self, on_windows: Callable[..., RecordingCrt], lock_path: Path
    ) -> None:
        """Leaving the handle open on Windows leaves the file locked."""
        crt = on_windows()
        held: list[object] = []

        with pytest.raises(OSError):
            with exclusive_file_mutex(lock_path, timeout=1) as handle:
                held.append(handle)
                # Fail only the release; the acquire above already succeeded.
                crt._failures.append(errno.EIO)

        assert held[0].closed, "the handle outlived the block, keeping the file locked"


# 🐍🏗️🔚
