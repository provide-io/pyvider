#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_create() { echo -e "✨ $1"; }
log_update() { echo -e "🔄 $1"; }
log_delete() { echo -e "🔥 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying changes to propagate test_mode_enabled to component contexts..."

log_update "Updating: pyvider/ephemerals/context.py"
mkdir -p pyvider/ephemerals/
cat <<'EOF' > pyvider/ephemerals/context.py
from typing import Generic, TypeVar

from attrs import define, field

from pyvider.common.context import BaseContext
from pyvider.resources.private_state import PrivateState

ConfigType = TypeVar("ConfigType")
PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)


@define(frozen=True)
class EphemeralResourceContext(BaseContext, Generic[ConfigType, PrivateStateType]):
    """
    Context for ephemeral resource operations. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: ConfigType | None = None
    private_state: PrivateStateType | None = None
    test_mode_enabled: bool = field(default=False, kw_only=True)
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/apply_resource_change.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/apply_resource_change.py
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
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/close_ephemeral_resource.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/close_ephemeral_resource.py
import time
from typing import Any

import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


@resilient()
async def CloseEphemeralResourceHandler(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Handles closing an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="CloseEphemeralResource")

    try:
        return await _close_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="CloseEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="CloseEphemeralResource")


async def _close_ephemeral_resource_impl(
    request: pb.CloseEphemeralResource.Request, context: Any
) -> pb.CloseEphemeralResource.Response:
    """Implementation of CloseEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource close operation",
        operation="close_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.CloseEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during close operation",
                operation="close_ephemeral_resource",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator.\n\n"
                f"Troubleshooting:\n"
                f"  1. Verify the ephemeral resource module is imported\n"
                f"  2. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  3. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
        if not resource_class.private_state_class:
            logger.error(
                "Ephemeral resource missing private_state_class",
                operation="close_ephemeral_resource",
                resource_type=request.type_name,
            )
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot close.\n\n"
                f"Suggestion: Ephemeral resources must define a private_state_class for lifecycle management.\n\n"
                f"Documentation: See ephemeral resource documentation for private state usage."
            )

        private_data = msgpack.unpackb(request.private, raw=False)
        private_state_instance = resource_class.private_state_class(**private_data)

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

        ctx = EphemeralResourceContext(
            private_state=private_state_instance, test_mode_enabled=test_mode_enabled
        )
        resource_instance = resource_class()

        await resource_instance.close(ctx)

        logger.info(
            "Ephemeral resource close completed successfully",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
        )

    except PyviderError as e:
        logger.error(
            "Ephemeral resource close failed with known error",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource close failed with unexpected error",
            operation="close_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/open_ephemeral_resource.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/open_ephemeral_resource.py
import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception, cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def OpenEphemeralResourceHandler(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Handles opening an ephemeral resource."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="OpenEphemeralResource")

    try:
        return await _open_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="OpenEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="OpenEphemeralResource")


async def _open_ephemeral_resource_impl(
    request: pb.OpenEphemeralResource.Request, context: Any
) -> pb.OpenEphemeralResource.Response:
    """Implementation of OpenEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource open operation",
        operation="open_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.OpenEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during open operation",
                operation="open_ephemeral_resource",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the ephemeral resource class has the @ephemeral decorator\n"
                f"  2. Verify the ephemeral resource module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  4. Review provider logs for component registration errors\n"
                f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )

        schema = resource_class.get_schema()
        config_cty = unmarshal(request.config, schema=schema.block)
        config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

        ctx = EphemeralResourceContext(config=config_instance, test_mode_enabled=test_mode_enabled)
        resource_instance = resource_class()

        result_obj, private_state_obj, renew_at = await resource_instance.open(ctx)

        # Marshal the results back to the wire format
        if result_obj:
            raw_result = attrs.asdict(result_obj)
            response.result.CopyFrom(marshal(raw_result, schema=schema.block))

        if private_state_obj:
            response.private = msgpack.packb(attrs.asdict(private_state_obj), use_bin_type=True)

        if renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(renew_at))

        logger.info(
            "Ephemeral resource open completed successfully",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            has_result=result_obj is not None,
            has_private_state=private_state_obj is not None,
            has_renew_at=renew_at is not None,
        )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Ephemeral resource open failed with known error",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource open failed with unexpected error",
            operation="open_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/plan_resource_change.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/plan_resource_change.py
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
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/read_data_source.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/read_data_source.py
import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import DataSourceError, PyviderError
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
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@resilient()
async def ReadDataSourceHandler(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Handle read data source request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ReadDataSource")

    try:
        return await _read_data_source_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ReadDataSource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ReadDataSource")


async def _read_data_source_impl(
    request: pb.ReadDataSource.Request, context: Any
) -> pb.ReadDataSource.Response:
    """Implementation of ReadDataSource handler."""
    logger.debug(
        "Starting data source read operation",
        operation="read_data_source",
        data_source_type=request.type_name,
    )

    response = pb.ReadDataSource.Response()
    resource_context = None
    try:
        ds_class = hub.get_component("data_source", request.type_name)
        if not ds_class:
            logger.error(
                "Data source type not found during read operation",
                operation="read_data_source",
                data_source_type=request.type_name,
                registered_data_sources=list(hub.get_components("data_source").keys())
                if hub.get_components("data_source")
                else [],
            )

            err = DataSourceError(
                f"Data source type '{request.type_name}' not registered.\n\n"
                f"Suggestion: Ensure the data source is registered using the @data_source decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the data source class has the @data_source decorator\n"
                f"  2. Verify the data source module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered data sources\n"
                f"  4. Review provider logs for component registration errors\n"
                f"  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
            err.add_context("data_source.type_name", request.type_name)
            err.add_context("terraform.summary", "Unknown data source type")
            err.add_context(
                "terraform.detail",
                f"The data source type '{request.type_name}' is not registered with this provider.",
            )
            raise err

        ds_schema = ds_class.get_schema()
        config_cty = unmarshal(request.config, schema=ds_schema.block)
        config_instance = cty_to_attrs_instance(config_cty, ds_class.config_class)

        data_source = ds_class()

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
        resource_context = ResourceContext(config=config_instance, test_mode_enabled=test_mode_enabled)

        # Auto-inject capabilities based on component_of registration
        read_kwargs = {}
        parent_capability = getattr(ds_class, "_parent_capability", None)

        logger.debug(
            "Checking capability injection for data source",
            operation="read_data_source",
            data_source_type=request.type_name,
            parent_capability=parent_capability,
        )

        if parent_capability and parent_capability != "provider":
            capability_class = hub.get_component("capability", parent_capability)
            if capability_class:
                # Ensure we have an instance, not a class
                if isinstance(capability_class, type):
                    capability_instance = capability_class()
                else:
                    capability_instance = capability_class
                read_kwargs[parent_capability] = capability_instance
                logger.debug(
                    "Auto-injected capability for data source",
                    operation="read_data_source",
                    data_source_type=request.type_name,
                    capability_name=parent_capability,
                )
            else:
                logger.warning(
                    "Capability not found for data source",
                    operation="read_data_source",
                    data_source_type=request.type_name,
                    capability_name=parent_capability,
                )
        else:
            logger.debug(
                "No capability injection needed for data source",
                operation="read_data_source",
                data_source_type=request.type_name,
            )

        logger.debug(
            "Calling data source read method",
            operation="read_data_source",
            data_source_type=request.type_name,
            injected_capabilities=list(read_kwargs.keys()),
        )
        state_attrs_obj = await data_source.read(resource_context, **read_kwargs)

        if state_attrs_obj is not None:
            raw_state_dict = attrs_to_dict_for_cty(state_attrs_obj)
            validator_type = ds_schema.block.to_cty_type()
            state_cty = validator_type.validate(raw_state_dict)

            marshalled_state = marshal(state_cty, schema=ds_schema.block)
            response.state.msgpack = marshalled_state.msgpack

            logger.info(
                "Data source read completed successfully with state",
                operation="read_data_source",
                data_source_type=request.type_name,
                has_state=True,
            )
        else:
            response.state.msgpack = b"\xc0"  # Represents null
            logger.info(
                "Data source read completed with null state",
                operation="read_data_source",
                data_source_type=request.type_name,
                has_state=False,
            )

    except (CtyValidationError, PyviderError) as e:
        logger.error(
            "Data source read failed with known error",
            operation="read_data_source",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Data source read failed with unexpected error",
            operation="read_data_source",
            data_source_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        logger.debug(
            "Adding resource context diagnostics to response",
            operation="read_data_source",
            data_source_type=request.type_name,
            diagnostic_count=len(resource_context.diagnostics),
        )
        response.diagnostics.extend(resource_context.diagnostics)

    return response
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/read_resource.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/read_resource.py
import time
from typing import Any

import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.common.encryption import decrypt
from pyvider.conversion import marshal, unmarshal
from pyvider.exceptions import PyviderError, ResourceError
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
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@resilient()
async def ReadResourceHandler(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Handle read resource request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ReadResource")

    try:
        return await _read_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ReadResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ReadResource")


async def _read_resource_impl(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None

    logger.debug(
        "ReadResource handler called",
        operation="read_resource",
        resource_type=request.type_name,
        has_current_state=bool(request.current_state.msgpack),
        has_private_state=bool(request.private),
    )

    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            logger.error(
                "Resource type not found during read operation",
                operation="read_resource",
                resource_type=request.type_name,
                registered_resources=list(hub.get_components("resource").keys())
                if hub.get_components("resource")
                else [],
            )

            err = ResourceError(
                f"Resource type '{request.type_name}' not registered.\n\n"
                f"Suggestion: Ensure the resource is registered using the @resource decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the resource class has the @resource decorator\n"
                f"  2. Verify the resource module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered resources\n"
                f"  4. Review provider logs for component registration errors"
            )
            err.add_context("resource.type_name", request.type_name)
            raise err

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            logger.error(
                "Provider instance not found in hub during read operation",
                operation="read_resource",
                resource_type=request.type_name,
            )
            raise RuntimeError(
                "Provider instance not found in hub.\n\n"
                "This is an internal framework error. The provider should be registered "
                "during server initialization.\n\n"
                "Suggestion: Report this issue - it indicates a provider initialization problem."
            )

        logger.debug(
            "Resource and provider instances retrieved for read",
            operation="read_resource",
            resource_type=request.type_name,
        )

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                logger.debug(
                    "Deserializing private state for read operation",
                    operation="read_resource",
                    resource_type=request.type_name,
                    private_state_size=len(request.private),
                )

                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)

                logger.debug(
                    "Private state deserialized successfully",
                    operation="read_resource",
                    resource_type=request.type_name,
                )

            except Exception as e:
                logger.error(
                    "Failed to deserialize private state during read",
                    operation="read_resource",
                    resource_type=request.type_name,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    exc_info=True,
                )

                err = ResourceError(
                    f"Failed to deserialize private state for resource '{request.type_name}': {e}\n\n"
                    f"Suggestion: This usually indicates a mismatch between the state encryption key "
                    f"or corrupted private state data.\n\n"
                    f"Troubleshooting:\n"
                    f"  1. Verify PYVIDER_PRIVATE_STATE_SHARED_SECRET hasn't changed\n"
                    f"  2. Check if the private state schema has changed incompatibly\n"
                    f"  3. Review the original error: {type(e).__name__}: {e}\n"
                    f"  4. Consider destroying and recreating the resource if schema changed"
                )
                err.add_context("resource.type_name", request.type_name)
                err.add_context("private_state.error", str(e))
                raise err from e

        logger.debug(
            "Invoking resource read method",
            operation="read_resource",
            resource_type=request.type_name,
        )

        resource_handler = resource_class()
        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
            test_mode_enabled=test_mode_enabled,
        )
        new_state_attrs = await resource_handler.read(resource_context)

        if new_state_attrs is not None:
            raw_state_dict = attrs_to_dict_for_cty(new_state_attrs)
            validator_type = resource_schema.block.to_cty_type()
            new_state_cty = validator_type.validate(raw_state_dict)
            marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
            response.new_state.msgpack = marshalled_new_state.msgpack

            logger.info(
                "Resource read completed successfully with new state",
                operation="read_resource",
                resource_type=request.type_name,
                state_fields=list(raw_state_dict.keys()),
            )
        else:
            response.new_state.msgpack = b"\xc0"

            logger.info(
                "Resource read completed - resource no longer exists",
                operation="read_resource",
                resource_type=request.type_name,
            )

        response.private = request.private

    except PyviderError as e:
        logger.error(
            "ReadResource failed with framework error",
            operation="read_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "ReadResource failed with unexpected error",
            operation="read_resource",
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
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/renew_ephemeral_resource.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/renew_ephemeral_resource.py
import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.ephemerals import EphemeralResourceContext
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.utils import datetime_to_proto


@resilient()
async def RenewEphemeralResourceHandler(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Handles renewing an ephemeral resource's lease."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="RenewEphemeralResource")

    try:
        return await _renew_ephemeral_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="RenewEphemeralResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="RenewEphemeralResource")


async def _renew_ephemeral_resource_impl(
    request: pb.RenewEphemeralResource.Request, context: Any
) -> pb.RenewEphemeralResource.Response:
    """Implementation of RenewEphemeralResource handler."""
    logger.debug(
        "Starting ephemeral resource renew operation",
        operation="renew_ephemeral_resource",
        resource_type=request.type_name,
    )

    response = pb.RenewEphemeralResource.Response()
    try:
        resource_class = hub.get_component("ephemeral_resource", request.type_name)
        if not resource_class:
            logger.error(
                "Ephemeral resource type not found during renew operation",
                operation="renew_ephemeral_resource",
                resource_type=request.type_name,
                registered_ephemeral_resources=list(hub.get_components("ephemeral_resource").keys())
                if hub.get_components("ephemeral_resource")
                else [],
            )
            raise ValueError(
                f"Ephemeral resource type '{request.type_name}' not found.\n\n"
                f"Suggestion: Ensure the ephemeral resource is registered using the @ephemeral decorator.\n\n"
                f"Troubleshooting:\n"
                f"  1. Verify the ephemeral resource module is imported\n"
                f"  2. Run 'pyvider components list' to see registered ephemeral resources\n"
                f"  3. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
        if not resource_class.private_state_class:
            logger.error(
                "Ephemeral resource missing private_state_class",
                operation="renew_ephemeral_resource",
                resource_type=request.type_name,
            )
            raise ResourceError(
                f"Resource '{request.type_name}' does not define a private_state_class, cannot renew.\n\n"
                f"Suggestion: Ephemeral resources that support renewal must define a private_state_class.\n\n"
                f"Documentation: See ephemeral resource documentation for private state usage."
            )

        private_data = msgpack.unpackb(request.private, raw=False)
        private_state_instance = resource_class.private_state_class(**private_data)

        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

        ctx = EphemeralResourceContext(
            private_state=private_state_instance, test_mode_enabled=test_mode_enabled
        )
        resource_instance = resource_class()

        new_private_state_obj, new_renew_at = await resource_instance.renew(ctx)

        if new_private_state_obj:
            response.private = msgpack.packb(attrs.asdict(new_private_state_obj), use_bin_type=True)

        if new_renew_at:
            response.renew_at.CopyFrom(datetime_to_proto(new_renew_at))

        logger.info(
            "Ephemeral resource renew completed successfully",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            has_new_private_state=new_private_state_obj is not None,
            has_new_renew_at=new_renew_at is not None,
        )

    except PyviderError as e:
        logger.error(
            "Ephemeral resource renew failed with known error",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "Ephemeral resource renew failed with unexpected error",
            operation="renew_ephemeral_resource",
            resource_type=request.type_name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
EOF

log_update "Updating: pyvider/resources/context.py"
mkdir -p pyvider/resources/
cat <<'EOF' > pyvider/resources/context.py
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

import attrs
from attrs import define, field

from pyvider.common.context import BaseContext
from pyvider.common.types import ConfigType, StateType
from pyvider.cty import CtyValue
from pyvider.resources.private_state import PrivateState

if TYPE_CHECKING:
    from pyvider.capabilities import BaseCapability

PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)


@define(frozen=True)
class ResourceContext(BaseContext, Generic[ConfigType, StateType, PrivateStateType]):
    config: ConfigType | None = None
    state: StateType | None = None
    planned_state: StateType | None = None
    private_state: PrivateStateType | None = None
    config_cty: CtyValue | None = None
    planned_state_cty: CtyValue | None = None
    capabilities: dict[str, BaseCapability] = field(factory=dict)
    test_mode_enabled: bool = field(default=False, kw_only=True)

    def get_private_state(self, private_state_class: type[PrivateStateType]) -> PrivateStateType | None:
        """
        Get typed private state with automatic casting.

        Args:
            private_state_class: The private state class type to cast to

        Returns:
            Typed private state instance or None if no private state exists

        Example:
            private_data = ctx.get_private_state(MyPrivateState)
            if private_data:
                token = private_data.token
        """
        if self.private_state:
            # If it's already the correct type, return as-is
            if isinstance(self.private_state, private_state_class):
                return self.private_state
            # Otherwise, convert from dict representation
            if hasattr(self.private_state, "__dict__") or isinstance(self.private_state, dict):
                state_dict = (
                    attrs.asdict(self.private_state)
                    if hasattr(self.private_state, "__dict__")
                    else self.private_state
                )
                return private_state_class(**state_dict)
        return None

    def has_private_state(self) -> bool:
        """
        Check if private state exists.

        Returns:
            True if private state is present, False otherwise
        """
        return self.private_state is not None

    def is_field_unknown(self, field_name: str, source: str = "config") -> bool:
        """
        Check if a configuration or state field has an unknown value during planning.

        This is the proper way for resources to handle unknown values - check explicitly
        rather than catching errors or working around None values.

        Args:
            field_name: Name of the field to check
            source: Which CTY value to check - "config" or "planned_state" (default: "config")

        Returns:
            True if the field exists but has an unknown value, False otherwise

        Example:
            async def _create(self, ctx: ResourceContext, base_plan: dict) -> ...:
                if ctx.is_field_unknown("content"):
                    # Content is unknown during planning, can't compute hash
                    base_plan["exists"] = True
                    return base_plan, None

                # Content is known, use typed config
                config = cast(FileContentConfig, ctx.config)
                base_plan["content_hash"] = hashlib.sha256(config.content.encode()).hexdigest()
                return base_plan, None
        """
        cty_value = self.config_cty if source == "config" else self.planned_state_cty

        if not cty_value or cty_value.is_null:
            return False

        if not hasattr(cty_value, "value") or not isinstance(cty_value.value, dict):
            return False

        field_cty = cty_value.value.get(field_name)
        if field_cty is None:
            return False

        # Check if it's a CtyValue with unknown marker
        if isinstance(field_cty, CtyValue):
            return field_cty.is_unknown

        return False
EOF

log_success "Project update for test mode propagation complete."