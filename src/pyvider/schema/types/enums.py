#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from enum import Enum


class StringKind(str, Enum):
    """Defines the interpretation of a string (e.g., for descriptions)."""

    PLAIN = "PLAIN"
    MARKDOWN = "MARKDOWN"


class NestingMode(str, Enum):
    """Defines how a nested block is represented in the configuration."""

    SINGLE = "SINGLE"
    LIST = "LIST"
    SET = "SET"
    MAP = "MAP"
    GROUP = "GROUP"


# 🐍🏗️🔚
