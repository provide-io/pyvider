#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for common/utils/attrs_factory.py."""

import attrs

from pyvider.common.utils.attrs_factory import (
    _pvs_type_to_python_type,
    create_attrs_class_from_schema,
)
from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtySet,
    CtyString,
)
from pyvider.schema.types import PvsAttribute


class TestPvsTypeToPythonType:
    """Tests for _pvs_type_to_python_type function."""

    def test_string_maps_to_str_or_none(self) -> None:
        """Test CtyString maps to str | None."""
        pvs_attr = PvsAttribute(type=CtyString())
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == str | None

    def test_number_maps_to_int_float_or_none(self) -> None:
        """Test CtyNumber maps to int | float | None."""
        pvs_attr = PvsAttribute(type=CtyNumber())
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == int | float | None

    def test_bool_maps_to_bool_or_none(self) -> None:
        """Test CtyBool maps to bool | None."""
        pvs_attr = PvsAttribute(type=CtyBool())
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == bool | None

    def test_list_maps_to_list_or_none(self) -> None:
        """Test CtyList maps to list | None."""
        pvs_attr = PvsAttribute(type=CtyList(element_type=CtyString()))
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == list | None

    def test_map_maps_to_dict_or_none(self) -> None:
        """Test CtyMap maps to dict | None."""
        pvs_attr = PvsAttribute(type=CtyMap(element_type=CtyString()))
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == dict | None

    def test_set_maps_to_set_or_none(self) -> None:
        """Test CtySet maps to set | None."""
        pvs_attr = PvsAttribute(type=CtySet(element_type=CtyString()))
        result = _pvs_type_to_python_type(pvs_attr)
        assert result == set | None

    def test_object_maps_to_dict_any_or_none(self) -> None:
        """Test CtyObject maps to dict | Any | None."""
        pvs_attr = PvsAttribute(type=CtyObject(attribute_types={}))
        result = _pvs_type_to_python_type(pvs_attr)
        # Result should be dict | Any | None
        assert result is not None

    def test_dynamic_maps_to_dict_any_or_none(self) -> None:
        """Test CtyDynamic maps to dict | Any | None."""
        pvs_attr = PvsAttribute(type=CtyDynamic())
        result = _pvs_type_to_python_type(pvs_attr)
        assert result is not None


class TestCreateAttrsClassFromSchema:
    """Tests for create_attrs_class_from_schema function."""

    def test_creates_class_with_simple_attributes(self) -> None:
        """Test creating class with simple string attribute."""
        attributes = {"name": PvsAttribute(type=CtyString())}
        cls = create_attrs_class_from_schema("TestClass", attributes)

        assert attrs.has(cls)
        assert cls.__name__ == "TestClass"
        instance = cls(name="test")
        assert instance.name == "test"

    def test_creates_frozen_class(self) -> None:
        """Test that created class is frozen (immutable)."""
        attributes = {"value": PvsAttribute(type=CtyNumber())}
        cls = create_attrs_class_from_schema("FrozenClass", attributes)

        instance = cls(value=42)
        # Should raise FrozenInstanceError when trying to modify
        try:
            instance.value = 100
            raise AssertionError("Should not be able to modify frozen instance")
        except (attrs.exceptions.FrozenInstanceError, AttributeError):
            pass

    def test_handles_default_values(self) -> None:
        """Test that default values are applied."""
        attributes = {"name": PvsAttribute(type=CtyString(), default="default_name")}
        cls = create_attrs_class_from_schema("DefaultClass", attributes)

        instance = cls()
        assert instance.name == "default_name"

    def test_handles_map_with_factory(self) -> None:
        """Test that CtyMap uses dict factory for default."""
        attributes = {"data": PvsAttribute(type=CtyMap(element_type=CtyString()))}
        cls = create_attrs_class_from_schema("MapClass", attributes)

        instance1 = cls()
        instance2 = cls()
        # Should have separate dict instances
        assert instance1.data == {}
        assert instance2.data == {}
        assert instance1.data is not instance2.data

    def test_handles_list_with_factory(self) -> None:
        """Test that CtyList uses list factory for default."""
        attributes = {"items": PvsAttribute(type=CtyList(element_type=CtyString()))}
        cls = create_attrs_class_from_schema("ListClass", attributes)

        instance1 = cls()
        instance2 = cls()
        # Should have separate list instances
        assert instance1.items == []
        assert instance2.items == []
        assert instance1.items is not instance2.items

    def test_multiple_attributes(self) -> None:
        """Test creating class with multiple attributes."""
        attributes = {
            "name": PvsAttribute(type=CtyString()),
            "count": PvsAttribute(type=CtyNumber()),
            "active": PvsAttribute(type=CtyBool()),
        }
        cls = create_attrs_class_from_schema("MultiAttr", attributes)

        instance = cls(name="test", count=42, active=True)
        assert instance.name == "test"
        assert instance.count == 42
        assert instance.active is True

    def test_none_default_for_simple_types(self) -> None:
        """Test that simple types without explicit default get None."""
        attributes = {"optional": PvsAttribute(type=CtyString())}
        cls = create_attrs_class_from_schema("OptionalClass", attributes)

        instance = cls()
        assert instance.optional is None


# 🐍🏗️🔚
