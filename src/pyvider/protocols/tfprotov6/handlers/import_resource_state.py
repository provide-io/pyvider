#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import msgpack  # type: ignore[import-untyped]
from provide.foundation import logger

from pyvider.common.encryption import encrypt
from pyvider.conversion import marshal
from pyvider.conversion.identity import marshal_identity, unmarshal_identity
from pyvider.exceptions import Deferral, ResourceError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    check_test_only_access,
    create_diagnostic_from_exception,
    derive_identity_values,
    resolve_identity_schema,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext


@rpc_handler("ImportResourceState")
async def ImportResourceStateHandler(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Handle import resource state request."""
    return await _import_resource_state_impl(request, context)


def _registered_resource(type_name: str) -> Any:
    """The registered resource class for a type name, or an error naming what to check."""
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(
            f"Resource type '{type_name}' not registered.\n\n"
            f"Suggestion: Ensure the resource is registered with @register_resource "
            f"and that component discovery has completed.\n\n"
            f"Run 'pyvider components list' to see what was registered."
        )
        err.add_context("resource.type_name", type_name)
        raise err

    check_test_only_access(resource_class, type_name, "resource")
    return resource_class


def _requested_identity(request: pb.ImportResourceState.Request, identity_schema: Any) -> Any:
    """The identity Terraform sent, when the resource declares a schema to read it with."""
    if identity_schema is None:
        return None
    return unmarshal_identity(request.identity, identity_schema)


def _build_imported_resource(
    resource_class: Any,
    resource_schema: Any,
    identity_schema: Any,
    imported: Any,
    imported_private: Any,
    raw_state_dict: dict[str, Any],
    type_name: str,
) -> pb.ImportResourceState.ImportedResource:
    """Marshal an adopted object into the ImportedResource Terraform writes to state."""
    validator_type = resource_schema.block.to_cty_type()
    state_cty = validator_type.validate(raw_state_dict)
    marshalled = marshal(state_cty, schema=resource_schema.block)

    imported_resource = pb.ImportResourceState.ImportedResource(type_name=type_name)
    imported_resource.state.msgpack = marshalled.msgpack
    imported_resource.private = (
        encrypt(msgpack.packb(attrs.asdict(imported_private), use_bin_type=True))
        if imported_private is not None
        else b""
    )

    # Terraform reads ImportedResource.identity and writes it to state, so a
    # resource that declares an identity schema and is then imported without
    # this arrives in state with an empty identity -- and every later plan
    # sees a change it cannot explain.
    if identity_schema is not None:
        identity_values = derive_identity_values(resource_class, imported, type_name, "import_resource_state")
        if identity_values is not None:
            imported_resource.identity.CopyFrom(marshal_identity(identity_values, identity_schema))

    return imported_resource


async def _import_resource_state_impl(
    request: pb.ImportResourceState.Request, context: Any
) -> pb.ImportResourceState.Response:
    """Adopt an object that already exists into Terraform state.

    A resource participates by implementing `import_state(ctx, id) -> state | None`,
    or `-> (state, private_state) | None` when it keeps private state; the framework
    marshals whatever it returns through the resource schema.

    `read()` is deliberately not used as a fallback: read is given prior state,
    while import is given an ID STRING and must locate the object from that alone.
    A resource whose identity is more than its id — a workspace plus a name, say —
    can only answer the second question deliberately.

    Identity needs no hook of its own. `ImportResourceState.Request` carries both
    `id` and `identity`, and Terraform sends whichever the practitioner wrote, so
    this is one operation with two input forms rather than two operations — a
    separate `import_by_identity` would let a resource implement one and silently
    return no identity from the other. So the identity arrives on `ctx.identity`,
    exactly as it does for read, plan and apply, and the answer is derived from
    the returned state by the same `get_identity()` those three use. A resource
    gains all of it by declaring `get_identity_schema()` and nothing else.
    """
    response = pb.ImportResourceState.Response()

    logger.debug(
        "ImportResourceState handler called",
        operation="import_resource_state",
        resource_type=request.type_name,
        import_id=request.id,
    )

    try:
        resource_class = _registered_resource(request.type_name)

        resource_schema = resource_class.get_schema()
        identity_schema = resolve_identity_schema(resource_class)
        resource_handler = resource_class()
        import_state = getattr(resource_handler, "import_state", None)
        if import_state is None:
            # A resource that cannot be imported is a normal thing to be, so this
            # reports the resource rather than the framework.
            logger.info(
                "Resource does not implement import_state",
                operation="import_resource_state",
                resource_type=request.type_name,
            )
            response.diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary=f"{request.type_name} does not support import",
                    detail=(
                        f"The resource type '{request.type_name}' does not implement "
                        f"`import_state`, so an existing object cannot be adopted into state.\n\n"
                        f"Suggestion: implement `async def import_state(self, ctx, import_id)` on the "
                        f"resource, returning its state object — or declare the resource in "
                        f"configuration and apply it instead."
                    ),
                )
            )
            return response

        provider_instance = hub.get_component("singleton", "provider")
        provider_context = hub.get_component("singleton", "provider_context")
        test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)
        resource_context: ResourceContext = ResourceContext(
            config=None,
            state=None,
            capabilities=provider_instance.metadata.capabilities if provider_instance else {},  # type: ignore[arg-type]
            test_mode_enabled=test_mode_enabled,
            identity=_requested_identity(request, identity_schema),
        )

        imported = await import_state(resource_context, request.id)

        # A resource that keeps private state may return it alongside the state,
        # the same (state, private_state) shape the plan and apply hooks use.
        # Terraform hands ImportedResource.private straight back as
        # ReadResourceRequest.Private, and read_resource.py gates on it being
        # non-empty -- so without this, the first refresh after an import sees no
        # private state at all and the resource cannot tell that apart from
        # never having had any.
        imported_private = None
        if isinstance(imported, tuple):
            imported, imported_private = imported

        if imported is None:
            # "Not found" and "cannot import" are different answers; Terraform has a
            # specific message for the first, and conflating them misdirects the reader.
            response.diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Cannot import non-existent remote object",
                    detail=(
                        f"No {request.type_name} was found for id {request.id!r}. Only objects that "
                        f"already exist can be imported; check the id, or use `tofu apply` to create it."
                    ),
                )
            )
            return response

        raw_state_dict = attrs_to_dict_for_cty(imported)
        response.imported_resources.append(
            _build_imported_resource(
                resource_class,
                resource_schema,
                identity_schema,
                imported,
                imported_private,
                raw_state_dict,
                request.type_name,
            )
        )

        logger.info(
            "Resource imported successfully",
            operation="import_resource_state",
            resource_type=request.type_name,
            import_id=request.id,
            state_fields=list(raw_state_dict.keys()),
        )
        return response

    except Deferral as e:
        logger.info(
            "Response deferred",
            operation="import_resource_state",
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
        return response
    except Exception as e:
        logger.error(
            "Resource import failed",
            operation="import_resource_state",
            resource_type=request.type_name,
            import_id=request.id,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        response.diagnostics.append(await create_diagnostic_from_exception(e))
        return response
