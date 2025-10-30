#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The pyvider.conversion package provides the primary bridge between the wire
protocol (via DynamicValue) and the framework's internal CtyValue representation."""

from pyvider.conversion.adapter import cty_to_native
from pyvider.conversion.marshaler import marshal, marshal_value, unmarshal, unmarshal_value
from pyvider.conversion.schema_adapter import pvs_schema_to_proto
from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.cty.conversion import infer_cty_type_from_raw

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

# 🐍🏗️🔚
