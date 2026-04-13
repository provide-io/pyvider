#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.schema import PvsObjectType, PvsSchema, a_num, a_str, s_resource


@pytest.fixture
def simple_resource_schema() -> PvsSchema:
    return s_resource(
        PvsObjectType(
            attribute_types={"name": a_str(required=True).type, "count": a_num().type},
            optional_attributes=frozenset(["count"]),
        )
    )


# 🐍🏗️🔚
