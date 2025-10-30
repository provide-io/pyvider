#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Defines common, primitive type aliases used across the framework."""

from typing import Any, TypeAlias, TypeVar

StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")

SchemaType: TypeAlias = dict[str, Any]

__all__ = ["ConfigType", "SchemaType", "StateType"]

# 🐍🏗️🔚
