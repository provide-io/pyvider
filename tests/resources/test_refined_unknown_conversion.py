#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A refined unknown must convert like any other unknown, not be iterated.

`_cty_to_attrs_recursive` recognised an unknown payload by identity against
`_UNREFINED_UNKNOWN_SENTINEL`, the singleton behind `CtyValue.unknown(...)`.
Terraform sends a *refined* unknown whenever it knows something about a value
it cannot yet compute -- most commonly "this will not be null" for
`targets = other_resource.some_list`. That payload is a different object, so
the identity check missed it and the value fell through to the list branch,
which iterated it:

    TypeError: 'RefinedUnknownValue' object is not iterable

reaching the practitioner as "Internal Provider Error" on every plan.

Refinements arrive as msgpack extension type 12; the nullness refinement above
encodes as `c7030c8101c2`. go-cty has emitted them since Terraform 1.6, so any
provider with a list or set attribute fed from another resource hits this.
"""

from __future__ import annotations

import attrs
import pytest

from pyvider.cty import CtyList, CtyObject, CtySet, CtyString, CtyValue
from pyvider.cty.codec import cty_from_msgpack, cty_to_msgpack
from pyvider.cty.values.markers import RefinedUnknownValue
from pyvider.resources.base import BaseResource


@attrs.define(frozen=True)
class ListState:
    targets: list[str] | None = None


def _refined_unknown(element_container: CtyList | CtySet) -> CtyValue:
    """An unknown Terraform has refined as "known not null"."""
    return CtyValue(
        vtype=element_container,
        is_unknown=True,
        value=RefinedUnknownValue(is_known_null=False),
    )


@pytest.mark.parametrize(
    "container",
    [
        CtyList(element_type=CtyString()),
        CtySet(element_type=CtyString()),
    ],
    ids=["list", "set"],
)
def test_a_refined_unknown_collection_converts_to_none(container: CtyList | CtySet) -> None:
    """The conversion yields None for the field rather than raising."""
    schema_type = CtyObject({"targets": container})
    value = schema_type.validate({"targets": _refined_unknown(container)})

    # Round-trip through the wire so the payload is what Terraform would send.
    decoded = cty_from_msgpack(cty_to_msgpack(value, schema_type), schema_type)
    payload = decoded["targets"].value

    assert isinstance(payload, RefinedUnknownValue), "the fixture no longer produces a refined unknown"
    assert BaseResource._cty_to_attrs_recursive(payload, list[str]) is None


def test_a_refined_unknown_survives_conversion_into_a_state_class() -> None:
    """The whole object converts, with the not-yet-known field left as None."""
    schema_type = CtyObject({"targets": CtyList(element_type=CtyString())})
    value = schema_type.validate({"targets": _refined_unknown(CtyList(element_type=CtyString()))})
    decoded = cty_from_msgpack(cty_to_msgpack(value, schema_type), schema_type)

    instance = BaseResource.from_cty(decoded, ListState)

    assert instance is not None, "a refined unknown collapsed the whole state class"
    assert instance.targets is None


def test_an_unrefined_unknown_still_converts_to_none() -> None:
    """The case the identity check already handled keeps working."""
    unknown = CtyValue.unknown(CtyList(element_type=CtyString()))

    assert BaseResource._cty_to_attrs_recursive(unknown.value, list[str]) is None


def test_a_known_collection_is_still_converted() -> None:
    """Refinement handling must not swallow real values."""
    schema_type = CtyObject({"targets": CtyList(element_type=CtyString())})
    value = schema_type.validate({"targets": ["a", "b"]})

    instance = BaseResource.from_cty(value, ListState)

    assert instance is not None
    assert instance.targets == ["a", "b"]


# 🐍🏗️🔚
