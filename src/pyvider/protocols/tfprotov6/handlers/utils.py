#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Iterable, Mapping
import inspect
import re
from typing import Any

import attrs
from provide.foundation import logger
from provide.foundation.errors import FoundationError

from pyvider.conversion.marshaler import _unmark_deep
from pyvider.cty import CtyList, CtyMap, CtyObject, CtySet, CtyTuple, CtyValue
from pyvider.cty.exceptions import (
    CtyAttributeValidationError,
    CtyBoolValidationError,
    CtyListValidationError,
    CtyMapValidationError,
    CtyNumberValidationError,
    CtySetValidationError,
    CtyStringValidationError,
    CtyTupleValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.exceptions import (
    DataSourceError,
    FrameworkConfigurationError,
    FunctionError,
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.schema import PvsSchema

# Regex to parse attribute paths like `attr`, `attr[0]`, `attr["key"]`
PATH_STEP_REGEX = re.compile(r"(\.?)(\w+)|\[(\d+)\]|\[['\"]([^'\"]+)['\"]\]")


def derive_identity_values(
    resource_class: Any,
    state_attrs: Any,
    resource_type: str,
    operation: str,
) -> dict[str, Any] | None:
    """Derive identity from a state that is fully known, or None with a warning.

    Read, apply and import all reach this with a state that exists: a destroy is
    excluded before the call, and a read or import that found nothing has already
    returned. So both failure modes are genuine defects rather than "not yet
    knowable":

    - A raised exception almost certainly indicates a bug in this resource's
      `get_identity()` override -- there is no missing-state excuse left here.
    - An ordinary None return means the identity schema's attribute names did not
      resolve against the state object -- a schema/state mismatch.

    Neither is surfaced as a Terraform diagnostic. The operation itself
    succeeded, and failing it over an identity-derivation bug would misreport a
    live resource as unreadable or a successful create as a failure. Both are
    logged at WARNING so they are visible in provider logs rather than
    disappearing.

    `plan_resource_change` keeps its own version deliberately: during plan the
    state may legitimately not be known yet, so a None there is an ordinary
    answer rather than a defect, and it must not warn.
    """
    try:
        identity_values: dict[str, Any] | None = resource_class.get_identity(state_attrs)
    except Exception as e:
        logger.warning(
            f"Omitting new identity: derivation raised an exception after a successful {operation}, "
            "which likely indicates a bug in this resource's get_identity() override",
            operation=operation,
            resource_type=resource_type,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        return None

    if identity_values is None:
        logger.warning(
            "Omitting new identity: get_identity() returned None even though the new state "
            "is fully known, which likely means the identity schema's attributes do not "
            "resolve against this resource's state object",
            operation=operation,
            resource_type=resource_type,
        )

    return identity_values


def resolve_identity_schema(resource_class: Any) -> PvsSchema | None:
    """Return a resource's identity schema, or None if it declares none.

    Registration does not require BaseResource: @register_resource only stamps
    marker attributes, and discovery registers on the marker alone. A duck-typed
    resource that predates identity therefore has no get_identity_schema() at
    all, and calling it unguarded would turn a previously working resource into
    an AttributeError. A missing method means the same thing as a method
    returning None -- this resource has no identity.
    """
    getter = getattr(resource_class, "get_identity_schema", None)
    if getter is None:
        return None
    schema: PvsSchema | None = getter()
    return schema


def get_all_components(component_type: str) -> dict[str, Any]:
    """
    Retrieves all components of a given type without filtering.

    Use this for schema generation where all components (including test-only)
    must be included in the provider schema.
    """
    return hub.get_components(component_type)


def is_test_mode_enabled() -> bool:
    """Resolve whether test-only components are currently accessible.

    The provider context is authoritative once ConfigureProvider has run, but it
    does not exist before that. PYVIDER_TESTMODE is the fallback, and for schema
    generation it is the *only* available signal: Terraform requests the provider
    schema before it configures the provider, and that schema is computed once per
    process. Without this fallback a test-only component can never reach the
    schema, so `pyvider_testmode` in the provider block cannot reveal one either.
    """
    try:
        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = bool(getattr(provider_context, "test_mode_enabled", False))
    except (KeyError, AttributeError):
        # No provider_context yet (pre-ConfigureProvider, or a unit test).
        test_mode_enabled = False

    if not test_mode_enabled:
        from provide.foundation.config import get_env, parse_bool_extended

        env_val = get_env("PYVIDER_TESTMODE", default=None)
        if env_val:
            test_mode_enabled = bool(parse_bool_extended(env_val))

    return test_mode_enabled


def get_filtered_components(component_type: str) -> dict[str, Any]:
    """
    Retrieves components of a given type, filtering out test-only components
    if the provider is not in test mode.

    Use this at runtime when components are actually being accessed.
    """
    all_components = hub.get_components(component_type)

    test_mode_enabled = is_test_mode_enabled()

    if test_mode_enabled:
        logger.info(
            "Test mode enabled, returning all components (including test-only)",
            component_type=component_type,
            total_count=len(all_components),
        )
        return all_components
    else:
        logger.debug(
            "Filtering components for production mode",
            component_type=component_type,
            total=len(all_components),
        )

    production_components = {
        name: comp for name, comp in all_components.items() if not getattr(comp, "_is_test_only", False)
    }
    logger.debug(
        "Filtered components for production mode",
        component_type=component_type,
        total=len(all_components),
        production=len(production_components),
    )
    return production_components


def check_test_only_access(
    component_class: Any,
    component_name: str,
    component_type: str,
) -> None:
    """
    Check if a test-only component is being accessed without test mode enabled.

    Raises appropriate error if access should be denied.

    Args:
        component_class: The component class to check
        component_name: Name of the component (for error messages)
        component_type: Type of component ("data_source", "resource", "function")

    Raises:
        DataSourceError/ResourceError/FunctionError: If test-only access denied
    """
    is_test_only = getattr(component_class, "_is_test_only", False)

    if not is_test_only:
        return  # Not test-only, access always allowed

    # Test mode comes from the provider context once configured, and from the
    # environment before that (e.g. functions evaluated before ConfigureProvider).
    test_mode_enabled = is_test_mode_enabled()

    if test_mode_enabled:
        # Info-level — test-only component access is an auditable event
        # (a production operator should be able to grep for these).
        logger.info(
            "Allowing access to test-only component",
            component_type=component_type,
            component_name=component_name,
            test_mode_enabled=True,
        )
        return  # Test mode enabled, access allowed

    # Test-only component accessed without test mode - DENY
    logger.warning(
        "Blocked access to test-only component",
        component_type=component_type,
        component_name=component_name,
        test_mode_enabled=False,
    )

    # Choose appropriate exception type
    error_class: type[DataSourceError] | type[ResourceError] | type[FunctionError]
    if component_type == "data_source":
        error_class = DataSourceError
        type_label = "Data source"
    elif component_type == "resource":
        error_class = ResourceError
        type_label = "Resource"
    elif component_type == "function":
        error_class = FunctionError
        type_label = "Function"
    else:
        error_class = DataSourceError  # Fallback
        type_label = "Component"

    err = error_class(
        f"{type_label} '{component_name}' is test-only and requires test mode.\n\n"
        f"This component is marked for testing and development purposes only. "
        f"It cannot be used in production mode.\n\n"
        f"Suggestion: Enable test mode to use this component.\n\n"
        f"Troubleshooting:\n"
        f"  1. Add 'pyvider_testmode = true' to your provider block to enable test mode\n"
        f"  2. Remove test-only components from production configurations\n"
        f"  3. Review component documentation to find production alternatives\n"
        f"  4. Test mode should only be used in testing/development environments"
    )
    err.add_context(f"{component_type}.name", component_name)
    err.add_context(f"{component_type}.test_only", True)
    err.add_context("provider.test_mode_enabled", False)
    err.add_context("terraform.summary", f"Test-only {component_type} requires test mode")
    err.add_context(
        "terraform.detail",
        f"The {component_type} '{component_name}' is marked as test-only and cannot be used when pyvider_testmode is false or unset.",
    )
    raise err


def _process_instance(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def attrs_to_dict_for_cty(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, _visited)


def _decide_unknown_or_null(plan: CtyValue, result: CtyValue) -> tuple[bool, str] | None:
    """Settle the unknown and null cases, or None when the values must be compared.

    The order is load-bearing, and getting it wrong is what this function exists
    to prevent:

    * `plan.is_unknown` comes first because an unknown may become *anything* of
      its type, null included. An unknown is not null, so asking `result.is_null`
      first reports "non-null in plan but became null in result" for the ordinary
      case of an optional+computed attribute resolving to null.
    * Both come before the structural branches in the caller, because an unknown
      container has no dict or tuple payload to walk -- the walk would reject it
      for the shape of its emptiness rather than for anything about its value.
    """
    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return None


def _check_object_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    # Type guard: ensure both values are dicts for object types
    if not isinstance(plan.value, dict) or not isinstance(result.value, dict):
        return False, "Object refinement check requires dict values"

    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def _check_collection_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    # Type guard: ensure both values are lists/tuples for collection types
    if not isinstance(plan.value, (list, tuple)) or not isinstance(result.value, (list, tuple)):
        return False, "Collection refinement check requires list/tuple values"

    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def _check_map_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """A known map keeps its keys; each value refines on its own.

    Without this a map is compared whole, so `tags = { name = random_pet.x.id }`
    -- a *known* map holding one unknown -- fails the moment the unknown resolves.
    """
    if not isinstance(plan.value, Mapping) or not isinstance(result.value, Mapping):
        return False, "Map refinement check requires mapping values"

    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Map key mismatch. Plan keys: {sorted(plan.value)}, Result keys: {sorted(result.value)}",
        )

    for key in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[key], result.value[key])
        if not is_valid:
            return False, f"Key '{key}': {reason}"
    return True, ""


def _check_set_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """A set whose elements are all known compares whole; one holding an unknown cannot.

    A set element is identified by its own value, so an unknown element names no
    particular result element and there is nothing to line up pairwise -- the
    resolved value legitimately lands anywhere in the set, and may even collapse
    into an element already there. Terraform Core does not correlate them either.
    """
    if not isinstance(plan.value, Iterable) or not isinstance(result.value, Iterable):
        return False, "Set refinement check requires iterable values"

    if any(isinstance(element, CtyValue) and element.is_unknown for element in plan.value):
        return True, ""

    if _unmark_deep(plan.value) != _unmark_deep(result.value):
        return (
            False,
            f"Value mismatch: the result differs from the planned value (type {plan.type}). "
            "Values are omitted here because this message is returned to Terraform.",
        )
    return True, ""


def is_valid_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """Is `result` a valid refinement of `plan`?

    A value may be refined from unknown to null or to a concrete value, and from
    null to a concrete value. It may not change from one concrete value to
    another, nor become unknown.
    """
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    decided = _decide_unknown_or_null(plan, result)
    if decided is not None:
        return decided

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if isinstance(plan.type, CtyMap):
        return _check_map_refinement(plan, result)

    if isinstance(plan.type, CtySet):
        return _check_set_refinement(plan, result)

    # Compared unmarked. Marks are metadata about a value, not part of it, and
    # the inbound path deliberately marks config from the schema -- so a
    # resource that echoes a sensitive attribute into its state hands back a
    # value that is equal in every respect except its marks. CtyValue.__eq__
    # counts marks, so comparing directly reports a contract violation for a
    # state that is in fact identical, and fails the apply.
    if _unmark_deep(plan.value) != _unmark_deep(result.value):
        # The values themselves are deliberately NOT in this message. It becomes
        # a tfplugin6.Diagnostic, which Terraform prints to the console and
        # writes to logs, and that channel has no redaction. A refinement
        # mismatch on a sensitive attribute would otherwise disclose the secret
        # in plaintext -- and any mismatch would disclose whatever the value is.
        return (
            False,
            f"Value mismatch: the result differs from the planned value (type {plan.type}). "
            "Values are omitted here because this message is returned to Terraform.",
        )

    return True, ""


def str_path_to_proto_path(path_str: str | None) -> pb.AttributePath | None:
    """Parse a hand-authored path string like `attr[0]["key"]` into proto steps.

    This is the string-literal counterpart to `cty_path_to_proto_path` and is
    meant for path strings a caller types out directly (e.g.
    `ctx.add_attribute_error("tags[0]", ...)`), not for `str(cty_path)` /
    `CtyPath.string()` output. That distinction matters for sets: `KeyStep`'s
    `__str__` renders a set element's *value* (e.g. `[3]` or `['a']`) once it
    no longer has the CtyValue to tell "this is a set element" apart from a
    genuine int/string key -- the regex below has no way to recover that once
    it is text, and would silently emit a plausible-but-wrong
    element_key_int/element_key_string step, same as the bug this module's
    `cty_path_to_proto_path` had. There is no fix at this layer because the
    information is already gone by the time a string reaches here; a `CtyPath`
    that might contain a set-element step should go through
    `cty_path_to_proto_path` directly instead of being stringified first.
    """
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def cty_path_to_proto_path(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                if isinstance(key, CtyValue):
                    # A set element keys itself (see KeyStep's docstring in
                    # pyvider-cty and walk.py's `_child_steps`) -- `key` here is
                    # a whole CtyValue, not a string or int. tfplugin6's
                    # AttributePath.Step is a oneof of attribute_name /
                    # element_key_string / element_key_int, documented as
                    # addressing "an element in an *indexable* collection type" --
                    # a set isn't one, so there is no honest string or int for
                    # this step. `str(key)` would render the CtyValue's attrs
                    # repr (e.g. "CtyValue(vtype=CtyString(), value='a', ...)"),
                    # a fabricated address that sends Terraform looking for a key
                    # that was never there. required.py's block-nesting check hits
                    # the same wall and resolves it the same way: stop at the set
                    # and report it, since that is the last position a consumer
                    # can actually navigate to.
                    break
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    # A path that is nothing but a set-element step (or starts with one)
    # truncates to zero proto steps above. Keep the same "nothing more
    # specific to point at" contract as an empty CtyPath rather than emit
    # an AttributePath with an empty steps list.
    if not proto_steps:
        return None
    return pb.AttributePath(steps=proto_steps)


async def create_diagnostic_from_exception(exc: Exception) -> pb.Diagnostic:
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        # Use the exception's message for the summary (it contains the prefixed error type)
        summary = exc.message if hasattr(exc, "message") else str(exc)
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        # Use the exception's message for the summary
        summary = exc.message if hasattr(exc, "message") else str(exc)
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    # Handle other specific exception types
    elif isinstance(exc, ResourceLifecycleContractError):
        detail = str(exc)
        if hasattr(exc, "detail") and exc.detail:
            detail += f"\n\nDetails:\n{exc.detail}"
    elif isinstance(exc, (FunctionError, ResourceError | DataSourceError, PyviderError)):
        detail = str(exc)
    else:
        summary = "Internal Provider Error"
        detail = (
            "The provider encountered an unexpected error. This is likely a bug in the provider."
            "\nPlease report this issue to the provider developers."
        )
        logger.error(
            f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
            exc_info=True,
        )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


def cty_to_attrs_instance(
    cty_val: CtyValue | None,
    attrs_cls: type[Any] | None,
    *,
    allow_unknown: bool = False,
    apply_defaults: bool = False,
) -> Any | None:
    """Convert a CtyValue into an instance of the given attrs-based class.

    The framework converts Terraform configuration/state shapes into
    Python objects by reading the target class's attrs field metadata.
    Non-attrs classes (plain `dataclasses`, `pydantic` models, bare
    `class` definitions) cannot be round-tripped and will silently
    produce empty or malformed values — so we reject them up front with
    a clear FrameworkConfigurationError, not a confusing failure later
    in the conversion layer.

    By default a value that is not wholly known converts to None, so that a
    provider's custom validator is never handed a half-known object (issue #5).
    That is a *validation* policy, and it is wrong anywhere None already means
    something else. Pass ``allow_unknown=True`` there: ``from_cty`` handles
    unknowns per attribute, yielding an instance whose not-yet-known fields are
    None rather than collapsing the whole object.

    Pass ``apply_defaults=True`` when decoding a *configuration*, where a null
    attribute is one the practitioner omitted and the target class's own field
    default is the right fallback. State is decoded without it: a null there is
    a recorded absence, and replacing it would rewrite history. See
    ``BaseResource.from_cty``.
    """
    if attrs_cls is None:
        return None
    if not allow_unknown and cty_val is not None and not cty_val.is_wholly_known():
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")
    if not attrs.has(attrs_cls):
        err = FrameworkConfigurationError(
            f"'{attrs_cls.__name__}' cannot be used as a config/state/private-state "
            f"class because it is not an attrs class.\n\n"
            f"Pyvider's cty ↔ Python conversion introspects fields via attrs.fields(); "
            f"plain dataclasses, pydantic models, and bare classes cannot be "
            f"converted and will silently round-trip to empty objects.\n\n"
            f"Fix: decorate '{attrs_cls.__name__}' with @attrs.define or @attrs.frozen."
        )
        err.add_context("target_class", attrs_cls.__name__)
        err.add_context("target_module", getattr(attrs_cls, "__module__", "unknown"))
        raise err

    return BaseResource.from_cty(cty_val, attrs_cls, apply_defaults=apply_defaults)


# 🐍🏗️🔚
