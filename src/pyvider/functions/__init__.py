#
# pyvider/functions/__init__.py
#

"""
Pyvider Functions Module

This module provides the core infrastructure for implementing and registering
Terraform functions in Pyvider providers.
"""

from .adapters import function_to_dict
from .base import (
    BaseFunction,
    FunctionAdapter,
    FunctionParameter,
    FunctionReturnType,
)
from .decorators import register_function

__all__ = [
    "BaseFunction",
    "FunctionAdapter",
    "FunctionParameter",
    "FunctionReturnType",
    "function_to_dict",
    "register_function",
]
