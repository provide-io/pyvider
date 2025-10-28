#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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
    check_test_only_access,
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

        # Check if this is a test-only component accessed without test mode
        check_test_only_access(resource_class, request.type_name, "resource")

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


# 🐍🏗️🔚
