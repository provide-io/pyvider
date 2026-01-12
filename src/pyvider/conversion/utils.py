#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Provides general-purpose, high-level conversion utilities for the framework."""

from typing import Any

from pyvider.cty import CtyDynamic, CtyList, CtyObject, CtyType, CtyValue

# FIX: Correctly import from the pyvider-cty library's canonical location.
from pyvider.cty.conversion import infer_cty_type_from_raw


def unify_and_validate_list_of_objects(dict_list: list[dict[str, Any]]) -> CtyValue[Any]:
    """
    Analyzes a list of dictionaries, infers a unified CtyObject schema,
    and returns a validated CtyValue representing a CtyList(CtyObject).
    """
    if not dict_list:
        return CtyList(element_type=CtyDynamic()).validate([])  # type: ignore[no-any-return]

    all_keys: set[str] = set()
    attribute_types: dict[str, CtyType[object]] = {}

    for item in dict_list:
        all_keys.update(item.keys())
        for key, value in item.items():
            inferred_type = infer_cty_type_from_raw(value)
            if key not in attribute_types:
                attribute_types[key] = inferred_type
            elif not attribute_types[key].equal(inferred_type):
                attribute_types[key] = CtyDynamic()

    optional_keys_list: list[str] = [key for key in all_keys if not all(key in item for item in dict_list)]

    unified_object_type = CtyObject(
        attribute_types=attribute_types,
        optional_attributes=optional_keys_list,  # type: ignore[arg-type]
    )

    final_list_type = CtyList(element_type=unified_object_type)

    return final_list_type.validate(dict_list)  # type: ignore[no-any-return]


# 🐍🏗️🔚
