# pyvider/src/pyvider/conversion/adapter.py
"""
Canonical adapter for converting between Python native types and CtyValue objects.
This module re-exports the canonical implementation from the cty library.
"""

# This is the single source of truth for this conversion.
from pyvider.cty.conversion.adapter import cty_to_native

# Re-export to make it available to the rest of the framework under this path.
__all__ = ["cty_to_native"]
