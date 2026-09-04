#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Flags on the members of a collection-of-objects attribute are not silently lost.

`a_obj` reaches Terraform as a `nested_type`, which is what carries a member's
`computed`, `sensitive`, `write_only` and default across the wire. Put the same
`a_obj` inside `a_list`, `a_set` or `a_map` and only its cty type survives: the
factory takes `attr.type` and drops everything else, because tfprotov6 models
that shape as a plain object type with no per-member flags.

pyvider does not yet emit LIST, SET or MAP nested types, so the flags genuinely
cannot be expressed. What it did was accept them and quietly discard them, which
is worse than refusing: a `computed=True` member looks declared, Terraform never
hears about it, and a provider that fills the value in during apply is told
"planned value for a non-computed attribute" with nothing pointing back at the
schema.

Declaring the shape without the flags still works, which is the whole feature
minus the part that was never delivered.
"""

from __future__ import annotations

import pytest

from pyvider.schema import a_list, a_map, a_num, a_obj, a_set, a_str


class TestFlagsThatCannotSurvive:
    def test_a_computed_member_inside_a_list_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="computed"):
            a_list(a_obj({"id": a_str(computed=True), "name": a_str()}))

    def test_a_sensitive_member_inside_a_set_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="sensitive"):
            a_set(a_obj({"token": a_str(sensitive=True)}))

    def test_a_write_only_member_inside_a_map_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="write_only"):
            a_map(a_obj({"secret": a_str(write_only=True)}))

    def test_a_defaulted_member_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="default"):
            a_list(a_obj({"size": a_str(default="small")}))

    def test_the_message_says_what_to_do_instead(self) -> None:
        with pytest.raises(ValueError, match="b_list"):
            a_list(a_obj({"id": a_str(computed=True)}))


class TestShapesThatStillWork:
    def test_a_plain_object_element_is_accepted(self) -> None:
        assert a_list(a_obj({"name": a_str(), "size": a_num()})) is not None

    def test_a_scalar_element_is_accepted(self) -> None:
        assert a_list(a_str()) is not None

    def test_a_single_object_attribute_keeps_its_member_flags(self) -> None:
        """`a_obj` on its own is a nested_type, where the flags do survive."""
        attribute = a_obj({"id": a_str(computed=True)})

        assert attribute.object_type is not None
        assert attribute.object_type.attributes["id"].computed is True

    def test_the_collection_attribute_may_still_carry_its_own_flags(self) -> None:
        """The restriction is about members, not the attribute holding them."""
        assert a_list(a_obj({"name": a_str()}), computed=True) is not None


# 🐍🏗️🔚
