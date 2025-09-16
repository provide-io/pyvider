# pyvider/schema/types/attribute.py
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
            raise ValueError(f"Attribute '{self.name}' cannot be both Required and Computed.")

        # Rule 4: Check that at least one flag is set after defaulting.
        # This check is now implicitly handled by the default-to-optional logic above.
        if not self.required and not self.optional and not self.computed:
            raise ValueError(f"Attribute '{self.name}' must be Optional, Required, or Computed.")
