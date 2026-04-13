#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.functions.adapters import function_to_dict

# --- Test Functions ---


def simple_func(a: str, b: int) -> bool:
    """A simple function with basic types."""
    return a == str(b)


def collection_func(items: list[str], config: dict[str, int]) -> list[int]:
    """A function with collection types."""
    return [config.get(item, 0) for item in items]


def optional_func(name: str | None, count: int = 10) -> str:
    """A function with optional/default parameters."""
    return (name or "default") * count


def dynamic_func(val: Any) -> Any:
    """A function with dynamic types."""
    return val


def union_func(val: str | int) -> str:
    """A function with a Union type hint."""
    return str(val)


# --- Test Cases ---


class TestFunctionAdapter:
    def test_adapt_simple_function(self) -> None:
        """TDD: Verifies adaptation of basic Python type hints."""
        meta = function_to_dict(simple_func)

        assert meta["name"] == "simple_func"
        assert meta["summary"] == "A simple function with basic types."

        params = {p["name"]: p for p in meta["parameters"]}
        assert len(params) == 2

        assert isinstance(params["a"]["cty_type"], CtyString)
        assert not params["a"]["allow_null"]

        assert isinstance(params["b"]["cty_type"], CtyNumber)
        assert not params["b"]["allow_null"]

        assert isinstance(meta["return"]["cty_type"], CtyBool)

    def test_adapt_collection_function(self) -> None:
        """TDD: Verifies adaptation of list and dict type hints."""
        meta = function_to_dict(collection_func)

        params = {p["name"]: p for p in meta["parameters"]}
        assert len(params) == 2

        # Test list parameter
        list_param_type = params["items"]["cty_type"]
        assert isinstance(list_param_type, CtyList)
        assert isinstance(list_param_type.element_type, CtyString)

        # Test dict parameter
        map_param_type = params["config"]["cty_type"]
        assert isinstance(map_param_type, CtyMap)
        assert isinstance(map_param_type.element_type, CtyNumber)

        # Test list return type
        return_type = meta["return"]["cty_type"]
        assert isinstance(return_type, CtyList)
        assert isinstance(return_type.element_type, CtyNumber)

    def test_adapt_optional_parameters(self) -> None:
        """TDD: Verifies adaptation of optional and default-value parameters."""
        meta = function_to_dict(optional_func)

        # Parameters without defaults go in "parameters"
        params = {p["name"]: p for p in meta["parameters"]}
        assert len(params) == 1

        # `str | None` should be nullable (no default, but nullable type)
        assert params["name"]["allow_null"] is True
        assert isinstance(params["name"]["cty_type"], CtyString)

        # Parameter with default value becomes variadic_parameter
        assert "variadic_parameter" in meta
        variadic = meta["variadic_parameter"]
        assert variadic["name"] == "count"
        assert variadic["allow_null"] is True
        assert isinstance(variadic["cty_type"], CtyNumber)

    def test_adapt_dynamic_types(self) -> None:
        """TDD: Verifies that `Any` correctly maps to `CtyDynamic`."""
        meta = function_to_dict(dynamic_func)

        params = {p["name"]: p for p in meta["parameters"]}
        assert isinstance(params["val"]["cty_type"], CtyDynamic)
        assert isinstance(meta["return"]["cty_type"], CtyDynamic)

    def test_adapt_union_types(self) -> None:
        """TDD: Verifies that a complex Union type maps to CtyDynamic."""
        meta = function_to_dict(union_func)

        params = {p["name"]: p for p in meta["parameters"]}
        # A Union of str and int cannot be represented by a single primitive CtyType,
        # so it should default to dynamic.
        assert isinstance(params["val"]["cty_type"], CtyDynamic)


# 🐍🏗️🔚
