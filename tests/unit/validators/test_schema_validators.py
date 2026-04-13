#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from tests.validators.schema_validators import validate_schema_dict


def test_schema_validation() -> None:
    schema = {
        "description": "Valid schema",
        "attributes": [{"name": "attr1", "type": "string"}],
        "block_types": [{"name": "block1", "nested": True}],
    }
    validate_schema_dict(schema)


# 🐍🏗️🔚
