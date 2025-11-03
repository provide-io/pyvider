#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import json

from pyvider.cty.conversion.type_encoder import encode_cty_type_to_wire_json
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.types import (
    NestingMode,
    PvsAttribute,
    PvsNestedBlock,
    PvsObjectType,
    PvsSchema,
)


async def pvs_schema_to_proto(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(version=schema.version, block=proto_block)


def _pvs_object_type_to_proto(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def _pvs_attribute_to_proto(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def _pvs_nested_block_to_proto(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
    """Converts a PvsNestedBlock to a protobuf NestedBlock message."""
    nesting_map = {
        NestingMode.SINGLE: pb.Schema.NestedBlock.NestingMode.SINGLE,
        NestingMode.LIST: pb.Schema.NestedBlock.NestingMode.LIST,
        NestingMode.SET: pb.Schema.NestedBlock.NestingMode.SET,
        NestingMode.MAP: pb.Schema.NestedBlock.NestingMode.MAP,
        NestingMode.GROUP: pb.Schema.NestedBlock.NestingMode.GROUP,
    }
    return pb.Schema.NestedBlock(
        type_name=nb.type_name,
        block=_pvs_object_type_to_proto(nb.block),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


# 🐍🏗️🔚
