#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import re
from typing import TYPE_CHECKING

from attrs import define, field

from pyvider.cty import CtyDynamic

# UNIFICATION FIX: Import the canonical NestingMode enum.
from pyvider.schema.types.enums import NestingMode

#: Terraform parses a block name with this, and rejects the provider otherwise
#: (configschema/internal_validate.go:58).
_BLOCK_NAME = re.compile(r"[a-z0-9_]+")

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
        self._validate_terraform_block_rules()

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

    def _validate_terraform_block_rules(self) -> None:
        """Reject a block Terraform's own `Block.InternalValidate` would reject.

        A violation takes the whole provider down at `terraform init` with
        "provider %s has invalid schema for ... which is a bug in the provider",
        naming the provider rather than the declaration that caused it
        (internal/schemarepo/loadschemas/plugins.go:134-186; rules in
        internal/configs/configschema/internal_validate.go). Checking here means
        the author sees it when they write it.
        """
        if not _BLOCK_NAME.fullmatch(self.type_name):
            raise ValueError(
                f"Invalid schema block configuration: block name {self.type_name!r} must "
                f"match {_BLOCK_NAME.pattern} -- lowercase letters, digits and underscores.\n\n"
                f"Terraform rejects the whole provider at init over a block name it cannot "
                f"parse (configschema/internal_validate.go:58)."
            )

        self._validate_item_counts()

        if self.nesting is NestingMode.SET:
            self._validate_set_block_contents()

    def _validate_item_counts(self) -> None:
        """min_items and max_items, which mean different things per nesting mode."""
        min_items = self.min_items or 0
        max_items = self.max_items or 0

        if min_items < 0 or max_items < 0:
            field = "min_items" if min_items < 0 else "max_items"
            raise ValueError(
                f"Invalid schema block configuration for {self.type_name!r}: {field} "
                f"cannot be negative (got min_items={self.min_items}, max_items={self.max_items})."
            )

        mode = self.nesting
        if mode is NestingMode.SINGLE:
            if min_items != max_items or min_items not in (0, 1):
                raise ValueError(
                    f"Invalid schema block configuration for {self.type_name!r}: a single "
                    f"block holds either nothing or one element, so min_items and max_items "
                    f"must be equal and either 0 or 1 (got min_items={self.min_items}, "
                    f"max_items={self.max_items}).\n\n"
                    f"Suggestion: use min_items=1, max_items=1 to require the block, or leave "
                    f"both unset to make it optional."
                )
        elif mode in (NestingMode.GROUP, NestingMode.MAP):
            if min_items or max_items:
                explanation = (
                    "a group block is always present -- an absent one decodes as an object of nulls"
                    if mode is NestingMode.GROUP
                    else "a map block is keyed rather than counted"
                )
                raise ValueError(
                    f"Invalid schema block configuration for {self.type_name!r}: "
                    f"{explanation}, so it cannot carry min_items or max_items."
                )
        elif max_items and min_items > max_items:
            # LIST and SET. max_items 0 means unbounded, so it is not a conflict.
            raise ValueError(
                f"Invalid schema block configuration for {self.type_name!r}: min_items "
                f"({min_items}) is greater than max_items ({max_items})."
            )

    def _validate_set_block_contents(self) -> None:
        """A set block's elements are identified by value, so some types cannot appear.

        Terraform refuses a dynamic type inside set nesting because two elements
        whose types differ cannot be compared, and refuses a write-only attribute
        because its value is always null and so cannot contribute to the identity
        of the element it belongs to
        (configschema/internal_validate.go:92-105).
        """
        dynamic = [name for name, attr in self.block.attributes.items() if isinstance(attr.type, CtyDynamic)]
        if dynamic:
            names = ", ".join(repr(name) for name in dynamic)
            raise ValueError(
                f"Invalid schema block configuration for {self.type_name!r}: a set block "
                f"cannot contain a dynamic attribute ({names}).\n\n"
                f"Set elements are identified by comparing their values, and two elements "
                f"whose types differ cannot be compared.\n\n"
                f"Suggestion: give the attribute a concrete type, or use b_list instead."
            )

        write_only = [name for name, attr in self.block.attributes.items() if attr.write_only]
        if write_only:
            names = ", ".join(repr(name) for name in write_only)
            raise ValueError(
                f"Invalid schema block configuration for {self.type_name!r}: a set block "
                f"cannot contain a write_only attribute ({names}).\n\n"
                f"A write-only value is null in everything the provider returns, so it "
                f"cannot contribute to the identity of the element it belongs to.\n\n"
                f"Suggestion: move the attribute to the top level of the schema, or use "
                f"b_list instead."
            )


# 🐍🏗️🔚
