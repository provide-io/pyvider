#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Property-based tests for CTY type conversions using Hypothesis."""

from hypothesis import HealthCheck, assume, given, settings, strategies as st
import pytest

from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtyString,
    CtyValue,
)


# Hypothesis strategies for generating test data
@st.composite
def cty_primitive_value(draw: st.DrawFn) -> str | int | float | bool | None:
    """Generate a primitive Python value compatible with CTY types."""
    return draw(
        st.one_of(
            st.text(max_size=100),
            st.integers(min_value=-1000000, max_value=1000000),
            st.floats(
                min_value=-1000000.0,
                max_value=1000000.0,
                allow_nan=False,
                allow_infinity=False,
            ),
            st.booleans(),
            st.none(),
        )
    )


@st.composite
def cty_dict(draw: st.DrawFn, max_keys: int = 5) -> dict[str, str | int | float | bool | None]:
    """Generate a dictionary compatible with CtyObject."""
    keys = draw(
        st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("Lu", "Ll"), min_codepoint=97, max_codepoint=122),
                min_size=1,
                max_size=10,
            ),
            min_size=0,
            max_size=max_keys,
            unique=True,
        )
    )
    return {key: draw(cty_primitive_value()) for key in keys}


@st.composite
def cty_list_of_dicts(
    draw: st.DrawFn, min_items: int = 0, max_items: int = 5
) -> list[dict[str, str | int | float | bool | None]]:
    """Generate a list of dictionaries for testing unify_and_validate_list_of_objects."""
    size = draw(st.integers(min_value=min_items, max_value=max_items))
    return [draw(cty_dict()) for _ in range(size)]


class TestCtyStringValidation:
    """Property-based tests for CtyString validation."""

    @given(text=st.text(max_size=1000))
    @settings(max_examples=50)
    def test_string_accepts_any_text(self, text: str) -> None:
        """Property: CtyString should accept any text value."""
        import unicodedata

        # Normalize input to avoid Unicode compatibility character issues
        # where the same visual character has multiple representations
        text = unicodedata.normalize("NFC", text)
        cty_str = CtyString()
        result = cty_str.validate(text)
        assert isinstance(result, CtyValue)
        assert unicodedata.normalize("NFC", result.value) == text

    @given(value=st.one_of(st.integers(), st.floats(), st.booleans()))
    @settings(max_examples=30)
    def test_string_rejects_non_string_primitives(self, value: int | float | bool) -> None:
        """Property: CtyString should reject non-string primitive types."""
        from pyvider.cty.exceptions.validation import CtyStringValidationError

        cty_str = CtyString()
        with pytest.raises((TypeError, ValueError, CtyStringValidationError)):
            cty_str.validate(value)


class TestCtyNumberValidation:
    """Property-based tests for CtyNumber validation."""

    @given(
        num=st.one_of(
            st.integers(min_value=-(10**6), max_value=10**6),
            st.floats(
                min_value=-(10**6),
                max_value=10**6,
                allow_nan=False,
                allow_infinity=False,
            ),
        )
    )
    @settings(max_examples=50)
    def test_number_accepts_numeric_values(self, num: int | float) -> None:
        """Property: CtyNumber should accept integers and floats."""
        from decimal import Decimal

        cty_num = CtyNumber()
        result = cty_num.validate(num)
        assert isinstance(result, CtyValue)
        # CtyNumber returns Decimal values
        assert isinstance(result.value, Decimal)

    @given(value=st.text(min_size=1, alphabet=st.characters(whitelist_categories=("Lu", "Ll"))))
    @settings(max_examples=30)
    def test_number_rejects_non_numeric_types(self, value: str) -> None:
        """Property: CtyNumber should reject non-numeric string types."""
        from pyvider.cty.exceptions.validation import CtyNumberValidationError

        # Skip special float strings that Python accepts
        if value.lower() in ("infinity", "inf", "nan"):
            return

        cty_num = CtyNumber()
        with pytest.raises((TypeError, ValueError, CtyNumberValidationError)):
            cty_num.validate(value)


