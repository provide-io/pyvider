#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Generic, TypeVar, get_args, get_origin

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
    config_class: type[ConfigType] | None = None
    state_class: type[StateType] | None = None
    private_state_class: type[PrivateStateType] | None = None

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema: ...

    @classmethod
    def from_cty(cls, cty_value: CtyValue | None, target_cls: type) -> Any | None:
        if cty_value is None:
            return None
        return cls._cty_to_attrs_recursive(cty_value, target_cls)

    @classmethod
    def _handle_cty_value(cls, cty_value: CtyValue, target_cls: type) -> Any | None:
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
        return cls._cty_to_attrs_recursive(cty_value.value, target_cls)

    @classmethod
    def _handle_list_conversion(cls, data: list, target_cls: type) -> list:
        element_type = get_args(target_cls)[0] if get_args(target_cls) else Any
        return [cls._cty_to_attrs_recursive(item, element_type) for item in data]

    @classmethod
    def _handle_dict_conversion(cls, data: dict, target_cls: type) -> dict:
        args = get_args(target_cls)
        value_type = args[1] if len(args) > 1 else Any
        return {k: cls._cty_to_attrs_recursive(v, value_type) for k, v in data.items()}

    @classmethod
    def _handle_attrs_conversion(cls, data: Any, target_cls: type) -> Any | None:
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
        target_fields = {f.name: f for f in attrs.fields(target_cls)}

        for name, field_def in target_fields.items():
            if name in data and field_def.init:
                raw_value = data[name]
                converted_value = cls._cty_to_attrs_recursive(raw_value, field_def.type)
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
    def _cty_to_attrs_recursive(cls, data: Any, target_cls: type) -> Any | None:
        if isinstance(data, CtyValue):
            return cls._handle_cty_value(data, target_cls)

        if data is None or data is _UNREFINED_UNKNOWN_SENTINEL:
            return None

        origin = get_origin(target_cls)
        is_union = origin is UnionType
        try:
            from typing import Union

            is_union = is_union or origin is Union
        except ImportError:
            pass

        if is_union:
            non_none_args = [arg for arg in get_args(target_cls) if arg is not type(None)]
            if len(non_none_args) == 1:
                target_cls = non_none_args[0]
                origin = get_origin(target_cls)

        if origin in (list, list):
            return cls._handle_list_conversion(data, target_cls)

        if origin in (dict, dict):
            return cls._handle_dict_conversion(data, target_cls)

        if attrs.has(target_cls):
            return cls._handle_attrs_conversion(data, target_cls)

        if isinstance(data, CtyValue):
            return cty_to_native(data)
        return data

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

        result = {}
        unknown_count = 0
        for key, value_cty in cty_value.value.items():
            if isinstance(value_cty, CtyValue):
                # Preserve unknown values as CtyValue objects
                if value_cty.is_unknown:
                    result[key] = value_cty
                    unknown_count += 1
                    logger.debug(
                        "Preserving unknown CTY value in conversion",
                        operation="cty_to_dict_preserving_unknown",
                        field_name=key,
                        reason="value_is_unknown",
                    )
                else:
                    result[key] = cty_to_native(value_cty)
                    logger.debug(
                        "Converted known CTY value to native type",
                        operation="cty_to_dict_preserving_unknown",
                        field_name=key,
                        converted_value=str(result[key])[:100],  # Truncate for safety
                    )
            else:
                result[key] = value_cty
                logger.debug(
                    "Non-CTY value passed through unchanged",
                    operation="cty_to_dict_preserving_unknown",
                    field_name=key,
                )

        logger.debug(
            "CTY to dict conversion completed",
            operation="cty_to_dict_preserving_unknown",
            total_fields=len(result),
            unknown_fields=unknown_count,
            field_names=list(result.keys()),
        )
        return result

    def _merge_config_into_plan(self, base_plan: dict[str, Any], ctx: ResourceContext) -> None:
        """Merge config fields into base_plan, skipping nulls and converting known CtyValues."""
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if (
            ctx.config_cty is not None
            and isinstance(ctx.config_cty, CtyValue)
            and hasattr(ctx.config_cty, "value")
        ):
            cty_value_dict = ctx.config_cty.value
            if isinstance(cty_value_dict, dict):
                for key, value in cty_value_dict.items():
                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key not in base_plan:
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
        else:
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
        else:
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
