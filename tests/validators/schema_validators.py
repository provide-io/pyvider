#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any


def validate_schema_dict(schema: dict[str, Any]) -> None:
    """
    Validates that a schema dictionary meets required specifications.

    Raises:
        ValueError: If any validation rule is violated.
    """
    if "description" not in schema or not schema["description"]:
        raise ValueError("Schema must include a non-empty 'description'.")

    if "attributes" not in schema or not schema["attributes"]:
        raise ValueError("Schema must include at least one 'attribute'.")

    for attr in schema["attributes"]:
        if "name" not in attr or not attr["name"]:
            raise ValueError(f"Attribute missing 'name': {attr}")
        if "type" not in attr or not attr["type"]:
            raise ValueError(f"Attribute missing 'type': {attr}")

    if "block_types" in schema:
        for block in schema["block_types"]:
            if "name" not in block or not block["name"]:
                raise ValueError(f"Block missing 'name': {block}")
            if "nested" not in block or not isinstance(block["nested"], bool):
                raise ValueError(f"Block 'nested' must be a boolean: {block}")


def validate_schema_object(schema: Any) -> None:
    """
    Validates a schema object that has `attributes` and `block_types` as attributes.

    Raises:
        ValueError: If any validation rule is violated.
    """
    if not schema.description:
        raise ValueError("Schema must include a non-empty 'description'.")

    if not schema.attributes:
        raise ValueError("Schema must include at least one 'attribute'.")

    for attr in schema.attributes:
        if not hasattr(attr, "name") or not attr.name:
            raise ValueError(f"Attribute missing 'name': {attr}")
        if not hasattr(attr, "type") or not attr.type:
            raise ValueError(f"Attribute missing 'type': {attr}")

    if hasattr(schema, "block_types"):
        for block in schema.block_types:
            if not hasattr(block, "name") or not block.name:
                raise ValueError(f"Block missing 'name': {block}")
            if not hasattr(block, "nested") or not isinstance(block.nested, bool):
                raise ValueError(f"Block 'nested' must be a boolean: {block}")


# 🐍🏗️🔚
