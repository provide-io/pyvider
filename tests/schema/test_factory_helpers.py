#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import pytest

from pyvider.cty.types import (
    CtyBool,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtySet,
    CtyString,
)
from pyvider.cty.values import CtyValue
from pyvider.schema.factory import (
    a_bool,
    a_list,
    a_map,
    a_null,
    a_num,
    a_obj,
    a_set,
    a_str,
    a_unknown,
    s_resource,
)


class TestAUnknownHelper:
    """
    Defines the complete behavior for the a_unknown() helper.
    """

    @pytest.mark.parametrize(
        "schema_builder, expected_type",
        [
            (a_str(), CtyString()),
            (a_num(), CtyNumber()),
            (a_bool(), CtyBool()),
            (a_list(a_str()), CtyList(element_type=CtyString())),
            (a_set(a_num()), CtySet(element_type=CtyNumber())),
            (a_map(a_bool()), CtyMap(element_type=CtyBool())),
        ],
        ids=["string", "number", "bool", "list(string)", "set(number)", "map(bool)"],
    )
    def test_a_unknown_with_various_types(self, schema_builder: Any, expected_type: Any) -> None:
        result = a_unknown(schema_builder)
        assert isinstance(result, CtyValue)
        assert result.is_unknown, "Value MUST be unknown"
        assert not result.is_null, "Value MUST NOT be null"
        assert result.vtype.equal(expected_type), "The CtyType of the value must match the schema"

    def test_a_unknown_with_complex_object_schema(self) -> None:
        schema_builder = s_resource(
            attributes={
                "name": a_str(),
                "ports": a_list(a_num()),
            }
        )
        result = a_unknown(schema_builder)
        assert isinstance(result, CtyValue)
        assert result.is_unknown
        assert not result.is_null
        assert result.vtype.equal(schema_builder.block.to_cty_type())
        assert isinstance(result.vtype, CtyObject)

    @pytest.mark.parametrize("invalid_input", ["not a schema builder", 12345, None])
    def test_a_unknown_raises_type_error_for_invalid_input(self, invalid_input: Any) -> None:
        with pytest.raises(TypeError, match=r"a_unknown.. expects a schema builder instance"):
            a_unknown(invalid_input)


class TestANullHelper:
    """
    Defines the complete behavior for the a_null() helper.
    """

    @pytest.mark.parametrize(
        "schema_builder, expected_type",
        [
            (a_str(), CtyString()),
            (a_num(), CtyNumber()),
            (a_bool(), CtyBool()),
            (a_list(a_str()), CtyList(element_type=CtyString())),
            (a_set(a_num()), CtySet(element_type=CtyNumber())),
            (a_map(a_bool()), CtyMap(element_type=CtyBool())),
        ],
        ids=["string", "number", "bool", "list(string)", "set(number)", "map(bool)"],
    )
    def test_a_null_with_various_types(self, schema_builder: Any, expected_type: Any) -> None:
        result = a_null(schema_builder)
        assert isinstance(result, CtyValue)
        assert not result.is_unknown, "Null values are always considered known"
        assert result.is_null, "Value MUST be null"
        assert result.vtype.equal(expected_type), "The CtyType of the value must match the schema"

    def test_a_null_with_complex_object_schema(self) -> None:
        schema_builder = s_resource(
            attributes={"id": a_str(), "config": a_obj(attributes={"enabled": a_bool()})}
        )
        result = a_null(schema_builder)
        assert isinstance(result, CtyValue)
        assert not result.is_unknown
        assert result.is_null
        assert result.vtype.equal(schema_builder.block.to_cty_type())
        assert isinstance(result.vtype, CtyObject)

    @pytest.mark.parametrize("invalid_input", ["not a schema builder", 12345, None])
    def test_a_null_raises_type_error_for_invalid_input(self, invalid_input: Any) -> None:
        with pytest.raises(TypeError, match=r"a_null.. expects a schema builder instance"):
            a_null(invalid_input)


# 🐍🏗️🔚
