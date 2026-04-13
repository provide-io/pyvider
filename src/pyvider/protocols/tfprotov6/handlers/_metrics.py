#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared metric-collection wrapper for tfprotov6 RPC handlers.

Every RPC handler follows the same outer pattern: increment a request
counter, time the call, bump an error counter on exceptions, and observe
a duration histogram in finally. This module factors that pattern into
a single decorator so the handlers themselves only express their
domain logic.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from functools import wraps
import time
from typing import TypeVar

from provide.foundation.errors import resilient

from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)

R = TypeVar("R")


def rpc_handler(
    name: str,
) -> Callable[[Callable[..., Awaitable[R]]], Callable[..., Awaitable[R]]]:
    """Decorator wrapping an async RPC handler with metrics + @resilient().

    Args:
        name: Metric label for this handler, e.g. "ApplyResourceChange".

    The decorated function retains its original signature. The wrapper:
      - Increments handler_requests on entry.
      - Delegates to the wrapped coroutine (under @resilient()).
      - Increments handler_errors if the wrapped coroutine raises.
      - Always observes handler_duration in finally.
    """

    def _wrap(fn: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        resilient_fn = resilient()(fn)

        @wraps(fn)
        async def _handler(*args: object, **kwargs: object) -> R:
            start = time.perf_counter()
            handler_requests.inc(handler=name)
            try:
                return await resilient_fn(*args, **kwargs)
            except Exception:
                handler_errors.inc(handler=name)
                raise
            finally:
                handler_duration.observe(time.perf_counter() - start, handler=name)

        return _handler

    return _wrap


# 🐍🏗️🔚
