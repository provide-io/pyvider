#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.cty import CtyValidationError
from pyvider.schema import (
    PvsObjectType,
    PvsSchema,
    a_num,
    a_str,
    s_resource,
)


@pytest.fixture
def valid_schema() -> PvsSchema:
    return s_resource(
        {
            "name": a_str(required=True),
            "count": a_num(optional=True),
        }
    )


class TestSchemaArchitecture:
    def test_schema_is_composed_correctly(self, valid_schema: PvsSchema) -> None:
        """Ensures the schema block is a PvsObjectType."""
        assert isinstance(valid_schema, PvsSchema)
        assert isinstance(valid_schema.block, PvsObjectType)
        assert "name" in valid_schema.block.attributes

    @pytest.mark.asyncio
    async def test_schema_validation_logic(self, valid_schema: PvsSchema) -> None:
        """Tests the high-level validation function."""
        valid_config = {"name": "test", "count": 1}
        # The method now raises no exception on success.
        valid_schema.validate_config(valid_config)

        invalid_config = {"name": "test", "count": "not-a-number"}
        with pytest.raises(CtyValidationError, match="Cannot represent str value"):
            valid_schema.validate_config(invalid_config)


# 🐍🏗️🔚
