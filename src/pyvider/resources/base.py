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
                if converted_value is not None:
                    kwargs[name] = converted_value

        try:
            return target_cls(**kwargs)
        except TypeError as e:
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

        base_plan = (
            cty_to_native(ctx.planned_state_cty)
            if ctx.planned_state_cty and not ctx.planned_state_cty.is_null
            else {}
        )

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
