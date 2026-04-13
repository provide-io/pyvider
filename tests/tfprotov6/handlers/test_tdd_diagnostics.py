#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.cty.exceptions import CtyAttributeValidationError
from pyvider.cty.path import CtyPath
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception


@pytest.mark.asyncio
async def test_create_diagnostic_produces_correct_attribute_path() -> None:
    """
    TDD Contract: Verifies that a CtyValidationError with a nested path
    is converted into a Protobuf Diagnostic with a correctly structured
    AttributePath message.
    """
    # GIVEN a validation error with a complex path
    path = CtyPath.get_attr("users").index_step(2).child("address").key_step("city")
    exc = CtyAttributeValidationError("Value cannot be empty", path=path)

    # WHEN a diagnostic is created from it
    diag = await create_diagnostic_from_exception(exc)

    # THEN the diagnostic's attribute path must match the exception's path
    assert diag.attribute is not None
    assert len(diag.attribute.steps) == 4
    assert diag.attribute.steps[0].attribute_name == "users"
    assert diag.attribute.steps[1].element_key_int == 2
    assert diag.attribute.steps[2].attribute_name == "address"
    assert diag.attribute.steps[3].element_key_string == "city"


# 🐍🏗️🔚
