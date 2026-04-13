#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from enum import StrEnum


class StringKind(StrEnum):
    """Defines the interpretation of a string (e.g., for descriptions)."""

    PLAIN = "PLAIN"
    MARKDOWN = "MARKDOWN"


class NestingMode(StrEnum):
    """Defines how a nested block is represented in the configuration."""

    SINGLE = "SINGLE"
    LIST = "LIST"
    SET = "SET"
    MAP = "MAP"
    GROUP = "GROUP"


# 🐍🏗️🔚
