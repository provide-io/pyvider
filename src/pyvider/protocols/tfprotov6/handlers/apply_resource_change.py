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
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import (
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    is_valid_refinement,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


async def _get_resource_and_provider_instances(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        logger.error(
            "Resource type not found during apply operation",
            operation="apply_resource_change",
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
            "Provider instance not found in hub during apply operation",
            operation="apply_resource_change",
            resource_type=type_name,
        )
        raise RuntimeError(
            "Provider instance not found in hub.\n\n"
            "This is an internal framework error. The provider should be registered "
            "during server initialization.\n\n"
            "Suggestion: Report this issue - it indicates a provider initialization problem."
        )

    logger.debug(
        "Resource and provider instances retrieved for apply",
        operation="apply_resource_change",
        resource_type=type_name,
    )

    return resource_class, provider_instance


async def _unmarshal_request_data(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def _process_private_state(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(
        "Processing private state for apply operation",
        operation="process_private_state",
        has_private_data=bool(planned_private),
        private_data_size=len(planned_private) if planned_private else 0,
    )

    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)

            logger.debug(
                "Private state deserialized successfully",
                operation="process_private_state",
                private_state_class=resource_class.private_state_class.__name__,
            )

        except Exception as e:
            logger.error(
                "Failed to deserialize private state from plan",
                operation="process_private_state",
                error_type=type(e).__name__,
                error_message=str(e),
                exc_info=True,
            )

            err = ResourceError(
                f"Failed to deserialize private state from plan: {e}\n\n"
                f"Suggestion: This usually indicates a mismatch between the state encryption key "
                f"or corrupted private state data.\n\n"
                f"Troubleshooting:\n"
                f"  1. Verify PYVIDER_PRIVATE_STATE_SHARED_SECRET hasn't changed\n"
                f"  2. Check if the private state schema has changed incompatibly\n"
                f"  3. Review the original error: {type(e).__name__}: {e}\n"
                f"  4. Consider destroying and recreating the resource if schema changed"
            )
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


def _create_resource_context(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    provider_context = hub.get_component("singleton", "provider_context")
    test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
        test_mode_enabled=test_mode_enabled,
    )


def _handle_apply_result(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


@resilient()
async def ApplyResourceChangeHandler(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    """Handle apply resource change request with metrics collection."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ApplyResourceChange")

    try:
        return await _apply_resource_change_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ApplyResourceChange")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ApplyResourceChange")


async def _apply_resource_change_impl(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None

    logger.debug(
        "ApplyResourceChange handler called",
        operation="apply_resource_change",
        resource_type=request.type_name,
        has_prior_state=bool(request.prior_state.msgpack),
        has_config=bool(request.config.msgpack),
        has_planned_state=bool(request.planned_state.msgpack),
    )

    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        logger.debug(
            "Invoking resource apply method",
            operation="apply_resource_change",
            resource_type=request.type_name,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        logger.info(
            "Resource apply completed successfully",
            operation="apply_resource_change",
            resource_type=request.type_name,
            has_new_state=new_state_attrs is not None,
            has_new_private_state=new_private_state_attrs is not None,
        )

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "ApplyResourceChange failed with framework error",
            operation="apply_resource_change",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "ApplyResourceChange failed with unexpected error",
            operation="apply_resource_change",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


# 🐍🏗️🔚
