#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.common.encryption import decrypt, encrypt
from pyvider.common.operation_context import OperationContext, operation_context
from pyvider.conversion import marshal, unmarshal
from pyvider.conversion.marshaler import _apply_schema_marks_iterative
from pyvider.cty import CtyObject, CtyValue
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


async def _get_resource_and_provider_instances(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        logger.error(
            "Resource type not found during plan operation",
            operation="plan_resource_change",
            resource_type=type_name,
            registered_resources=list(hub.get_components("resource").keys())
            if hub.get_components("resource")
            else [],
        )

        err = ResourceError(
            f"Resource type '{type_name}' not registered.\n\n"
            f"Suggestion: Ensure the resource is registered using the @resource decorator "
            f"and that component discovery has completed successfully.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that the resource class has the @resource decorator\n"
            f"  2. Verify the resource module is imported by the provider\n"
            f"  3. Run 'pyvider components list' to see registered resources\n"
            f"  4. Review provider logs for component registration errors"
        )
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    # Check if this is a test-only component accessed without test mode
    check_test_only_access(resource_class, type_name, "resource")

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        logger.error(
            "Provider instance not found in hub during plan operation",
            operation="plan_resource_change",
            resource_type=type_name,
        )
        raise RuntimeError(
            "Provider instance not found in hub.\n\n"
            "This is an internal framework error. The provider should be registered "
            "during server initialization.\n\n"
            "Suggestion: Report this issue - it indicates a provider initialization problem."
        )

    logger.debug(
        "Resource and provider instances retrieved for plan",
        operation="plan_resource_change",
        resource_type=type_name,
    )

    return resource_class, provider_instance


async def _unmarshal_request_data(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def _process_private_state(resource_class: Any, prior_private: bytes) -> Any | None:
    logger.debug(
        "Processing prior private state for plan operation",
        operation="process_private_state",
        has_prior_private=bool(prior_private),
        private_data_size=len(prior_private) if prior_private else 0,
    )

    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)

            logger.debug(
                "Prior private state deserialized successfully",
                operation="process_private_state",
                private_state_class=getattr(
                    resource_class.private_state_class, "__name__", str(resource_class.private_state_class)
                ),
            )

        except Exception as e:
            logger.warning(
                "Could not deserialize prior private state, continuing with plan",
                operation="process_private_state",
                resource_class=getattr(resource_class, "__name__", str(resource_class)),
                error_type=type(e).__name__,
                error_message=str(e),
                suggestion="This may be expected if the resource schema changed. Private state will be regenerated during apply.",
            )
    return private_state_instance


def _create_resource_context(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    provider_context = hub.get_component("singleton", "provider_context")
    test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
        test_mode_enabled=test_mode_enabled,
    )


def _handle_planned_state_dict(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values())

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


@resilient()
async def PlanResourceChangeHandler(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Handle plan resource change request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="PlanResourceChange")

    try:
        return await _plan_resource_change_impl(request, context)
    except Exception:
        handler_errors.inc(handler="PlanResourceChange")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="PlanResourceChange")


async def _plan_resource_change_impl(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None

    logger.debug(
        "PlanResourceChange handler called",
        operation="plan_resource_change",
        resource_type=request.type_name,
        has_prior_state=bool(request.prior_state.msgpack),
        has_config=bool(request.config.msgpack),
        has_proposed_state=bool(request.proposed_new_state.msgpack),
    )

    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        logger.debug(
            "Invoking resource plan method",
            operation="plan_resource_change",
            resource_type=request.type_name,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(
            "Resource plan method completed",
            operation="plan_resource_change",
            resource_type=request.type_name,
            has_planned_state=planned_state_dict is not None,
            planned_state_keys=list(planned_state_dict.keys()) if planned_state_dict else [],
        )

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)

            logger.debug(
                "Encrypted planned private state",
                operation="plan_resource_change",
                resource_type=request.type_name,
                private_state_size=len(response.planned_private),
            )

        logger.info(
            "Resource plan completed successfully",
            operation="plan_resource_change",
            resource_type=request.type_name,
            has_planned_state=bool(response.planned_state.msgpack),
            has_planned_private=bool(response.planned_private),
        )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "PlanResourceChange failed with framework error",
            operation="plan_resource_change",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "PlanResourceChange failed with unexpected error",
            operation="plan_resource_change",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


# 🐍🏗️🔚
