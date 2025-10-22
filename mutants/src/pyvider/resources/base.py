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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    async def xǁBaseResourceǁvalidate__mutmut_orig(self, config: ConfigType | None) -> list[str]:
        if config is None:
            return []
        return await self._validate_config(config)

    async def xǁBaseResourceǁvalidate__mutmut_1(self, config: ConfigType | None) -> list[str]:
        if config is not None:
            return []
        return await self._validate_config(config)

    async def xǁBaseResourceǁvalidate__mutmut_2(self, config: ConfigType | None) -> list[str]:
        if config is None:
            return []
        return await self._validate_config(None)
    
    xǁBaseResourceǁvalidate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseResourceǁvalidate__mutmut_1': xǁBaseResourceǁvalidate__mutmut_1, 
        'xǁBaseResourceǁvalidate__mutmut_2': xǁBaseResourceǁvalidate__mutmut_2
    }
    
    def validate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseResourceǁvalidate__mutmut_orig"), object.__getattribute__(self, "xǁBaseResourceǁvalidate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate.__signature__ = _mutmut_signature(xǁBaseResourceǁvalidate__mutmut_orig)
    xǁBaseResourceǁvalidate__mutmut_orig.__name__ = 'xǁBaseResourceǁvalidate'

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

    async def xǁBaseResourceǁplan__mutmut_orig(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_1(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = None
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_2(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(None)
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_3(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(None)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_4(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = None
        is_delete = ctx.config is None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_5(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is not None
        is_delete = ctx.config is None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_6(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_7(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None or ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_8(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is not None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_9(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None and ctx.planned_state is not None

        if is_delete:
            return await self._delete_plan(ctx)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_10(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
        validation_errors = await self.validate(ctx.config)
        if validation_errors:
            for err in validation_errors:
                ctx.add_error(err)
            return None, None

        is_create = ctx.state is None
        is_delete = ctx.config is None and ctx.planned_state is None

        if is_delete:
            return await self._delete_plan(None)

        # Create base_plan from planned_state_cty, preserving unknown values
        base_plan = self._cty_to_dict_preserving_unknown(ctx.planned_state_cty)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_11(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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
        base_plan = None

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_12(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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
        base_plan = self._cty_to_dict_preserving_unknown(None)

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_13(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) or hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_14(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None or isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_15(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_16(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(None, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_17(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, None):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_18(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr("value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_19(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, ):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_20(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "XXvalueXX"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_21(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "VALUE"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_22(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
            cty_value_dict = None
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_23(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
            cty_value_dict = ctx.config_cty.value
            if isinstance(cty_value_dict, dict):
                for key, value in cty_value_dict.items():
                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key in base_plan:
                        # Skip null values - they're likely computed fields
                        if isinstance(value, CtyValue) and value.is_null:
                            continue
                        # Convert known CtyValues to native Python values
                        # Unknown CtyValues are preserved as-is for the handler to detect
                        if isinstance(value, CtyValue) and not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_24(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
            cty_value_dict = ctx.config_cty.value
            if isinstance(cty_value_dict, dict):
                for key, value in cty_value_dict.items():
                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key not in base_plan:
                        # Skip null values - they're likely computed fields
                        if isinstance(value, CtyValue) or value.is_null:
                            continue
                        # Convert known CtyValues to native Python values
                        # Unknown CtyValues are preserved as-is for the handler to detect
                        if isinstance(value, CtyValue) and not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_25(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
            cty_value_dict = ctx.config_cty.value
            if isinstance(cty_value_dict, dict):
                for key, value in cty_value_dict.items():
                    # Only add if not already in base_plan (planned_state takes precedence)
                    if key not in base_plan:
                        # Skip null values - they're likely computed fields
                        if isinstance(value, CtyValue) and value.is_null:
                            break
                        # Convert known CtyValues to native Python values
                        # Unknown CtyValues are preserved as-is for the handler to detect
                        if isinstance(value, CtyValue) and not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_26(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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
                        if isinstance(value, CtyValue) or not value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_27(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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
                        if isinstance(value, CtyValue) and value.is_unknown:
                            base_plan[key] = cty_to_native(value)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_28(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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
                            base_plan[key] = None
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_29(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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
                            base_plan[key] = cty_to_native(None)
                        else:
                            base_plan[key] = value

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_30(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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
                            base_plan[key] = None

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_31(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = None
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_32(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(None, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_33(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, None)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_34(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_35(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, )
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_36(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(None)
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_37(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = None
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_38(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(None, base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_39(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, None)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_40(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(base_plan)
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_41(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, )
            logger.debug(f"Plan _update returned private_state: {private_state}")
            return planned_state, private_state

    async def xǁBaseResourceǁplan__mutmut_42(self, ctx: ResourceContext) -> tuple[dict[str, Any] | None, PrivateStateType | None]:
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

        # Merge in config fields - base_plan starts with all config values
        # Resources then add/modify computed fields in their _create()/_update() methods
        # NOTE: Don't use truthiness check on CtyValue - unknown values are falsy!
        # Use explicit 'is not None' instead
        if ctx.config_cty is not None and isinstance(ctx.config_cty, CtyValue) and hasattr(ctx.config_cty, "value"):
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

        if is_create:
            planned_state, private_state = await self._create(ctx, base_plan)
            logger.debug(f"Plan _create returned private_state: {private_state}")
            return planned_state, private_state
        else:
            planned_state, private_state = await self._update(ctx, base_plan)
            logger.debug(None)
            return planned_state, private_state
    
    xǁBaseResourceǁplan__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseResourceǁplan__mutmut_1': xǁBaseResourceǁplan__mutmut_1, 
        'xǁBaseResourceǁplan__mutmut_2': xǁBaseResourceǁplan__mutmut_2, 
        'xǁBaseResourceǁplan__mutmut_3': xǁBaseResourceǁplan__mutmut_3, 
        'xǁBaseResourceǁplan__mutmut_4': xǁBaseResourceǁplan__mutmut_4, 
        'xǁBaseResourceǁplan__mutmut_5': xǁBaseResourceǁplan__mutmut_5, 
        'xǁBaseResourceǁplan__mutmut_6': xǁBaseResourceǁplan__mutmut_6, 
        'xǁBaseResourceǁplan__mutmut_7': xǁBaseResourceǁplan__mutmut_7, 
        'xǁBaseResourceǁplan__mutmut_8': xǁBaseResourceǁplan__mutmut_8, 
        'xǁBaseResourceǁplan__mutmut_9': xǁBaseResourceǁplan__mutmut_9, 
        'xǁBaseResourceǁplan__mutmut_10': xǁBaseResourceǁplan__mutmut_10, 
        'xǁBaseResourceǁplan__mutmut_11': xǁBaseResourceǁplan__mutmut_11, 
        'xǁBaseResourceǁplan__mutmut_12': xǁBaseResourceǁplan__mutmut_12, 
        'xǁBaseResourceǁplan__mutmut_13': xǁBaseResourceǁplan__mutmut_13, 
        'xǁBaseResourceǁplan__mutmut_14': xǁBaseResourceǁplan__mutmut_14, 
        'xǁBaseResourceǁplan__mutmut_15': xǁBaseResourceǁplan__mutmut_15, 
        'xǁBaseResourceǁplan__mutmut_16': xǁBaseResourceǁplan__mutmut_16, 
        'xǁBaseResourceǁplan__mutmut_17': xǁBaseResourceǁplan__mutmut_17, 
        'xǁBaseResourceǁplan__mutmut_18': xǁBaseResourceǁplan__mutmut_18, 
        'xǁBaseResourceǁplan__mutmut_19': xǁBaseResourceǁplan__mutmut_19, 
        'xǁBaseResourceǁplan__mutmut_20': xǁBaseResourceǁplan__mutmut_20, 
        'xǁBaseResourceǁplan__mutmut_21': xǁBaseResourceǁplan__mutmut_21, 
        'xǁBaseResourceǁplan__mutmut_22': xǁBaseResourceǁplan__mutmut_22, 
        'xǁBaseResourceǁplan__mutmut_23': xǁBaseResourceǁplan__mutmut_23, 
        'xǁBaseResourceǁplan__mutmut_24': xǁBaseResourceǁplan__mutmut_24, 
        'xǁBaseResourceǁplan__mutmut_25': xǁBaseResourceǁplan__mutmut_25, 
        'xǁBaseResourceǁplan__mutmut_26': xǁBaseResourceǁplan__mutmut_26, 
        'xǁBaseResourceǁplan__mutmut_27': xǁBaseResourceǁplan__mutmut_27, 
        'xǁBaseResourceǁplan__mutmut_28': xǁBaseResourceǁplan__mutmut_28, 
        'xǁBaseResourceǁplan__mutmut_29': xǁBaseResourceǁplan__mutmut_29, 
        'xǁBaseResourceǁplan__mutmut_30': xǁBaseResourceǁplan__mutmut_30, 
        'xǁBaseResourceǁplan__mutmut_31': xǁBaseResourceǁplan__mutmut_31, 
        'xǁBaseResourceǁplan__mutmut_32': xǁBaseResourceǁplan__mutmut_32, 
        'xǁBaseResourceǁplan__mutmut_33': xǁBaseResourceǁplan__mutmut_33, 
        'xǁBaseResourceǁplan__mutmut_34': xǁBaseResourceǁplan__mutmut_34, 
        'xǁBaseResourceǁplan__mutmut_35': xǁBaseResourceǁplan__mutmut_35, 
        'xǁBaseResourceǁplan__mutmut_36': xǁBaseResourceǁplan__mutmut_36, 
        'xǁBaseResourceǁplan__mutmut_37': xǁBaseResourceǁplan__mutmut_37, 
        'xǁBaseResourceǁplan__mutmut_38': xǁBaseResourceǁplan__mutmut_38, 
        'xǁBaseResourceǁplan__mutmut_39': xǁBaseResourceǁplan__mutmut_39, 
        'xǁBaseResourceǁplan__mutmut_40': xǁBaseResourceǁplan__mutmut_40, 
        'xǁBaseResourceǁplan__mutmut_41': xǁBaseResourceǁplan__mutmut_41, 
        'xǁBaseResourceǁplan__mutmut_42': xǁBaseResourceǁplan__mutmut_42
    }
    
    def plan(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseResourceǁplan__mutmut_orig"), object.__getattribute__(self, "xǁBaseResourceǁplan__mutmut_mutants"), args, kwargs, self)
        return result 
    
    plan.__signature__ = _mutmut_signature(xǁBaseResourceǁplan__mutmut_orig)
    xǁBaseResourceǁplan__mutmut_orig.__name__ = 'xǁBaseResourceǁplan'

    async def xǁBaseResourceǁapply__mutmut_orig(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_1(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_2(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is not None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_3(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_4(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is not None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_5(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(None)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_6(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(None)
        else:
            return await self._update_apply(ctx)

    async def xǁBaseResourceǁapply__mutmut_7(self, ctx: ResourceContext) -> tuple[StateType | None, PrivateStateType | None]:
        is_create = ctx.state is None
        is_delete = ctx.planned_state is None

        if is_delete:
            await self._delete_apply(ctx)
            return None, None

        if is_create:
            return await self._create_apply(ctx)
        else:
            return await self._update_apply(None)
    
    xǁBaseResourceǁapply__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseResourceǁapply__mutmut_1': xǁBaseResourceǁapply__mutmut_1, 
        'xǁBaseResourceǁapply__mutmut_2': xǁBaseResourceǁapply__mutmut_2, 
        'xǁBaseResourceǁapply__mutmut_3': xǁBaseResourceǁapply__mutmut_3, 
        'xǁBaseResourceǁapply__mutmut_4': xǁBaseResourceǁapply__mutmut_4, 
        'xǁBaseResourceǁapply__mutmut_5': xǁBaseResourceǁapply__mutmut_5, 
        'xǁBaseResourceǁapply__mutmut_6': xǁBaseResourceǁapply__mutmut_6, 
        'xǁBaseResourceǁapply__mutmut_7': xǁBaseResourceǁapply__mutmut_7
    }
    
    def apply(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseResourceǁapply__mutmut_orig"), object.__getattribute__(self, "xǁBaseResourceǁapply__mutmut_mutants"), args, kwargs, self)
        return result 
    
    apply.__signature__ = _mutmut_signature(xǁBaseResourceǁapply__mutmut_orig)
    xǁBaseResourceǁapply__mutmut_orig.__name__ = 'xǁBaseResourceǁapply'

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
