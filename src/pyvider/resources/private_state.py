#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from attrs import define


@define(frozen=True)
class PrivateState:
    """
    A base marker class for private state data structures.
    Resource-specific private state classes can inherit from this
    for clarity and type-hinting purposes.
    """

    pass


# 🐍🏗️🔚
