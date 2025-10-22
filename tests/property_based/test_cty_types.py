"""Property-based tests for CTY type system using Hypothesis."""

from decimal import Decimal

from hypothesis import given, strategies as st
import pytest

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyString,
    CtyValue,
)


# Custom strategies for generating CTY values
@st.composite
def cty_string_values(draw):
    """Generate valid string values for CTY."""
    return CtyValue(draw(st.text(min_size=0, max_size=100)))


@st.composite
def cty_number_values(draw):
    """Generate valid number values for CTY."""
    choice = draw(st.integers(0, 2))
    if choice == 0:
        return CtyValue(draw(st.integers()))
    elif choice == 1:
        return CtyValue(draw(st.floats(allow_nan=False, allow_infinity=False)))
    else:
        return CtyValue(Decimal(draw(st.integers())))


@st.composite
def cty_bool_values(draw):
    """Generate valid boolean values for CTY."""
    return CtyValue(draw(st.booleans()))


class TestCtyStringPropertyBased:
    """Property-based tests for CtyString."""

    @given(text=st.text(min_size=0, max_size=1000))
    def test_cty_string_accepts_any_text(self, text: str):
        """Property: CtyString should accept any text value."""
        cty_type = CtyString()
        value = CtyValue(text)
        # Should not raise
        assert value.python_value == text

    @given(text=st.text(min_size=1))
    def test_cty_string_preserves_content(self, text: str):
        """Property: CtyString should preserve the exact content."""
        value = CtyValue(text)
        assert value.python_value == text

    @given(text=st.text())
    def test_cty_string_length_preserved(self, text: str):
        """Property: String length should be preserved."""
        value = CtyValue(text)
        assert len(value.python_value) == len(text)


class TestCtyNumberPropertyBased:
    """Property-based tests for CtyNumber."""

    @given(num=st.integers())
    def test_cty_number_accepts_integers(self, num: int):
        """Property: CtyNumber should accept any integer."""
        cty_type = CtyNumber()
        value = CtyValue(num)
        assert value.python_value == num

    @given(num=st.floats(allow_nan=False, allow_infinity=False))
    def test_cty_number_accepts_floats(self, num: float):
        """Property: CtyNumber should accept finite floats."""
        cty_type = CtyNumber()
        value = CtyValue(num)
        assert value.python_value == num

    @given(num=st.integers(min_value=0, max_value=1000000))
    def test_cty_number_preserves_integer_value(self, num: int):
        """Property: Integer values should be preserved exactly."""
        value = CtyValue(num)
        assert value.python_value == num
        assert isinstance(value.python_value, int)

    @given(
        a=st.integers(min_value=-1000, max_value=1000),
        b=st.integers(min_value=-1000, max_value=1000)
    )
    def test_cty_number_comparison(self, a: int, b: int):
        """Property: Number comparison should match Python comparison."""
        val_a = CtyValue(a)
        val_b = CtyValue(b)
        # Values should maintain their numerical relationship
        if a < b:
            assert val_a.python_value < val_b.python_value
        elif a > b:
            assert val_a.python_value > val_b.python_value
        else:
            assert val_a.python_value == val_b.python_value


class TestCtyBoolPropertyBased:
    """Property-based tests for CtyBool."""

    @given(value=st.booleans())
    def test_cty_bool_accepts_boolean(self, value: bool):
        """Property: CtyBool should accept any boolean value."""
        cty_type = CtyBool()
        cty_value = CtyValue(value)
        assert cty_value.python_value == value

    @given(value=st.booleans())
    def test_cty_bool_preserves_value(self, value: bool):
        """Property: Boolean values should be preserved exactly."""
        cty_value = CtyValue(value)
        assert cty_value.python_value is value

    @given(value=st.booleans())
    def test_cty_bool_negation(self, value: bool):
        """Property: Negation should work consistently."""
        cty_value = CtyValue(value)
        assert cty_value.python_value == value
        assert (not cty_value.python_value) == (not value)


class TestCtyListPropertyBased:
    """Property-based tests for CtyList."""

    @given(items=st.lists(st.text(), max_size=50))
    def test_cty_list_string_elements(self, items: list[str]):
        """Property: CtyList should accept lists of strings."""
        cty_type = CtyList(element_type=CtyString())
        value = CtyValue(items)
        assert value.python_value == items

    @given(items=st.lists(st.integers(), max_size=50))
    def test_cty_list_number_elements(self, items: list[int]):
        """Property: CtyList should accept lists of numbers."""
        cty_type = CtyList(element_type=CtyNumber())
        value = CtyValue(items)
        assert value.python_value == items

    @given(items=st.lists(st.booleans(), max_size=50))
    def test_cty_list_bool_elements(self, items: list[bool]):
        """Property: CtyList should accept lists of booleans."""
        cty_type = CtyList(element_type=CtyBool())
        value = CtyValue(items)
        assert value.python_value == items

    @given(items=st.lists(st.text(), min_size=0, max_size=100))
    def test_cty_list_preserves_length(self, items: list[str]):
        """Property: List length should be preserved."""
        value = CtyValue(items)
        assert len(value.python_value) == len(items)

    @given(items=st.lists(st.integers(), min_size=1, max_size=50))
    def test_cty_list_preserves_order(self, items: list[int]):
        """Property: List order should be preserved."""
        value = CtyValue(items)
        assert value.python_value == items
        for i, item in enumerate(items):
            assert value.python_value[i] == item

    @given(items=st.lists(st.text(), min_size=0, max_size=50))
    def test_cty_list_empty_list_handling(self, items: list[str]):
        """Property: Empty lists should be handled correctly."""
        value = CtyValue(items)
        if len(items) == 0:
            assert value.python_value == []
        else:
            assert len(value.python_value) > 0


