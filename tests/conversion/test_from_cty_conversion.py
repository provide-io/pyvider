#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive TDD test suite for the CtyValue -> attrs conversion logic.
This suite validates the refactored single-path, recursive conversion
in `BaseResource.from_cty`."""

import attrs
import pytest

from pyvider.cty import CtyBool, CtyList, CtyNumber, CtyObject, CtyString, CtyValue
from pyvider.resources.base import BaseResource

# --- Test Data Structures (attrs classes) ---


@attrs.define(frozen=True)
class SimpleConfig:
    """
    Represents a config where 'count' might be unknown in a plan and
    computed in the apply, so it must be optional in the attrs model.
    """

    name: str
    enabled: bool
    count: int | None = None
    optional_field: str | None = None


@attrs.define(frozen=True)
class NestedConfig:
    id: str
    simple: SimpleConfig
    tags: list[str] | None = None


@attrs.define(frozen=True)
class CollectionConfig:
    items: list[SimpleConfig]


# --- Pytest Fixtures for CtyValue objects ---


@pytest.fixture
def simple_cty_type() -> CtyObject:
    """A fixture for the CtyObject type for SimpleConfig."""
    # CORRECTED: Explicitly mark attributes that can be unknown/null as optional
    # at the CTY level. This is crucial for validation to pass.
    return CtyObject(
        attribute_types={
            "name": CtyString(),
            "count": CtyNumber(),
            "enabled": CtyBool(),
            "optional_field": CtyString(),
        },
        optional_attributes={"count", "optional_field"},
    )


@pytest.fixture
def simple_cty_known(simple_cty_type: CtyObject) -> CtyValue:
    """A CtyValue for SimpleConfig with all known values."""
    return simple_cty_type.validate({"name": "test", "count": 10, "enabled": True})


@pytest.fixture
def simple_cty_with_null(simple_cty_type: CtyObject) -> CtyValue:
    """A CtyValue for SimpleConfig with a null optional field."""
    return simple_cty_type.validate({"name": "test", "count": 10, "enabled": True, "optional_field": None})


@pytest.fixture
def nested_cty_known(simple_cty_type: CtyObject) -> CtyValue:
    """A CtyValue for NestedConfig with all known values."""
    nested_type = CtyObject(
        attribute_types={"id": CtyString(), "simple": simple_cty_type},
        optional_attributes=frozenset(),
    )
    return nested_type.validate({"id": "nested-123", "simple": {"name": "test", "count": 10, "enabled": True}})


@pytest.fixture
def nested_cty_with_inner_unknown(simple_cty_type: CtyObject) -> CtyValue:
    """A CtyValue for NestedConfig where an inner field ('simple.count') is unknown."""
    nested_type = CtyObject(
        attribute_types={"id": CtyString(), "simple": simple_cty_type},
        optional_attributes=frozenset(),
    )
    return nested_type.validate(
        {
            "id": "nested-456",
            "simple": {
                "name": "partial",
                "count": CtyValue.unknown(CtyNumber()),
                "enabled": True,
            },
        }
    )


@pytest.fixture
def collection_cty_with_unknowns(simple_cty_type: CtyObject) -> CtyValue:
    """
    CORRECTED FIXTURE: This now creates a CtyObject that WRAPS the list,
    matching the structure of the CollectionConfig attrs class.
    """
    collection_type = CtyObject(
        attribute_types={"items": CtyList(element_type=simple_cty_type)},
        optional_attributes=frozenset(),
    )

    return collection_type.validate(
        {
            "items": [
                {"name": "item-1", "count": 1, "enabled": True},
                {"name": "item-2", "count": CtyValue.unknown(CtyNumber()), "enabled": False},
                {"name": "item-3", "count": 3, "enabled": True},
            ]
        }
    )


# --- Test Cases ---


def test_from_cty_simple_conversion(simple_cty_known: CtyValue) -> None:
    result = BaseResource.from_cty(simple_cty_known, SimpleConfig)
    assert isinstance(result, SimpleConfig)
    assert result.name == "test"
    assert result.count == 10
    assert result.enabled is True
    assert result.optional_field is None


def test_from_cty_with_null_value(simple_cty_with_null: CtyValue) -> None:
    result = BaseResource.from_cty(simple_cty_with_null, SimpleConfig)
    assert isinstance(result, SimpleConfig)
    assert result.optional_field is None


def test_from_cty_top_level_null() -> None:
    null_cty = CtyValue.null(CtyObject({"a": CtyString()}))
    result = BaseResource.from_cty(null_cty, SimpleConfig)
    assert result is None


def test_from_cty_top_level_unknown() -> None:
    unknown_cty = CtyValue.unknown(CtyObject({"a": CtyString()}))
    result = BaseResource.from_cty(unknown_cty, SimpleConfig)
    assert result is None


def test_from_cty_nested_object_conversion(nested_cty_known: CtyValue) -> None:
    result = BaseResource.from_cty(nested_cty_known, NestedConfig)
    assert isinstance(result, NestedConfig)
    assert result.id == "nested-123"
    assert isinstance(result.simple, SimpleConfig)
    assert result.simple.name == "test"


def test_from_cty_with_nested_unknown_value(nested_cty_with_inner_unknown: CtyValue) -> None:
    result = BaseResource.from_cty(nested_cty_with_inner_unknown, NestedConfig)
    assert isinstance(result, NestedConfig)
    assert result.id == "nested-456"
    assert isinstance(result.simple, SimpleConfig)
    assert result.simple.name == "partial"
    assert result.simple.enabled is True
    assert result.simple.count is None


def test_from_cty_collection_with_unknowns(collection_cty_with_unknowns: CtyValue) -> None:
    result = BaseResource.from_cty(collection_cty_with_unknowns, CollectionConfig)
    assert isinstance(result, CollectionConfig)
    assert isinstance(result.items, list)
    assert len(result.items) == 3
    assert result.items[0].name == "item-1"
    assert result.items[0].count == 1
    assert result.items[1].name == "item-2"
    assert result.items[1].count is None
    assert result.items[2].name == "item-3"
    assert result.items[2].count == 3


def test_from_cty_ignores_extra_attributes() -> None:
    cty_val = CtyObject(
        {"name": CtyString(), "count": CtyNumber(), "enabled": CtyBool(), "extra": CtyString()}
    ).validate({"name": "test", "count": 1, "enabled": True, "extra": "ignore-me"})
    result = BaseResource.from_cty(cty_val, SimpleConfig)
    assert isinstance(result, SimpleConfig)
    assert not hasattr(result, "extra")


# 🐍🏗️🔚
