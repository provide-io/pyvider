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
