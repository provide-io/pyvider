"""Tests for conversion utility helpers."""

from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyNumber, CtyObject, CtyString


def test_unify_and_validate_list_of_objects_handles_empty_list() -> None:
    result = unify_and_validate_list_of_objects([])

    assert isinstance(result.type, CtyList)
    assert isinstance(result.type.element_type, CtyDynamic)
    assert result.value == []


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
    assert result.value == items


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
    assert result.value == items
