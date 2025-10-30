#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import pytest

from pyvider.cty import CtyString
from pyvider.schema import PvsObjectType, PvsSchema


@pytest.fixture
def simple_schema():
    """Provides a simple schema for testing."""
    return PvsSchema(version=1, block=PvsObjectType(attribute_types={"name": CtyString()}))


# 🐍🏗️🔚
