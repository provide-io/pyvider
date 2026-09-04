#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""An ephemeral resource without private state can still be closed and renewed.

Private state is optional in the protocol: `OpenEphemeralResource.Response.private`
is an optional field, and Close and Renew carry back whatever Open produced, or
nothing. Terraform closes every ephemeral resource it opened -- close nodes are
wired to the last referencer and a root-module sweep catches the rest
(transform_ephemeral_resource_close.go), using `context.WithoutCancel` so it
happens even on an interrupt.

Both handlers required a `private_state_class` and then called
`msgpack.unpackb(request.private)` unconditionally. `msgpack.unpackb(b"")` raises
`ValueError: Unpack failed: incomplete input`, so an ephemeral resource that
keeps no private state -- the ordinary case for something that just reads a
secret -- failed on every close, and the failure surfaced as "Internal Provider
Error" because a bare ValueError carries nothing a practitioner can act on.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, ClassVar

import attrs
import pytest

from pyvider.ephemerals.base import BaseEphemeralResource
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource import (
    CloseEphemeralResourceHandler,
)
from pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource import (
    OpenEphemeralResourceHandler,
)
from pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource import (
    RenewEphemeralResourceHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import PvsSchema, a_str, s_resource

STATELESS = "stateless_token"


@attrs.define(frozen=True)
class TokenConfig:
    name: str | None = None


@attrs.define(frozen=True)
class TokenResult:
    value: str | None = None


class StatelessToken(BaseEphemeralResource):
    """Reads a value and keeps nothing between calls, so declares no private state."""

    config_class = TokenConfig

    closed: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"value": a_str(computed=True)})

    async def open(self, ctx: Any) -> tuple[Any, Any, Any]:
        return TokenResult(value="opened"), None, None

    async def renew(self, ctx: Any) -> tuple[Any, Any]:
        return None, datetime.now(UTC) + timedelta(minutes=5)

    async def close(self, ctx: Any) -> None:
        type(self).closed.append("closed")


@pytest.fixture
def stateless() -> Any:
    StatelessToken.closed = []
    hub.register("ephemeral_resource", STATELESS, StatelessToken)

    yield StatelessToken

    hub.unregister("ephemeral_resource", STATELESS)
    StatelessToken.closed = []


@pytest.mark.asyncio
async def test_open_succeeds_without_private_state(stateless: Any) -> None:
    """Baseline: opening one is fine, which is why close has to be too."""
    opened = await OpenEphemeralResourceHandler(
        pb.OpenEphemeralResource.Request(type_name=STATELESS),
        context=None,
    )

    assert not opened.diagnostics, f"open failed: {opened.diagnostics}"
    assert not opened.private, "the fixture unexpectedly produced private state"


@pytest.mark.asyncio
async def test_close_succeeds_without_private_state(stateless: Any) -> None:
    """Terraform closes everything it opened; this must not be the failure."""
    closed = await CloseEphemeralResourceHandler(
        pb.CloseEphemeralResource.Request(type_name=STATELESS),
        context=None,
    )

    assert not closed.diagnostics, (
        f"closing an ephemeral resource that keeps no private state failed: {closed.diagnostics}"
    )
    assert stateless.closed == ["closed"], "the resource's own close hook never ran"


@pytest.mark.asyncio
async def test_renew_succeeds_without_private_state(stateless: Any) -> None:
    renewed = await RenewEphemeralResourceHandler(
        pb.RenewEphemeralResource.Request(type_name=STATELESS),
        context=None,
    )

    assert not renewed.diagnostics, f"renew failed: {renewed.diagnostics}"


@pytest.mark.asyncio
async def test_an_unknown_type_still_reports_a_usable_error(stateless: Any) -> None:
    """The genuine failure keeps a diagnostic a practitioner can act on."""
    closed = await CloseEphemeralResourceHandler(
        pb.CloseEphemeralResource.Request(type_name="no_such_ephemeral"),
        context=None,
    )

    assert closed.diagnostics, "an unknown ephemeral type produced no diagnostic"
    detail = " ".join(d.summary + " " + d.detail for d in closed.diagnostics)
    assert "no_such_ephemeral" in detail


# 🐍🏗️🔚
