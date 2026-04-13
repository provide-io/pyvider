#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any


def pre_mutation(context: Any) -> None:
    """
    Called before each mutation is tested.
    Can be used to skip certain mutations.
    """
    # Skip mutations in test files
    if "test_" in context.filename or "/tests/" in context.filename:
        context.skip = True

    # Skip mutations in generated files
    if "_version.py" in context.filename:
        context.skip = True

    # Skip mutations in protobuf generated files
    if "pb2" in context.filename or "_pb2" in context.filename:
        context.skip = True

    # Skip mutations in __init__ files (mostly imports)
    if "__init__.py" in context.filename:
        context.skip = True


# 🐍🏗️🔚
