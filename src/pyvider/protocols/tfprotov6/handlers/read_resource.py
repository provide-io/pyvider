#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import msgpack  # type: ignore[import-untyped]
from provide.foundation import logger

from pyvider.common.encryption import decrypt
from pyvider.conversion import marshal, marshal_identity, unmarshal, unmarshal_identity
from pyvider.exceptions import Deferral, PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    derive_identity_values,
    resolve_identity_schema,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema


@rpc_handler("ReadResource")
async def ReadResourceHandler(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Handle read resource request."""
    return await _read_resource_impl(request, context)


def _set_new_identity(
    response: pb.ReadResource.Response,
    resource_class: Any,
    identity_schema: PvsSchema | None,
    new_state_attrs: Any,
    resource_type: str,
) -> None:
    """Attach derived identity to the response, only when fully determinable."""
    if identity_schema is None:
        return
    identity_values = derive_identity_values(resource_class, new_state_attrs, resource_type, "read_resource")
    if identity_values is not None:
        response.new_identity.CopyFrom(marshal_identity(identity_values, identity_schema))


def _registered_resource(type_name: str) -> Any:
    """The registered resource class, or an error naming what to check."""
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        registered = hub.get_components("resource")
        logger.error(
            "Resource type not found during read operation",
            operation="read_resource",
            resource_type=type_name,
            registered_resources=list(registered.keys()) if registered else [],
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
        raise err

    # Check if this is a test-only component accessed without test mode
    check_test_only_access(resource_class, type_name, "resource")
    return resource_class


def _require_provider(type_name: str) -> Any:
    """The registered provider. Its absence is a framework fault, not a configuration one."""
    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        logger.error(
            "Provider instance not found in hub during read operation",
            operation="read_resource",
            resource_type=type_name,
        )
        raise RuntimeError(
            "Provider instance not found in hub.\n\n"
            "This is an internal framework error. The provider should be registered "
            "during server initialization.\n\n"
            "Suggestion: Report this issue - it indicates a provider initialization problem."
        )
    return provider_instance


def _load_private_state(resource_class: Any, request: pb.ReadResource.Request) -> Any:
    """Decrypt the private state Terraform handed back, if this resource keeps any."""
    if not (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and request.private
    ):
        return None

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

    return private_state_instance


def _write_new_state(
    response: pb.ReadResource.Response,
    resource_class: Any,
    resource_schema: Any,
    identity_schema: Any,
    new_state_attrs: Any,
    type_name: str,
) -> None:
    """Marshal what read() found, or record that the object is gone."""
    if new_state_attrs is None:
        response.new_state.msgpack = b"\xc0"
        logger.info(
            "Resource read completed - resource no longer exists",
            operation="read_resource",
            resource_type=type_name,
        )
        return

    raw_state_dict = attrs_to_dict_for_cty(new_state_attrs)

    # Force write-only attributes to None (null in state)
    write_only_attrs = {
        name
        for name, attr in getattr(resource_schema.block, "attributes", {}).items()
        if getattr(attr, "write_only", False)
    }
    for attr_name in write_only_attrs:
        if attr_name in raw_state_dict:
            raw_state_dict[attr_name] = None

    new_state_cty = resource_schema.block.to_cty_type().validate(raw_state_dict)
    response.new_state.msgpack = marshal(new_state_cty, schema=resource_schema.block).msgpack
    _set_new_identity(response, resource_class, identity_schema, new_state_attrs, type_name)

    logger.info(
        "Resource read completed successfully with new state",
        operation="read_resource",
        resource_type=type_name,
        state_fields=list(raw_state_dict.keys()),
    )


async def _read_resource_impl(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context: Any = None

    logger.debug(
        "ReadResource handler called",
        operation="read_resource",
        resource_type=request.type_name,
        has_current_state=bool(request.current_state.msgpack),
        has_private_state=bool(request.private),
    )

    try:
        resource_class = _registered_resource(request.type_name)
        provider_instance = _require_provider(request.type_name)

        logger.debug(
            "Resource and provider instances retrieved for read",
            operation="read_resource",
            resource_type=request.type_name,
        )

        resource_schema = resource_class.get_schema()
        identity_schema = resolve_identity_schema(resource_class)
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = _load_private_state(resource_class, request)

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
            identity=(
                unmarshal_identity(request.current_identity, identity_schema)
                if identity_schema is not None
                else None
            ),
        )
        new_state_attrs = await resource_handler.read(resource_context)

        _write_new_state(
            response, resource_class, resource_schema, identity_schema, new_state_attrs, request.type_name
        )
        response.private = request.private

    except Deferral as e:
        logger.info(
            "Response deferred",
            operation="read_resource",
            resource_type=request.type_name,
            reason=e.reason.name,
        )
        if not getattr(request.client_capabilities, "deferral_allowed", False):
            diag = pb.Diagnostic(
                severity=pb.Diagnostic.ERROR,
                summary="Invalid Deferral",
                detail="The provider raised a Deferral but Terraform did not set deferral_allowed for this request.",
            )
            response.diagnostics.append(diag)
        else:
            response.deferred.reason = pb.Deferred.Reason.Value(e.reason.name)  # type: ignore[assignment]
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


# 🐍🏗️🔚
