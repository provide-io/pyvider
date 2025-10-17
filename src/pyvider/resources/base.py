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
                f"Cannot construct attrs class '{target_cls.__name__}' from non-dict type '{type(data).__name__}'"
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
                    f"Cannot create '{target_cls.__name__}' instance - unknown/computed values present",
                    error=str(e)
                )
                return None
            # Re-raise other TypeErrors as they indicate real problems
            raise TypeError(f"Could not create '{target_cls.__name__}' from data: {e}") from e

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
            logger.debug("_cty_to_dict_preserving_unknown: cty_value is None or null")
            return {}

        if not isinstance(cty_value.type, CtyObject):
            logger.debug(f"_cty_to_dict_preserving_unknown: cty_value type is not CtyObject: {type(cty_value.type)}")
            return cty_to_native(cty_value) if cty_value else {}

        result = {}
        for key, value_cty in cty_value.value.items():
            if isinstance(value_cty, CtyValue):
                # Preserve unknown values as CtyValue objects
                if value_cty.is_unknown:
                    result[key] = value_cty
                    logger.debug(f"_cty_to_dict_preserving_unknown: preserving unknown value for key '{key}'")
                else:
                    result[key] = cty_to_native(value_cty)
                    logger.debug(f"_cty_to_dict_preserving_unknown: converted known value for key '{key}' to {result[key]}")
            else:
                result[key] = value_cty
                logger.debug(f"_cty_to_dict_preserving_unknown: non-CtyValue for key '{key}': {value_cty}")

        logger.debug(f"_cty_to_dict_preserving_unknown: returning dict with keys: {list(result.keys())}")
        return result

    async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)
        logger.debug("BaseResource.plan() base_plan from planned_state_cty", keys=list(base_plan.keys()))

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods

        # DEBUG: Check conditions before if statement
        cond1 = ctx.config_cty is not None and ctx.config_cty
        cond2 = isinstance(ctx.config_cty, CtyValue) if ctx.config_cty else False
        cond3 = hasattr(ctx.config_cty, "value") if ctx.config_cty else False
        logger.warning("BaseResource.plan() PRE-IF-CHECK", cond1=cond1, cond2=cond2, cond3=cond3,
                    combined=cond1 and cond2 and cond3)

        if ctx.config_cty and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
            cty_value_dict = ctx.config_cty.value
            logger.debug("BaseResource.plan() inside if block", value_type=type(cty_value_dict).__name__)
            if isinstance(cty_value_dict, dict):
                logger.debug("BaseResource.plan() merging fields", num_fields=len(cty_value_dict))
                for key, value in cty_value_dict.items():
                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key not in base_plan:
                        # Convert known CtyValues to native Python values
                        # Unknown CtyValues are preserved as-is for the handler to detect
                        if isinstance(value, CtyValue) and not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value
            else:
                logger.warning("BaseResource.plan() config_cty.value is not a dict",
                             value_type=type(cty_value_dict).__name__)
        else:
            logger.warning("BaseResource.plan() NOT merging config",
                         config_cty_is_none=ctx.config_cty is None,
                         config_cty_repr=repr(ctx.config_cty),
                         config_cty_type=type(ctx.config_cty).__name__,
                         is_ctyvalue=isinstance(ctx.config_cty, CtyValue),
                         has_value_attr=hasattr(ctx.config_cty, "value"))

        logger.debug("BaseResource.plan() final base_plan", keys=list(base_plan.keys()))

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def apply(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

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
