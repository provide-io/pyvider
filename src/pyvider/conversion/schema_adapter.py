#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from functools import lru_cache
import json

from pyvider.cty import CtyBool, CtyNumber, CtyString, CtyType
from pyvider.cty.conversion.type_encoder import encode_cty_type_to_wire_json
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.exceptions import PvsSchemaDefinitionError
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


_proto_block_cache: dict[int, tuple[PvsObjectType, pb.Schema.Block]] = {}
_proto_schema_cache: dict[int, tuple[PvsSchema, pb.Schema]] = {}


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


def _pvs_attribute_to_proto(attr: PvsAttribute, name: str | None = None) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message.

    An object-typed attribute (`a_obj`) is sent as a `nested_type` rather than a
    flat object type. Terraform treats a flat object attribute as a single
    opaque value -- the planned value must equal the configured one exactly, so
    a member's Optional+Computed flags, and therefore any default the provider
    resolves for it, could never take effect. `nested_type` is what carries the
    per-member flags across the wire; the configuration syntax is unchanged.
    """
    attribute = pb.Schema.Attribute(
        name=name if name is not None else attr.name,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
        write_only=attr.write_only,
    )
    if attr.object_type is not None:
        # `type` and `nested_type` are mutually exclusive; Terraform reads the
        # implied type off the nested schema.
        attribute.nested_type.CopyFrom(_pvs_object_type_to_proto_object(attr.object_type))
    else:
        attribute.type = _encode_cty_type_bytes(attr.type)
    return attribute


def _pvs_object_type_to_proto_object(obj: PvsObjectType) -> pb.Schema.Object:
    """Converts the `PvsObjectType` behind an `a_obj()` attribute to a nested type."""
    if obj.block_types:
        names = ", ".join(repr(block.type_name) for block in obj.block_types)
        raise PvsSchemaDefinitionError(
            "An a_obj() nested type cannot contain nested blocks because the "
            f"Terraform protocol cannot encode them in Schema.Object: {names}. "
            "Declare the blocks on a Schema.Block with the b_* factories instead."
        )
    return pb.Schema.Object(
        attributes=[_pvs_attribute_to_proto(attr, name) for name, attr in obj.attributes.items()],
        nesting=pb.Schema.Object.NestingMode.SINGLE,
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


# Identity is compared by equality and must be "wholly representative of all
# data necessary to compare two managed resource instances", so only flat
# scalars are valid.
_IDENTITY_SCALAR_TYPES = (CtyString, CtyNumber, CtyBool)


def pvs_identity_schema_to_proto(schema: PvsSchema) -> pb.ResourceIdentitySchema:
    """Convert an identity PvsSchema into a protobuf ResourceIdentitySchema.

    Identity reuses PvsSchema, so this is the single place the identity-specific
    constraints are enforced. `required` maps to `required_for_import` and
    `optional` to `optional_for_import`, matching the collapse Terraform core
    performs in ProtoToIdentitySchema.
    """
    block = schema.block

    if block.block_types:
        raise PvsSchemaDefinitionError(
            "Identity schemas cannot declare nested blocks. Identity must be a flat set of scalar attributes."
        )

    attributes = []
    for name, attr in block.attributes.items():
        if not isinstance(attr.type, _IDENTITY_SCALAR_TYPES):
            raise PvsSchemaDefinitionError(
                f"Identity attribute '{name}' has type {type(attr.type).__name__}; "
                "identity attributes must be scalar (string, number, or bool)."
            )
        if attr.default is not None:
            # Checked before `computed`, which a default implies: reporting the
            # implied flag would name something the practitioner never wrote.
            raise PvsSchemaDefinitionError(
                f"Identity attribute '{name}' declares a default, which is not "
                "meaningful for identity. Identity is assigned by the provider "
                "when a resource is created and read back verbatim on import; it "
                "is never filled in from configuration, so a default could never "
                "apply.\n\n"
                "Suggestion: drop `default=` and set the value in the resource's "
                "create or import logic."
            )

        if attr.computed:
            raise PvsSchemaDefinitionError(
                f"Identity attribute '{name}' is marked computed, which is not "
                "meaningful for identity and would alter the identity object type."
            )
        if attr.sensitive:
            raise PvsSchemaDefinitionError(
                f"Identity attribute '{name}' is marked sensitive, which is not meaningful for identity."
            )

        attributes.append(
            pb.ResourceIdentitySchema.IdentityAttribute(
                name=name,
                type=_encode_cty_type_bytes(attr.type),
                required_for_import=attr.required,
                optional_for_import=attr.optional,
                description=attr.description,
            )
        )

    return pb.ResourceIdentitySchema(version=schema.version, identity_attributes=attributes)


# 🐍🏗️🔚
