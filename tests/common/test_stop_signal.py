#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""StopProvider asks in-flight work to stop; it does not tear the server down.

Terraform's contract for Stop is advisory: it halts what is running and returns
immediately, and Terraform then waits for the calls already in flight to come
back on their own (internal/providers/provider.go:63-73). Tearing the process
down is a separate step, driven by `Close()` and go-plugin's `Kill()`
(internal/plugin6/grpc_provider.go:1885-1904). terraform-plugin-go implements
Stop by cancelling contexts and carries on serving
(tfprotov6/tf6server/server.go:412-454).

This module is the signal a resource can watch to cooperate with that.
"""

from __future__ import annotations

import pytest

from pyvider.common.stop_signal import is_stop_requested, request_stop, reset_stop_signal


@pytest.fixture(autouse=True)
def _clean_signal() -> None:
    reset_stop_signal()
    yield
    reset_stop_signal()


def test_no_stop_is_requested_to_begin_with() -> None:
    assert is_stop_requested() is False


def test_requesting_a_stop_is_visible() -> None:
    request_stop()

    assert is_stop_requested() is True


def test_requesting_a_stop_twice_is_harmless() -> None:
    """Terraform may call StopProvider more than once for one interruption."""
    request_stop()
    request_stop()

    assert is_stop_requested() is True


def test_the_signal_can_be_awaited() -> None:
    """A resource that is idle-waiting can block on the signal instead of polling."""
    from pyvider.common.stop_signal import stop_event

    event = stop_event()
    assert not event.is_set()

    request_stop()

    assert event.is_set()


def test_a_context_reports_the_request(monkeypatch: pytest.MonkeyPatch) -> None:
    """Resource code reaches the signal through the context it is already given."""
    from pyvider.resources.context import ResourceContext

    ctx: ResourceContext = ResourceContext()
    assert ctx.stop_requested is False

    request_stop()

    assert ctx.stop_requested is True


# 🐍🏗️🔚
