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
        if self.default is None:
            return

        rules = (
            (
                is_comp and not is_opt and not is_req,
                "A computed-only attribute cannot declare a default.",
                "Defaults fill omitted configuration, but a computed-only attribute cannot be configured.",
                (
                    "optional=True, default=...: Allow configuration and default it when omitted",
                    "computed=True, no default: Calculate the fallback in create/read logic",
                ),
            ),
            (
                is_req,
                "A required attribute cannot declare a default.",
                "A required attribute cannot be omitted, so its default would be unreachable.",
                (
                    "optional=True, default=...: Allow omission and supply the default",
                    "required=True, no default: Require the practitioner to supply a value",
                ),
            ),
            (
                self.write_only,
                "A write-only attribute cannot declare a default.",
                "Terraform requires write-only values to remain null in prior and planned state.",
                (
                    "write_only=True, no default: Apply the fallback in create/update logic",
                    "default=..., write_only=False: Default and store the value in state",
                ),
            ),
        )
        for condition, headline, why, options in rules:
            if condition:
                self._reject_default(headline, why, options)

        # Rule 11: An attribute with a default is Optional *and* Computed -- the
        # practitioner may set it, and the provider fills it in otherwise.
        # Terraform rejects a provider-supplied value on an attribute that is not
        # computed, so a default is unusable without the flag.
        #
        # `default=None` is indistinguishable from declaring no default; there is
        # no way to express "defaults to null", which is what a null already is.
        try:
            self.type.validate(self.default)
        except Exception as exc:
            raise ValueError(
                f"Invalid schema attribute configuration for '{self.name}': "
                f"the declared default {self.default!r} is not a valid "
                f"{type(self.type).__name__} value.\n\n"
                f"Underlying error: {exc}\n\n"
                f"Suggestion: give the default the same type as the attribute."
            ) from exc
        object.__setattr__(self, "computed", True)

    def _reject_default(
        self,
        headline: str,
        why: str,
        options: tuple[str, str],
    ) -> None:
        suggestions = "\n".join(f"  - {option}" for option in options)
        raise ValueError(
            f"Invalid schema attribute configuration for '{self.name}': {headline}\n\n"
            f"{why}\n\n"
            f"Suggestion: Choose one of the following:\n{suggestions}\n\n"
            f"Current configuration: required={self.required}, optional={self.optional}, "
            f"computed={self.computed}, write_only={self.write_only}, default={self.default!r}"
        )


# 🐍🏗️🔚
