#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from pyvider.cty import CtyList, CtyMap, CtyObject, CtySet
from pyvider.schema.types.enums import NestingMode
from pyvider.schema.types.types_base import PvsType

if TYPE_CHECKING:
    from pyvider.schema.types.attribute import PvsAttribute
    from pyvider.schema.types.blocks import PvsNestedBlock


@define(frozen=True, kw_only=True)
class PvsObjectType(PvsType):
    """
    A schema object that holds full attribute definitions.
    It no longer inherits from CtyObject, but can produce one.
    """

    attributes: dict[str, PvsAttribute] = field(factory=dict)
    block_types: tuple[PvsNestedBlock, ...] = field(factory=tuple)
    description: str | None = field(default=None)
    deprecated: bool = field(default=False)

    def to_cty_type(self) -> CtyObject:
        """
        Converts this schema definition into its equivalent CtyObject type
        for validation and data manipulation. This now correctly includes
        attributes derived from nested blocks.
        """
        attribute_types = {name: attr.type for name, attr in self.attributes.items()}
        optional_attributes = {
            name for name, attr in self.attributes.items() if attr.optional or attr.computed
        }

        # FIX: Add types for nested blocks so the CtyObject is complete.
        for block in self.block_types:
            block_cty_type = block.block.to_cty_type()
            if block.nesting == NestingMode.LIST:
                attribute_types[block.type_name] = CtyList(element_type=block_cty_type)
            elif block.nesting == NestingMode.SET:
                attribute_types[block.type_name] = CtySet(element_type=block_cty_type)
            elif block.nesting == NestingMode.MAP:
                attribute_types[block.type_name] = CtyMap(element_type=block_cty_type)
            else:  # SINGLE or GROUP
                attribute_types[block.type_name] = block_cty_type

            optional_attributes.add(block.type_name)

        return CtyObject(
            attribute_types=attribute_types,
            optional_attributes=frozenset(optional_attributes),  # type: ignore[arg-type]
        )


# 🐍🏗️🔚
