#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ResourceContext convenience helpers."""

import attrs

from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState


@attrs.define(frozen=True)
class TokenState(PrivateState):
    token: str


def test_get_private_state_returns_existing_instance() -> None:
    state = TokenState(token="abc")
    ctx = ResourceContext(private_state=state)

    fetched = ctx.get_private_state(TokenState)
    assert fetched is state


def test_get_private_state_casts_from_dict() -> None:
    ctx = ResourceContext(private_state={"token": "xyz"})

    fetched = ctx.get_private_state(TokenState)
    assert isinstance(fetched, TokenState)
    assert fetched.token == "xyz"


def test_get_private_state_returns_none_when_missing() -> None:
    ctx = ResourceContext()

    assert ctx.get_private_state(TokenState) is None
    assert ctx.has_private_state() is False


def test_has_private_state_true_when_present() -> None:
    ctx = ResourceContext(private_state=TokenState(token="present"))

    assert ctx.has_private_state() is True


def test_is_field_unknown_returns_true_for_unknown_field() -> None:
    """Test that is_field_unknown returns True for unknown fields."""
    from pyvider.cty import CtyObject, CtyString, CtyValue

    config_cty = CtyValue(
        vtype=CtyObject(attribute_types={"name": CtyString()}),
        value={"name": CtyValue(vtype=CtyString(), value="test", is_unknown=True)},
    )
    ctx = ResourceContext(config_cty=config_cty)

    assert ctx.is_field_unknown("name", source="config") is True


def test_is_field_unknown_returns_false_for_known_field() -> None:
    """Test that is_field_unknown returns False for known fields."""
    from pyvider.cty import CtyObject, CtyString, CtyValue

    config_cty = CtyValue(
        vtype=CtyObject(attribute_types={"name": CtyString()}),
        value={"name": CtyValue(vtype=CtyString(), value="test")},
    )
    ctx = ResourceContext(config_cty=config_cty)

    assert ctx.is_field_unknown("name", source="config") is False


def test_is_field_unknown_returns_false_for_missing_field() -> None:
    """Test that is_field_unknown returns False for missing fields."""
    from pyvider.cty import CtyObject, CtyString, CtyValue

    config_cty = CtyValue(
        vtype=CtyObject(attribute_types={"name": CtyString()}),
        value={"name": CtyValue(vtype=CtyString(), value="test")},
    )
    ctx = ResourceContext(config_cty=config_cty)

    assert ctx.is_field_unknown("other_field", source="config") is False


def test_is_field_unknown_returns_false_when_no_config_cty() -> None:
    """Test that is_field_unknown returns False when config_cty is None."""
    ctx = ResourceContext()

    assert ctx.is_field_unknown("name", source="config") is False


def test_is_field_unknown_returns_false_when_config_cty_is_null() -> None:
    """Test that is_field_unknown returns False when config_cty is null."""
    from pyvider.cty import CtyObject, CtyValue

    config_cty = CtyValue(vtype=CtyObject(attribute_types={}), value={}, is_null=True)
    ctx = ResourceContext(config_cty=config_cty)

    assert ctx.is_field_unknown("name", source="config") is False


def test_is_field_unknown_with_planned_state_source() -> None:
    """Test that is_field_unknown works with planned_state source."""
    from pyvider.cty import CtyObject, CtyString, CtyValue

    planned_state_cty = CtyValue(
        vtype=CtyObject(attribute_types={"count": CtyString()}),
        value={"count": CtyValue(vtype=CtyString(), value="5", is_unknown=True)},
    )
    ctx = ResourceContext(planned_state_cty=planned_state_cty)

    assert ctx.is_field_unknown("count", source="planned_state") is True


def test_is_field_unknown_returns_false_for_non_dict_value() -> None:
    """Test that is_field_unknown returns False when cty value is not a dict."""
    from pyvider.cty import CtyString, CtyValue

    config_cty = CtyValue(vtype=CtyString(), value="not_a_dict")
    ctx = ResourceContext(config_cty=config_cty)

    assert ctx.is_field_unknown("name", source="config") is False


def test_require_replace_starts_empty() -> None:
    assert ResourceContext().requires_replace_paths == []


def test_require_replace_records_paths_in_order() -> None:
    ctx = ResourceContext()

    ctx.require_replace("size_gb")
    ctx.require_replace("disks[0].type")

    assert ctx.requires_replace_paths == ["size_gb", "disks[0].type"]


def test_require_replace_is_idempotent() -> None:
    """A resource may hit the same condition from more than one branch."""
    ctx = ResourceContext()

    ctx.require_replace("size_gb")
    ctx.require_replace("size_gb")

    assert ctx.requires_replace_paths == ["size_gb"]


def test_require_replace_ignores_empty_path() -> None:
    """An empty path addresses nothing; Terraform would reject it."""
    ctx = ResourceContext()

    ctx.require_replace("")

    assert ctx.requires_replace_paths == []


def test_require_replace_is_per_instance() -> None:
    """The list is a mutable default -- it must not be shared between contexts."""
    first = ResourceContext()
    second = ResourceContext()

    first.require_replace("name")

    assert second.requires_replace_paths == []


# 🐍🏗️🔚
