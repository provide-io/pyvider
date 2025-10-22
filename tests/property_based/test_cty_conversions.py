"""Property-based tests for CTY conversions using Hypothesis."""

from hypothesis import given, strategies as st, assume
import json

from pyvider.conversion.from_cty import from_cty
from pyvider.cty import CtyValue, CtyString, CtyNumber, CtyBool, CtyList, CtyMap


# Helper strategies for generating CTY values
@st.composite
def cty_string_value(draw):
    """Generate a CtyValue containing a string."""
    text = draw(st.text(min_size=0, max_size=100))
    return CtyValue(value=text, cty_type=CtyString())


@st.composite
def cty_number_value(draw):
    """Generate a CtyValue containing a number."""
    number = draw(st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)))
    return CtyValue(value=number, cty_type=CtyNumber())


@st.composite
def cty_bool_value(draw):
    """Generate a CtyValue containing a boolean."""
    boolean = draw(st.booleans())
    return CtyValue(value=boolean, cty_type=CtyBool())


@given(text=st.text(min_size=0, max_size=1000))
def test_string_conversion_preserves_value(text: str):
    """
    Property: Converting a CtyString value should preserve the string value.
    """
    cty_val = CtyValue(value=text, cty_type=CtyString())
    result = from_cty(cty_val, target_type=str)
    assert result == text
    assert isinstance(result, str)


@given(num=st.integers(min_value=-(2**53), max_value=2**53))
def test_integer_conversion_preserves_value(num: int):
    """
    Property: Converting a CtyNumber with integer value should preserve the value.
    """
    cty_val = CtyValue(value=num, cty_type=CtyNumber())
    result = from_cty(cty_val, target_type=int)
    assert result == num
    assert isinstance(result, (int, float))


@given(boolean=st.booleans())
def test_bool_conversion_preserves_value(boolean: bool):
    """
    Property: Converting a CtyBool value should preserve the boolean value.
    """
    cty_val = CtyValue(value=boolean, cty_type=CtyBool())
    result = from_cty(cty_val, target_type=bool)
    assert result == boolean
    assert isinstance(result, bool)


@given(string_list=st.lists(st.text(min_size=0, max_size=50), min_size=0, max_size=20))
def test_list_of_strings_conversion(string_list: list[str]):
    """
    Property: Converting a list of strings should preserve the list and all elements.
    """
    cty_elements = [CtyValue(value=s, cty_type=CtyString()) for s in string_list]
    cty_val = CtyValue(value=cty_elements, cty_type=CtyList(element_type=CtyString()))

    result = from_cty(cty_val, target_type=list)
    assert len(result) == len(string_list)
    assert result == string_list


@given(num_list=st.lists(st.integers(min_value=-1000, max_value=1000), min_size=0, max_size=20))
def test_list_of_numbers_conversion(num_list: list[int]):
    """
    Property: Converting a list of numbers should preserve the list and all elements.
    """
    cty_elements = [CtyValue(value=n, cty_type=CtyNumber()) for n in num_list]
    cty_val = CtyValue(value=cty_elements, cty_type=CtyList(element_type=CtyNumber()))

    result = from_cty(cty_val, target_type=list)
    assert len(result) == len(num_list)
    assert result == num_list


@given(
    string_dict=st.dictionaries(
        keys=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
        values=st.text(min_size=0, max_size=50),
        min_size=0,
        max_size=10,
    )
)
def test_map_of_strings_conversion(string_dict: dict[str, str]):
    """
    Property: Converting a map of strings should preserve the dictionary.
    """
    cty_elements = {k: CtyValue(value=v, cty_type=CtyString()) for k, v in string_dict.items()}
    cty_val = CtyValue(value=cty_elements, cty_type=CtyMap(element_type=CtyString()))

    result = from_cty(cty_val, target_type=dict)
    assert result == string_dict


@given(data=st.one_of(st.integers(), st.text(), st.booleans(), st.floats(allow_nan=False, allow_infinity=False)))
def test_json_roundtrip_for_primitives(data):
    """
    Property: Primitive values should survive JSON serialization/deserialization.
    """
    # Serialize and deserialize
    json_str = json.dumps(data)
    result = json.loads(json_str)

    # For numbers, the type might change (int -> float) but value should be close
    if isinstance(data, (int, float)):
        assert abs(result - data) < 1e-10 or result == data
    else:
        assert result == data


@given(
    nested_list=st.lists(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=5),
        min_size=0,
        max_size=5
    )
)
def test_nested_list_conversion(nested_list: list[list[int]]):
    """
    Property: Nested lists should be converted correctly.
    """
    inner_cty_lists = []
    for inner_list in nested_list:
        inner_elements = [CtyValue(value=n, cty_type=CtyNumber()) for n in inner_list]
        inner_cty_lists.append(
            CtyValue(value=inner_elements, cty_type=CtyList(element_type=CtyNumber()))
        )

    cty_val = CtyValue(
        value=inner_cty_lists,
        cty_type=CtyList(element_type=CtyList(element_type=CtyNumber()))
    )

    result = from_cty(cty_val, target_type=list)
    assert result == nested_list


@given(text=st.text(min_size=0, max_size=100))
def test_string_length_preserved(text: str):
    """
    Property: String length should be preserved through conversion.
    """
    cty_val = CtyValue(value=text, cty_type=CtyString())
    result = from_cty(cty_val, target_type=str)
    assert len(result) == len(text)
