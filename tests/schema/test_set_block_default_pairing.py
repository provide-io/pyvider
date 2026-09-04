#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A set block element takes its defaults from its own configuration, never a neighbour's.

`_merge_nested_into_plan` pairs planned set elements with the configuration
they came from by value, because a set has no order. That pairing was gated on
`len(plan_value) > 1`, so a plan holding exactly one set element fell through to
the list branch and was paired by *position* instead -- with configuration
element zero, whichever element that happens to be.

A plan hook that drops one element of a two-element set therefore hands the
surviving element the other one's explicitly configured values. The practitioner
sees a value they never wrote, and if the resource reads `ctx.config` during
apply, Terraform rejects the result with "Provider produced inconsistent result
after apply: .enabled: was false, but now true".

A set is unordered at every length, so the pairing cannot depend on how many
elements survived.
"""

from __future__ import annotations

from pyvider.schema import (
    a_bool,
    a_str,
    b_set,
    merge_schema_defaults_into_plan,
    resolve_schema_defaults,
    s_resource,
)

SCHEMA = s_resource(
    attributes={"name": a_str(required=True)},
    block_types=[
        b_set(
            "port",
            attributes={
                "name": a_str(required=True),
                "enabled": a_bool(default=True),
            },
        )
    ],
)

BLOCK_TYPE = SCHEMA.block.to_cty_type()


def _config(ports: list[dict[str, object]]) -> object:
    """A configuration with `enabled` left to its default unless stated."""
    return resolve_schema_defaults(
        BLOCK_TYPE.validate({"name": "example", "port": ports}),
        SCHEMA.block,
    )


def test_a_surviving_set_element_keeps_its_own_default() -> None:
    """The reported failure: one element dropped, the other inherits its values."""
    config = _config(
        [
            {"name": "a", "enabled": False},  # explicitly disabled
            {"name": "b", "enabled": None},  # left to the default, which is True
        ]
    )
    # The plan hook kept only "b".
    plan = {"port": [{"name": "b", "enabled": None}]}

    merge_schema_defaults_into_plan(plan, config, SCHEMA.block)

    assert plan["port"][0]["name"] == "b", "the surviving element was replaced"
    assert plan["port"][0]["enabled"] is True, (
        "the surviving set element took the explicit `enabled = false` from the "
        "element that was dropped, because a single-element set was paired by "
        "position rather than by value"
    )


def test_a_single_element_set_still_takes_its_own_configuration() -> None:
    """With one element on both sides, pairing by value must agree with position."""
    config = _config([{"name": "solo", "enabled": False}])
    plan = {"port": [{"name": "solo", "enabled": None}]}

    merge_schema_defaults_into_plan(plan, config, SCHEMA.block)

    assert plan["port"][0]["enabled"] is False, "an explicit configuration value was overwritten"


def test_multiple_elements_are_still_paired_by_value() -> None:
    """The behaviour that already worked, kept honest: order must not matter.

    An explicitly configured value is already in the plan -- Terraform's
    proposed new state carries the configuration through -- so only the
    defaulted attribute is null here. That is the shape the matcher pairs on.
    """
    config = _config(
        [
            {"name": "a", "enabled": False},
            {"name": "b", "enabled": None},
        ]
    )
    # The plan lists them in the other order, which a set is entitled to do.
    plan = {"port": [{"name": "b", "enabled": None}, {"name": "a", "enabled": False}]}

    merge_schema_defaults_into_plan(plan, config, SCHEMA.block)

    by_name = {element["name"]: element for element in plan["port"]}
    assert by_name["a"]["enabled"] is False
    assert by_name["b"]["enabled"] is True


def test_an_element_the_provider_added_takes_nothing_from_another() -> None:
    """An element with no configuration to pair with must not inherit one."""
    config = _config([{"name": "a", "enabled": False}])
    plan = {"port": [{"name": "a", "enabled": False}, {"name": "provider-added", "enabled": None}]}

    merge_schema_defaults_into_plan(plan, config, SCHEMA.block)

    by_name = {element["name"]: element for element in plan["port"]}
    assert by_name["a"]["enabled"] is False
    # There is no configuration for this element, so there is no default to take
    # from one. What matters is that it did not acquire the other element's False.
    assert by_name["provider-added"]["enabled"] is not False


# 🐍🏗️🔚
