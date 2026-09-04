#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""State ids that differ only in case, or that name a device, get their own file.

``_encode_segment`` maps a Terraform-supplied name to exactly one path segment.
It is an allow-list -- lowercase letters, digits, ``-`` and ``_`` survive, and
everything else is percent-escaped -- because the alternative is to enumerate
the characters a filesystem treats specially, and that list is not knowable in
advance. Path separators, ``..``, trailing dots and spaces, letter case and
reserved device names each turned up after the encoder was written.

Two of them cost state. On APFS and NTFS, ``prod`` and ``Prod`` name one file,
so a read of one served the other's bytes and ``list_states`` could not see
that anything was missing. And Windows resolves ``con``, ``prn``, ``aux``,
``nul``, ``com1``-``com9`` and ``lpt1``-``lpt9`` to devices whatever extension
follows, so a state with one of those ids was never a file at all.
"""

from __future__ import annotations

import errno
from pathlib import Path

import pytest

from pyvider.state_stores import FileSystemStateStore
from pyvider.state_stores.defaults import LOCK_FILE_SUFFIX, STATE_FILE_SUFFIX
from pyvider.state_stores.filesystem import (
    _decode_segment,
    _encode_segment,
    _legacy_encode_segment,
)

DEVICE_NAMES = ["con", "prn", "aux", "nul", "com1", "com9", "lpt1", "lpt9"]


@pytest.fixture
def store(tmp_path: Path) -> FileSystemStateStore:
    root = tmp_path / "state"
    root.mkdir(parents=True)
    return FileSystemStateStore(root=root)


class TestIdsThatDifferOnlyInCase:
    def test_they_encode_to_different_names(self) -> None:
        assert _encode_segment("prod") != _encode_segment("Prod")

    async def test_they_keep_separate_states(self, store: FileSystemStateStore) -> None:
        await store.write_state("t", "prod", b"LOWER")
        await store.write_state("t", "Prod", b"UPPER")

        assert await store.read_state("t", "prod") == b"LOWER", (
            "writing `Prod` overwrote `prod`; the two share one file on this filesystem"
        )
        assert await store.read_state("t", "Prod") == b"UPPER"

    async def test_both_are_listed(self, store: FileSystemStateStore) -> None:
        await store.write_state("t", "prod", b"LOWER")
        await store.write_state("t", "Prod", b"UPPER")

        assert await store.list_states("t") == ["Prod", "prod"]

    async def test_their_locks_are_separate(self, store: FileSystemStateStore) -> None:
        """A shared lock file would serialise two unrelated states against each other."""
        await store.lock_state("t", "prod", operation="plan")

        lock = await store.lock_state("t", "Prod", operation="plan")

        assert lock.state_id == "Prod"


class TestWindowsDeviceNames:
    @pytest.mark.parametrize("device", DEVICE_NAMES)
    def test_a_device_name_does_not_survive_encoding(self, device: str) -> None:
        """`con.tfstate` opens the console on Windows, whatever the extension."""
        assert _encode_segment(device) != device

    @pytest.mark.parametrize("device", DEVICE_NAMES)
    def test_a_device_name_still_round_trips(self, device: str) -> None:
        assert _decode_segment(_encode_segment(device)) == device

    @pytest.mark.parametrize("device", DEVICE_NAMES)
    async def test_a_state_named_for_a_device_reads_back(
        self, store: FileSystemStateStore, device: str
    ) -> None:
        await store.write_state("t", device, b"NOT-A-DEVICE")

        assert await store.read_state("t", device) == b"NOT-A-DEVICE"

    def test_a_name_that_merely_contains_one_is_left_alone(self) -> None:
        """Only the whole segment is reserved, so `console` is an ordinary name."""
        assert _encode_segment("console") == "console"


@pytest.mark.parametrize(
    "value",
    ["Prod", "PROD", "MiXeD", "con", "com1", "..", "with/slash", "with space", "üñî", "100%"],
)
def test_encoding_stays_reversible(value: str) -> None:
    assert _decode_segment(_encode_segment(value)) == value


class TestAdoptingNamesFromThePreviousEncoder:
    """A store written before the allow-list is taken over, not abandoned.

    The previous encoder left uppercase and device names unescaped, so its
    files sit under names this one no longer produces. They are renamed forward
    the first time the state is touched.
    """

    def _write_legacy(self, store: FileSystemStateStore, state_id: str, payload: bytes) -> Path:
        directory = store.root / "t"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{_legacy_encode_segment(state_id)}{STATE_FILE_SUFFIX}"
        path.write_bytes(payload)
        return path

    async def test_a_state_under_the_old_name_is_found(self, store: FileSystemStateStore) -> None:
        self._write_legacy(store, "Prod", b"WRITTEN-BEFORE")

        assert await store.read_state("t", "Prod") == b"WRITTEN-BEFORE"

    async def test_it_is_renamed_forward_rather_than_read_in_place(self, store: FileSystemStateStore) -> None:
        """Adopting once is what lets this compatibility be deleted later."""
        legacy = self._write_legacy(store, "Prod", b"WRITTEN-BEFORE")

        await store.read_state("t", "Prod")

        assert not legacy.exists()
        assert (store.root / "t" / f"{_encode_segment('Prod')}{STATE_FILE_SUFFIX}").exists()

    async def test_a_lock_under_the_old_name_is_found(self, store: FileSystemStateStore) -> None:
        """Missing it would let a second process take a lock the first still holds."""
        directory = store.root / "t"
        directory.mkdir(parents=True, exist_ok=True)
        legacy = directory / f"{_legacy_encode_segment('Prod')}{LOCK_FILE_SUFFIX}"
        held = await store.lock_state("t", "Prod", operation="plan")
        # Put the lease back where the previous encoder would have kept it.
        canonical = directory / f"{_encode_segment('Prod')}{LOCK_FILE_SUFFIX}"
        canonical.rename(legacy)

        found = await store.get_lock("t", "Prod")
        assert found is not None, "the lease written under the old name was not found"
        assert found.lock_id == held.lock_id

    async def test_a_case_collision_is_not_taken_from_another_id(self, store: FileSystemStateStore) -> None:
        """`Prod` must not adopt the file `prod` wrote.

        On a case-insensitive filesystem `Prod.tfstate` opens the file stored
        as `prod.tfstate`. Only the entry's stored spelling says which id wrote
        it, so an adoption that merely resolved would hand one state's bytes to
        another -- silently, and destructively, since it renames.
        """
        self._write_legacy(store, "prod", b"BELONGS-TO-LOWERCASE")

        assert await store.read_state("t", "Prod") is None
        assert await store.read_state("t", "prod") == b"BELONGS-TO-LOWERCASE"

    async def test_a_type_directory_under_the_old_name_is_adopted(self, store: FileSystemStateStore) -> None:
        legacy_dir = store.root / _legacy_encode_segment("MyType")
        legacy_dir.mkdir(parents=True)
        (legacy_dir / f"{_encode_segment('s')}{STATE_FILE_SUFFIX}").write_bytes(b"IN-OLD-DIR")

        assert await store.read_state("MyType", "s") == b"IN-OLD-DIR"

    async def test_a_rename_that_fails_still_serves_the_state(
        self, store: FileSystemStateStore, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Reporting the state missing is the one unrecoverable answer here.

        A read-only directory, or a peer holding the file open on Windows, must
        cost the tidier name and nothing else.
        """
        self._write_legacy(store, "Prod", b"WRITTEN-BEFORE")

        def refuse(self: Path, target: object) -> Path:
            raise OSError(errno.EACCES, "refused")

        monkeypatch.setattr(Path, "rename", refuse)

        assert await store.read_state("t", "Prod") == b"WRITTEN-BEFORE"

    async def test_an_ordinary_name_is_left_exactly_where_it_is(self, store: FileSystemStateStore) -> None:
        """The common case must not pay for the migration, or move on disk."""
        await store.write_state("t", "production-1", b"PLAIN")

        assert (store.root / "t" / f"production-1{STATE_FILE_SUFFIX}").exists()


# 🐍🏗️🔚
