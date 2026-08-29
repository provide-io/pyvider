#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Every state lands inside the store root, whatever Terraform sends as its name.

`type_name` and `state_id` arrive over the wire, and `_backend()` resolves an
unregistered `type_name` to a default backend rather than rejecting it, so
nothing upstream filters them.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pyvider.state_stores.filesystem import (
    FileSystemStateStore,
    _decode_segment,
    _encode_segment,
)

TRAVERSAL = ["..", ".", "...", "../..", "..%2f..", "a/../..", "\\..\\.."]


@pytest.mark.parametrize("hostile", TRAVERSAL)
async def test_a_hostile_type_name_cannot_escape_the_root(tmp_path: Path, hostile: str) -> None:
    root = tmp_path / "store" / "state"
    root.mkdir(parents=True)
    store = FileSystemStateStore(root=root)

    await store.write_state(hostile, "victim", b"PWNED")

    escaped = [p for p in tmp_path.rglob("*.tfstate") if root not in p.parents and p.parent != root]
    assert not escaped, f"{hostile!r} wrote outside the store root: {escaped}"


@pytest.mark.parametrize("hostile", TRAVERSAL)
async def test_a_hostile_state_id_cannot_escape_the_root(tmp_path: Path, hostile: str) -> None:
    root = tmp_path / "store" / "state"
    root.mkdir(parents=True)
    store = FileSystemStateStore(root=root)

    await store.write_state("ordinary", hostile, b"PWNED")

    escaped = [p for p in tmp_path.rglob("*.tfstate") if root not in p.parents and p.parent != root]
    assert not escaped, f"{hostile!r} wrote outside the store root: {escaped}"


@pytest.mark.parametrize(
    "value",
    ["..", ".", "ordinary", "my.store", "..foo", "foo..", "with/slash", "with space", "üñî"],
)
def test_encoding_stays_reversible(value: str) -> None:
    assert _decode_segment(_encode_segment(value)) == value


@pytest.mark.parametrize(
    "value",
    [*TRAVERSAL, "foo..", "foo.", "ordinary", "my.store", "..foo", "üñî", "trailing space "],
)
def test_an_encoded_segment_never_ends_in_a_dot_or_space(value: str) -> None:
    """Windows drops trailing dots and spaces from a path component.

    So a name encoded to something ending in one is a *different* directory on
    disk than the one the encoder named, and the mapping `list_states` relies on
    stops being reversible -- silently, since nothing errors at encode time.
    `../..` encodes to `..%2F..`, which Windows resolves against `..%2F`:

        [WinError 3] The system cannot find the path specified:
        '...\\store\\state\\..%2F\\tmphiaxm3tu.tmp' ->
        '...\\store\\state\\..%2F..\\victim.tfstate'

    Asserted on every platform because the encoder is the thing being
    constrained, and it must not depend on which host it runs on.
    """
    encoded = _encode_segment(value)

    assert encoded == encoded.rstrip(". "), f"{value!r} encoded to {encoded!r}"


@pytest.mark.parametrize("value", ["ordinary", "my.store", "..foo", "a-b_c", "a.b.c"])
def test_ordinary_names_are_unchanged_on_disk(value: str) -> None:
    """A name that cannot traverse keeps its existing on-disk spelling, so no migration."""
    assert _encode_segment(value) == value


def test_a_name_ending_in_a_dot_is_the_one_that_changes_spelling() -> None:
    """`foo..` is the only shape whose on-disk name moves, and it had no valid one.

    It was listed above as needing no migration, which was true on POSIX and
    false on Windows, where it had always been stored as `foo` -- the trailing
    dots dropped by the filesystem, not by this encoder. There is no
    cross-platform stored state to preserve, so the escape is safe to introduce.
    """
    assert _encode_segment("foo..") == "foo%2E%2E"
    assert _decode_segment(_encode_segment("foo..")) == "foo.."


async def test_a_written_state_reads_back_under_a_hostile_name(tmp_path: Path) -> None:
    root = tmp_path / "state"
    root.mkdir(parents=True)
    store = FileSystemStateStore(root=root)

    await store.write_state("..", "..", b"CONFINED")
    assert await store.read_state("..", "..") == b"CONFINED"


# 🌊🪢🔚
