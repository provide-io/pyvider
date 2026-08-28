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


@pytest.mark.parametrize("value", ["ordinary", "my.store", "..foo", "foo..", "a-b_c"])
def test_ordinary_names_are_unchanged_on_disk(value: str) -> None:
    """A name that cannot traverse keeps its existing on-disk spelling, so no migration."""
    assert _encode_segment(value) == value


async def test_a_written_state_reads_back_under_a_hostile_name(tmp_path: Path) -> None:
    root = tmp_path / "state"
    root.mkdir(parents=True)
    store = FileSystemStateStore(root=root)

    await store.write_state("..", "..", b"CONFINED")
    assert await store.read_state("..", "..") == b"CONFINED"


# 🌊🪢🔚
