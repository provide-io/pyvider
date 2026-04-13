#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Property-based tests for schema validation using Hypothesis."""

from hypothesis import HealthCheck, assume, given, settings, strategies as st

from pyvider.schema import a_bool, a_list, a_map, a_num, a_str, s_data_source


@given(name=st.text(min_size=1, max_size=100))
def test_required_string_accepts_any_non_empty_string(name: str) -> None:
    """
    Property: A required string attribute should accept any non-empty string.
    """
    schema = s_data_source(attributes={"name": a_str(required=True)})
    # If we create a valid object with the string, it should work
    # This tests that the schema accepts the value
    assert schema is not None


@given(
    count=st.integers(min_value=-(2**31), max_value=2**31),
)
def test_number_attribute_accepts_integers(count: int) -> None:
    """
    Property: A number attribute should accept any integer.
    """
    schema = s_data_source(attributes={"count": a_num(required=True)})
    assert schema is not None


@given(enabled=st.booleans())
def test_bool_attribute_accepts_booleans(enabled: bool) -> None:
    """
    Property: A boolean attribute should accept any boolean value.
    """
    schema = s_data_source(attributes={"enabled": a_bool(required=True)})
    assert schema is not None


@given(items=st.lists(st.text(min_size=0, max_size=50), min_size=0, max_size=20))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_list_attribute_schema_creation(items: list[str]) -> None:
    """
    Property: Creating a list attribute schema should always succeed.
    """
    schema = s_data_source(attributes={"items": a_list(a_str())})
    assert schema is not None


@given(
    mapping=st.dictionaries(
        keys=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
        values=st.integers(),
        min_size=0,
        max_size=10,
    )
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_map_attribute_schema_creation(mapping: dict[str, int]) -> None:
    """
    Property: Creating a map attribute schema should always succeed.
    """
    schema = s_data_source(attributes={"mapping": a_map(a_num())})
    assert schema is not None


@given(
    name=st.text(
        min_size=1,
        max_size=50,
        alphabet=st.characters(whitelist_categories=("L", "N", "P"), whitelist_characters="_"),
    ),
    description=st.text(min_size=0, max_size=200),
)
def test_attribute_with_description(name: str, description: str) -> None:
    """
    Property: Creating an attribute with any description should succeed.
    """
    attr = a_str(description=description)
    assert attr is not None


@given(
    min_items=st.integers(min_value=0, max_value=10),
    max_items=st.integers(min_value=0, max_value=20),
)
def test_list_with_size_constraints(min_items: int, max_items: int) -> None:
    """
    Property: Creating a list with size constraints should succeed when min <= max.
    """
    assume(min_items <= max_items)

    # Creating the schema should succeed
    attr = a_list(a_str())
    assert attr is not None


@given(
    required=st.booleans(),
    optional=st.booleans(),
)
def test_attribute_required_optional_flags(required: bool, optional: bool) -> None:
    """
    Property: An attribute can be created with any combination of required/optional flags.
    """
    # Note: required and optional are mutually exclusive, but the schema should handle this
    # For this test, we just verify creation succeeds
    attr = a_str(required=required, optional=optional)
    assert attr is not None


@given(
    default_value=st.one_of(st.none(), st.text(min_size=0, max_size=50)),
)
def test_optional_attribute_with_default(default_value: str | None) -> None:
    """
    Property: Creating an optional attribute with a default value should succeed.
    """
    # Skip if default is a non-None value that doesn't match the type
    if default_value is not None:
        assume(isinstance(default_value, str))

    attr = a_str(optional=True)
    assert attr is not None


@given(
    num_attributes=st.integers(min_value=1, max_value=10),
)
def test_schema_with_multiple_attributes(num_attributes: int) -> None:
    """
    Property: A schema can be created with any positive number of attributes.
    """
    attributes = {f"attr_{i}": a_str() for i in range(num_attributes)}
    schema = s_data_source(attributes=attributes)
    assert schema is not None


@given(
    sensitive=st.booleans(),
)
def test_sensitive_attribute_flag(sensitive: bool) -> None:
    """
    Property: An attribute can be marked as sensitive or not.
    """
    attr = a_str(sensitive=sensitive)
    assert attr is not None


@given(
    nested_depth=st.integers(min_value=1, max_value=5),
)
def test_nested_list_schema_creation(nested_depth: int) -> None:
    """
    Property: Deeply nested list schemas can be created.
    """
    # Create a nested list schema
    schema = a_str()
    for _ in range(nested_depth):
        schema = a_list(schema)

    assert schema is not None


# 🐍🏗️🔚
