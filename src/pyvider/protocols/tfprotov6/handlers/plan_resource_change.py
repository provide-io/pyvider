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
from pyvider.protocols.tfprotov6.handlers._component_config import (
    config_to_attrs_instance,
    unmarshal_config,
)
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    null_write_only_attributes,
    resolve_identity_schema,
    str_path_to_proto_path,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, merge_schema_defaults_into_plan
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
        config_cty = unmarshal_config(request.config, resource_schema.block)
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
        # Failing to decrypt and failing to rebuild the object are different
        # things, and only the second one is recoverable.
        #
        # A decrypt failure means the bytes are not what this provider wrote:
        # the shared secret was rotated or lost, or the blob is corrupt. There
        # is nothing to continue with, and continuing anyway used to plan as
        # though the resource had never had private state -- while apply raised
        # on the very same bytes, so a clean-looking plan was followed by a
        # failed apply.
        try:
            decrypted_bytes = decrypt(prior_private)
        except Exception as e:
            err = ResourceError(
                "The private state stored for this resource could not be decrypted.\n\n"
                "This usually means PYVIDER_PRIVATE_STATE_SHARED_SECRET has changed "
                "since the state was written, or differs between the machines that "
                "run this provider.\n\n"
                "Suggestion: restore the previous shared secret. The value is not "
                "recoverable without it."
            )
            err.add_context("resource.type_name", getattr(resource_class, "__name__", str(resource_class)))
            err.add_context("terraform.summary", "Private state could not be decrypted")
            raise err from e

        # Past decryption the bytes are ours. Failing to rebuild the object from
        # them means the resource's private_state_class has changed shape since
        # they were written, which is an ordinary consequence of upgrading a
        # provider. The resource is expected to rebuild what it needs, so the
        # plan continues without it.
        try:
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
                suggestion="This may be expected if the resource's private state class changed. Private state will be regenerated during apply.",
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
    #
    # Only the configuration is decoded with `apply_defaults`: a null there is
    # an attribute the practitioner omitted, whereas a null in prior state is a
    # recorded absence that must survive the round trip unchanged.
    config_instance = config_to_attrs_instance(config_cty_marked, resource_class.config_class)
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


def _fill_undetermined_computed_attributes(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    validator_type: CtyObject,
    prior_state_cty: CtyValue | None,
) -> None:
    """Decide what an unset optional+computed attribute is planned as.

    On a create the provider does not know the value yet, so it plans unknown --
    what Terraform shows as "known after apply". Planning null there promises a
    null that apply then contradicts, and Core rejects the apply with "Provider
    produced inconsistent result after apply: .id: was null, but now ...".

    On an update the value is not undetermined: the last read already found out
    what it is, and it is sitting in prior state. Re-planning it unknown says it
    may change on every run, which never converges -- `terraform plan` is never
    empty, and with `requires_replace` the attribute lands in the replacement
    paths and the resource is destroyed and recreated on every plan. Terraform's
    own ProposedNew carries the prior value forward for an optional+computed
    attribute whose configuration is null (terraform/internal/plans/objchange/
    objchange.go:328-345), so that is what is kept here, including when the prior
    value is a null the remote API legitimately returned.

    An earlier version of this filled unknown only when some *other* attribute
    already happened to be unknown, which broke creates from a wholly known
    configuration; the fix for that filled unconditionally and broke updates.
    Both cases are pinned in tests/tfprotov6/handlers/
    test_plan_computed_null_stability.py.
    """
    has_prior = prior_state_cty is not None and not prior_state_cty.is_null

    for attr in resource_schema.block.attributes.values():
        if not attr.computed or attr.required:
            continue
        if planned_state_dict.get(attr.name) is not None:
            continue
        attr_type = validator_type.attribute_types.get(attr.name)
        if attr_type is None:
            continue

        prior_value: CtyValue | None = None
        if has_prior and prior_state_cty is not None:
            try:
                prior_value = prior_state_cty[attr.name]
            except (KeyError, TypeError):
                # Not in prior state at all, which happens when the schema gained
                # the attribute since the state was written. Nothing to carry
                # forward, so it is undetermined in the same sense as a create.
                prior_value = None

        planned_state_dict[attr.name] = prior_value if prior_value is not None else CtyValue.unknown(attr_type)


