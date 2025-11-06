#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import inspect
import re
from typing import Any

import attrs
from provide.foundation import logger
from provide.foundation.errors import FoundationError

from pyvider.cty import CtyList, CtyObject, CtyTuple, CtyValue
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
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
from pyvider.exceptions import (
    DataSourceError,
    FunctionError,
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource

# Regex to parse attribute paths like `attr`, `attr[0]`, `attr["key"]`
PATH_STEP_REGEX = re.compile(r"(\.?)(\w+)|\[(\d+)\]|\[['\"]([^'\"]+)['\"]\]")


def get_all_components(component_type: str) -> dict[str, Any]:
    """
    Retrieves all components of a given type without filtering.

    Use this for schema generation where all components (including test-only)
    must be included in the provider schema.
    """
    return hub.get_components(component_type)


def get_filtered_components(component_type: str) -> dict[str, Any]:
    """
    Retrieves components of a given type, filtering out test-only components
    if the provider is not in test mode.

    Use this at runtime when components are actually being accessed.
    """
    all_components = hub.get_components(component_type)

    # Try to get provider context to check test mode, but don't fail if it doesn't exist
    try:
        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
    except (KeyError, AttributeError):
        # If provider_context doesn't exist (e.g., in unit tests), assume not in test mode
        test_mode_enabled = False

    if test_mode_enabled:
        logger.info(
            f"Test mode enabled, returning all {component_type} components (including test-only).",
            component_type=component_type,
            total_count=len(all_components),
        )
        return all_components
    else:
        logger.debug(
            f"Test mode is not enabled, filtering {component_type} components for production mode.",
            component_type=component_type,
            total=len(all_components),
        )

    production_components = {
        name: comp for name, comp in all_components.items() if not getattr(comp, "_is_test_only", False)
    }
    logger.debug(
        f"Filtered {component_type} components for production mode.",
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

    # Get test mode status
    try:
        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
    except (KeyError, AttributeError):
        test_mode_enabled = False

    if test_mode_enabled:
        logger.debug(
            f"Allowing access to test-only {component_type}",
            component_name=component_name,
            test_mode_enabled=True,
        )
        return  # Test mode enabled, access allowed

    # Test-only component accessed without test mode - DENY
    logger.warning(
        f"⚠️  Blocked access to test-only {component_type}",
        component_name=component_name,
        test_mode_enabled=False,
    )

    # Choose appropriate exception type
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


def _check_type_and_unknown(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def _check_null_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, ""


def _check_object_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
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


def is_valid_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    # If plan is null, refinement to any concrete value is valid
    if plan.is_null:
        return True, ""

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def str_path_to_proto_path(path_str: str | None) -> pb.AttributePath | None:
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
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


async def create_diagnostic_from_exception(exc: Exception) -> pb.Diagnostic:  # noqa: C901
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
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
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


def cty_to_attrs_instance(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)


# 🐍🏗️🔚
