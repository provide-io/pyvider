#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Resolution of `PvsAttribute.default` into a decoded configuration value.

The plugin protocol schema has no default-value field. Terraform sends an
attribute the practitioner omitted as null and never learns what the provider
considers the default, so the provider is the only party that can resolve one --
and it has to do so *before* anything reads the configuration, not only while
planning. A default resolved on the plan alone would leave ``ctx.config``
reporting None, so apply would return a state that does not match the state
Terraform planned.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any, TypeGuard

import attrs

from pyvider.cty import CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.schema.types.attribute import PvsAttribute
from pyvider.schema.types.blocks import PvsNestedBlock
from pyvider.schema.types.enums import NestingMode
from pyvider.schema.types.object import PvsObjectType


def resolve_schema_defaults(value: CtyValue | None, block: PvsObjectType) -> CtyValue | None:
    """Return `value` with every null attribute replaced by its schema default.

    The walk is recursive: an attribute declared with `a_obj()` carries its own
    `PvsObjectType`, and the attributes inside it take their defaults exactly as
    top-level ones do -- as do the attributes of nested blocks, to any depth.

    Nulls only: an unknown attribute is one whose value is not yet known, not an
    absent one, and replacing it would plan a value Terraform is about to
    compute. Only attributes that declare a non-null default are eligible.

    The value is returned unchanged when nothing needed resolving, so callers
    can pass anything through this without paying for a rebuild.
    """
    if not _is_resolvable(value):
        return value
    if not isinstance(value.value, Mapping):
        return value

    resolved = dict(value.value)
    changed = False

    for name, attribute in block.attributes.items():
        current = resolved.get(name)
        replacement = _resolve_attribute(current, attribute)
        if replacement is not current:
            resolved[name] = replacement
            changed = True

    for nested in block.block_types:
        current = resolved.get(nested.type_name)
        replacement = _resolve_nested(current, nested)
        if replacement is not current:
            resolved[nested.type_name] = replacement
            changed = True

    if not changed:
        return value
    return attrs.evolve(value, value=resolved)


def _resolve_attribute(value: Any, attribute: PvsAttribute) -> Any:
    """Return one attribute's value with its own default and any object members resolved."""
    if attribute.write_only:
        # A write-only value is never stored, so nothing inside it may be filled
        # in either. The attribute cannot carry a default of its own (Rule 10);
        # this stops the defaults its object members declare.
        return value

    resolved = value
    if attribute.default is not None and _is_null(resolved):
        resolved = attribute.type.validate(attribute.default)

    if attribute.object_type is not None:
        # An object-typed attribute is a block's structure written as a value:
        # its members declare defaults of their own, including a default the
        # object attribute itself just supplied but left partly unfilled.
        resolved = resolve_schema_defaults(resolved, attribute.object_type)

    return resolved


def merge_schema_defaults_into_plan(
    plan: dict[str, Any], config: CtyValue | None, block: PvsObjectType
) -> None:
    """Make `plan` agree with the effective configuration for defaulted attributes, in place.

    Defaults are resolved into the decoded configuration, which is what a
    resource reads at apply time -- so the plan has to carry the same value, or
    apply returns a state Terraform did not plan. Terraform itself knows nothing
    about provider-side defaults: an attribute the practitioner omitted comes
    back in the proposed new state carrying the *prior* value, at the top level,
    inside object-typed attributes, and inside nested blocks alike.

    For an attribute that declares a default the effective configuration
    therefore wins outright, prior state included. Prior state losing here is
    deliberate: an omitted attribute means "whatever the provider considers the
    default", and if the plan kept a stale non-default value while `ctx.config`
    reported the default, the two would disagree and apply would fail the
    refinement check.

    Only attributes that declare a default are touched. Everything else in the
    proposed new state is Terraform's own merge of configuration and prior state
    and is left exactly as it arrived.
    """
    merged = _merge_block_into_plan(plan, config, block)
    if merged is not plan:
        plan.update(merged)


def _merge_block_into_plan(plan_value: Any, config_value: Any, block: PvsObjectType) -> Any:
    """Return one planned block value -- root object included -- with its defaults corrected."""
    if not isinstance(plan_value, dict):
        # An absent or not-yet-known block has nothing to merge into.
        return plan_value
    if not _is_resolvable(config_value):
        return plan_value
    if not isinstance(config_value.value, Mapping):
        return plan_value

    config_values = config_value.value
    merged = dict(plan_value)

    for name, attribute in block.attributes.items():
        _merge_attribute_default(merged, name, attribute, config_values.get(name))

    for nested in block.block_types:
        if nested.type_name not in merged:
            continue
        merged[nested.type_name] = _merge_nested_into_plan(
            merged[nested.type_name], config_values.get(nested.type_name), nested
        )

    return merged


