#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A short-lived, cross-process mutex over a single file.

This guards the read-modify-write of a lease record, not the lease itself. The
distinction matters: the lease can outlive the process that took it (that is the
point of an expiry), whereas this mutex is held for microseconds and is released
by the kernel if the holder dies. Building the lease on top of a real kernel
mutex is what makes "check the lease, then claim it" a single atomic step
instead of a race between concurrent providers.

Both platforms supply that mutex as a byte-range lock on an open descriptor.
POSIX has ``fcntl.lockf`` -- the record-lock variant rather than ``flock``,
because it is the one NFS implements, and a state directory on a network share
is a normal deployment for remote state. Windows has ``msvcrt.locking``, which
locks a range measured from the descriptor's current position and releases it
when the handle closes; the OS closes every handle at process termination.

Neither can be left behind by a process that dies, and that is the whole reason
both are used. A lock represented by an ordinary file cannot promise it: nothing
removes it when its holder is killed, so it has to be paired with a staleness
heuristic that guesses when a holder is dead -- and a wrong guess puts two
providers inside the critical section, which is the one outcome a mutex exists
to prevent. A host offering neither primitive is therefore refused outright
rather than served a lock that only looks like one.

Record locks are owned by the *process*, not by the thread or the descriptor, so
they do not separate two threads of one provider at all: a second ``lockf`` from
the same process replaces the first rather than waiting for it, and releasing
any descriptor drops the process's lock on that inode -- unlocking a peer thread
mid-section. Every handler here reaches the mutex through ``asyncio.to_thread``,
so that is the ordinary case, not an exotic one. An in-process ``threading.Lock``
per path is therefore taken first, and the kernel lock guards the remaining case
of a second process.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import errno
import os
from pathlib import Path
import threading
import time
from types import ModuleType
from typing import IO

try:  # pragma: no cover - the absent branch is Windows-only
    import fcntl

    HAVE_FCNTL = True
except ImportError:  # pragma: no cover - Windows and other non-POSIX hosts
    HAVE_FCNTL = False

#: Annotated rather than imported bare so this module type-checks on POSIX,
#: where `msvcrt` does not exist. Looked up through the module global on every
#: call, which is also what lets the Windows path be exercised off-platform.
msvcrt: ModuleType | None
try:  # pragma: no cover - the present branch is Windows-only
    import msvcrt
except ImportError:
    msvcrt = None

# How long to wait for the mutex before giving up. The critical section is a
# small read plus a small write, so anything approaching this bound means a peer
# process died mid-section or the filesystem is not honoring locks.
DEFAULT_MUTEX_TIMEOUT_SECONDS = 10.0

# Poll interval while a peer holds the lock. Both primitives are asked in their
# non-blocking form so the timeout stays this module's to enforce.
_POLL_SECONDS = 0.01

# `msvcrt.locking` locks a range, not a file, so every caller has to agree on
# the same one. A single byte at offset 0 is the cheapest such agreement, and
# Windows permits locking a range that reaches past the end of the file, so it
# works on a lock file that has never been written.
_WINDOWS_LOCK_BYTES = 1

# What "a peer holds it" looks like from each primitive. POSIX reports a held
# record lock as EACCES or EAGAIN, which of the two being the platform's
# choice. The Windows CRT reports EACCES for a refused `LK_NBLCK`, and
# EDEADLOCK once `LK_LOCK` has exhausted its own internal retries; the name is
# absent from `errno` on POSIX, where this tuple is never consulted.
_POSIX_CONTENDED = (errno.EACCES, errno.EAGAIN)
_WINDOWS_CONTENDED = (errno.EACCES, getattr(errno, "EDEADLOCK", 36))


class FileMutexTimeoutError(TimeoutError):
    """Raised when the cross-process mutex could not be acquired in time."""


class FileMutexUnsupportedError(RuntimeError):
    """Raised on a host that offers neither ``fcntl`` nor ``msvcrt``."""


