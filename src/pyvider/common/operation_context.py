#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Manages the operational context for CTY type and value processing."""

from collections.abc import Generator
import contextlib
from contextvars import ContextVar
from enum import Enum, auto


class OperationContext(Enum):
    """
    Enumerates different operational contexts within the Pyvider system.
    """

    DEFAULT = auto()
    CONFIG = auto()
    STATE = auto()
    PLAN = auto()
    APPLY = auto()
    READ = auto()
    FUNCTION = auto()
    SCHEMA = auto()


_current_operation_context: ContextVar[OperationContext] = ContextVar(
    "current_operation_context", default=OperationContext.DEFAULT
)


def get_current_operation() -> OperationContext:
    """Returns the currently active OperationContext."""
    return _current_operation_context.get()


@contextlib.contextmanager
def operation_context(context: OperationContext) -> Generator[None, None, None]:
    """A context manager to temporarily set the CTY operational context."""
    token = _current_operation_context.set(context)
    try:
        yield
    finally:
        _current_operation_context.reset(token)


# 🐍🏗️🔚
