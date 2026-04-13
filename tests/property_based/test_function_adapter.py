#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from decimal import Decimal
from typing import Any

import pytest

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyString
from pyvider.functions.adapters import function_to_dict

# This test uses a parameterized approach rather than random generation, as generating
# valid Python functions with type hints is not a good fit for Hypothesis.
# The goal is to comprehensively test the type hint mapping logic.

TYPE_HINT_TEST_CASES = [
    # Primitives
    (str, CtyString),
    (int, CtyNumber),
    (float, CtyNumber),
    (Decimal, CtyNumber),
    (bool, CtyBool),
    # Optionals
    (str | None, CtyString),
    (str | None, CtyString),
    # Any / Dynamic
    (Any, CtyDynamic),
    # Simple Collections
    (list, CtyList),
    (list[str], CtyList),
    (dict, CtyMap),
    (dict[str, int], CtyMap),
    # Complex Unions
    (str | int, CtyDynamic),  # Should resolve to dynamic
    (int | str, CtyDynamic),
    (int | float | None, CtyNumber),  # Should resolve to number
    # Nested Collections
    (list[dict[str, bool]], CtyList),
]


@pytest.mark.parametrize("py_type, expected_cty_class", TYPE_HINT_TEST_CASES)
def test_function_adapter_type_inference(py_type: Any, expected_cty_class: type) -> None:
    """
    Verifies that the function adapter correctly infers the CtyType
    from a wide range of Python type hints.
    """

    # Dynamically create a dummy function with the type hint to test
    def dummy_func(param: py_type) -> None:
        pass

    # Adapt the function and inspect the inferred parameter type
    meta = function_to_dict(dummy_func)
    assert len(meta["parameters"]) == 1
    inferred_param_type = meta["parameters"][0]["cty_type"]

    assert isinstance(inferred_param_type, expected_cty_class), (
        f"For hint '{py_type}', expected {expected_cty_class}, but got {type(inferred_param_type)}"
    )

    # Specific checks for collection element types
    if expected_cty_class is CtyList and py_type is list[dict[str, bool]]:
        assert isinstance(inferred_param_type.element_type, CtyMap)
        assert isinstance(inferred_param_type.element_type.element_type, CtyBool)


# 🐍🏗️🔚
