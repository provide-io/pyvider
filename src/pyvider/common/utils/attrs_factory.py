#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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

# Ordered, because the first match wins. Primitives, then collections, then the
# complex and dynamic types that carry no useful Python hint of their own.
_PYTHON_TYPE_HINTS: tuple[tuple[Any, Any], ...] = (
    (CtyString, str | None),
    (CtyNumber, int | float | None),
    (CtyBool, bool | None),
    (CtyList, list | None),
    (CtyMap, dict | None),
    (CtySet, set | None),
    (CtyTuple, tuple | None),
    (CtyObject | CtyDynamic, dict | Any | None),
)


def _pvs_type_to_python_type(pvs_type: PvsAttribute) -> Any:
    """Maps a CtyType from a PvsAttribute to a Python type hint."""
    for cty_class, hint in _PYTHON_TYPE_HINTS:
        if isinstance(pvs_type.type, cty_class):
            return hint
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
