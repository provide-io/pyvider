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
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    is_valid_refinement,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


async def _get_resource_and_provider_instances(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
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
    logger.debug(f"Processing private state. planned_private: {planned_private}")
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
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
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

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
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

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response
