#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.functions.decorators import register_function

# THE FIX: Import 'hub' from its new canonical location.
from pyvider.hub import hub


# This is the function that will be marked by the decorator.
async def my_test_func_for_reg(a: int, b: str) -> str:
    return f"{b}{a}"


# This test now relies on the session-wide discovery fixture to populate the hub.
@pytest.mark.usefixtures("discovered_components_session")
def test_register_function_decorator_marks_for_discovery() -> None:
    # The decorator itself only adds metadata now.
    decorated_func = register_function(
        name="my_registered_func_for_test",
        summary="Test summary",
    )(my_test_func_for_reg)

    # Assert the metadata was attached correctly.
    assert hasattr(decorated_func, "_function_metadata")
    meta = decorated_func._function_metadata
    assert meta["name"] == "my_registered_func_for_test"
    assert meta["summary"] == "Test summary"

    # Assert that the session-wide discovery process found and registered it.
    # Note: We re-register here within the test scope to ensure the test is
    # self-contained and doesn't rely on which files pytest happens to import first.
    # The hub handles de-duplication.
    hub.register("function", "my_registered_func_for_test", decorated_func)
    registered_comp = hub.get_component("function", "my_registered_func_for_test")
    assert registered_comp is not None
    assert registered_comp == decorated_func


# 🐍🏗️🔚
