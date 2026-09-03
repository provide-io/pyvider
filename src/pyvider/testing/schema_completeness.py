#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Static schema/state-class parity checks for resource authors.

Go providers cannot construct an incomplete state value: ``tftypes.NewValue``
panics if the value map doesn't exactly match the object type's attribute
set, and ``terraform-plugin-framework``'s ``resp.State.Set`` requires a
struct field for every schema attribute. Python's ``attrs``-class-as-state
model has no such invariant -- a class can simply not declare a field -- so
the same mistake surfaces at runtime instead, deep in a real apply. This
module is the closest Python analogue: a static check a resource author runs
in their own test suite, one call per resource, so the mismatch is caught at
test time instead.
"""

from typing import Any

import attrs

from pyvider.exceptions import FrameworkConfigurationError


def find_missing_state_fields(resource_class: type[Any]) -> list[str]:
    """Return the schema attribute names ``resource_class.state_class`` doesn't declare.

    Every non-write-only attribute a resource's schema declares must have a
    matching field on its state class: ``attrs_to_dict_for_cty`` only emits
    fields the state class actually has, and pyvider's apply/read handlers
    raise ``IncompleteResourceStateError`` at runtime for anything missing.
    This is that same check, run statically against the class.

    Write-only attributes are exempt: pyvider nulls them unconditionally
    regardless of whether the state class declares them, so a state class is
    free to omit one (the idiomatic choice) or keep it (harmless).
    """
    state_class = getattr(resource_class, "state_class", None)
    if state_class is None:
        raise FrameworkConfigurationError(
            f"{resource_class.__name__} has no state_class set; cannot check schema/state parity."
        )
    if not attrs.has(state_class):
        raise FrameworkConfigurationError(
            f"{state_class.__name__} is not an attrs class; pyvider state classes must be "
            "decorated with @attrs.define or @attrs.frozen."
        )

    schema = resource_class.get_schema()
    field_names = {f.name for f in attrs.fields(state_class)}

    return sorted(
        name
        for name, attr in schema.block.attributes.items()
        if not getattr(attr, "write_only", False) and name not in field_names
    )


def assert_schema_state_parity(resource_class: type[Any]) -> None:
    """Fail immediately if ``resource_class``'s state class is missing a schema attribute.

    Intended for a resource author's own test suite: one call per resource,
    in a plain unit test, no protocol server or real Terraform/OpenTofu run
    required. Catches the mistake behind pyvider issue #50 at test time --
    the closest Python analogue to how Go's ``tftypes``/``terraform-plugin-
    framework`` catch it at construction time.
    """
    missing = find_missing_state_fields(resource_class)
    if missing:
        # Not a bare `assert`: this must still fire under `python -O`, which
        # strips assert statements -- the whole point of this check is to be
        # unconditional, the same way pyvider's runtime check is.
        raise AssertionError(
            f"{resource_class.__name__}.state_class ({resource_class.state_class.__name__}) is "
            f"missing field(s) for schema attribute(s): {', '.join(missing)}.\n\n"
            f"Declare each on {resource_class.state_class.__name__}, or mark it write_only=True "
            "if it should never be persisted to state."
        )


# 🐍🏗️🔚
