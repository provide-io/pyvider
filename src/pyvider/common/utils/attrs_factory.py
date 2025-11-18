#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

import attrs

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtySet,
    CtyString,
    CtyTuple,
)
from pyvider.schema.types import PvsAttribute


def _pvs_type_to_python_type(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    cty_type = pvs_type.type
    # Primitives
    if isinstance(cty_type, CtyString):
        return str | None
    if isinstance(cty_type, CtyNumber):
        return int | float | None
    if isinstance(cty_type, CtyBool):
        return bool | None
    # Collections
    if isinstance(cty_type, CtyList):
        return list | None
    if isinstance(cty_type, CtyMap):
        return dict | None
    if isinstance(cty_type, CtySet):
        return set | None
    if isinstance(cty_type, CtyTuple):
        return tuple | None
    # Complex/Dynamic
    if isinstance(cty_type, CtyObject | CtyDynamic):
        return dict | Any | None
    return Any | None


def create_attrs_class_from_schema(class_name: str, attributes: dict[str, PvsAttribute]) -> type:
    """
    Dynamically creates an attrs-decorated class from a schema definition.

    Args:
        class_name: The desired name for the new class.
        attributes: A dictionary of PvsAttribute objects defining the schema.

    Returns:
        A new, frozen attrs class.
    """
    attrs_fields = {}
    for name, pvs_attr in attributes.items():
        # Determine the default value or factory for the attrs.field
        if pvs_attr.default is not None:
            default_val = pvs_attr.default
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))
        elif isinstance(pvs_attr.type, CtyMap | CtyList):
            # Use a factory for mutable defaults like dict or list
            default_factory = dict if isinstance(pvs_attr.type, CtyMap) else list
            field_def = attrs.field(factory=default_factory, type=_pvs_type_to_python_type(pvs_attr))
        else:
            default_val = None
            field_def = attrs.field(default=default_val, type=_pvs_type_to_python_type(pvs_attr))

        attrs_fields[name] = field_def

    # Use attrs.make_class to programmatically create the class
    return attrs.make_class(class_name, attrs_fields, frozen=True)


# 🐍🏗️🔚
