#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Generic, TypeVar, Union, cast, get_args, get_origin

import attrs
from provide.foundation import logger

from pyvider.cty import (
    CtyDynamic,
    CtyList,
    CtyObject,
    CtySet,
    CtyTuple,
    CtyValue,
)
from pyvider.cty.conversion import cty_to_native
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema

ResourceType = TypeVar("ResourceType")
StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")
PrivateStateType = TypeVar("PrivateStateType", bound=PrivateState)

_UNREFINED_UNKNOWN_SENTINEL = CtyValue.unknown(CtyDynamic()).value


class BaseResource(ABC, Generic[ResourceType, StateType, ConfigType]):
    """Base class for Terraform-managed resources.

    Subclasses declare three class attributes that describe the resource's
    data model:

        config_class:        the user-supplied configuration block
        state_class:         the persisted state shape
        private_state_class: optional opaque state kept between apply runs

    **Important: these classes must be `attrs` classes** (decorated with
    ``@attrs.define`` / ``@attrs.frozen``). The framework introspects them
    via ``attrs.fields()`` during every cty ↔ Python conversion; plain
    ``dataclasses``, ``pydantic`` models, or bare ``class`` definitions
    will silently round-trip to empty objects or fail with confusing
    ``TypeError``s deep in the conversion layer.

    The validator at ``cty_to_attrs_instance`` raises
    ``FrameworkConfigurationError`` up front when a non-attrs class is
    supplied, so misuse fails fast rather than corrupting state.
    """

    config_class: type[ConfigType] | None = None
    state_class: type[StateType] | None = None
    private_state_class: type[PrivateState] | None = None

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema: ...

    @classmethod
    def get_identity_schema(cls) -> PvsSchema | None:
        """Opt in to resource identity.

        Returning None means this resource has no identity, which is the
        default. Terraform treats identity as optional for managed resources;
        it is only mandatory for list resources.
        """
        return None

    @classmethod
    def get_identity(cls, state: Any) -> dict[str, Any] | None:
        """Derive identity values from state by attribute name.

        Identity attributes are almost always a subset of state, so this
        default means a resource gains identity by declaring
        get_identity_schema() and nothing else. Override when identity is not
        derivable from state.

        Returns None when identity cannot be fully determined -- no schema, no
        state, or any attribute missing, null, or still unknown during plan.
        """
        schema = cls.get_identity_schema()
        if schema is None or state is None:
            return None

        values: dict[str, Any] = {}
        for name in schema.block.attributes:
            value = getattr(state, name, None)
            if value is None:
                return None
            if isinstance(value, CtyValue) and (value.is_unknown or value.is_null):
                return None
            values[name] = value

        return values

    async def generate_config(self, state: StateType | CtyValue | None) -> Any:
        """Turn existing state into a valid configuration for this resource.

        Terraform calls this when generating configuration for a resource it
        discovered rather than one the practitioner wrote, so the result has to
        be a value the resource's own config schema accepts -- computed-only
        attributes dropped, required ones present.

        Returning None means "use the state as it stands", which is both the
        default and the right answer whenever state is already a valid
        configuration. The framework then forwards the original wire bytes
        untouched instead of re-encoding them.
        """
        return None

    @classmethod
    async def upgrade_identity(cls, version: int, raw_identity: dict[str, Any]) -> dict[str, Any]:
        """Upgrade identity data written under an older identity version.

        Only called when the stored version differs from the schema's current
        version. The default passes data through unchanged.
        """
        return raw_identity

    @classmethod
    def from_cty(
        cls, cty_value: CtyValue | None, target_cls: type, *, apply_defaults: bool = False
    ) -> Any | None:
        """Decode a cty value into `target_cls`.

        `apply_defaults` decides what a *null* attribute means, and it exists
        because the two things this decodes disagree about that:

        - In a **configuration**, a null attribute is one the practitioner
          omitted. Pass True, and a field whose attrs class declares a default
          gets it, exactly as if the keyword had been left off the constructor.
        - In **state**, a null attribute is a recorded absence -- the provider
          stored null and meant it. Decoding it as a default would rewrite
          history, so the flag stays False and null decodes to None.

        This is the *class* default (`size: str = "small"` on the attrs class),
        which is a Python-level fallback and distinct from `PvsAttribute.default`
        in the schema. The schema default is resolved one layer earlier, into the
        cty value itself, by `unmarshal(..., apply_defaults=True)` -- so it never
        reaches here as a null at all. The two flags share a name because they
        answer the same question at their own layer, and every inbound
        configuration passes True to both.
        """
        if cty_value is None:
            return None
        return cls._cty_to_attrs_recursive(cty_value, target_cls, apply_defaults=apply_defaults)

    @classmethod
    def _handle_cty_value(
        cls, cty_value: CtyValue, target_cls: type, *, apply_defaults: bool = False
    ) -> Any | None:
        if cty_value.is_null:
            return None
        if cty_value.is_unknown and not isinstance(cty_value.type, CtyObject | CtyList | CtySet | CtyTuple):
            return None
        logger.trace(
            "Processing CtyValue in _handle_cty_value",
            operation="_handle_cty_value",
            is_unknown=cty_value.is_unknown,
            is_structural=isinstance(cty_value.type, CtyObject | CtyList | CtySet | CtyTuple),
            value_type=type(cty_value.value).__name__,
            target_cls=getattr(target_cls, "__name__", str(target_cls)),
        )
        return cls._cty_to_attrs_recursive(cty_value.value, target_cls, apply_defaults=apply_defaults)

    @classmethod
    def _handle_list_conversion(cls, data: list, target_cls: type, *, apply_defaults: bool = False) -> list:
        element_type = get_args(target_cls)[0] if get_args(target_cls) else Any
        return [
            cls._cty_to_attrs_recursive(item, element_type, apply_defaults=apply_defaults) for item in data
        ]

    @classmethod
    def _handle_dict_conversion(cls, data: dict, target_cls: type, *, apply_defaults: bool = False) -> dict:
        args = get_args(target_cls)
        value_type = args[1] if len(args) > 1 else Any
        return {
            k: cls._cty_to_attrs_recursive(v, value_type, apply_defaults=apply_defaults)
            for k, v in data.items()
        }

    @classmethod
    def _resolved_fields(cls, target_cls: type) -> tuple[Any, ...]:
        """attrs fields with their type annotations resolved to real types.

        Under `from __future__ import annotations` every annotation is a STRING, so
        `field.type` is `"list[str] | None"` rather than the type. `get_origin` of a
        string is None, so the converter cannot see a list and returns the raw
        CtyValue elements — a config whose `targets` is a list of CtyValue reads
        fine until something treats one as a str.

        `resolve_types` mutates the class, so the cost is paid once per class.

        ..note::
            ``attrs.resolve_types()`` resolves a class in ONE call, so it is
            all-or-nothing: a single annotation naming something unavailable at
            runtime (typically a name imported only under ``TYPE_CHECKING``) leaves
            *every* field on the class unresolved, including plain ones like
            ``list[str]``. There is no per-field recovery -- attrs offers no
            per-attribute resolution hook, and `Attribute` instances are frozen, so
            the failure is reported loudly with the names still unresolved rather
            than papered over.
        """
        try:
            attrs.resolve_types(target_cls)
        except Exception as e:
            unresolved = [f.name for f in attrs.fields(target_cls) if isinstance(f.type, str)]
            logger.warning(
                "Could not resolve type annotations; these fields stay wrapped in CtyValue",
                class_name=getattr(target_cls, "__name__", str(target_cls)),
                unresolved_fields=unresolved,
                error_type=type(e).__name__,
                error_message=str(e),
            )
        return cast(tuple[Any, ...], attrs.fields(target_cls))

    @classmethod
    def _is_null(cls, value: Any) -> bool:
        """True when a decoded attribute carries no value, as opposed to an unknown one."""
        if isinstance(value, CtyValue):
            return bool(value.is_null)
        return value is None

    @classmethod
    def _handle_attrs_conversion(
        cls, data: Any, target_cls: type, *, apply_defaults: bool = False
    ) -> Any | None:
        if not isinstance(data, dict):
            logger.warning(
                "Cannot construct attrs class from non-dict data type",
                operation="attrs_conversion",
                class_name=target_cls.__name__,
                received_type=type(data).__name__,
                expected_type="dict",
                suggestion="Ensure configuration data is structured as a dictionary/object",
            )
            return None

        kwargs = {}
        target_fields = {f.name: f for f in cls._resolved_fields(target_cls)}

        for name, field_def in target_fields.items():
            if name in data and field_def.init:
                raw_value = data[name]
                # In a configuration a null attribute is one the practitioner
                # omitted, and the protocol has no way to send a default -- so
                # passing None here would override the fallback the resource's
                # own attrs class declares. Leave the keyword out and let attrs
                # apply it.
                #
                # Only for a configuration: `apply_defaults` is False when this
                # decodes state, where a null is a recorded absence rather than
                # an omission. Unknown values are not null either way, so they
                # still come through as None and stay unknown.
                if apply_defaults and cls._is_null(raw_value) and field_def.default is not attrs.NOTHING:
                    continue
                converted_value = cls._cty_to_attrs_recursive(
                    raw_value, field_def.type, apply_defaults=apply_defaults
                )
                # Include the field even if converted_value is None
                # This handles unknown/computed values during validation/planning
                kwargs[name] = converted_value

        try:
            return target_cls(**kwargs)
        except TypeError as e:
            # If we can't create the instance due to missing required fields,
            # it's likely because some values are unknown/computed during planning.
            # Return None to signal "attrs instance not available - use is_field_unknown() instead"
            #
            # Resources should check ctx.is_field_unknown("field_name") to handle unknown values
            # explicitly rather than relying on ctx.config being None.
            if "missing" in str(e) and "required" in str(e):
                logger.debug(
                    "Cannot create attrs instance - unknown or computed values present",
                    class_name=target_cls.__name__,
                    error=str(e),
                    available_fields=list(kwargs.keys()),
                )
                return None
            # Re-raise other TypeErrors as they indicate real problems
            # Extract field information for better error messages
            provided_fields = list(kwargs.keys())
            required_fields = [f.name for f in attrs.fields(target_cls) if f.default == attrs.NOTHING]
            missing_fields = [f for f in required_fields if f not in provided_fields]

            logger.error(
                "Failed to create attrs instance from configuration data",
                class_name=target_cls.__name__,
                error=str(e),
                provided_fields=provided_fields,
                required_fields=required_fields,
                missing_fields=missing_fields,
            )

            raise TypeError(
                f"Could not create '{target_cls.__name__}' instance from configuration data. "
                f"Error: {e}\n\n"
                f"Suggestion: Ensure all required fields are provided with valid types. "
                f"Check the resource schema for required vs optional fields.\n"
                f"Required fields: {', '.join(required_fields) if required_fields else 'none'}\n"
                f"Missing fields: {', '.join(missing_fields) if missing_fields else 'none'}\n"
                f"Provided fields: {', '.join(provided_fields) if provided_fields else 'none'}"
            ) from e

    @classmethod
    def _cty_to_attrs_recursive(
        cls, data: Any, target_cls: type, *, apply_defaults: bool = False
    ) -> Any | None:
        if isinstance(data, CtyValue):
            return cls._handle_cty_value(data, target_cls, apply_defaults=apply_defaults)

        if data is None or data is _UNREFINED_UNKNOWN_SENTINEL:
            return None

        origin = get_origin(target_cls)
        if origin in (UnionType, Union):
            non_none_args = [arg for arg in get_args(target_cls) if arg is not type(None)]
            if len(non_none_args) == 1:
                target_cls = non_none_args[0]
                origin = get_origin(target_cls)

        if origin is list:
            return cls._handle_list_conversion(data, target_cls, apply_defaults=apply_defaults)

        if origin is dict:
            return cls._handle_dict_conversion(data, target_cls, apply_defaults=apply_defaults)

        if attrs.has(target_cls):
            return cls._handle_attrs_conversion(data, target_cls, apply_defaults=apply_defaults)

        return data

    @classmethod
    def _cty_to_native_preserving_unknown(cls, value: Any) -> Any:
        """Convert CTY recursively while retaining unknown values as CtyValue objects."""
        if not isinstance(value, CtyValue):
            return value
        if value.is_unknown:
            return value
        if value.is_null:
            return None
        if value.is_wholly_known():
            return cty_to_native(value)

        payload = value.value
        if isinstance(payload, dict):
            return {key: cls._cty_to_native_preserving_unknown(item) for key, item in payload.items()}
        if isinstance(payload, (list, tuple)):
            converted = [cls._cty_to_native_preserving_unknown(item) for item in payload]
            return tuple(converted) if isinstance(value.type, CtyTuple) else converted
        return cty_to_native(value)

    async def validate(self, config: ConfigType | None) -> list[str]:
        if config is None:
            return []
        return await self._validate_config(config)

    @abstractmethod
    async def _validate_config(self, config: ConfigType) -> list[str]: ...

    @classmethod
    def _cty_to_dict_preserving_unknown(cls, cty_value: CtyValue | None) -> dict[str, Any]:
        """Convert CTY value to dict, but preserve unknown CtyValue objects instead of converting to None."""
        if not cty_value or cty_value.is_null:
            logger.debug(
                "CTY value conversion skipped - value is None or null",
                operation="cty_to_dict_preserving_unknown",
                reason="null_or_none",
            )
            return {}

        if not isinstance(cty_value.type, CtyObject):
            logger.debug(
                "CTY value is not an object type, converting to native",
                operation="cty_to_dict_preserving_unknown",
                cty_type=type(cty_value.type).__name__,
            )
            return cty_to_native(cty_value) if cty_value else {}

        # Type guard: ensure value is a dict for object types
        if not isinstance(cty_value.value, dict):
            logger.warning(
                "Expected dict for CtyObject value",
                operation="cty_to_dict_preserving_unknown",
                actual_type=type(cty_value.value).__name__,
            )
            return {}
        result = {key: cls._cty_to_native_preserving_unknown(v) for key, v in cty_value.value.items()}

        logger.debug(
            "CTY to dict conversion completed",
            operation="cty_to_dict_preserving_unknown",
            total_fields=len(result),
            field_names=list(result.keys()),
        )
        return result

    def _merge_config_into_plan(self, base_plan: dict[str, Any], ctx: ResourceContext) -> None:
        """Merge config fields into base_plan, skipping nulls and converting known CtyValues."""
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        # Force write-only attributes to None (null in state)
        schema = self.get_schema()
        schema_attributes = getattr(schema.block, "attributes", {}) or {}
        write_only_attrs = {
            name for name, attr in schema_attributes.items() if getattr(attr, "write_only", False)
        }
        for attr_name in write_only_attrs:
            base_plan[attr_name] = None

        if (
            ctx.config_cty is not None
            and isinstance(ctx.config_cty, CtyValue)
            and hasattr(ctx.config_cty, "value")
        ):
            cty_value_dict = ctx.config_cty.value
            if isinstance(cty_value_dict, dict):
                for key, value in cty_value_dict.items():
                    # Skip write-only attributes entirely from config copy
                    if key in write_only_attrs:
                        continue

                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key not in base_plan or base_plan[key] is None:
                        # Skip null values - they're likely computed fields
                        if isinstance(value, CtyValue) and value.is_null:
                            continue
                        # Convert known CtyValues to native Python values
                        # Unknown CtyValues are preserved as-is for the handler to detect
                        if isinstance(value, CtyValue) and not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

    async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            logger.warning(
                "Resource configuration validation failed during planning",
                operation="plan",
                resource_type=self.__class__.__name__,
                error_count=len(validation_errors),
                errors=validation_errors,
            )
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None and ctx.planned_state is None

        logger.debug(
            "Resource plan operation started",
            operation="plan",
            resource_type=self.__class__.__name__,
            operation_type="delete" if is_delete else "create" if is_create else "update",
            has_state=ctx.state is not None,
            has_config=ctx.config is not None,
        )

        if is_delete:
            result = await self._delete_plan(ctx)
            logger.debug(
                "Resource delete plan completed",
                operation="plan_delete",
                resource_type=self.__class__.__name__,
            )
            return result

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        self._merge_config_into_plan(base_plan, ctx)

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(
                "Resource create plan completed",
                operation="plan_create",
                resource_type=self.__class__.__name__,
                has_private_state=private_state is not None,
                planned_fields=list(planned_state.keys()) if planned_state else [],
            )
            return planned_state, private_state
        planned_state, private_state = await self._update(ctx, base_plan)
        logger.debug(
            "Resource update plan completed",
            operation="plan_update",
            resource_type=self.__class__.__name__,
            has_private_state=private_state is not None,
            planned_fields=list(planned_state.keys()) if planned_state else [],
        )
        return planned_state, private_state

    async def apply(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        logger.debug(
            "Resource apply operation started",
            operation="apply",
            resource_type=self.__class__.__name__,
            operation_type="delete" if is_delete else "create" if is_create else "update",
        )

        if is_delete:
            await self._delete_apply(ctx)
            logger.info(
                "Resource deleted successfully",
                operation="apply_delete",
                resource_type=self.__class__.__name__,
            )
            return None, None

        if is_create:
            result = await self._create_apply(ctx)
            logger.info(
                "Resource created successfully",
                operation="apply_create",
                resource_type=self.__class__.__name__,
                has_private_state=result[1] is not None,
            )
            return result
        result = await self._update_apply(ctx)
        logger.info(
            "Resource updated successfully",
            operation="apply_update",
            resource_type=self.__class__.__name__,
            has_private_state=result[1] is not None,
        )
        return result

    @abstractmethod
    async def read(self, ctx: ResourceContext) -> StateType | None: ...

    # --- New CRUD Lifecycle Hooks ---
    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        return base_plan, None

    async def _update(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        return base_plan, None

    async def _delete_plan(
        self, ctx: ResourceContext
    ) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        return None, None

    async def _create_apply(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        return ctx.planned_state, ctx.private_state

    async def _update_apply(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        return ctx.planned_state, ctx.private_state

    @abstractmethod
    async def _delete_apply(self, ctx: ResourceContext) -> None: ...


# 🐍🏗️🔚
