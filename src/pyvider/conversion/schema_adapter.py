#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from functools import lru_cache
import json
from functools import lru_cache

from pyvider.cty import CtyType
from pyvider.cty.conversion.type_encoder import encode_cty_type_to_wire_json
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.types import (
    NestingMode,
    PvsAttribute,
    PvsNestedBlock,
    PvsObjectType,
    PvsSchema,
)


@lru_cache(maxsize=256)
def _encode_cty_type_bytes(cty_type: CtyType) -> bytes:
    """Cache JSON-encoded wire representation of CtyType objects."""
    return json.dumps(encode_cty_type_to_wire_json(cty_type)).encode("utf-8")


# Module-level constant — avoids rebuilding on every call
_NESTING_MODE_MAP: dict[NestingMode, int] | None = None


def _get_nesting_mode_map() -> dict[NestingMode, int]:
    global _NESTING_MODE_MAP  # noqa: PLW0603
    if _NESTING_MODE_MAP is None:
        _NESTING_MODE_MAP = {
            NestingMode.SINGLE: pb.Schema.NestedBlock.NestingMode.SINGLE,
            NestingMode.LIST: pb.Schema.NestedBlock.NestingMode.LIST,
            NestingMode.SET: pb.Schema.NestedBlock.NestingMode.SET,
            NestingMode.MAP: pb.Schema.NestedBlock.NestingMode.MAP,
            NestingMode.GROUP: pb.Schema.NestedBlock.NestingMode.GROUP,
        }
    return _NESTING_MODE_MAP


async def pvs_schema_to_proto(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message.

    Caches by object identity since PvsSchema is frozen (immutable).
    Stores a reference to the source object to prevent id reuse after GC.
    """
    schema_id = id(schema)
    entry = _proto_schema_cache.get(schema_id)
    if entry is not None and entry[0] is schema:
        return entry[1]
    proto_block = _pvs_object_type_to_proto(schema.block)
    result = pb.Schema(version=schema.version, block=proto_block)
    _proto_schema_cache[schema_id] = (schema, result)
    return result


def _pvs_object_type_to_proto(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message.

    Caches by object identity since PvsObjectType is frozen (immutable).
    Stores a reference to the source object to prevent id reuse after GC.
    """
    block_id = id(block)
    entry = _proto_block_cache.get(block_id)
    if entry is not None and entry[0] is block:
        return entry[1]
    result = pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )
    _proto_block_cache[block_id] = (block, result)
    return result


def _pvs_attribute_to_proto(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    return pb.Schema.Attribute(
        name=attr.name,
        type=_encode_cty_type_bytes(attr.type),
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def _pvs_nested_block_to_proto(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
    """Converts a PvsNestedBlock to a protobuf NestedBlock message."""
    nesting_map = _get_nesting_mode_map()
    return pb.Schema.NestedBlock(
        type_name=nb.type_name,
        block=_pvs_object_type_to_proto(nb.block),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


# 🐍🏗️🔚
