#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The provider-wide "stop what you are doing" signal.

Terraform's StopProvider is advisory. It asks the provider to halt whatever is
running and expects an immediate answer; the calls already in flight are still
expected to return on their own, and Terraform waits for them
(terraform/internal/providers/provider.go:63-73). Tearing the process down is a
separate step, driven by `Close()` and go-plugin's `Kill()`
(terraform/internal/plugin6/grpc_provider.go:1885-1904).

terraform-plugin-go implements Stop by cancelling the contexts it handed to
in-flight calls and carries on serving (tfprotov6/tf6server/server.go:412-454).
Python has no equivalent ambient cancellation, so this module is the signal a
long-running resource can watch instead, reachable from any context as
`ctx.stop_requested`.

A `threading.Event` rather than an `asyncio.Event` so that a resource doing
blocking work in a worker thread can watch the same signal as one awaiting on
the event loop, without either having to know which loop created it.
"""

from __future__ import annotations

import threading

__all__ = ["is_stop_requested", "request_stop", "reset_stop_signal", "stop_event"]

_STOP_EVENT = threading.Event()


def stop_event() -> threading.Event:
    """The signal itself, for a resource that would rather wait than poll."""
    return _STOP_EVENT


def request_stop() -> None:
    """Ask every in-flight operation to wind up. Idempotent.

    Terraform can send StopProvider more than once for a single interruption --
    the second Ctrl-C escalates -- so this says nothing about how many times it
    was asked, only that it was.
    """
    _STOP_EVENT.set()


def is_stop_requested() -> bool:
    """Whether Terraform has asked this provider to stop."""
    return _STOP_EVENT.is_set()


def reset_stop_signal() -> None:
    """Clear the signal.

    A provider process is not reused after a stop, so this exists for tests,
    which share one process across many simulated provider lifetimes.
    """
    _STOP_EVENT.clear()


# 🐍🏗️🔚
