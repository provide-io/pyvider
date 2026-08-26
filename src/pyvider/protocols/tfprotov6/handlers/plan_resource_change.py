#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import msgpack  # type: ignore[import-untyped]
from provide.foundation import logger

from pyvider.common.encryption import decrypt, encrypt
from pyvider.common.operation_context import OperationContext, operation_context
from pyvider.conversion import marshal, marshal_identity, unmarshal, unmarshal_identity
from pyvider.conversion.marshaler import _apply_schema_marks_iterative
from pyvider.cty import CtyObject, CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import Deferral, PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    resolve_identity_schema,
    str_path_to_proto_path,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema
from pyvider.schema.required import check_required_attributes


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
    *,
    identity_schema: PvsSchema | None = None,
    prior_identity: pb.ResourceIdentityData | None = None,
) -> ResourceContext:
    # config and prior state keep the default policy: a config that is not
    # wholly known collapses to None, so a provider's custom validator is never
    # handed a half-known object (issue #5).
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    # The proposed new state must NOT collapse. `BaseResource.plan` reads "no
    # config and no planned state" as a delete, so a config carrying an unknown
    # -- the ordinary `name = other_resource.computed` dependency -- would plan
    # absence, and Terraform rejects the whole plan with "planned for absence
    # but config wants existence". `from_cty` handles unknowns per attribute,
    # yielding an instance whose not-yet-known fields are None.
    proposed_new_state_instance = cty_to_attrs_instance(
        proposed_new_state_cty, resource_class.state_class, allow_unknown=True
    )

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
        identity=(
            unmarshal_identity(prior_identity, identity_schema) if identity_schema is not None else None
        ),
    )


def _handle_planned_state_dict(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
    *,
    identity_schema: PvsSchema | None = None,
    identity_values: dict[str, Any] | None = None,
) -> CtyValue:
    logger.debug("_handle_planned_state_dict received", keys=list(planned_state_dict.keys()))
    logger.debug("Planned state dict values", planned_state_dict=planned_state_dict)

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

    logger.debug("Raw values for validation", keys=list(raw_values_for_validation.keys()))

    # cty 0.5 no longer refuses a present-but-null value for a required
    # attribute (see pyvider.schema.required). Config nulls are already
    # rejected earlier, at ValidateResourceConfig -- this catches a different
    # thing: a bug in *this provider's* plan() implementation that left a
    # required, non-computed attribute null in the planned state it is about
    # to hand back to Terraform. Raises, and is caught the same way as every
    # other planning failure by _plan_resource_change_impl's own exception
    # handling.
    check_required_attributes(resource_schema.block, raw_values_for_validation, is_state=True)

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final: CtyValue = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack

    if identity_schema is not None and identity_values is not None:
        response.planned_identity.CopyFrom(marshal_identity(identity_values, identity_schema))

    return planned_state_cty_final


def _attribute_changed(prior_value: Any, planned_value: Any) -> bool:
    """Decide whether an attribute's planned value differs from its prior value.

    An unknown planned value counts as a change. It may well resolve to the
    prior value at apply time, but the plan has to be decided now, and
    Terraform's own plan modifiers treat unknown-vs-known as unequal for
    exactly this reason: under-reporting replacement produces an in-place
    update the provider cannot honour, while over-reporting is at worst a
    conservative plan the practitioner sees before approving.

    Comparison is on native Python values rather than CtyValues: prior state
    arrives unmarshalled and unmarked, while planned values may still carry
    schema marks (sensitive, write-only) picked up from the marked config, and
    a mark difference does not mean the value changed.
    """
    if isinstance(planned_value, CtyValue) and planned_value.is_unknown:
        return True
    if isinstance(prior_value, CtyValue) and prior_value.is_unknown:
        return True

    prior_native = cty_to_native(prior_value) if isinstance(prior_value, CtyValue) else prior_value
    planned_native = cty_to_native(planned_value) if isinstance(planned_value, CtyValue) else planned_value
    return bool(prior_native != planned_native)


