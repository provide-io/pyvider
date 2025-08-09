#
# pyvider/conversion/__init__.py
#
"""
The pyvider.conversion package provides the primary bridge between the wire
protocol (via DynamicValue) and the framework's internal CtyValue representation.
"""

# Import the canonical type inference logic from the cty package.
from pyvider.cty.conversion import infer_cty_type_from_raw

from .adapter import cty_to_native
from .marshaler import marshal, marshal_value, unmarshal, unmarshal_value
from .schema_adapter import pvs_schema_to_proto
from .utils import unify_and_validate_list_of_objects

__all__ = [
    "cty_to_native",
    "infer_cty_type_from_raw",  # Export the canonical function
    "marshal",
    "marshal_value",
    "pvs_schema_to_proto",
    "unify_and_validate_list_of_objects",
    "unmarshal",
    "unmarshal_value",
]


# 🐍🏗️🚀🪄
