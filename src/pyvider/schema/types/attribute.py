#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from attrs import define, field

from pyvider.cty import CtyType
from pyvider.schema.types.enums import StringKind  # Import StringKind
from pyvider.schema.types.object import PvsObjectType


@define(frozen=True, kw_only=True)
class PvsAttribute:
    """Represents a fully resolved schema attribute, holding a CtyType."""

    name: str = field(default="")
    type: CtyType = field()
    description: str = field(default="")
    required: bool = field(default=False)
    optional: bool = field(default=False)
    computed: bool = field(default=False)
    sensitive: bool = field(default=False)
    deprecated: bool = field(default=False)
    default: Any = field(default=None)
    description_kind: StringKind = field(default=StringKind.PLAIN)  # Use Enum member
    object_type: "PvsObjectType" = field(default=None)

    def __attrs_post_init__(self) -> None:
        """
        Validates and sets default flags for the attribute.
        Terraform requires that an attribute is explicitly one of:
        - Required
        - Optional
        - Computed
        This hook enforces that logic.
        """
        # Use object.__setattr__ because the instance is frozen.
        is_req = self.required
        is_opt = self.optional
        is_comp = self.computed

        # Rule 1: If nothing is specified, it defaults to Optional.
        if not is_req and not is_opt and not is_comp:
            object.__setattr__(self, "optional", True)
            is_opt = True

        # Rule 2: An attribute can't be both Required and Optional. Required wins.
        if is_req and is_opt:
            object.__setattr__(self, "optional", False)

        # Rule 3: An attribute can't be both Required and Computed.
        if is_req and is_comp:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"An attribute cannot be both Required and Computed.\n\n"
                f"Suggestion: Choose one of the following:\n"
                f"  - required=True, computed=False: For fields that must be provided by the user\n"
                f"  - required=False, computed=True: For fields that are calculated by the provider\n"
                f"  - optional=True, computed=True: For fields that can be provided or computed\n\n"
                f"Current configuration: required={is_req}, optional={is_opt}, computed={is_comp}\n\n"
                f"See: https://developer.hashicorp.com/terraform/plugin/framework/schemas"
            )

        # Rule 4: Check that at least one flag is set after defaulting.
        # This check is now implicitly handled by the default-to-optional logic above.
        if not self.required and not self.optional and not self.computed:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"An attribute must be explicitly marked as Optional, Required, or Computed.\n\n"
                f"Suggestion: Set one of these flags:\n"
                f"  - required=True: For fields that users must provide\n"
                f"  - optional=True: For fields that users may provide (default)\n"
                f"  - computed=True: For fields that the provider calculates\n\n"
                f"Current configuration: required={self.required}, optional={self.optional}, computed={self.computed}"
            )


# 🐍🏗️🔚
