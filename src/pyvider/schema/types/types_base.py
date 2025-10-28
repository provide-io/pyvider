#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Base protocols to prevent circular imports in schema definitions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pyvider.cty import CtyType


@runtime_checkable
class PvsType(Protocol):
    """
    A Protocol that all Pyvider Schema type definition classes must implement.
    It ensures that any schema type object can be converted into its
    corresponding CtyType, which is essential for the conversion and
    marshalling layers of the framework.
    """

    def to_cty_type(self) -> CtyType:
        """Converts the Pyvider Schema type to its equivalent CtyType."""
        ...


# 🐍🏗️🔚
