#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.cty import CtyValidationError
from pyvider.schema import a_obj, a_str, s_resource


@pytest.mark.asyncio
async def test_null_values() -> None:
    """
    Tests that providing a null value for a required attribute fails
    validation as expected.
    """
    schema = s_resource(
        attributes={
            "name": a_str(required=True),
            "optional_object": a_obj(attributes={"field": a_str()}, optional=True),
        }
    )

    invalid_config = {"name": None}

    with pytest.raises(CtyValidationError, match="Attribute cannot be null"):
        schema.validate_config(invalid_config)


# 🐍🏗️🔚
