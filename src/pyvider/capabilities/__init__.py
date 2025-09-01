# pyvider/capabilities/__init__.py

from pyvider.capabilities.base import BaseCapability
from pyvider.capabilities.decorators import register_capability, requires_capability

__all__ = [
    "BaseCapability",
    "register_capability",
    "requires_capability",
]
