#
# pyvider/common_types.py
#
"""Defines common, primitive type aliases used across the framework."""

from typing import Any, TypeAlias, TypeVar

StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")

SchemaType: TypeAlias = dict[str, Any]

__all__ = ["ConfigType", "SchemaType", "StateType"]

# 🐍🏗️
