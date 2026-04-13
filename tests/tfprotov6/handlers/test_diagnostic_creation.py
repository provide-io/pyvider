#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.cty.exceptions import (
    CtyAttributeValidationError,
    CtyNumberValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_create_diagnostic_from_ctyattibutevalidationerror() -> None:
    """
    Verifies that a CtyAttributeValidationError for a missing attribute
    is converted into a clear diagnostic.
    """
    path = CtyPath.get_attr("config").child("retries")
    exc = CtyAttributeValidationError(r"Missing required attribute", path=path)
    exc.type_name = "Object"

    diag = await create_diagnostic_from_exception(exc)

    assert diag.severity == pb.Diagnostic.ERROR
    assert diag.detail == r"Validation failed for a value of type 'Object'."
    assert diag.attribute.steps[0].attribute_name == "config"
    assert diag.attribute.steps[1].attribute_name == "retries"


@pytest.mark.asyncio
async def test_create_diagnostic_from_ctynumbervalidationerror() -> None:
    """
    Verifies that a specific primitive error (CtyNumberValidationError)
    is converted into a diagnostic with a precise detail message.
    """
    path = CtyPath.get_attr("config").child("retries")
    exc = CtyNumberValidationError("Cannot represent str value 'five' as Decimal", path=path, value="five")

    diag = await create_diagnostic_from_exception(exc)

    assert diag.severity == pb.Diagnostic.ERROR
    assert "Validation failed for a value of type 'Number'." in diag.detail
    assert "The invalid value provided was 'five'." in diag.detail
    assert diag.attribute.steps[0].attribute_name == "config"
    assert diag.attribute.steps[1].attribute_name == "retries"


@pytest.mark.asyncio
async def test_create_diagnostic_from_generic_ctyvalidationerror() -> None:
    """
    Verifies that a generic CtyValidationError falls back to the
    generic detail message.
    """
    exc = CtyValidationError("A generic validation error.")
    diag = await create_diagnostic_from_exception(exc)

    assert diag.severity == pb.Diagnostic.ERROR
    assert diag.detail == "A configuration validation error occurred."
    assert not diag.attribute.steps


# 🐍🏗️🔚