class TestCtyMapPropertyBased:
    """Property-based tests for CtyMap."""

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.text(), max_size=20))
    def test_cty_map_string_values(self, mapping: dict[str, str]):
        """Property: CtyMap should accept dicts with string values."""
        cty_type = CtyMap(element_type=CtyString())
        value = CtyValue(mapping)
        assert value.python_value == mapping

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.integers(), max_size=20))
    def test_cty_map_number_values(self, mapping: dict[str, int]):
        """Property: CtyMap should accept dicts with number values."""
        cty_type = CtyMap(element_type=CtyNumber())
        value = CtyValue(mapping)
        assert value.python_value == mapping

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.booleans(), max_size=20))
    def test_cty_map_bool_values(self, mapping: dict[str, bool]):
        """Property: CtyMap should accept dicts with bool values."""
        cty_type = CtyMap(element_type=CtyBool())
        value = CtyValue(mapping)
        assert value.python_value == mapping

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.text(), min_size=0, max_size=50))
    def test_cty_map_preserves_size(self, mapping: dict[str, str]):
        """Property: Map size should be preserved."""
        value = CtyValue(mapping)
        assert len(value.python_value) == len(mapping)

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.integers(), min_size=1, max_size=20))
    def test_cty_map_preserves_keys(self, mapping: dict[str, int]):
        """Property: Map keys should be preserved."""
        value = CtyValue(mapping)
        assert set(value.python_value.keys()) == set(mapping.keys())

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=20), st.integers(), min_size=1, max_size=20))
    def test_cty_map_preserves_values(self, mapping: dict[str, int]):
        """Property: Map values should be preserved."""
        value = CtyValue(mapping)
        for key, val in mapping.items():
            assert value.python_value[key] == val


class TestCtyDynamicPropertyBased:
    """Property-based tests for CtyDynamic."""

    @given(value=st.one_of(
        st.text(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.lists(st.text(), max_size=20),
        st.dictionaries(st.text(min_size=1, max_size=10), st.text(), max_size=10)
    ))
    def test_cty_dynamic_accepts_any_value(self, value):
        """Property: CtyDynamic should accept any value type."""
        cty_type = CtyDynamic()
        cty_value = CtyValue(value)
        # Should not raise
        assert cty_value.python_value == value


class TestCtyValueConversionPropertyBased:
    """Property-based tests for type conversions."""

    @given(text=st.text(min_size=0, max_size=100))
    def test_string_round_trip(self, text: str):
        """Property: String values should survive round-trip conversion."""
        value = CtyValue(text)
        result = value.python_value
        assert result == text
        assert type(result) == type(text)

    @given(num=st.integers(min_value=-1000000, max_value=1000000))
    def test_integer_round_trip(self, num: int):
        """Property: Integer values should survive round-trip conversion."""
        value = CtyValue(num)
        result = value.python_value
        assert result == num
        assert isinstance(result, int)

    @given(items=st.lists(st.text(), max_size=30))
    def test_list_round_trip(self, items: list[str]):
        """Property: List values should survive round-trip conversion."""
        value = CtyValue(items)
        result = value.python_value
        assert result == items
        assert len(result) == len(items)

    @given(mapping=st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), max_size=20))
    def test_dict_round_trip(self, mapping: dict[str, int]):
        """Property: Dict values should survive round-trip conversion."""
        value = CtyValue(mapping)
        result = value.python_value
        assert result == mapping
        assert len(result) == len(mapping)


class TestCtyNestedStructuresPropertyBased:
    """Property-based tests for nested CTY structures."""

    @given(nested=st.lists(st.lists(st.text(), max_size=5), max_size=5))
    def test_nested_lists(self, nested: list[list[str]]):
        """Property: Nested lists should be handled correctly."""
        value = CtyValue(nested)
        assert value.python_value == nested

    @given(nested=st.dictionaries(
        st.text(min_size=1, max_size=10),
        st.dictionaries(st.text(min_size=1, max_size=10), st.text(), max_size=3),
        max_size=5
    ))
    def test_nested_maps(self, nested: dict[str, dict[str, str]]):
        """Property: Nested maps should be handled correctly."""
        value = CtyValue(nested)
        assert value.python_value == nested

    @given(nested=st.lists(
        st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), max_size=3),
        max_size=5
    ))
    def test_list_of_maps(self, nested: list[dict[str, int]]):
        """Property: Lists of maps should be handled correctly."""
        value = CtyValue(nested)
        assert value.python_value == nested


class TestCtyEdgeCases:
    """Property-based tests for edge cases."""

    @given(size=st.integers(min_value=0, max_value=1000))
    def test_large_lists(self, size: int):
        """Property: Large lists should be handled correctly."""
        items = ["item"] * size
        value = CtyValue(items)
        assert len(value.python_value) == size

    @given(text=st.text(min_size=0, max_size=10000))
    def test_very_long_strings(self, text: str):
        """Property: Very long strings should be handled correctly."""
        value = CtyValue(text)
        assert value.python_value == text
        assert len(value.python_value) == len(text)

    def test_empty_list(self):
        """Property: Empty lists should work."""
        value = CtyValue([])
        assert value.python_value == []
        assert len(value.python_value) == 0

    def test_empty_dict(self):
        """Property: Empty dicts should work."""
        value = CtyValue({})
        assert value.python_value == {}
        assert len(value.python_value) == 0

    @given(text=st.text())
    def test_unicode_strings(self, text: str):
        """Property: Unicode strings should be handled correctly."""
        value = CtyValue(text)
        assert value.python_value == text
