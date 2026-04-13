#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for conversion utility helpers."""

from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyNumber,
    CtyObject,
    CtyString,
)


def test_unify_and_validate_list_of_objects_handles_empty_list() -> None:
    result = unify_and_validate_list_of_objects([])

    assert isinstance(result.type, CtyList)
    assert isinstance(result.type.element_type, CtyDynamic)
    assert result.value == ()


def test_unify_and_validate_list_of_objects_infers_schema() -> None:
    items = [
        {"name": "alpha", "size": 1},
        {"name": "beta", "enabled": True},
    ]

    result = unify_and_validate_list_of_objects(items)
    element_type = result.type.element_type

    assert isinstance(result.type, CtyList)
    assert isinstance(element_type, CtyObject)
    assert set(element_type.attribute_types) == {"name", "size", "enabled"}
    assert isinstance(element_type.attribute_types["name"], CtyString)
    assert isinstance(element_type.attribute_types["size"], CtyNumber)
    assert isinstance(element_type.attribute_types["enabled"], CtyBool)
    assert element_type.optional_attributes == frozenset({"size", "enabled"})

    first, second = result.value
    assert first.value["name"].value == "alpha"
    assert first.value["size"].value == 1
    # Missing keys become null values in the unified object
    assert first.value["enabled"].is_null is True

    assert second.value["name"].value == "beta"
    assert second.value["enabled"].value is True
    assert second.value["size"].is_null is True


def test_unify_and_validate_list_of_objects_promotes_conflicting_types() -> None:
    items = [
        {"value": 1},
        {"value": "one"},
    ]

    result = unify_and_validate_list_of_objects(items)
    element_type = result.type.element_type

    assert isinstance(element_type, CtyObject)
    assert isinstance(element_type.attribute_types["value"], CtyDynamic)
    assert element_type.optional_attributes == frozenset()

    first, second = result.value
    assert first.value["value"].value.value == 1
    assert second.value["value"].value.value == "one"


# 🐍🏗️🔚
