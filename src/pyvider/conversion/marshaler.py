#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any, cast

import attrs

from pyvider.cty import CtyObject, CtyType, CtyValue
from pyvider.cty.codec import cty_from_msgpack, cty_to_msgpack
from pyvider.cty.marks import CtyMark
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.defaults import resolve_schema_defaults
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


_SEQUENCE_PAYLOADS = (list, tuple, set, frozenset)
_CONTAINER_PAYLOADS = (dict, *_SEQUENCE_PAYLOADS)


def _children_to_unmark(node: Any) -> list[Any]:
    """The nested values `node` holds, or an empty list if it holds none.

    Raw Python containers are walked as well as CtyValues. `validate` is
    routinely handed a plain list or dict whose elements are already-validated
    values, and those elements can be marked -- an earlier version stopped at
    the first non-CtyValue and left their marks in place.
    """
    payload = node.value if isinstance(node, CtyValue) else node
    if isinstance(payload, dict):
        return list(payload.values())
    if isinstance(payload, _SEQUENCE_PAYLOADS):
        return list(payload)
    if isinstance(payload, CtyValue):
        return [payload]
    return []


def _rebuild_unmarked(node: Any, done: dict[int, Any]) -> Any:
    """Reassemble `node` from its already-unmarked children."""
    payload = node.value if isinstance(node, CtyValue) else node

    if isinstance(payload, dict):
        rebuilt: Any = {k: done.get(id(v), v) for k, v in payload.items()}
    elif isinstance(payload, _SEQUENCE_PAYLOADS):
        rebuilt = type(payload)(done.get(id(v), v) for v in payload)
    elif isinstance(payload, CtyValue):
        rebuilt = done.get(id(payload), payload)
    else:
        rebuilt = payload

    if not isinstance(node, CtyValue):
        return rebuilt
    if rebuilt is payload:
        return attrs.evolve(node, marks=frozenset()) if node.marks else node
    return attrs.evolve(node, value=rebuilt, marks=frozenset())


def _unmark_deep(value: Any) -> Any:
    """A copy of `value` with every mark removed, at any depth.

    Iterative, like `_apply_schema_marks_iterative` and for the same reason: a
    deeply nested state value must not blow the Python stack on its way to the
    wire. An earlier version of this said it was iterative while being plainly
    recursive, and did raise RecursionError at a nesting depth pyvider-cty
    advertises as supported, once a realistic handler stack was underneath it.

    Deliberately local rather than `pyvider.cty.marks.unmark_deep`, which only
    exists from pyvider-cty 0.5. Keeping it here means this module behaves the
    same against 0.4 and 0.5, so the two repositories can be released in either
    order.
    """
    post_process = object()
    done: dict[int, Any] = {}
    processing: set[int] = set()
    stack: list[Any] = [value]

    while stack:
        node = stack.pop()

        if node is post_process:
            original = stack.pop()
            processing.discard(id(original))
            done[id(original)] = _rebuild_unmarked(original, done)
            continue

        node_id = id(node)
        if node_id in done or node_id in processing:
            continue

        children = _children_to_unmark(node)
        if not children:
            done[node_id] = _rebuild_unmarked(node, done)
            continue

        processing.add(node_id)
        stack.extend([node, post_process])
        stack.extend(children)

    return done.get(id(value), value)


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

    # Deliberately not marked on the way out. Marks have no wire
    # representation -- tfplugin6.DynamicValue carries only msgpack and json --
    # so applying schema marks here only to serialize immediately afterwards
    # discarded them again. Sensitivity reaches Terraform through the schema
    # instead (Schema.Attribute.sensitive), which is why nothing was lost.
    #
    # pyvider-cty now refuses to serialize a marked value rather than dropping
    # the marks silently, matching go-cty, so marking here would fail every
    # sensitive attribute at apply time.
    #
    # The inbound direction still marks: see the plan and apply handlers, where
    # `_apply_schema_marks_iterative` is how a resource learns an attribute is
    # sensitive at all, marks having not survived the wire.
    #
    # Which is exactly why the value is unmarked here rather than merely left
    # alone. Resource code is handed a marked config and may legitimately build
    # its planned or new state out of it, so marked values do reach this
    # function -- and reaching cty's refusal would crash the provider at plan or
    # apply. This is the wire boundary and the one place that may drop marks:
    # sensitivity travels to Terraform in the schema, not the value.
    msgpack_data = cty_to_msgpack(_unmark_deep(validated_value), schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def unmarshal(dv: pb.DynamicValue, *, schema: PvsType | CtyType, apply_defaults: bool = False) -> CtyValue:
    """
    Unmarshals a DynamicValue from the wire protocol into a CtyValue.
    """
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        value = cty_from_msgpack(dv.msgpack, root_cty_type)
    elif dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")
    else:
        value = CtyValue.null(root_cty_type)

    if apply_defaults and isinstance(schema, PvsObjectType):
        return cast(CtyValue, resolve_schema_defaults(value, schema))
    return value


def marshal_value(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(value, schema=declared_return_type)


def unmarshal_value(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(value, schema=cty_type)


# 🐍🏗️🔚
