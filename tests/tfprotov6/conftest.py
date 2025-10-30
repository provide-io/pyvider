# 
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import pytest

from pyvider.schema import PvsObjectType, a_num, a_str, s_resource


@pytest.fixture
def simple_resource_schema():
    return s_resource(
        PvsObjectType(
            attribute_types={"name": a_str(required=True).type, "count": a_num().type},
            optional_attributes=frozenset(["count"]),
        )
    )

# 🐍🏗️🔚
