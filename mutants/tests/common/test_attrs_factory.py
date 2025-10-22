"""Tests for dynamic attrs class generation utilities."""

from typing import Any

import attrs

from pyvider.common.utils.attrs_factory import create_attrs_class_from_schema
from pyvider.cty import CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.schema.types import PvsAttribute


def _get_field(cls: type, field_name: str) -> attrs.Attribute:
    """Helper to fetch an attrs field by name."""
    for field in attrs.fields(cls):
        if field.name == field_name:
            return field
    raise AssertionError(f"Expected attrs field '{field_name}' to be generated.")


def test_create_attrs_class_uses_scalar_default() -> None:
    """Scalar attributes should honour defaults and expose helpful type hints."""
    schema = {
        "name": PvsAttribute(name="name", type=CtyString(), default="acme", optional=True),
    }

    generated = create_attrs_class_from_schema("Example", schema)
    field = _get_field(generated, "name")

    instance = generated()
    assert instance.name == "acme"
    assert field.default == "acme"
    assert field.type == (str | None)


def test_create_attrs_class_uses_factory_for_mutable_defaults() -> None:
    """Collection attributes should receive fresh mutable values per instance."""
    schema = {
        "items": PvsAttribute(name="items", type=CtyList(element_type=CtyNumber())),
    }

    generated = create_attrs_class_from_schema("WithList", schema)
    field = _get_field(generated, "items")

    first = generated()
    second = generated()

    assert isinstance(field.default, attrs.Factory)
    assert field.default.factory is list

    assert first.items == []
    assert second.items == []
    assert first.items is not second.items
    assert field.type == (list | None)


def test_create_attrs_class_supports_dynamic_payloads() -> None:
    """Dynamic/object attributes should map to permissive typing information."""
    schema = {
        "payload": PvsAttribute(name="payload", type=CtyDynamic()),
    }

    generated = create_attrs_class_from_schema("DynamicValue", schema)
    field = _get_field(generated, "payload")

    instance = generated()
    assert instance.payload is None
    assert field.default is None
    assert field.type == (dict | Any | None)


def test_create_attrs_class_uses_dict_factory_for_maps() -> None:
    """Map attributes should leverage dict factories to avoid shared state."""
    schema = {
        "settings": PvsAttribute(name="settings", type=CtyMap(element_type=CtyString())),
    }

    generated = create_attrs_class_from_schema("MapConfig", schema)
    field = _get_field(generated, "settings")

    first = generated()
    second = generated()

    assert isinstance(field.default, attrs.Factory)
    assert field.default.factory is dict

    assert first.settings == {}
    assert second.settings == {}
    assert first.settings is not second.settings
    assert field.type == (dict | None)
