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
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
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
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def _process_private_state(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
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
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def _handle_planned_state_dict(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    raw_values_for_validation = {}
    unknown_keys = set()
    for key, value in planned_state_dict.items():
        if isinstance(value, CtyValue) and value.is_unknown:
            unknown_keys.add(key)
            raw_values_for_validation[key] = None
        else:
            raw_values_for_validation[key] = value

    planned_state_with_nulls = validator_type.validate(raw_values_for_validation)
    final_value_map = planned_state_with_nulls.value.copy()
    for key in unknown_keys:
        if key in validator_type.attribute_types:
            final_value_map[key] = CtyValue.unknown(validator_type.attribute_types[key])

    planned_state_cty_final = CtyValue(validator_type, final_value_map)
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

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

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
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
