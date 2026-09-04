#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtySet,
    CtyString,
    CtyTuple,
    CtyType,
    CtyValue,
)
from pyvider.schema.types import NestingMode, PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema

#: Member flags that only reach Terraform through a `nested_type`, and so cannot
#: survive being used as a collection's element type.
_FLAGS_NEEDING_NESTED_TYPE = ("computed", "sensitive", "write_only")


def _reject_lost_member_flags(type_def: PvsAttribute) -> None:
    """Refuse an object element whose members declare flags that cannot be sent.

    `a_obj` reaches Terraform as a `nested_type`, which is what carries a
    member's `computed`, `sensitive`, `write_only` and default. Inside `a_list`,
    `a_set` or `a_map` only the cty type survives, because this framework does
    not yet emit LIST, SET or MAP nested types and tfprotov6 has no other way to
    express per-member flags on a collection element
    (tfprotov6/schema.go:58-81 models the nesting this would need).

    Accepting them and dropping them silently is worse than refusing: a
    `computed=True` member looks declared, Terraform is never told, and a
    provider that fills the value in during apply is told "planned value for a
    non-computed attribute" with nothing pointing back at the schema.
    """
    object_type = type_def.object_type
    if object_type is None:
        return

    offenders: list[str] = []
    for name, member in object_type.attributes.items():
        flags = [flag for flag in _FLAGS_NEEDING_NESTED_TYPE if getattr(member, flag, False)]
        if member.default is not None:
            flags.append("default")
        offenders.extend(f"{name}.{flag}" for flag in flags)

    if not offenders:
        return

    raise ValueError(
        f"Invalid schema attribute: a collection of objects cannot carry per-member "
        f"flags ({', '.join(offenders)}).\n\n"
        f"An a_obj() attribute is sent to Terraform as a nested type, which is what "
        f"carries a member's computed, sensitive, write_only and default. Inside "
        f"a_list(), a_set() or a_map() only the object's type is sent, so those flags "
        f"would be silently dropped and Terraform would never know about them.\n\n"
        f"Suggestion: declare the collection as a nested block instead -- b_list(), "
        f"b_set() or b_map() -- which carries the flags per attribute; or drop the "
        f"flags if the members really are plain values."
    )


def _get_cty_type(type_def: Any) -> CtyType:
    """Gets the CtyType from a PvsAttribute or a raw CtyType."""
    if isinstance(type_def, PvsAttribute):
        _reject_lost_member_flags(type_def)
        return type_def.type
    if isinstance(type_def, CtyType):
        return type_def
    raise TypeError(f"Invalid type definition for attribute element: got {type(type_def).__name__}")


# --- Attribute Factories (a_*) ---
def a_str(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyString(), description=description, **kwargs)


def a_num(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyNumber(), description=description, **kwargs)


def a_bool(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyBool(), description=description, **kwargs)


