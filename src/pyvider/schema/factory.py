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
    CtySet,
    CtyString,
    CtyTuple,
    CtyType,
    CtyValue,
)
from pyvider.schema.types import NestingMode, PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema


def _get_cty_type(type_def: Any) -> CtyType:
    """Gets the CtyType from a PvsAttribute or a raw CtyType."""
    if isinstance(type_def, PvsAttribute):
        return type_def.type
    if isinstance(type_def, CtyType):
        return type_def
    raise TypeError(f"Invalid type definition for attribute element: got {type(type_def).__name__}")


# --- Attribute Factories (a_*) ---
def a_str(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=description, **kwargs)


def a_num(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=description, **kwargs)


def a_bool(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=description, **kwargs)


def a_dyn(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=description, **kwargs)


def a_list(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_map(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_set(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_tuple(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=description,
        **kwargs,
    )


def a_obj(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


# --- Block Factories (b_*) ---
def b_main(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


def _nested_block_factory(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def b_list(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.LIST, **kwargs)


def b_set(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SET, **kwargs)


def b_map(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.MAP, **kwargs)


def b_single(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SINGLE, **kwargs)


def b_group(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.GROUP, **kwargs)


# --- Schema Factories (s_*) ---
def _create_schema(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=version, block=block)


def s_resource(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


def s_data_source(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


def s_provider(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    return _create_schema(1, attributes=attributes, block_types=block_types)


# --- Special Value Factories ---


def a_unknown(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


def a_null(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


# 🐍🏗️🔚