def _handle_planned_state_dict(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
    *,
    prior_state_cty: CtyValue | None = None,
    identity_schema: PvsSchema | None = None,
    identity_values: dict[str, Any] | None = None,
) -> CtyValue:
    logger.debug("_handle_planned_state_dict received", keys=list(planned_state_dict.keys()))
    logger.debug("Planned state dict values", planned_state_dict=planned_state_dict)

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Write-only attributes are nulled here, at the protocol boundary, rather
    # than relying on BaseResource._merge_config_into_plan: `plan()` is a
    # documented extension point, and a resource that overrides it used to hand
    # the secret straight to Terraform. Terraform rejects a non-null write-only
    # value in a plan ("returned a value for the write-only attribute ... during
    # planning"), and an older Terraform stores it in the plan file instead.
    null_write_only_attributes(planned_state_dict, resource_schema.block)

    _fill_undetermined_computed_attributes(
        planned_state_dict, resource_schema, validator_type, prior_state_cty
    )

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
    `ctx.require_replace()`. `PvsNestedBlock` and `PvsAttribute` reject
    `requires_replace` inside a block or an object-typed attribute at
    schema-definition time rather than letting the flag look effective here
    while silently doing nothing.

    Write-only attributes never reach the comparison below: their values are
    nulled in both prior and planned state, so the diff would always be
    empty. `PvsAttribute` rejects `write_only=True` combined with
    `requires_replace=True` at schema-definition time rather than letting the
    flag look effective while silently doing nothing.

    On an `optional=True, computed=True` attribute the unknown-counts-as-changed
    rule above is reachable in one narrow case: the normal path carries prior
    state forward, so the planned value stays known and nothing fires, but a
    plan hook that deliberately leaves the attribute unknown will force
    replacement on every plan. That is the conservative half of the trade-off,
    not a defect -- an unknown value may still resolve to something the remote
    API cannot change in place.
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

    # Resolved against the schema: a path Terraform is asked to replace on must
    # name something that exists. `changed_names` always does, but a context
    # path comes from a `ctx.require_replace()` call and can be misspelt, and a
    # well-formed path naming nothing is indistinguishable from a real one until
    # it is resolved.
    within = resource_schema.block.to_cty_type()
    proto_paths = []
    for path in ordered_paths:
        proto_path = str_path_to_proto_path(path, within=within)
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


def _finalize_planned_state(
    response: pb.PlanResourceChange.Response,
    planned_state_dict: dict[str, Any],
    config_cty: CtyValue,
    prior_state_cty: CtyValue,
    resource_class: Any,
    resource_schema: Any,
    resource_context: Any,
    identity_schema: Any,
    type_name: str,
) -> None:
    """Reconcile, marshal and annotate the plan a resource returned."""
    # Defaults are a framework invariant, not an implementation detail of
    # BaseResource.plan().  A resource may override that documented extension
    # point (or implement ResourceProtocol directly), but its returned plan must
    # still agree with the effective configuration the apply hook receives.
    # Reconcile at the protocol boundary, after the hook has made its changes and
    # before identity, replacement paths, validation, and marshaling inspect the plan.
    merge_schema_defaults_into_plan(planned_state_dict, config_cty, resource_schema.block)

    identity_values = (
        _derive_planned_identity_values(resource_class, resource_schema, planned_state_dict, type_name)
        if identity_schema is not None
        else None
    )
    planned_state_cty = _handle_planned_state_dict(
        planned_state_dict,
        resource_schema,
        response,
        prior_state_cty=prior_state_cty,
        identity_schema=identity_schema,
        identity_values=identity_values,
    )
    response.requires_replace.extend(
        _collect_requires_replace_paths(
            resource_schema,
            prior_state_cty,
            planned_state_cty,
            resource_context.requires_replace_paths,
            type_name,
        )
    )


def _store_planned_private_state(
    response: pb.PlanResourceChange.Response,
    planned_private_state_attrs: Any,
    type_name: str,
    *,
    prior_private: bytes = b"",
) -> None:
    """Store whatever private state the plan produced, or keep what was already there.

    Terraform records the plan's private state verbatim and hands it back as
    `prior_private` next time, so returning nothing erases it rather than
    leaving it alone (node_resource_abstract_instance.go:549,1396). Most
    resources establish private state at create and never mention it again --
    the default `_update` returns `(base_plan, None)` -- so the first plan after
    a create used to wipe it.

    terraform-plugin-sdk assigns `resp.PlannedPrivate = req.PriorPrivate` before
    the hook runs (helper/schema/grpc_provider.go:1040,1065,1164), and this is
    the same default. The prior bytes are passed through as they arrived, still
    encrypted: they are opaque here, and decrypting only to re-encrypt would add
    a way to fail without adding anything.
    """
    if not planned_private_state_attrs:
        if prior_private:
            response.planned_private = prior_private
            logger.debug(
                "Carried prior private state forward",
                operation="plan_resource_change",
                resource_type=type_name,
                private_state_size=len(prior_private),
            )
        return

    serialized_private_bytes = msgpack.packb(attrs.asdict(planned_private_state_attrs), use_bin_type=True)
    response.planned_private = encrypt(serialized_private_bytes)

    logger.debug(
        "Encrypted planned private state",
        operation="plan_resource_change",
        resource_type=type_name,
        private_state_size=len(response.planned_private),
    )


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

        if planned_state_dict is not None:
            _finalize_planned_state(
                response,
                planned_state_dict,
                config_cty,
                prior_state_cty,
                resource_class,
                resource_schema,
                resource_context,
                identity_schema,
                request.type_name,
            )

        _store_planned_private_state(
            response,
            planned_private_state_attrs,
            request.type_name,
            prior_private=request.prior_private,
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