class TestCtyBoolValidation:
    """Property-based tests for CtyBool validation."""

    @given(value=st.booleans())
    @settings(max_examples=20)
    def test_bool_accepts_boolean_values(self, value: bool) -> None:
        """Property: CtyBool should accept boolean values."""
        cty_bool = CtyBool()
        result = cty_bool.validate(value)
        assert isinstance(result, CtyValue)
        assert result.value == value
        assert isinstance(result.value, bool)


class TestCtyListValidation:
    """Property-based tests for CtyList validation."""

    @given(items=st.lists(st.text(max_size=50), max_size=20))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_list_of_strings_validates(self, items: list[str]) -> None:
        """Property: CtyList(CtyString) should accept lists of strings."""
        cty_list = CtyList(element_type=CtyString())
        result = cty_list.validate(items)
        assert isinstance(result, CtyValue)
        assert len(result.value) == len(items)

    @given(items=st.lists(st.integers(min_value=-1000, max_value=1000), max_size=20))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_list_of_numbers_validates(self, items: list[int]) -> None:
        """Property: CtyList(CtyNumber) should accept lists of numbers."""
        cty_list = CtyList(element_type=CtyNumber())
        result = cty_list.validate(items)
        assert isinstance(result, CtyValue)
        assert len(result.value) == len(items)

    @given(items=st.lists(st.booleans(), max_size=20))
    @settings(max_examples=20)
    def test_list_of_bools_validates(self, items: list[bool]) -> None:
        """Property: CtyList(CtyBool) should accept lists of booleans."""
        cty_list = CtyList(element_type=CtyBool())
        result = cty_list.validate(items)
        assert isinstance(result, CtyValue)
        assert len(result.value) == len(items)

    def test_empty_list_validates(self) -> None:
        """Property: CtyList should accept empty lists."""
        cty_list = CtyList(element_type=CtyDynamic())
        result = cty_list.validate([])
        assert isinstance(result, CtyValue)
        assert len(result.value) == 0


class TestCtyMapValidation:
    """Property-based tests for CtyMap validation."""

    @given(
        mapping=st.dictionaries(
            keys=st.text(min_size=1, max_size=20), values=st.text(max_size=50), max_size=10
        )
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_map_of_strings_validates(self, mapping: dict[str, str]) -> None:
        """Property: CtyMap(CtyString) should accept dicts with string values."""
        cty_map = CtyMap(element_type=CtyString())
        result = cty_map.validate(mapping)
        assert isinstance(result, CtyValue)
        assert len(result.value) == len(mapping)

    @given(
        mapping=st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.integers(min_value=-1000, max_value=1000),
            max_size=10,
        )
    )
    @settings(max_examples=30)
    def test_map_of_numbers_validates(self, mapping: dict[str, int]) -> None:
        """Property: CtyMap(CtyNumber) should accept dicts with number values."""
        cty_map = CtyMap(element_type=CtyNumber())
        result = cty_map.validate(mapping)
        assert isinstance(result, CtyValue)
        assert len(result.value) == len(mapping)