def a_dyn(description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(type=CtyDynamic(), description=description, **kwargs)


def a_list(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyList(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_map(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyMap(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_set(element_type_def: Any, description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtySet(element_type=_get_cty_type(element_type_def)),
        description=description,
        **kwargs,
    )


def a_tuple(element_type_defs: list[Any], description: str = "", **kwargs: Any) -> PvsAttribute:
    return PvsAttribute(
        type=CtyTuple(element_types=tuple(_get_cty_type(v) for v in element_type_defs)),
        description=description,
        **kwargs,
    )


def a_obj(attributes: dict[str, PvsAttribute], description: str = "", **kwargs: Any) -> PvsAttribute:
    obj_type_def = PvsObjectType(attributes=attributes, description=description)
    return PvsAttribute(
        type=obj_type_def.to_cty_type(),
        object_type=obj_type_def,
        description=description,
        **kwargs,
    )


# --- Block Factories (b_*) ---
def b_main(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    **kwargs: Any,
) -> PvsObjectType:
    final_attrs = {}
    if attributes:
        for name, attr in attributes.items():
            final_attrs[name] = attrs.evolve(attr, name=name)
    return PvsObjectType(
        attributes=final_attrs,
        block_types=tuple(block_types) if block_types else (),
        **kwargs,
    )


def _nested_block_factory(type_name: str, nesting: NestingMode, **kwargs: Any) -> PvsNestedBlock:
    attributes = kwargs.pop("attributes", {})
    block_types = kwargs.pop("block_types", None)
    block_content = b_main(
        attributes=attributes,
        block_types=block_types,
        description=kwargs.get("description", ""),
    )
    return PvsNestedBlock(type_name=type_name, nesting=nesting, block=block_content, **kwargs)


def b_list(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.LIST, **kwargs)


def b_set(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SET, **kwargs)


def b_map(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.MAP, **kwargs)


def b_single(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.SINGLE, **kwargs)


def b_group(type_name: str, **kwargs: Any) -> PvsNestedBlock:
    return _nested_block_factory(type_name, NestingMode.GROUP, **kwargs)


# --- Schema Factories (s_*) ---
def _reject_name_collisions(
    attributes: dict[str, PvsAttribute] | None,
    block_types: list[PvsNestedBlock] | None,
) -> None:
    """An attribute and a block cannot share a name.

    Terraform rejects the whole provider at init over it
    (configschema/internal_validate.go:56): the configuration language has no
    way to tell which of the two `auth = ...` or `auth { ... }` means.
    """
    if not attributes or not block_types:
        return

    block_names = {nested.type_name for nested in block_types}
    shared = sorted(set(attributes) & block_names)
    if shared:
        names = ", ".join(repr(name) for name in shared)
        raise ValueError(
            f"Invalid schema configuration: {names} is declared both as an attribute "
            f"and as a nested block.\n\n"
            f"Terraform rejects a provider whose schema does this, because a "
            f"configuration cannot say which one it means.\n\n"
            f"Suggestion: rename one of them."
        )


def _reject_write_only(
    attributes: dict[str, PvsAttribute] | None,
    block_types: list[PvsNestedBlock] | None,
    *,
    schema_kind: str,
) -> None:
    """Write-only belongs to managed resources only.

    terraform-plugin-sdk rejects it on provider and data source schemas
    (helper/schema/provider.go:202,208,242), and Terraform's own write-only
    checks only ever run against managed resources -- so the flag would be
    advertised, never enforced, and the value stored in plain text.
    """
    offenders = sorted(name for name, attr in (attributes or {}).items() if attr.write_only)
    for nested in block_types or []:
        offenders.extend(
            f"{nested.type_name}.{name}" for name, attr in nested.block.attributes.items() if attr.write_only
        )

    if offenders:
        names = ", ".join(repr(name) for name in offenders)
        raise ValueError(
            f"Invalid {schema_kind} schema: write_only cannot be set on {names}.\n\n"
            f"Write-only is a managed-resource concept: Terraform's checks that the "
            f"value is never persisted only run against managed resources, so on a "
            f"{schema_kind} the flag would be advertised and never enforced.\n\n"
            f"Suggestion: drop write_only, or mark the attribute sensitive if the "
            f"intent is to keep it out of logs and plan output."
        )


def _create_schema(
    version: int,
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    _reject_name_collisions(attributes, block_types)
    block = b_main(attributes=attributes, block_types=block_types)
    return PvsSchema(version=version, block=block)


def s_resource(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
    version: int = 1,
) -> PvsSchema:
    """Create a managed resource schema.

    Bump `version` whenever a change to this schema makes state written under
    the old one unreadable -- an attribute renamed, a type changed, one
    attribute split into two -- and implement `upgrade_state` on the resource to
    perform the migration. Terraform records the version in state alongside the
    instance and calls `UpgradeResourceState` when it differs from the one the
    provider now advertises; without a bump it has no signal that anything
    changed and hands the old state to the new schema.

    The default of 1 is load-bearing rather than arbitrary. Every pyvider
    resource has advertised 1 since the framework began, so that is what is
    recorded in the state of every provider built on it. Defaulting to anything
    else would make existing state disagree with the schema on the next plan --
    and defaulting to 0 would make it a *downgrade*, which Terraform refuses
    outright rather than upgrading.
    """
    return _create_schema(version, attributes=attributes, block_types=block_types)


def s_data_source(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    _reject_write_only(attributes, block_types, schema_kind="data source")
    return _create_schema(1, attributes=attributes, block_types=block_types)


def s_provider(
    attributes: dict[str, PvsAttribute] | None = None,
    block_types: list[PvsNestedBlock] | None = None,
) -> PvsSchema:
    _reject_write_only(attributes, block_types, schema_kind="provider")
    return _create_schema(1, attributes=attributes, block_types=block_types)


def s_identity(
    attributes: dict[str, PvsAttribute] | None = None,
    version: int = 0,
) -> PvsSchema:
    """Create a resource identity schema.

    Identity reuses PvsSchema and PvsAttribute rather than parallel types.
    `required` on an attribute becomes `required_for_import` on the wire and
    `optional` becomes `optional_for_import` -- the same collapse Terraform
    core performs in ProtoToIdentitySchema.

    Identity versions start at 0 and increment by 1 on each change. The default
    of 0 is load-bearing, not cosmetic: Terraform records
    `IdentitySchemaVersion` in state and it is 0 for every instance written
    before the resource declared identity
    (`internal/states/instance_object_src.go`). A resource adopting identity at
    version 0 therefore matches what is already in state and never triggers
    `UpgradeResourceIdentity`; adopting at version 1 would fire the upgrade RPC
    for every pre-existing instance with an *empty* stored identity. The
    protocol states the same rule directly -- identity "versioning implicitly
    starts at 0 and by convention should be incremented by 1 each change"
    (`docs/plugin-protocol/tfplugin6.proto`, `ResourceIdentitySchema.version`).

    Identity attributes must be flat scalars and must not set computed or
    sensitive; both are enforced in pvs_identity_schema_to_proto.
    """
    return _create_schema(version, attributes=attributes)


def s_function(
    parameters: list[PvsAttribute] | None = None,
    return_type: PvsAttribute | None = None,
    variadic_parameter: PvsAttribute | None = None,
) -> PvsSchema:
    """
    Create a schema for a Terraform function.

    Args:
        parameters: List of function parameters (created with a_str(), a_num(), etc.)
        return_type: The function's return type (created with a_str(), a_num(), etc.)
        variadic_parameter: Optional variadic parameter for functions that accept variable arguments

    Returns:
        PvsSchema: A schema representing the function signature

    Example:
        >>> schema = s_function(
        ...     parameters=[
        ...         a_str(description="Input string"),
        ...         a_num(description="Multiplier"),
        ...     ],
        ...     return_type=a_str(description="Processed result"),
        ... )
    """
    # Build attributes dict to store function metadata
    # We use a special structure where parameters are stored as numbered attributes
    attributes: dict[str, PvsAttribute] = {}

    # Store parameters as param_0, param_1, etc.
    if parameters:
        for idx, param in enumerate(parameters):
            attributes[f"param_{idx}"] = param

    # Store return type as special attribute
    if return_type:
        attributes["return_type"] = return_type

    # Store variadic parameter if provided
    if variadic_parameter:
        attributes["variadic_param"] = variadic_parameter

    return _create_schema(1, attributes=attributes, block_types=None)


# --- Special Value Factories ---


def a_unknown(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates an unknown CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_unknown() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.unknown(target_type)


def a_null(schema_builder: PvsAttribute | PvsSchema) -> CtyValue:
    """Creates a null CtyValue for a given schema attribute or object."""
    target_type: CtyType | None = None
    if isinstance(schema_builder, PvsAttribute):
        target_type = schema_builder.type
    elif isinstance(schema_builder, PvsSchema):
        target_type = schema_builder.block.to_cty_type()

    if target_type is None:
        raise TypeError("a_null() expects a schema builder instance like a_str() or s_resource()")
    return CtyValue.null(target_type)


# 🐍🏗️🔚