def _collect_requires_replace_paths(
    resource_schema: Any,
    prior_state_cty: CtyValue | None,
    planned_state_cty: CtyValue | None,
    context_paths: list[str],
    resource_type: str,
) -> list[pb.AttributePath]:
    """Build the attribute paths that force a destroy-and-create.

    Two sources feed this: attributes declared `requires_replace=True` in the
    schema, whose planned value is compared against prior state, and paths a
    resource added imperatively via `ctx.require_replace()`.

    Nothing is reported when there is no prior state (a resource being created
    cannot be replaced) or no planned state (it is being destroyed); Terraform
    rejects requires_replace paths in both cases.

    Only top-level attributes are compared. An attribute inside a nested block
    has no single path until the block's elements are matched up between prior
    and planned state -- a correspondence Terraform itself establishes and this
    layer cannot guess for list or set nesting -- so a resource that needs
    replacement on a nested attribute states the path itself via
    `ctx.require_replace()`.

    Write-only attributes never reach the comparison below: their values are
    nulled in both prior and planned state, so the diff would always be
    empty. `PvsAttribute` rejects `write_only=True` combined with
    `requires_replace=True` at schema-definition time rather than letting the
    flag look effective while silently doing nothing.
    """
    if prior_state_cty is None or prior_state_cty.is_null or planned_state_cty is None:
        return []

    prior_values = prior_state_cty.value if isinstance(prior_state_cty.value, dict) else {}
    planned_values = planned_state_cty.value if isinstance(planned_state_cty.value, dict) else {}

    changed_names = [
        name
        for name, attr in resource_schema.block.attributes.items()
        if attr.requires_replace and _attribute_changed(prior_values.get(name), planned_values.get(name))
    ]

    # Schema-declared names first, then context paths, de-duplicated while
    # preserving order so the plan output is stable across runs.
    ordered_paths: list[str] = list(changed_names)
    ordered_paths.extend(path for path in context_paths if path not in ordered_paths)

    proto_paths = []
    for path in ordered_paths:
        proto_path = str_path_to_proto_path(path)
        if proto_path is not None:
            proto_paths.append(proto_path)

    if proto_paths:
        logger.info(
            "Planning resource replacement",
            operation="plan_resource_change",
            resource_type=resource_type,
            requires_replace=ordered_paths,
        )

    return proto_paths


def _derive_planned_identity_values(
    resource_class: Any,
    resource_schema: Any,
    planned_state_dict: dict[str, Any],
    resource_type: str,
) -> dict[str, Any] | None:
    """Derive identity from the planned state, when fully determinable.

    The common "not yet knowable" case during plan -- an identity attribute
    that depends on a value still unknown at plan time -- does not raise:
    validation preserves the unknown, cty_to_attrs_instance yields None for
    that field, and get_identity()'s own null-check returns None cleanly.
    What this actually catches is malformed/incomplete planned-state data, or
    a bug in a resource's custom get_identity() override -- genuine defects,
    not "not yet". Identity is still omitted rather than surfaced as a
    Terraform diagnostic here (a partial or unknown-bearing identity would
    itself make Terraform report the provider as buggy), but the failure is
    logged at WARNING so it is visible in provider logs instead of silently
    disappearing.
    """
    try:
        # cty 0.5 no longer refuses a present-but-null value for a required
        # attribute (see pyvider.schema.required); a null there is exactly
        # the "malformed/incomplete planned-state data" this function's
        # broad except already documents catching, so it is checked here
        # too and left to that same except -- omit identity, warn, move on.
        check_required_attributes(resource_schema.block, planned_state_dict, is_state=True)
        identity_values: dict[str, Any] | None = resource_class.get_identity(
            cty_to_attrs_instance(
                resource_schema.block.to_cty_type().validate(planned_state_dict),
                resource_class.state_class,
            )
        )
        return identity_values
    except Exception as e:
        logger.warning(
            "Omitting planned identity: derivation raised an exception. This is not the "
            "ordinary not-yet-knowable case, which returns None without raising -- it is "
            "either planned-state data that failed to validate against the resource schema "
            "or a bug in this resource's get_identity() override",
            operation="plan_resource_change",
            resource_type=resource_type,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        return None


@rpc_handler("PlanResourceChange")
async def PlanResourceChangeHandler(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Handle plan resource change request."""
    return await _plan_resource_change_impl(request, context)


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

        identity_schema = resolve_identity_schema(resource_class)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
            identity_schema=identity_schema,
            prior_identity=request.prior_identity,
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
            identity_values = (
                _derive_planned_identity_values(
                    resource_class, resource_schema, planned_state_dict, request.type_name
                )
                if identity_schema is not None
                else None
            )
            planned_state_cty = _handle_planned_state_dict(
                planned_state_dict,
                resource_schema,
                response,
                identity_schema=identity_schema,
                identity_values=identity_values,
            )
            response.requires_replace.extend(
                _collect_requires_replace_paths(
                    resource_schema,
                    prior_state_cty,
                    planned_state_cty,
                    resource_context.requires_replace_paths,
                    request.type_name,
                )
            )

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

    except Deferral as e:
        logger.info(
            "Response deferred",
            operation="plan_resource_change",
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
