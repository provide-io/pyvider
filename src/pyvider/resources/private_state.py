# pyvider/resources/private_state.py
from attrs import define


@define(frozen=True)
class PrivateState:
    """
    A base marker class for private state data structures.
    Resource-specific private state classes can inherit from this
    for clarity and type-hinting purposes.
    """

    pass
