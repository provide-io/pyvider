# pyvider/src/pyvider/conversion/schema_adapter.py
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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


async def x_pvs_schema_to_proto__mutmut_orig(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(version=schema.version, block=proto_block)


async def x_pvs_schema_to_proto__mutmut_1(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = None
    return pb.Schema(version=schema.version, block=proto_block)


async def x_pvs_schema_to_proto__mutmut_2(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(None)
    return pb.Schema(version=schema.version, block=proto_block)


async def x_pvs_schema_to_proto__mutmut_3(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(version=None, block=proto_block)


async def x_pvs_schema_to_proto__mutmut_4(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(version=schema.version, block=None)


async def x_pvs_schema_to_proto__mutmut_5(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(block=proto_block)


async def x_pvs_schema_to_proto__mutmut_6(schema: PvsSchema) -> pb.Schema:
    """Converts a PvsSchema into a protobuf Schema message."""
    proto_block = _pvs_object_type_to_proto(schema.block)
    return pb.Schema(version=schema.version, )

x_pvs_schema_to_proto__mutmut_mutants : ClassVar[MutantDict] = {
'x_pvs_schema_to_proto__mutmut_1': x_pvs_schema_to_proto__mutmut_1, 
    'x_pvs_schema_to_proto__mutmut_2': x_pvs_schema_to_proto__mutmut_2, 
    'x_pvs_schema_to_proto__mutmut_3': x_pvs_schema_to_proto__mutmut_3, 
    'x_pvs_schema_to_proto__mutmut_4': x_pvs_schema_to_proto__mutmut_4, 
    'x_pvs_schema_to_proto__mutmut_5': x_pvs_schema_to_proto__mutmut_5, 
    'x_pvs_schema_to_proto__mutmut_6': x_pvs_schema_to_proto__mutmut_6
}

def pvs_schema_to_proto(*args, **kwargs):
    result = _mutmut_trampoline(x_pvs_schema_to_proto__mutmut_orig, x_pvs_schema_to_proto__mutmut_mutants, args, kwargs)
    return result 

pvs_schema_to_proto.__signature__ = _mutmut_signature(x_pvs_schema_to_proto__mutmut_orig)
x_pvs_schema_to_proto__mutmut_orig.__name__ = 'x_pvs_schema_to_proto'


def x__pvs_object_type_to_proto__mutmut_orig(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_1(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=None,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_2(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=None,
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_3(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=None,
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_4(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=None,
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_5(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=None,
    )


def x__pvs_object_type_to_proto__mutmut_6(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_7(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_8(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_9(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_10(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        )


def x__pvs_object_type_to_proto__mutmut_11(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=2,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_12(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(None) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_13(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(None) for nb in block.block_types],
        description=block.description or "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_14(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description and "",
        deprecated=block.deprecated,
    )


def x__pvs_object_type_to_proto__mutmut_15(block: PvsObjectType) -> pb.Schema.Block:
    """Converts a PvsObjectType to a protobuf Block message."""
    return pb.Schema.Block(
        version=1,
        attributes=[_pvs_attribute_to_proto(attr) for attr in block.attributes.values()],
        block_types=[_pvs_nested_block_to_proto(nb) for nb in block.block_types],
        description=block.description or "XXXX",
        deprecated=block.deprecated,
    )

x__pvs_object_type_to_proto__mutmut_mutants : ClassVar[MutantDict] = {
'x__pvs_object_type_to_proto__mutmut_1': x__pvs_object_type_to_proto__mutmut_1, 
    'x__pvs_object_type_to_proto__mutmut_2': x__pvs_object_type_to_proto__mutmut_2, 
    'x__pvs_object_type_to_proto__mutmut_3': x__pvs_object_type_to_proto__mutmut_3, 
    'x__pvs_object_type_to_proto__mutmut_4': x__pvs_object_type_to_proto__mutmut_4, 
    'x__pvs_object_type_to_proto__mutmut_5': x__pvs_object_type_to_proto__mutmut_5, 
    'x__pvs_object_type_to_proto__mutmut_6': x__pvs_object_type_to_proto__mutmut_6, 
    'x__pvs_object_type_to_proto__mutmut_7': x__pvs_object_type_to_proto__mutmut_7, 
    'x__pvs_object_type_to_proto__mutmut_8': x__pvs_object_type_to_proto__mutmut_8, 
    'x__pvs_object_type_to_proto__mutmut_9': x__pvs_object_type_to_proto__mutmut_9, 
    'x__pvs_object_type_to_proto__mutmut_10': x__pvs_object_type_to_proto__mutmut_10, 
    'x__pvs_object_type_to_proto__mutmut_11': x__pvs_object_type_to_proto__mutmut_11, 
    'x__pvs_object_type_to_proto__mutmut_12': x__pvs_object_type_to_proto__mutmut_12, 
    'x__pvs_object_type_to_proto__mutmut_13': x__pvs_object_type_to_proto__mutmut_13, 
    'x__pvs_object_type_to_proto__mutmut_14': x__pvs_object_type_to_proto__mutmut_14, 
    'x__pvs_object_type_to_proto__mutmut_15': x__pvs_object_type_to_proto__mutmut_15
}

def _pvs_object_type_to_proto(*args, **kwargs):
    result = _mutmut_trampoline(x__pvs_object_type_to_proto__mutmut_orig, x__pvs_object_type_to_proto__mutmut_mutants, args, kwargs)
    return result 

_pvs_object_type_to_proto.__signature__ = _mutmut_signature(x__pvs_object_type_to_proto__mutmut_orig)
x__pvs_object_type_to_proto__mutmut_orig.__name__ = 'x__pvs_object_type_to_proto'


def x__pvs_attribute_to_proto__mutmut_orig(attr: PvsAttribute) -> pb.Schema.Attribute:
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


def x__pvs_attribute_to_proto__mutmut_1(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = None
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


def x__pvs_attribute_to_proto__mutmut_2(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode(None)
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


def x__pvs_attribute_to_proto__mutmut_3(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(None).encode("utf-8")
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


def x__pvs_attribute_to_proto__mutmut_4(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(None)).encode("utf-8")
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


def x__pvs_attribute_to_proto__mutmut_5(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("XXutf-8XX")
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


def x__pvs_attribute_to_proto__mutmut_6(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("UTF-8")
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


def x__pvs_attribute_to_proto__mutmut_7(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=None,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_8(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=None,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_9(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=None,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_10(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=None,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_11(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=None,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_12(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=None,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_13(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=None,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_14(attr: PvsAttribute) -> pb.Schema.Attribute:
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
        deprecated=None,
    )


def x__pvs_attribute_to_proto__mutmut_15(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_16(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_17(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_18(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        optional=attr.optional,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_19(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        computed=attr.computed,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_20(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        sensitive=attr.sensitive,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_21(attr: PvsAttribute) -> pb.Schema.Attribute:
    """Converts a PvsAttribute to a protobuf Attribute message."""
    type_bytes = json.dumps(encode_cty_type_to_wire_json(attr.type)).encode("utf-8")
    return pb.Schema.Attribute(
        name=attr.name,
        type=type_bytes,
        description=attr.description,
        required=attr.required,
        optional=attr.optional,
        computed=attr.computed,
        deprecated=attr.deprecated,
    )


def x__pvs_attribute_to_proto__mutmut_22(attr: PvsAttribute) -> pb.Schema.Attribute:
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
        )

x__pvs_attribute_to_proto__mutmut_mutants : ClassVar[MutantDict] = {
'x__pvs_attribute_to_proto__mutmut_1': x__pvs_attribute_to_proto__mutmut_1, 
    'x__pvs_attribute_to_proto__mutmut_2': x__pvs_attribute_to_proto__mutmut_2, 
    'x__pvs_attribute_to_proto__mutmut_3': x__pvs_attribute_to_proto__mutmut_3, 
    'x__pvs_attribute_to_proto__mutmut_4': x__pvs_attribute_to_proto__mutmut_4, 
    'x__pvs_attribute_to_proto__mutmut_5': x__pvs_attribute_to_proto__mutmut_5, 
    'x__pvs_attribute_to_proto__mutmut_6': x__pvs_attribute_to_proto__mutmut_6, 
    'x__pvs_attribute_to_proto__mutmut_7': x__pvs_attribute_to_proto__mutmut_7, 
    'x__pvs_attribute_to_proto__mutmut_8': x__pvs_attribute_to_proto__mutmut_8, 
    'x__pvs_attribute_to_proto__mutmut_9': x__pvs_attribute_to_proto__mutmut_9, 
    'x__pvs_attribute_to_proto__mutmut_10': x__pvs_attribute_to_proto__mutmut_10, 
    'x__pvs_attribute_to_proto__mutmut_11': x__pvs_attribute_to_proto__mutmut_11, 
    'x__pvs_attribute_to_proto__mutmut_12': x__pvs_attribute_to_proto__mutmut_12, 
    'x__pvs_attribute_to_proto__mutmut_13': x__pvs_attribute_to_proto__mutmut_13, 
    'x__pvs_attribute_to_proto__mutmut_14': x__pvs_attribute_to_proto__mutmut_14, 
    'x__pvs_attribute_to_proto__mutmut_15': x__pvs_attribute_to_proto__mutmut_15, 
    'x__pvs_attribute_to_proto__mutmut_16': x__pvs_attribute_to_proto__mutmut_16, 
    'x__pvs_attribute_to_proto__mutmut_17': x__pvs_attribute_to_proto__mutmut_17, 
    'x__pvs_attribute_to_proto__mutmut_18': x__pvs_attribute_to_proto__mutmut_18, 
    'x__pvs_attribute_to_proto__mutmut_19': x__pvs_attribute_to_proto__mutmut_19, 
    'x__pvs_attribute_to_proto__mutmut_20': x__pvs_attribute_to_proto__mutmut_20, 
    'x__pvs_attribute_to_proto__mutmut_21': x__pvs_attribute_to_proto__mutmut_21, 
    'x__pvs_attribute_to_proto__mutmut_22': x__pvs_attribute_to_proto__mutmut_22
}

def _pvs_attribute_to_proto(*args, **kwargs):
    result = _mutmut_trampoline(x__pvs_attribute_to_proto__mutmut_orig, x__pvs_attribute_to_proto__mutmut_mutants, args, kwargs)
    return result 

_pvs_attribute_to_proto.__signature__ = _mutmut_signature(x__pvs_attribute_to_proto__mutmut_orig)
x__pvs_attribute_to_proto__mutmut_orig.__name__ = 'x__pvs_attribute_to_proto'


def x__pvs_nested_block_to_proto__mutmut_orig(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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


def x__pvs_nested_block_to_proto__mutmut_1(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
    """Converts a PvsNestedBlock to a protobuf NestedBlock message."""
    nesting_map = None
    return pb.Schema.NestedBlock(
        type_name=nb.type_name,
        block=_pvs_object_type_to_proto(nb.block),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_2(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
    """Converts a PvsNestedBlock to a protobuf NestedBlock message."""
    nesting_map = {
        NestingMode.SINGLE: pb.Schema.NestedBlock.NestingMode.SINGLE,
        NestingMode.LIST: pb.Schema.NestedBlock.NestingMode.LIST,
        NestingMode.SET: pb.Schema.NestedBlock.NestingMode.SET,
        NestingMode.MAP: pb.Schema.NestedBlock.NestingMode.MAP,
        NestingMode.GROUP: pb.Schema.NestedBlock.NestingMode.GROUP,
    }
    return pb.Schema.NestedBlock(
        type_name=None,
        block=_pvs_object_type_to_proto(nb.block),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_3(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        block=None,
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_4(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=None,
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_5(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        min_items=None,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_6(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        max_items=None,
    )


def x__pvs_nested_block_to_proto__mutmut_7(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
    """Converts a PvsNestedBlock to a protobuf NestedBlock message."""
    nesting_map = {
        NestingMode.SINGLE: pb.Schema.NestedBlock.NestingMode.SINGLE,
        NestingMode.LIST: pb.Schema.NestedBlock.NestingMode.LIST,
        NestingMode.SET: pb.Schema.NestedBlock.NestingMode.SET,
        NestingMode.MAP: pb.Schema.NestedBlock.NestingMode.MAP,
        NestingMode.GROUP: pb.Schema.NestedBlock.NestingMode.GROUP,
    }
    return pb.Schema.NestedBlock(
        block=_pvs_object_type_to_proto(nb.block),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_8(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_9(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_10(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_11(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        )


def x__pvs_nested_block_to_proto__mutmut_12(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        block=_pvs_object_type_to_proto(None),
        nesting=nesting_map.get(nb.nesting, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_13(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=nesting_map.get(None, pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_14(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=nesting_map.get(nb.nesting, None),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_15(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=nesting_map.get(pb.Schema.NestedBlock.NestingMode.INVALID),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_16(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        nesting=nesting_map.get(nb.nesting, ),
        min_items=nb.min_items or 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_17(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        min_items=nb.min_items and 0,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_18(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        min_items=nb.min_items or 1,
        max_items=nb.max_items or 0,
    )


def x__pvs_nested_block_to_proto__mutmut_19(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        max_items=nb.max_items and 0,
    )


def x__pvs_nested_block_to_proto__mutmut_20(nb: PvsNestedBlock) -> pb.Schema.NestedBlock:
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
        max_items=nb.max_items or 1,
    )

x__pvs_nested_block_to_proto__mutmut_mutants : ClassVar[MutantDict] = {
'x__pvs_nested_block_to_proto__mutmut_1': x__pvs_nested_block_to_proto__mutmut_1, 
    'x__pvs_nested_block_to_proto__mutmut_2': x__pvs_nested_block_to_proto__mutmut_2, 
    'x__pvs_nested_block_to_proto__mutmut_3': x__pvs_nested_block_to_proto__mutmut_3, 
    'x__pvs_nested_block_to_proto__mutmut_4': x__pvs_nested_block_to_proto__mutmut_4, 
    'x__pvs_nested_block_to_proto__mutmut_5': x__pvs_nested_block_to_proto__mutmut_5, 
    'x__pvs_nested_block_to_proto__mutmut_6': x__pvs_nested_block_to_proto__mutmut_6, 
    'x__pvs_nested_block_to_proto__mutmut_7': x__pvs_nested_block_to_proto__mutmut_7, 
    'x__pvs_nested_block_to_proto__mutmut_8': x__pvs_nested_block_to_proto__mutmut_8, 
    'x__pvs_nested_block_to_proto__mutmut_9': x__pvs_nested_block_to_proto__mutmut_9, 
    'x__pvs_nested_block_to_proto__mutmut_10': x__pvs_nested_block_to_proto__mutmut_10, 
    'x__pvs_nested_block_to_proto__mutmut_11': x__pvs_nested_block_to_proto__mutmut_11, 
    'x__pvs_nested_block_to_proto__mutmut_12': x__pvs_nested_block_to_proto__mutmut_12, 
    'x__pvs_nested_block_to_proto__mutmut_13': x__pvs_nested_block_to_proto__mutmut_13, 
    'x__pvs_nested_block_to_proto__mutmut_14': x__pvs_nested_block_to_proto__mutmut_14, 
    'x__pvs_nested_block_to_proto__mutmut_15': x__pvs_nested_block_to_proto__mutmut_15, 
    'x__pvs_nested_block_to_proto__mutmut_16': x__pvs_nested_block_to_proto__mutmut_16, 
    'x__pvs_nested_block_to_proto__mutmut_17': x__pvs_nested_block_to_proto__mutmut_17, 
    'x__pvs_nested_block_to_proto__mutmut_18': x__pvs_nested_block_to_proto__mutmut_18, 
    'x__pvs_nested_block_to_proto__mutmut_19': x__pvs_nested_block_to_proto__mutmut_19, 
    'x__pvs_nested_block_to_proto__mutmut_20': x__pvs_nested_block_to_proto__mutmut_20
}

def _pvs_nested_block_to_proto(*args, **kwargs):
    result = _mutmut_trampoline(x__pvs_nested_block_to_proto__mutmut_orig, x__pvs_nested_block_to_proto__mutmut_mutants, args, kwargs)
    return result 

_pvs_nested_block_to_proto.__signature__ = _mutmut_signature(x__pvs_nested_block_to_proto__mutmut_orig)
x__pvs_nested_block_to_proto__mutmut_orig.__name__ = 'x__pvs_nested_block_to_proto'
