"""Property-based tests for marshaler round-trip conversions using Hypothesis."""

import pytest
from hypothesis import given, strategies as st, assume, settings
from pyvider.cty import CtyString, CtyNumber, CtyBool, CtyList, CtyMap, CtyObject, CtyDynamic
from pyvider.conversion.marshaler import marshal, unmarshal
from pyvider.schema.types.types_base import PvsString, PvsNumber, PvsBool, PvsList, PvsMap, PvsObject


# Hypothesis strategies for generating test data
@st.composite
def marshaler_primitive_value(draw):
    """Generate a primitive value for marshaler testing."""
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
        )
    )


@st.composite
def marshaler_dict(draw, max_keys=5):
    """Generate a dictionary for marshaler testing."""
    keys = draw(
        st.lists(
            st.text(
                alphabet=st.characters(
                    whitelist_categories=("Lu", "Ll"), min_codepoint=97, max_codepoint=122
                ),
                min_size=1,
                max_size=10,
            ),
            min_size=1,
            max_size=max_keys,
            unique=True,
        )
    )
    return {key: draw(marshaler_primitive_value()) for key in keys}


class TestMarshalUnmarshalRoundTrips:
    """Property-based tests for marshal/unmarshal round-trip conversions."""

    @given(value=st.text(max_size=200))
    @settings(max_examples=50)
    def test_string_roundtrip(self, value):
        """Property: String values should survive marshal->unmarshal round-trip."""
        schema = PvsString()

        # Marshal Python value to DynamicValue
        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None
        assert dynamic_value.msgpack or dynamic_value.json

        # Unmarshal back to CtyValue
        result = unmarshal(dynamic_value, schema)
        assert result.value == value

    @given(
        value=st.one_of(
            st.integers(min_value=-10**9, max_value=10**9),
            st.floats(
                min_value=-10**9,
                max_value=10**9,
                allow_nan=False,
                allow_infinity=False,
            ),
        )
    )
    @settings(max_examples=50)
    def test_number_roundtrip(self, value):
        """Property: Number values should survive marshal->unmarshal round-trip."""
        schema = PvsNumber()

        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)

        # For floating point, allow small differences
        if isinstance(value, float):
            assert abs(result.value - value) < 1e-9 or result.value == value
        else:
            assert result.value == value

    @given(value=st.booleans())
    @settings(max_examples=30)
    def test_bool_roundtrip(self, value):
        """Property: Boolean values should survive marshal->unmarshal round-trip."""
        schema = PvsBool()

        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert result.value == value
        assert isinstance(result.value, bool)

    @given(values=st.lists(st.text(max_size=50), min_size=0, max_size=20))
    @settings(max_examples=30)
    def test_list_of_strings_roundtrip(self, values):
        """Property: List of strings should survive round-trip."""
        schema = PvsList(element_type=PvsString())

        dynamic_value = marshal(values, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert len(result.value) == len(values)
        for i, expected_value in enumerate(values):
            assert result.value[i] == expected_value

    @given(values=st.lists(st.integers(min_value=-1000, max_value=1000), min_size=0, max_size=20))
    @settings(max_examples=30)
    def test_list_of_numbers_roundtrip(self, values):
        """Property: List of numbers should survive round-trip."""
        schema = PvsList(element_type=PvsNumber())

        dynamic_value = marshal(values, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert len(result.value) == len(values)
        for i, expected_value in enumerate(values):
            assert result.value[i] == expected_value

    @given(
        mapping=st.dictionaries(
            keys=st.text(min_size=1, max_size=20), values=st.text(max_size=50), min_size=1, max_size=10
        )
    )
    @settings(max_examples=30)
    def test_map_of_strings_roundtrip(self, mapping):
        """Property: Map of strings should survive round-trip."""
        schema = PvsMap(element_type=PvsString())

        dynamic_value = marshal(mapping, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert len(result.value) == len(mapping)
        for key, expected_value in mapping.items():
            assert key in result.value
            assert result.value[key] == expected_value

    @given(name=st.text(min_size=1, max_size=50), count=st.integers(min_value=0, max_value=1000))
    @settings(max_examples=30)
    def test_object_roundtrip(self, name, count):
        """Property: Object with string and number should survive round-trip."""
        schema = PvsObject(attribute_types={"name": PvsString(), "count": PvsNumber()})

        data = {"name": name, "count": count}
        dynamic_value = marshal(data, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert result.value["name"] == name
        assert result.value["count"] == count


class TestMarshalUnmarshalWithCtyTypes:
    """Property-based tests for marshal/unmarshal with CtyType schemas."""

    @given(value=st.text(max_size=200))
    @settings(max_examples=30)
    def test_string_roundtrip_with_cty_type(self, value):
        """Property: String values with CtyString schema should round-trip."""
        schema = CtyString()

        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert result.value == value

    @given(
        value=st.one_of(
            st.integers(min_value=-10000, max_value=10000),
            st.floats(
                min_value=-10000.0,
                max_value=10000.0,
                allow_nan=False,
                allow_infinity=False,
            ),
        )
    )
    @settings(max_examples=30)
    def test_number_roundtrip_with_cty_type(self, value):
        """Property: Number values with CtyNumber schema should round-trip."""
        schema = CtyNumber()

        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)

        if isinstance(value, float):
            assert abs(result.value - value) < 1e-9 or result.value == value
        else:
            assert result.value == value

    @given(value=st.booleans())
    @settings(max_examples=20)
    def test_bool_roundtrip_with_cty_type(self, value):
        """Property: Boolean values with CtyBool schema should round-trip."""
        schema = CtyBool()

        dynamic_value = marshal(value, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert result.value == value


class TestMarshalUnmarshalNestedStructures:
    """Property-based tests for nested structure round-trips."""

    @given(data=marshaler_dict(max_keys=5))
    @settings(max_examples=20)
    def test_nested_object_roundtrip(self, data):
        """Property: Nested objects should survive round-trip."""
        assume(len(data) > 0)

        # Build schema dynamically from data
        from pyvider.cty.conversion import infer_cty_type_from_raw

        attribute_types = {}
        for key, value in data.items():
            cty_type = infer_cty_type_from_raw(value)
            # Convert CtyType to PvsType
            if isinstance(cty_type, CtyString):
                attribute_types[key] = PvsString()
            elif isinstance(cty_type, CtyNumber):
                attribute_types[key] = PvsNumber()
            elif isinstance(cty_type, CtyBool):
                attribute_types[key] = PvsBool()
            else:
                attribute_types[key] = PvsDynamic()

        from pyvider.schema.types.types_base import PvsDynamic

        schema = PvsObject(attribute_types=attribute_types)

        dynamic_value = marshal(data, schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, schema)
        assert isinstance(result.value, dict)

        # Check all keys are preserved
        for key in data.keys():
            assert key in result.value

    @given(
        items=st.lists(
            st.dictionaries(
                keys=st.text(
                    min_size=1,
                    max_size=10,
                    alphabet=st.characters(min_codepoint=97, max_codepoint=122),
                ),
                values=st.text(max_size=20),
                min_size=1,
                max_size=3,
            ),
            min_size=1,
            max_size=5,
        )
    )
    @settings(max_examples=15)
    def test_list_of_objects_roundtrip(self, items):
        """Property: List of objects should survive round-trip."""
        assume(len(items) > 0)

        # Get all unique keys across all items
        all_keys = set()
        for item in items:
            all_keys.update(item.keys())

        # Build object schema with all keys as strings
        obj_schema = PvsObject(
            attribute_types={key: PvsString() for key in all_keys},
            optional_attributes=frozenset(all_keys),
        )

        list_schema = PvsList(element_type=obj_schema)

        dynamic_value = marshal(items, list_schema)
        assert dynamic_value is not None

        result = unmarshal(dynamic_value, list_schema)
        assert len(result.value) == len(items)


class TestMarshalUnmarshalEmptyValues:
    """Property-based tests for empty/edge case values."""

    @settings(max_examples=10)
    def test_empty_string_roundtrip(self):
        """Property: Empty string should round-trip correctly."""
        schema = PvsString()
        value = ""

        dynamic_value = marshal(value, schema)
        result = unmarshal(dynamic_value, schema)
        assert result.value == ""

    @settings(max_examples=10)
    def test_empty_list_roundtrip(self):
        """Property: Empty list should round-trip correctly."""
        schema = PvsList(element_type=PvsString())
        value = []

        dynamic_value = marshal(value, schema)
        result = unmarshal(dynamic_value, schema)
        assert len(result.value) == 0

    @settings(max_examples=10)
    def test_empty_map_roundtrip(self):
        """Property: Empty map should round-trip correctly."""
        schema = PvsMap(element_type=PvsString())
        value = {}

        dynamic_value = marshal(value, schema)
        result = unmarshal(dynamic_value, schema)
        assert len(result.value) == 0

    @given(value=st.integers(min_value=-10**6, max_value=10**6))
    @settings(max_examples=30)
    def test_zero_and_negative_numbers_roundtrip(self, value):
        """Property: Zero and negative numbers should round-trip correctly."""
        schema = PvsNumber()

        dynamic_value = marshal(value, schema)
        result = unmarshal(dynamic_value, schema)
        assert result.value == value
