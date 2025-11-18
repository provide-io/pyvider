#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any, cast

import attrs

from pyvider.cty import CtyObject, CtyType, CtyValue
from pyvider.cty.codec import cty_from_msgpack, cty_to_msgpack
from pyvider.cty.marks import CtyMark
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.types import PvsAttribute, PvsObjectType, PvsType


def _process_single_item(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        if isinstance(val.value, dict):
            for attr_name, attr_value in val.value.items():
                if attr_name in schema.attributes:
                    children_to_process.append(
                        (
                            cast(CtyValue, attr_value),
                            cast(PvsType | CtyType[Any], schema.attributes[attr_name]),
                        )
                    )
    return marked_value, children_to_process


def _finalize_container(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(CtyMark("sensitive"))
    return container_val


def _apply_schema_marks_iterative(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null or root_value.is_unknown:
        return root_value

    POST_PROCESS = object()
    work_stack: list[Any] = [(root_value, root_schema)]
    results: dict[int, CtyValue] = {}
    processing: set[int] = set()

    while work_stack:
        current_item = work_stack.pop()

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value: dict[str, CtyValue] = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[cast(str, key)] = cast(CtyValue, processed_child)

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def marshal(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """
    Marshals a Python or CtyValue into a protobuf DynamicValue.
    """
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def unmarshal(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """
    Unmarshals a DynamicValue from the wire protocol into a CtyValue.
    """
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def marshal_value(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(value, schema=declared_return_type)


def unmarshal_value(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(value, schema=cty_type)


# 🐍🏗️🔚