def _merge_attribute_default(
    merged: dict[str, Any], name: str, attribute: PvsAttribute, resolved: Any
) -> None:
    """Correct one planned attribute against the value the configuration resolved."""
    if attribute.write_only:
        # A write-only value is never stored, so nothing inside it may be
        # planned either. The attribute cannot carry a default of its own
        # (Rule 10); this stops the defaults its object members declare.
        return
    # An unknown value is not yet known, not absent: Terraform is about to
    # compute it, and planning the default would contradict that.
    if isinstance(resolved, CtyValue) and resolved.is_unknown:
        return

    if attribute.object_type is not None and not _is_null(resolved):
        # A default on the object attribute supplies the whole effective
        # object, not merely defaults for selected members.  When that value
        # is wholly known it must therefore replace Terraform's retained prior
        # object outright, just like a scalar attribute default does below.
        #
        # Keep partially unknown objects on the member-wise path: converting
        # one with cty_to_native would flatten nested unknowns to None and let
        # a default overwrite a value Terraform is still computing.
        if attribute.default is not None and isinstance(resolved, CtyValue) and resolved.is_wholly_known():
            merged[name] = cty_to_native(resolved)
            return

        # An object-typed attribute is a block written as a value: its members
        # take their defaults the same way, and only they are corrected -- the
        # object as a whole is Terraform's proposal unless the attribute itself
        # declared the whole-object default handled above.
        current = merged.get(name)
        if isinstance(current, dict):
            merged[name] = _merge_block_into_plan(current, resolved, attribute.object_type)
        return

    if attribute.default is None or _is_null(resolved):
        # This merge follows the effective configuration produced by
        # resolve_schema_defaults. If a caller supplies an unresolved null,
        # there is no normalized value to copy into the plan; resolving again
        # here would duplicate that earlier phase and risk the two paths
        # disagreeing about validation or nested-object normalization.
        return
    merged[name] = cty_to_native(resolved) if isinstance(resolved, CtyValue) else resolved


def _merge_nested_into_plan(plan_value: Any, config_value: Any, nested: PvsNestedBlock) -> Any:
    """Correct the defaults in a planned nested block, whatever its nesting mode."""
    if not _is_resolvable(config_value):
        return plan_value

    if nested.nesting in (NestingMode.SINGLE, NestingMode.GROUP):
        return _merge_block_into_plan(plan_value, config_value, nested.block)

    if nested.nesting is NestingMode.MAP:
        if not isinstance(plan_value, Mapping) or not isinstance(config_value.value, Mapping):
            return plan_value
        return {
            key: _merge_block_into_plan(element, config_value.value.get(key), nested.block)
            for key, element in plan_value.items()
        }

    # LIST and SET are both carried as an ordered collection of elements.
    if not isinstance(plan_value, list | tuple) or not isinstance(config_value.value, tuple):
        return plan_value
    if len(plan_value) != len(config_value.value):
        # Nothing pairs an element up with the configuration it came from once
        # the counts differ, so Terraform's proposal is left alone.
        return plan_value
    if nested.nesting is NestingMode.SET and len(plan_value) > 1:
        return _merge_set_into_plan(plan_value, config_value.value, nested)

    merged = [
        _merge_block_into_plan(element, config_element, nested.block)
        for element, config_element in zip(plan_value, config_value.value, strict=True)
    ]
    return merged if isinstance(plan_value, list) else tuple(merged)


def _merge_set_into_plan(
    plan_values: list[Any] | tuple[Any, ...],
    config_values: tuple[Any, ...],
    nested: PvsNestedBlock,
) -> list[Any] | tuple[Any, ...]:
    """Merge set elements that can be paired without relying on their order."""
    merged = list(plan_values)
    unmatched_plans = set(range(len(plan_values)))
    unmatched_configs = set(range(len(config_values)))

    while unmatched_plans:
        candidates = {
            plan_index: [
                config_index
                for config_index in unmatched_configs
                if _set_elements_match(plan_values[plan_index], config_values[config_index], nested.block)
            ]
            for plan_index in unmatched_plans
        }
        candidate_counts = Counter(config_index for matches in candidates.values() for config_index in matches)
        unique_pairs = [
            (plan_index, matches[0])
            for plan_index, matches in candidates.items()
            if len(matches) == 1 and candidate_counts[matches[0]] == 1
        ]
        if not unique_pairs:
            break

        for plan_index, config_index in unique_pairs:
            merged[plan_index] = _merge_block_into_plan(
                plan_values[plan_index], config_values[config_index], nested.block
            )
            unmatched_plans.remove(plan_index)
            unmatched_configs.remove(config_index)

    return merged if isinstance(plan_values, list) else tuple(merged)


def _set_elements_match(plan_value: Any, config_value: Any, block: PvsObjectType) -> bool:
    """Match set elements by configured attributes whose values are not defaults."""
    if not isinstance(plan_value, Mapping):
        return False
    if not isinstance(config_value, CtyValue) or not isinstance(config_value.value, Mapping):
        return False

    for name, attribute in block.attributes.items():
        configured = config_value.value.get(name)
        if attribute.write_only or attribute.default is not None or not _is_resolvable(configured):
            continue

        planned = plan_value.get(name)
        if attribute.object_type is not None:
            if not _set_elements_match(planned, configured, attribute.object_type):
                return False
        elif planned != cty_to_native(configured):
            return False

    return True


def _is_resolvable(value: Any) -> TypeGuard[CtyValue]:
    return isinstance(value, CtyValue) and not value.is_null and not value.is_unknown


def _is_null(value: Any) -> bool:
    if isinstance(value, CtyValue):
        return bool(value.is_null)
    return value is None


def _resolve_nested(value: Any, nested: PvsNestedBlock) -> Any:
    """Resolve defaults inside a nested block, whatever its nesting mode."""
    if not _is_resolvable(value):
        return value

    if nested.nesting in (NestingMode.SINGLE, NestingMode.GROUP):
        return resolve_schema_defaults(value, nested.block)

    if nested.nesting is NestingMode.MAP:
        if not isinstance(value.value, Mapping):
            return value
        mapped = {k: resolve_schema_defaults(v, nested.block) for k, v in value.value.items()}
        if all(mapped[k] is v for k, v in value.value.items()):
            return value
        return attrs.evolve(value, value=mapped)

    # LIST and SET are both carried as a tuple of element values.
    if not isinstance(value.value, tuple):
        return value
    elements = tuple(resolve_schema_defaults(element, nested.block) for element in value.value)
    if all(new is old for new, old in zip(elements, value.value, strict=True)):
        return value
    return attrs.evolve(value, value=elements)


# 🐍🏗️🔚
