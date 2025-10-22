from typing import Any

import attrs

from pyvider.cty import CtyObject, CtyType, CtyValue
from pyvider.cty.codec import cty_from_msgpack, cty_to_msgpack
from pyvider.cty.marks import CtyMark
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema.types import PvsAttribute, PvsObjectType, PvsType
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


def x__process_single_item__mutmut_orig(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_1(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = None
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_2(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) or schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_3(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = None

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_4(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(None)

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_5(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark(None))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_6(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("XXsensitiveXX"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_7(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("SENSITIVE"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_8(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = None
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_9(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) or val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_10(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) or isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_11(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(None)
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_12(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(None))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_13(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name not in schema.attributes:
                children_to_process.append((attr_value, schema.attributes[attr_name]))
    return marked_value, children_to_process


def x__process_single_item__mutmut_14(
    val: CtyValue, schema: PvsType | CtyType, processing: set[int]
) -> tuple[CtyValue, list[tuple[CtyValue, PvsType | CtyType]]]:
    marked_value = val
    if isinstance(schema, PvsAttribute) and schema.sensitive:
        marked_value = marked_value.mark(CtyMark("sensitive"))

    children_to_process = []
    if isinstance(schema, PvsObjectType) and isinstance(val.type, CtyObject) and val.value:
        processing.add(id(val))
        for attr_name, attr_value in val.value.items():
            if attr_name in schema.attributes:
                children_to_process.append(None)
    return marked_value, children_to_process

x__process_single_item__mutmut_mutants : ClassVar[MutantDict] = {
'x__process_single_item__mutmut_1': x__process_single_item__mutmut_1, 
    'x__process_single_item__mutmut_2': x__process_single_item__mutmut_2, 
    'x__process_single_item__mutmut_3': x__process_single_item__mutmut_3, 
    'x__process_single_item__mutmut_4': x__process_single_item__mutmut_4, 
    'x__process_single_item__mutmut_5': x__process_single_item__mutmut_5, 
    'x__process_single_item__mutmut_6': x__process_single_item__mutmut_6, 
    'x__process_single_item__mutmut_7': x__process_single_item__mutmut_7, 
    'x__process_single_item__mutmut_8': x__process_single_item__mutmut_8, 
    'x__process_single_item__mutmut_9': x__process_single_item__mutmut_9, 
    'x__process_single_item__mutmut_10': x__process_single_item__mutmut_10, 
    'x__process_single_item__mutmut_11': x__process_single_item__mutmut_11, 
    'x__process_single_item__mutmut_12': x__process_single_item__mutmut_12, 
    'x__process_single_item__mutmut_13': x__process_single_item__mutmut_13, 
    'x__process_single_item__mutmut_14': x__process_single_item__mutmut_14
}

def _process_single_item(*args, **kwargs):
    result = _mutmut_trampoline(x__process_single_item__mutmut_orig, x__process_single_item__mutmut_mutants, args, kwargs)
    return result 

_process_single_item.__signature__ = _mutmut_signature(x__process_single_item__mutmut_orig)
x__process_single_item__mutmut_orig.__name__ = 'x__process_single_item'


def x__finalize_container__mutmut_orig(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(CtyMark("sensitive"))
    return container_val


def x__finalize_container__mutmut_1(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(None)
    return container_val


def x__finalize_container__mutmut_2(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(None, value=new_inner_value).mark(CtyMark("sensitive"))
    return container_val


def x__finalize_container__mutmut_3(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=None).mark(CtyMark("sensitive"))
    return container_val


def x__finalize_container__mutmut_4(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(value=new_inner_value).mark(CtyMark("sensitive"))
    return container_val


def x__finalize_container__mutmut_5(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, ).mark(CtyMark("sensitive"))
    return container_val


def x__finalize_container__mutmut_6(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(CtyMark(None))
    return container_val


def x__finalize_container__mutmut_7(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(CtyMark("XXsensitiveXX"))
    return container_val


def x__finalize_container__mutmut_8(
    container_val: CtyValue,
    new_inner_value: dict[str, CtyValue],
    made_change: bool,
) -> CtyValue:
    if made_change:
        return attrs.evolve(container_val, value=new_inner_value).mark(CtyMark("SENSITIVE"))
    return container_val

x__finalize_container__mutmut_mutants : ClassVar[MutantDict] = {
'x__finalize_container__mutmut_1': x__finalize_container__mutmut_1, 
    'x__finalize_container__mutmut_2': x__finalize_container__mutmut_2, 
    'x__finalize_container__mutmut_3': x__finalize_container__mutmut_3, 
    'x__finalize_container__mutmut_4': x__finalize_container__mutmut_4, 
    'x__finalize_container__mutmut_5': x__finalize_container__mutmut_5, 
    'x__finalize_container__mutmut_6': x__finalize_container__mutmut_6, 
    'x__finalize_container__mutmut_7': x__finalize_container__mutmut_7, 
    'x__finalize_container__mutmut_8': x__finalize_container__mutmut_8
}

def _finalize_container(*args, **kwargs):
    result = _mutmut_trampoline(x__finalize_container__mutmut_orig, x__finalize_container__mutmut_mutants, args, kwargs)
    return result 

_finalize_container.__signature__ = _mutmut_signature(x__finalize_container__mutmut_orig)
x__finalize_container__mutmut_orig.__name__ = 'x__finalize_container'


def x__apply_schema_marks_iterative__mutmut_orig(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_1(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null and root_value.is_unknown:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_2(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null or root_value.is_unknown:
        return root_value

    POST_PROCESS = None
    work_stack: list[Any] = [(root_value, root_schema)]
    results: dict[int, CtyValue] = {}
    processing: set[int] = set()

    while work_stack:
        current_item = work_stack.pop()

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_3(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null or root_value.is_unknown:
        return root_value

    POST_PROCESS = object()
    work_stack: list[Any] = None
    results: dict[int, CtyValue] = {}
    processing: set[int] = set()

    while work_stack:
        current_item = work_stack.pop()

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_4(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null or root_value.is_unknown:
        return root_value

    POST_PROCESS = object()
    work_stack: list[Any] = [(root_value, root_schema)]
    results: dict[int, CtyValue] = None
    processing: set[int] = set()

    while work_stack:
        current_item = work_stack.pop()

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_5(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
    """
    A dedicated, iterative function to apply marks from a schema to an
    already validated CtyValue, avoiding recursion limits.
    """
    if root_value.is_null or root_value.is_unknown:
        return root_value

    POST_PROCESS = object()
    work_stack: list[Any] = [(root_value, root_schema)]
    results: dict[int, CtyValue] = {}
    processing: set[int] = None

    while work_stack:
        current_item = work_stack.pop()

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_6(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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
        current_item = None

        if current_item is POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_7(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

        if current_item is not POST_PROCESS:
            container_val, _ = work_stack.pop()
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_8(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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
            container_val, _ = None
            container_id = id(container_val)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_9(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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
            container_id = None
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_10(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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
            container_id = id(None)
            processing.remove(container_id)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_11(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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
            processing.remove(None)

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_12(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = None
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_13(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = None

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_14(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = True

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_15(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = None
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_16(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(None, child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_17(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), None)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_18(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_19(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), )
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_20(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(None), child_val)
                    new_inner_value[key] = processed_child

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


def x__apply_schema_marks_iterative__mutmut_21(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = None

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


def x__apply_schema_marks_iterative__mutmut_22(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val and processed_child.marks:
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


def x__apply_schema_marks_iterative__mutmut_23(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is child_val or processed_child.marks:
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


def x__apply_schema_marks_iterative__mutmut_24(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = None

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


def x__apply_schema_marks_iterative__mutmut_25(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = False

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


def x__apply_schema_marks_iterative__mutmut_26(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = None
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


def x__apply_schema_marks_iterative__mutmut_27(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(None, new_inner_value, made_change)
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


def x__apply_schema_marks_iterative__mutmut_28(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, None, made_change)
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


def x__apply_schema_marks_iterative__mutmut_29(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, None)
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


def x__apply_schema_marks_iterative__mutmut_30(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(new_inner_value, made_change)
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


def x__apply_schema_marks_iterative__mutmut_31(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, made_change)
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


def x__apply_schema_marks_iterative__mutmut_32(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, )
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


def x__apply_schema_marks_iterative__mutmut_33(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = None
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


def x__apply_schema_marks_iterative__mutmut_34(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            break

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


def x__apply_schema_marks_iterative__mutmut_35(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = None
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


def x__apply_schema_marks_iterative__mutmut_36(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = None

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_37(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(None)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_38(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results and val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_39(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id not in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_40(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id not in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_41(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            break

        marked_value, children_to_process = _process_single_item(val, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_42(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = None

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_43(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(None, schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_44(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, None, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_45(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, None)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_46(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(schema, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_47(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, processing)

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_48(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

                    if processed_child is not child_val or processed_child.marks:
                        made_change = True

            final_container = _finalize_container(container_val, new_inner_value, made_change)
            results[container_id] = final_container
            continue

        val, schema = current_item
        val_id = id(val)

        if val_id in results or val_id in processing:
            continue

        marked_value, children_to_process = _process_single_item(val, schema, )

        if children_to_process:
            work_stack.extend([(val, schema), POST_PROCESS])
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_49(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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
            work_stack.extend(None)
            work_stack.extend(reversed(children_to_process))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_50(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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
            work_stack.extend(None)
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_51(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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
            work_stack.extend(reversed(None))
        else:
            results[val_id] = marked_value

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_52(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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
            results[val_id] = None

    return results.get(id(root_value), root_value)


def x__apply_schema_marks_iterative__mutmut_53(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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

    return results.get(None, root_value)


def x__apply_schema_marks_iterative__mutmut_54(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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

    return results.get(id(root_value), None)


def x__apply_schema_marks_iterative__mutmut_55(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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

    return results.get(root_value)


def x__apply_schema_marks_iterative__mutmut_56(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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

    return results.get(id(root_value), )


def x__apply_schema_marks_iterative__mutmut_57(root_value: CtyValue, root_schema: PvsType | CtyType) -> CtyValue:
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

            new_inner_value = {}
            made_change = False

            if isinstance(container_val.value, dict):
                for key, child_val in container_val.value.items():
                    processed_child = results.get(id(child_val), child_val)
                    new_inner_value[key] = processed_child

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

    return results.get(id(None), root_value)

x__apply_schema_marks_iterative__mutmut_mutants : ClassVar[MutantDict] = {
'x__apply_schema_marks_iterative__mutmut_1': x__apply_schema_marks_iterative__mutmut_1, 
    'x__apply_schema_marks_iterative__mutmut_2': x__apply_schema_marks_iterative__mutmut_2, 
    'x__apply_schema_marks_iterative__mutmut_3': x__apply_schema_marks_iterative__mutmut_3, 
    'x__apply_schema_marks_iterative__mutmut_4': x__apply_schema_marks_iterative__mutmut_4, 
    'x__apply_schema_marks_iterative__mutmut_5': x__apply_schema_marks_iterative__mutmut_5, 
    'x__apply_schema_marks_iterative__mutmut_6': x__apply_schema_marks_iterative__mutmut_6, 
    'x__apply_schema_marks_iterative__mutmut_7': x__apply_schema_marks_iterative__mutmut_7, 
    'x__apply_schema_marks_iterative__mutmut_8': x__apply_schema_marks_iterative__mutmut_8, 
    'x__apply_schema_marks_iterative__mutmut_9': x__apply_schema_marks_iterative__mutmut_9, 
    'x__apply_schema_marks_iterative__mutmut_10': x__apply_schema_marks_iterative__mutmut_10, 
    'x__apply_schema_marks_iterative__mutmut_11': x__apply_schema_marks_iterative__mutmut_11, 
    'x__apply_schema_marks_iterative__mutmut_12': x__apply_schema_marks_iterative__mutmut_12, 
    'x__apply_schema_marks_iterative__mutmut_13': x__apply_schema_marks_iterative__mutmut_13, 
    'x__apply_schema_marks_iterative__mutmut_14': x__apply_schema_marks_iterative__mutmut_14, 
    'x__apply_schema_marks_iterative__mutmut_15': x__apply_schema_marks_iterative__mutmut_15, 
    'x__apply_schema_marks_iterative__mutmut_16': x__apply_schema_marks_iterative__mutmut_16, 
    'x__apply_schema_marks_iterative__mutmut_17': x__apply_schema_marks_iterative__mutmut_17, 
    'x__apply_schema_marks_iterative__mutmut_18': x__apply_schema_marks_iterative__mutmut_18, 
    'x__apply_schema_marks_iterative__mutmut_19': x__apply_schema_marks_iterative__mutmut_19, 
    'x__apply_schema_marks_iterative__mutmut_20': x__apply_schema_marks_iterative__mutmut_20, 
    'x__apply_schema_marks_iterative__mutmut_21': x__apply_schema_marks_iterative__mutmut_21, 
    'x__apply_schema_marks_iterative__mutmut_22': x__apply_schema_marks_iterative__mutmut_22, 
    'x__apply_schema_marks_iterative__mutmut_23': x__apply_schema_marks_iterative__mutmut_23, 
    'x__apply_schema_marks_iterative__mutmut_24': x__apply_schema_marks_iterative__mutmut_24, 
    'x__apply_schema_marks_iterative__mutmut_25': x__apply_schema_marks_iterative__mutmut_25, 
    'x__apply_schema_marks_iterative__mutmut_26': x__apply_schema_marks_iterative__mutmut_26, 
    'x__apply_schema_marks_iterative__mutmut_27': x__apply_schema_marks_iterative__mutmut_27, 
    'x__apply_schema_marks_iterative__mutmut_28': x__apply_schema_marks_iterative__mutmut_28, 
    'x__apply_schema_marks_iterative__mutmut_29': x__apply_schema_marks_iterative__mutmut_29, 
    'x__apply_schema_marks_iterative__mutmut_30': x__apply_schema_marks_iterative__mutmut_30, 
    'x__apply_schema_marks_iterative__mutmut_31': x__apply_schema_marks_iterative__mutmut_31, 
    'x__apply_schema_marks_iterative__mutmut_32': x__apply_schema_marks_iterative__mutmut_32, 
    'x__apply_schema_marks_iterative__mutmut_33': x__apply_schema_marks_iterative__mutmut_33, 
    'x__apply_schema_marks_iterative__mutmut_34': x__apply_schema_marks_iterative__mutmut_34, 
    'x__apply_schema_marks_iterative__mutmut_35': x__apply_schema_marks_iterative__mutmut_35, 
    'x__apply_schema_marks_iterative__mutmut_36': x__apply_schema_marks_iterative__mutmut_36, 
    'x__apply_schema_marks_iterative__mutmut_37': x__apply_schema_marks_iterative__mutmut_37, 
    'x__apply_schema_marks_iterative__mutmut_38': x__apply_schema_marks_iterative__mutmut_38, 
    'x__apply_schema_marks_iterative__mutmut_39': x__apply_schema_marks_iterative__mutmut_39, 
    'x__apply_schema_marks_iterative__mutmut_40': x__apply_schema_marks_iterative__mutmut_40, 
    'x__apply_schema_marks_iterative__mutmut_41': x__apply_schema_marks_iterative__mutmut_41, 
    'x__apply_schema_marks_iterative__mutmut_42': x__apply_schema_marks_iterative__mutmut_42, 
    'x__apply_schema_marks_iterative__mutmut_43': x__apply_schema_marks_iterative__mutmut_43, 
    'x__apply_schema_marks_iterative__mutmut_44': x__apply_schema_marks_iterative__mutmut_44, 
    'x__apply_schema_marks_iterative__mutmut_45': x__apply_schema_marks_iterative__mutmut_45, 
    'x__apply_schema_marks_iterative__mutmut_46': x__apply_schema_marks_iterative__mutmut_46, 
    'x__apply_schema_marks_iterative__mutmut_47': x__apply_schema_marks_iterative__mutmut_47, 
    'x__apply_schema_marks_iterative__mutmut_48': x__apply_schema_marks_iterative__mutmut_48, 
    'x__apply_schema_marks_iterative__mutmut_49': x__apply_schema_marks_iterative__mutmut_49, 
    'x__apply_schema_marks_iterative__mutmut_50': x__apply_schema_marks_iterative__mutmut_50, 
    'x__apply_schema_marks_iterative__mutmut_51': x__apply_schema_marks_iterative__mutmut_51, 
    'x__apply_schema_marks_iterative__mutmut_52': x__apply_schema_marks_iterative__mutmut_52, 
    'x__apply_schema_marks_iterative__mutmut_53': x__apply_schema_marks_iterative__mutmut_53, 
    'x__apply_schema_marks_iterative__mutmut_54': x__apply_schema_marks_iterative__mutmut_54, 
    'x__apply_schema_marks_iterative__mutmut_55': x__apply_schema_marks_iterative__mutmut_55, 
    'x__apply_schema_marks_iterative__mutmut_56': x__apply_schema_marks_iterative__mutmut_56, 
    'x__apply_schema_marks_iterative__mutmut_57': x__apply_schema_marks_iterative__mutmut_57
}

def _apply_schema_marks_iterative(*args, **kwargs):
    result = _mutmut_trampoline(x__apply_schema_marks_iterative__mutmut_orig, x__apply_schema_marks_iterative__mutmut_mutants, args, kwargs)
    return result 

_apply_schema_marks_iterative.__signature__ = _mutmut_signature(x__apply_schema_marks_iterative__mutmut_orig)
x__apply_schema_marks_iterative__mutmut_orig.__name__ = 'x__apply_schema_marks_iterative'


def x_marshal__mutmut_orig(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
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


def x_marshal__mutmut_1(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if isinstance(schema, CtyType | PvsType):
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


def x_marshal__mutmut_2(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(None)

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_3(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(None).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_4(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = None

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_5(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(None, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_6(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, None) else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_7(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr("to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_8(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, ) else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_9(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "XXto_cty_typeXX") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_10(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "TO_CTY_TYPE") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_11(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = None
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_12(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = None
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_13(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(None) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_14(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(None) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_15(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(None)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_16(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = None

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_17(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(None)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_18(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = None

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_19(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(None, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_20(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, None)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_21(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(schema)

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_22(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, )

    msgpack_data = cty_to_msgpack(final_cty_value, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_23(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = None
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_24(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(None, schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_25(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, None)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_26(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(schema_cty_type)
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_27(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    schema_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if isinstance(value, CtyValue):
        validated_value = value
    else:
        raw_value = attrs.asdict(value) if attrs.has(type(value)) else value
        validated_value = schema_cty_type.validate(raw_value)

    final_cty_value = _apply_schema_marks_iterative(validated_value, schema)

    msgpack_data = cty_to_msgpack(final_cty_value, )
    return pb.DynamicValue(msgpack=msgpack_data)


def x_marshal__mutmut_28(value: CtyValue | Any, *, schema: PvsType | CtyType) -> pb.DynamicValue:
    """Marshals a Python or CtyValue into a protobuf DynamicValue."""
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
    return pb.DynamicValue(msgpack=None)

x_marshal__mutmut_mutants : ClassVar[MutantDict] = {
'x_marshal__mutmut_1': x_marshal__mutmut_1, 
    'x_marshal__mutmut_2': x_marshal__mutmut_2, 
    'x_marshal__mutmut_3': x_marshal__mutmut_3, 
    'x_marshal__mutmut_4': x_marshal__mutmut_4, 
    'x_marshal__mutmut_5': x_marshal__mutmut_5, 
    'x_marshal__mutmut_6': x_marshal__mutmut_6, 
    'x_marshal__mutmut_7': x_marshal__mutmut_7, 
    'x_marshal__mutmut_8': x_marshal__mutmut_8, 
    'x_marshal__mutmut_9': x_marshal__mutmut_9, 
    'x_marshal__mutmut_10': x_marshal__mutmut_10, 
    'x_marshal__mutmut_11': x_marshal__mutmut_11, 
    'x_marshal__mutmut_12': x_marshal__mutmut_12, 
    'x_marshal__mutmut_13': x_marshal__mutmut_13, 
    'x_marshal__mutmut_14': x_marshal__mutmut_14, 
    'x_marshal__mutmut_15': x_marshal__mutmut_15, 
    'x_marshal__mutmut_16': x_marshal__mutmut_16, 
    'x_marshal__mutmut_17': x_marshal__mutmut_17, 
    'x_marshal__mutmut_18': x_marshal__mutmut_18, 
    'x_marshal__mutmut_19': x_marshal__mutmut_19, 
    'x_marshal__mutmut_20': x_marshal__mutmut_20, 
    'x_marshal__mutmut_21': x_marshal__mutmut_21, 
    'x_marshal__mutmut_22': x_marshal__mutmut_22, 
    'x_marshal__mutmut_23': x_marshal__mutmut_23, 
    'x_marshal__mutmut_24': x_marshal__mutmut_24, 
    'x_marshal__mutmut_25': x_marshal__mutmut_25, 
    'x_marshal__mutmut_26': x_marshal__mutmut_26, 
    'x_marshal__mutmut_27': x_marshal__mutmut_27, 
    'x_marshal__mutmut_28': x_marshal__mutmut_28
}

def marshal(*args, **kwargs):
    result = _mutmut_trampoline(x_marshal__mutmut_orig, x_marshal__mutmut_mutants, args, kwargs)
    return result 

marshal.__signature__ = _mutmut_signature(x_marshal__mutmut_orig)
x_marshal__mutmut_orig.__name__ = 'x_marshal'


def x_unmarshal__mutmut_orig(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_1(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_2(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(None)

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_3(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(None).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_4(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = None

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_5(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(None, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_6(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, None) else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_7(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr("to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_8(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, ) else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_9(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "XXto_cty_typeXX") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_10(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "TO_CTY_TYPE") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_11(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(None, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_12(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, None)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_13(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_14(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, )

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_15(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError(None)

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_16(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("XXJSON unmarshalling is not yet implemented.XX")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_17(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("json unmarshalling is not yet implemented.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_18(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON UNMARSHALLING IS NOT YET IMPLEMENTED.")

    return CtyValue.null(root_cty_type)


def x_unmarshal__mutmut_19(dv: pb.DynamicValue, *, schema: PvsType | CtyType) -> CtyValue:
    """Unmarshals a DynamicValue from the wire protocol into a CtyValue."""
    if not isinstance(schema, CtyType | PvsType):
        raise TypeError(f"Schema must be a CtyType or PvsType, but got {type(schema).__name__}")

    root_cty_type = schema.to_cty_type() if hasattr(schema, "to_cty_type") else schema

    if dv.msgpack:
        return cty_from_msgpack(dv.msgpack, root_cty_type)

    if dv.json:
        raise NotImplementedError("JSON unmarshalling is not yet implemented.")

    return CtyValue.null(None)

x_unmarshal__mutmut_mutants : ClassVar[MutantDict] = {
'x_unmarshal__mutmut_1': x_unmarshal__mutmut_1, 
    'x_unmarshal__mutmut_2': x_unmarshal__mutmut_2, 
    'x_unmarshal__mutmut_3': x_unmarshal__mutmut_3, 
    'x_unmarshal__mutmut_4': x_unmarshal__mutmut_4, 
    'x_unmarshal__mutmut_5': x_unmarshal__mutmut_5, 
    'x_unmarshal__mutmut_6': x_unmarshal__mutmut_6, 
    'x_unmarshal__mutmut_7': x_unmarshal__mutmut_7, 
    'x_unmarshal__mutmut_8': x_unmarshal__mutmut_8, 
    'x_unmarshal__mutmut_9': x_unmarshal__mutmut_9, 
    'x_unmarshal__mutmut_10': x_unmarshal__mutmut_10, 
    'x_unmarshal__mutmut_11': x_unmarshal__mutmut_11, 
    'x_unmarshal__mutmut_12': x_unmarshal__mutmut_12, 
    'x_unmarshal__mutmut_13': x_unmarshal__mutmut_13, 
    'x_unmarshal__mutmut_14': x_unmarshal__mutmut_14, 
    'x_unmarshal__mutmut_15': x_unmarshal__mutmut_15, 
    'x_unmarshal__mutmut_16': x_unmarshal__mutmut_16, 
    'x_unmarshal__mutmut_17': x_unmarshal__mutmut_17, 
    'x_unmarshal__mutmut_18': x_unmarshal__mutmut_18, 
    'x_unmarshal__mutmut_19': x_unmarshal__mutmut_19
}

def unmarshal(*args, **kwargs):
    result = _mutmut_trampoline(x_unmarshal__mutmut_orig, x_unmarshal__mutmut_mutants, args, kwargs)
    return result 

unmarshal.__signature__ = _mutmut_signature(x_unmarshal__mutmut_orig)
x_unmarshal__mutmut_orig.__name__ = 'x_unmarshal'


def x_marshal_value__mutmut_orig(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(value, schema=declared_return_type)


def x_marshal_value__mutmut_1(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(None, schema=declared_return_type)


def x_marshal_value__mutmut_2(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(value, schema=None)


def x_marshal_value__mutmut_3(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(schema=declared_return_type)


def x_marshal_value__mutmut_4(value: CtyValue, declared_return_type: CtyType) -> pb.DynamicValue:
    return marshal(value, )

x_marshal_value__mutmut_mutants : ClassVar[MutantDict] = {
'x_marshal_value__mutmut_1': x_marshal_value__mutmut_1, 
    'x_marshal_value__mutmut_2': x_marshal_value__mutmut_2, 
    'x_marshal_value__mutmut_3': x_marshal_value__mutmut_3, 
    'x_marshal_value__mutmut_4': x_marshal_value__mutmut_4
}

def marshal_value(*args, **kwargs):
    result = _mutmut_trampoline(x_marshal_value__mutmut_orig, x_marshal_value__mutmut_mutants, args, kwargs)
    return result 

marshal_value.__signature__ = _mutmut_signature(x_marshal_value__mutmut_orig)
x_marshal_value__mutmut_orig.__name__ = 'x_marshal_value'


def x_unmarshal_value__mutmut_orig(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(value, schema=cty_type)


def x_unmarshal_value__mutmut_1(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(None, schema=cty_type)


def x_unmarshal_value__mutmut_2(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(value, schema=None)


def x_unmarshal_value__mutmut_3(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(schema=cty_type)


def x_unmarshal_value__mutmut_4(value: pb.DynamicValue, cty_type: CtyType) -> CtyValue:
    return unmarshal(value, )

x_unmarshal_value__mutmut_mutants : ClassVar[MutantDict] = {
'x_unmarshal_value__mutmut_1': x_unmarshal_value__mutmut_1, 
    'x_unmarshal_value__mutmut_2': x_unmarshal_value__mutmut_2, 
    'x_unmarshal_value__mutmut_3': x_unmarshal_value__mutmut_3, 
    'x_unmarshal_value__mutmut_4': x_unmarshal_value__mutmut_4
}

def unmarshal_value(*args, **kwargs):
    result = _mutmut_trampoline(x_unmarshal_value__mutmut_orig, x_unmarshal_value__mutmut_mutants, args, kwargs)
    return result 

unmarshal_value.__signature__ = _mutmut_signature(x_unmarshal_value__mutmut_orig)
x_unmarshal_value__mutmut_orig.__name__ = 'x_unmarshal_value'
