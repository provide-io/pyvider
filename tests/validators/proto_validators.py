#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any


def validate_proto(proto: Any) -> None:
    """
    Validates a protocol buffer object to ensure it meets expected schema rules.

    Raises:
        ValueError: If any validation rule is violated.
    """
    if not proto.description:
        raise ValueError("Proto must have a non-empty 'description'.")

    if not proto.attributes:
        raise ValueError("Proto must include at least one 'attribute'.")

    for attr in proto.attributes:
        if not hasattr(attr, "name") or not attr.name:
            raise ValueError(f"Proto attribute missing 'name': {attr}")
        if not hasattr(attr, "type") or not attr.type:
            raise ValueError(f"Proto attribute missing 'type': {attr}")

    if hasattr(proto, "block_types"):
        for block in proto.block_types:
            if not hasattr(block, "name") or not block.name:
                raise ValueError(f"Proto block missing 'name': {block}")
            if not hasattr(block, "nested") or not isinstance(block.nested, bool):
                raise ValueError(f"Proto block 'nested' must be a boolean: {block}")


# 🐍🏗️🔚
