#
# pyvider/resources/__init__.py
#

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.decorators import register_resource
from pyvider.resources.private_state import PrivateState

__all__ = [
    "BaseResource",
    "PrivateState",
    "ResourceContext",
    "register_resource",
]
