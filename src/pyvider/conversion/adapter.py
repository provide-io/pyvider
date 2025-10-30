#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Canonical adapter for converting between Python native types and CtyValue objects.
This module re-exports the canonical implementation from the cty library."""

from pyvider.cty.conversion.adapter import cty_to_native

# Re-export to make it available to the rest of the framework under this path.
__all__ = ["cty_to_native"]

# 🐍🏗️🔚
