#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""An absent collection block is empty, not null.

Terraform decodes a block that appears no times as the empty value for its
nesting mode, not as null (configschema/empty_value.go:37-61):

    list  -> empty list        map    -> empty map
    set   -> empty set         group  -> object with all attributes null
    single -> null object

and it rejects the wrong one in a plan, per nesting mode
(objchange/plan_valid.go:74-91):

    attribute representing a list of nested blocks must be empty to indicate no
    blocks, not null

Every absent block encoded as null here, so a resource that simply did not
mention one produced a plan Terraform refuses. Only `single` was right, and only
by accident.
"""

from __future__ import annotations

from typing import Any

import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.protocols.tfprotov6.handlers.utils import normalise_absent_blocks
from pyvider.schema import a_str, b_group, b_list, b_map, b_set, b_single, s_resource

SCHEMA = s_resource(
    attributes={"name": a_str(required=True)},
    block_types=[
        b_list("cred", attributes={"user": a_str()}),
        b_set("tag", attributes={"key": a_str()}),
        b_map("zone", attributes={"region": a_str()}),
        b_single("auth", attributes={"token": a_str()}),
        b_group("meta", attributes={"owner": a_str()}),
    ],
)


def _normalised(values: dict[str, Any]) -> dict[str, Any]:
    normalise_absent_blocks(values, SCHEMA.block)
    return values


@pytest.mark.parametrize(
    ("block_name", "expected"),
    [("cred", []), ("tag", []), ("zone", {})],
    ids=["list", "set", "map"],
)
def test_an_absent_collection_block_becomes_empty(block_name: str, expected: Any) -> None:
    values = _normalised({"name": "alpha"})

    assert values[block_name] == expected, (
        f"an absent {block_name} block encoded as null; Terraform rejects that with "
        '"must be empty to indicate no blocks, not null"'
    )


def test_an_absent_single_block_stays_null() -> None:
    """Single is the one mode where null is the empty value."""
    values = _normalised({"name": "alpha"})

    assert values["auth"] is None


def test_an_absent_group_block_becomes_an_object_of_nulls() -> None:
    """A group block is always present; an absent one is all-null, not null."""
    values = _normalised({"name": "alpha"})

    assert values["meta"] == {"owner": None}


def test_a_block_that_is_present_is_left_alone() -> None:
    values = _normalised({"name": "alpha", "cred": [{"user": "root"}]})

    assert values["cred"] == [{"user": "root"}]


def test_an_explicit_none_is_normalised_too() -> None:
    """A resource that sets the key to None means the same as omitting it."""
    values = _normalised({"name": "alpha", "cred": None, "zone": None})

    assert values["cred"] == []
    assert values["zone"] == {}


def test_a_nested_block_inside_a_present_block_is_normalised() -> None:
    """Depth does not change the rule."""
    schema = s_resource(
        attributes={"name": a_str(required=True)},
        block_types=[
            b_single(
                "outer",
                attributes={"label": a_str()},
                block_types=[b_list("inner", attributes={"value": a_str()})],
            )
        ],
    )
    values: dict[str, Any] = {"name": "alpha", "outer": {"label": "x"}}

    normalise_absent_blocks(values, schema.block)

    assert values["outer"]["inner"] == []


def test_the_result_round_trips_as_an_empty_collection() -> None:
    """The point of all this: what reaches Terraform is empty rather than null."""
    values = _normalised({"name": "alpha"})
    decoded = unmarshal(marshal(values, schema=SCHEMA.block), schema=SCHEMA.block)

    assert not decoded["cred"].is_null, "the encoded list is still null"
    assert len(decoded["cred"].value) == 0
    assert not decoded["zone"].is_null
    assert decoded["auth"].is_null, "an absent single block must stay null"


# 🐍🏗️🔚
