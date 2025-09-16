# pyvider/common/operation_context.py
"""
Manages the operational context for CTY type and value processing.
"""

import contextlib
from contextvars import ContextVar
from enum import Enum, auto

from provide.foundation import logger


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
def operation_context(context: OperationContext) -> None:
    """A context manager to temporarily set the CTY operational context."""
    logger.debug(f"🧰🔄📊 Pushing operation context: {context.name}")
    token = _current_operation_context.set(context)
    try:
        yield
    finally:
        _current_operation_context.reset(token)
        logger.debug(f"🧰🔄📊 Popped operation context, restored to: {_current_operation_context.get().name}")
