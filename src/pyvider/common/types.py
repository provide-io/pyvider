#
# pyvider/common/types.py
#
"""Defines common, primitive type aliases used across the framework."""

from typing import Any, TypeVar

StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")

type SchemaType = dict[str, Any]

__all__ = ["ConfigType", "SchemaType", "StateType"]

# 🐍🏗️


# 🐍🏗️📄🪄
