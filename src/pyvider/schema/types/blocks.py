#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import TYPE_CHECKING

from attrs import define, field

# UNIFICATION FIX: Import the canonical NestingMode enum.
from pyvider.schema.types.enums import NestingMode

if TYPE_CHECKING:
    from pyvider.schema.types.object import PvsObjectType


@define(frozen=True, kw_only=True)
class PvsNestedBlock:
    """
    Defines a nested block type within a schema.
    """

    type_name: str = field()
    block: "PvsObjectType" = field()
    nesting: NestingMode = field(default=NestingMode.LIST)
    description: str | None = field(default=None)
    min_items: int | None = field(default=None)
    max_items: int | None = field(default=None)


# 🐍🏗️🔚
