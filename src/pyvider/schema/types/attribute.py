#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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
    write_only: bool = field(default=False)
    requires_replace: bool = field(default=False)
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
        is_req, is_opt, is_comp = self._normalize_flags()
        self._validate_flag_combinations(is_req, is_opt, is_comp)
        self._validate_requires_replace()
        self._apply_default_rules(is_req, is_opt, is_comp)

    def _normalize_flags(self) -> tuple[bool, bool, bool]:
        """Applies the Required/Optional/Computed defaulting rules."""
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

        return is_req, is_opt, is_comp

    def _validate_flag_combinations(self, is_req: bool, is_opt: bool, is_comp: bool) -> None:
        """Rejects Required/Optional/Computed combinations Terraform cannot express."""
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

    def _validate_requires_replace(self) -> None:
        """Rejects requires_replace placements that could never take effect."""
        # Rule 5: requires_replace is meaningless on a computed-only attribute.
        if self.requires_replace and self.computed and not self.required and not self.optional:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"requires_replace cannot be set on a computed-only attribute.\n\n"
                f"A computed-only attribute is never supplied by the practitioner, so "
                f"replacement could only ever be triggered by the provider's own computed "
                f"value changing -- which would force replacement on every plan where the "
                f"value is not yet known.\n\n"
                f"Suggestion: Set requires_replace on the required/optional attribute the "
                f"practitioner actually changes, or add optional=True if this attribute is "
                f"both practitioner-settable and provider-computed."
            )

        # Rule 6: requires_replace is unenforceable on a write-only attribute.
        if self.requires_replace and self.write_only:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"requires_replace cannot be set on a write-only attribute.\n\n"
                f"Terraform requires every write-only value to be null in both prior and "
                f"planned state, so the plan can never observe a change to compare against "
                f"and replacement would silently never trigger. Terraform's own SDK rejects "
                f"the equivalent combination ('WriteOnly cannot be set with ForceNew').\n\n"
                f"Suggestion: Pair the write-only attribute with a companion attribute the "
                f"practitioner bumps when the secret rotates (commonly named "
                f"'{self.name}_version' or '{self.name}_wo_version') and set requires_replace "
                f"on that attribute instead, or trigger replacement imperatively from the "
                f"resource's plan hook via ctx.require_replace()."
            )

        # Rule 7: requires_replace is unreachable on an attribute nested inside
        # an object-typed attribute.
        if self.object_type is not None:
            nested = [
                nested_name
                for nested_name, nested_attr in self.object_type.attributes.items()
                if nested_attr.requires_replace
            ]
            if nested:
                # An object-typed attribute is constructed as an argument to the
                # schema builder that names it, so `self.name` is still empty in the
                # case a practitioner will actually hit. The message must therefore
                # identify the offender by the nested name and describe the enclosing
                # object rather than trying to print a name it does not yet have.
                prefix = f"{self.name}." if self.name else ""
                offenders = ", ".join(f"{prefix}{n}" for n in nested)
                if self.name:
                    enclosing = f"the object-typed attribute '{self.name}'"
                    declare_on = f"'{self.name}'"
                    call = f"ctx.require_replace('{self.name}.{nested[0]}')."
                else:
                    enclosing = "an object-typed attribute"
                    declare_on = "the object-typed attribute"
                    call = (
                        f"ctx.require_replace('<object>.{nested[0]}'), substituting the "
                        f"object attribute's own name for '<object>'."
                    )
                raise ValueError(
                    f"Invalid schema attribute configuration for nested attribute "
                    f"'{offenders}': requires_replace cannot be set on an attribute "
                    f"nested inside {enclosing}.\n\n"
                    f"Replacement is decided per-plan from a flat list of attribute paths, "
                    f"and the plan handler only compares top-level attributes -- so the flag "
                    f"would look effective while silently doing nothing, and the practitioner "
                    f"would see an in-place update that the remote API cannot honour.\n\n"
                    f"Suggestion: Declare requires_replace on {declare_on} itself if any change "
                    f"to the object should force replacement, or trigger replacement "
                    f"imperatively from the resource's plan hook via {call}"
                )

    def _apply_default_rules(self, is_req: bool, is_opt: bool, is_comp: bool) -> None:
        """Validates and normalizes the interaction between `default` and the flags."""
        # Rule 8: A computed-only attribute cannot have a default. A default is
        # the value used when the practitioner omits something they *could* have
        # written, and `computed=True` without `optional=True` means they cannot
        # write it at all -- so there is nothing to default from. The provider's
        # own fallback for a value it computes belongs in the resource, not the
        # schema.
        if self.default is not None and is_comp and not is_opt and not is_req:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"A computed-only attribute cannot declare a default.\n\n"
                f"A default applies to an attribute the practitioner omitted, and a "
                f"computed-only attribute cannot be set in configuration at all.\n\n"
                f"Suggestion: Choose one of the following:\n"
                f"  - optional=True, default=...: The practitioner may set it, and the "
                f"provider uses the default otherwise\n"
                f"  - computed=True, no default: The provider calculates the value; set "
                f"your fallback in the resource's own create/read logic\n\n"
                f"Current configuration: required={is_req}, optional={is_opt}, "
                f"computed={is_comp}, default={self.default!r}"
            )

        # Rule 9: A required attribute cannot have a default. A default is the
        # value used when the practitioner omits the attribute, and `required`
        # means they cannot omit it -- so the default could never be reached, and
        # filling one in would mask the missing value from the required-attribute
        # check.
        if self.default is not None and self.required:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"A required attribute cannot declare a default.\n\n"
                f"A default applies to an attribute the practitioner omitted, and a "
                f"required attribute must always be set -- so the default would never "
                f"be used, and filling one in would hide a missing required value.\n\n"
                f"Suggestion: Choose one of the following:\n"
                f"  - optional=True, default=...: The practitioner may set it, and the "
                f"provider uses the default otherwise\n"
                f"  - required=True, no default: The practitioner must always supply a "
                f"value\n\n"
                f"Current configuration: required={is_req}, optional={is_opt}, "
                f"computed={is_comp}, default={self.default!r}"
            )

        # Rule 10: A write-only attribute cannot have a default. Terraform
        # requires every write-only value to be null in both prior and planned
        # state, so a default would put into the plan what must show null -- and
        # a write-only attribute cannot be computed, which a default requires.
        if self.default is not None and self.write_only:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"A write-only attribute cannot declare a default.\n\n"
                f"Terraform requires every write-only value to be null in both prior "
                f"and planned state, so a provider-supplied default would put into the "
                f"plan the very value that must show null.\n\n"
                f"Suggestion: Choose one of the following:\n"
                f"  - write_only=True, no default: Apply the fallback inside the "
                f"resource's own create/update logic, where the value is never stored\n"
                f"  - default=..., write_only=False: The value is defaulted and stored "
                f"in state like any other attribute\n\n"
                f"Current configuration: required={is_req}, optional={is_opt}, "
                f"computed={is_comp}, write_only={self.write_only}, default={self.default!r}"
            )

        # Rule 11: An attribute with a default is Optional *and* Computed -- the
        # practitioner may set it, and the provider fills it in otherwise.
        # Terraform rejects a provider-supplied value on an attribute that is not
        # computed, so a default is unusable without the flag.
        #
        # `default=None` is indistinguishable from declaring no default; there is
        # no way to express "defaults to null", which is what a null already is.
        if self.default is not None:
            object.__setattr__(self, "computed", True)


# 🐍🏗️🔚