class TestCtyObjectValidation:
    """Property-based tests for CtyObject validation."""

    @given(name=st.text(min_size=1, max_size=50), age=st.integers(min_value=0, max_value=150))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_object_with_fixed_schema_validates(self, name: str, age: int) -> None:
        """Property: CtyObject should validate objects matching its schema."""
        import unicodedata

        # Normalize to avoid Unicode compatibility character issues
        name = unicodedata.normalize("NFC", name)
        cty_obj = CtyObject(attribute_types={"name": CtyString(), "age": CtyNumber()})
        data = {"name": name, "age": age}
        result = cty_obj.validate(data)
        assert isinstance(result, CtyValue)
        # CtyObject values contain CtyValue objects for each attribute
        assert unicodedata.normalize("NFC", result.value["name"].value) == name
        from decimal import Decimal

        assert isinstance(result.value["age"].value, Decimal)

    @given(data=cty_dict(max_keys=5))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_dynamic_object_validates_any_dict(self, data: dict) -> None:
        """Property: CtyObject with inferred types should validate any dict."""
        # Skip if empty dict (no attributes to infer)
        assume(len(data) > 0)

        # Infer types from the data
        from pyvider.cty.conversion import infer_cty_type_from_raw

        attribute_types = {k: infer_cty_type_from_raw(v) for k, v in data.items()}

        cty_obj = CtyObject(attribute_types=attribute_types)
        result = cty_obj.validate(data)
        assert isinstance(result, CtyValue)


class TestUnifyAndValidateListOfObjects:
    """Property-based tests for unify_and_validate_list_of_objects utility."""

    @given(dict_list=cty_list_of_dicts(min_items=1, max_items=5))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_unify_returns_cty_value(self, dict_list: list[dict]) -> None:
        """Property: unify_and_validate_list_of_objects should return a CtyValue."""
        assume(len(dict_list) > 0)
        result = unify_and_validate_list_of_objects(dict_list)
        assert isinstance(result, CtyValue)

    @given(dict_list=cty_list_of_dicts(min_items=1, max_items=5))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_unify_preserves_list_length(self, dict_list: list[dict]) -> None:
        """Property: Result should have same length as input list."""
        assume(len(dict_list) > 0)
        result = unify_and_validate_list_of_objects(dict_list)
        assert len(result.value) == len(dict_list)

    def test_unify_empty_list_returns_dynamic(self) -> None:
        """Property: Empty list should return CtyList(CtyDynamic) with empty value."""
        result = unify_and_validate_list_of_objects([])
        assert isinstance(result, CtyValue)
        assert len(result.value) == 0

    @given(
        common_keys=st.lists(
            st.text(min_size=1, max_size=10, alphabet=st.characters(min_codepoint=97, max_codepoint=122)),
            min_size=1,
            max_size=3,
            unique=True,
        )
    )
    @settings(max_examples=20)
    def test_unify_with_common_keys_preserves_keys(self, common_keys: list[str]) -> None:
        """Property: Common keys across all dicts should be non-optional."""
        # Create a list where all dicts have the same keys
        dict_list = [{key: f"value_{i}_{key}" for key in common_keys} for i in range(3)]

        result = unify_and_validate_list_of_objects(dict_list)
        assert isinstance(result, CtyValue)
        assert len(result.value) == 3

        # All items should have all the common keys
        for item in result.value:
            for key in common_keys:
                assert key in item


class TestCtyTypeEquality:
    """Property-based tests for CTY type equality."""

    def test_same_primitive_types_are_equal(self) -> None:
        """Property: Two instances of the same primitive type should be equal."""
        assert CtyString().equal(CtyString())
        assert CtyNumber().equal(CtyNumber())
        assert CtyBool().equal(CtyBool())
        assert CtyDynamic().equal(CtyDynamic())

    def test_different_primitive_types_are_not_equal(self) -> None:
        """Property: Different primitive types should not be equal."""
        assert not CtyString().equal(CtyNumber())
        assert not CtyNumber().equal(CtyBool())
        assert not CtyBool().equal(CtyString())

    def test_list_types_with_same_element_type_are_equal(self) -> None:
        """Property: CtyList with same element type should be equal."""
        list1 = CtyList(element_type=CtyString())
        list2 = CtyList(element_type=CtyString())
        assert list1.equal(list2)

    def test_list_types_with_different_element_types_are_not_equal(self) -> None:
        """Property: CtyList with different element types should not be equal."""
        list1 = CtyList(element_type=CtyString())
        list2 = CtyList(element_type=CtyNumber())
        assert not list1.equal(list2)


# 🐍🏗️🔚