# One lock per lock-file path, shared by every thread in this process. Keyed on
# the resolved path so two spellings of the same file cannot take two locks.
# Bounded by the number of distinct states this provider touches.
_THREAD_MUTEXES: dict[str, threading.Lock] = {}
_THREAD_MUTEX_REGISTRY = threading.Lock()


def _thread_mutex(path: Path) -> threading.Lock:
    key = os.path.realpath(path)
    with _THREAD_MUTEX_REGISTRY:
        return _THREAD_MUTEXES.setdefault(key, threading.Lock())


@contextmanager
def exclusive_file_mutex(
    path: Path,
    *,
    timeout: float = DEFAULT_MUTEX_TIMEOUT_SECONDS,
    file_mode: int = 0o600,
) -> Iterator[IO[bytes]]:
    """Hold an exclusive cross-process lock on ``path`` for the block's duration.

    Yields the open file handle so the caller can read and rewrite the record
    without reopening it, which would reintroduce the race the mutex closes.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    # Taken before the kernel lock, and required: a record lock cannot tell two
    # threads of this process apart, so without this both would enter the
    # critical section and both would write a lease.
    thread_mutex = _thread_mutex(path)
    if not thread_mutex.acquire(timeout=timeout):
        raise FileMutexTimeoutError(f"Timed out waiting {timeout}s for the in-process mutex on {path}")
    try:
        # Opened r+b-style via os.open so the file is created if absent without
        # truncating an existing lease record.
        fd = os.open(path, os.O_RDWR | os.O_CREAT, file_mode)
        handle: IO[bytes] = os.fdopen(fd, "r+b")
        try:
            _acquire(handle, path, timeout)
            try:
                yield handle
            finally:
                _release(handle)
        finally:
            # Closing is what releases the lock on Windows, so it happens even
            # when the release above failed -- otherwise a failed unlock would
            # leave the file locked for the life of the process.
            handle.close()
    finally:
        thread_mutex.release()


def _acquire(handle: IO[bytes], path: Path, timeout: float) -> None:
    """Take the kernel's exclusive lock, waiting out a peer that holds it."""
    contended = _POSIX_CONTENDED if HAVE_FCNTL else _WINDOWS_CONTENDED
    deadline = time.monotonic() + timeout
    while True:
        try:
            _lock_exclusive(handle)
            return
        except OSError as exc:
            if exc.errno not in contended:
                raise
            if time.monotonic() >= deadline:
                raise FileMutexTimeoutError(
                    f"Timed out after {timeout}s waiting for the state mutex at {path}."
                ) from exc
            time.sleep(_POLL_SECONDS)


def _lock_exclusive(handle: IO[bytes]) -> None:
    """Ask the platform for the lock once, without blocking."""
    if HAVE_FCNTL:
        fcntl.lockf(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    elif msvcrt is not None:
        _seek_to_locked_range(handle)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, _WINDOWS_LOCK_BYTES)
    else:
        raise FileMutexUnsupportedError(
            "This host has neither fcntl nor msvcrt, so no lock can be taken that a "
            "dead holder would release. State cannot be served safely here."
        )


def _release(handle: IO[bytes]) -> None:
    """Give the lock back. Only reached once ``_lock_exclusive`` has succeeded."""
    if HAVE_FCNTL:
        fcntl.lockf(handle.fileno(), fcntl.LOCK_UN)
    elif msvcrt is not None:
        _seek_to_locked_range(handle)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, _WINDOWS_LOCK_BYTES)


def _seek_to_locked_range(handle: IO[bytes]) -> None:
    """Point the descriptor at the range Windows locks.

    The position is part of naming the lock there, not a convenience: the
    caller's block reads and rewrites the lease through this same handle, so by
    release time the position is wherever that left it, and unlocking from
    there would name a range nobody locked.
    """
    handle.seek(0)


# 🐍🏗️🔚
