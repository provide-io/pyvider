#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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

    def __attrs_post_init__(self) -> None:
        """Reject `requires_replace` on attributes declared inside this block.

        Replacement is decided per-plan from a flat list of attribute paths, and
        an attribute inside a nested block has no single path until the block's
        elements are matched up between prior and planned state -- a
        correspondence Terraform itself establishes and the plan handler cannot
        guess for list, set or map nesting. The declarative flag is therefore
        unreachable here, and accepting it silently would hand the practitioner
        an in-place update the remote API cannot honour, discovered only at
        apply time. Same failure `PvsAttribute` Rules 5-7 exist to remove, one
        nesting level down.

        Only this block's own attributes are inspected: deeper blocks validate
        their own contents when they are constructed, which happens before the
        block that contains them.
        """
        offenders = [name for name, attr in self.block.attributes.items() if attr.requires_replace]
        if offenders:
            example = f"{self.type_name}.{offenders[0]}"
            raise ValueError(
                f"Invalid schema block configuration for '{self.type_name}': "
                f"requires_replace cannot be set on an attribute inside a nested block "
                f"({', '.join(f'{self.type_name}.{name}' for name in offenders)}).\n\n"
                f"Terraform decides replacement from a flat list of attribute paths, and an "
                f"attribute inside a '{self.nesting.name.lower()}' block has no stable path "
                f"until Terraform matches the block's elements between prior and planned "
                f"state. The flag would look effective while silently doing nothing.\n\n"
                f"Suggestion: Promote the attribute to the top level of the schema and set "
                f"requires_replace there, or trigger replacement imperatively from the "
                f"resource's plan hook via ctx.require_replace('{example}') -- the hook "
                f"knows which element changed and can state the exact path."
            )


# 🐍🏗️🔚
