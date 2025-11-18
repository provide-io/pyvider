#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Base Functionality for Implementing Terraform Functions in Pyvider.

Defines core abstractions for creating, registering, and adapting custom functions
callable from Terraform configurations via a Pyvider provider. This module focuses
on protocol-agnostic definitions using Pyvider's CTY types."""

from abc import ABC, abstractmethod
import asyncio
from collections.abc import Callable
import inspect
import typing
from typing import Any, TypeVar

from attrs import define, field

# Pyvider Imports
from provide.foundation import logger

# CTY Imports (Core dependency for function signatures)
from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyString,
    CtyType,
)
from pyvider.exceptions import FunctionError

# Type Variables
T = TypeVar("T")
R = TypeVar("R")


@define(frozen=True, kw_only=True)
class FunctionParameter:
    """
    Definition of a Terraform function parameter using attrs.

    Attributes:
        name: Parameter name in Terraform calls. Must be a valid identifier.
        type: CTY type constraint for the parameter (instance of CtyType).
        description: Human-readable description (Markdown supported).
        allow_null: If true, the function accepts a null value for this parameter.
        allow_unknown: If true, the function accepts an unknown value for this parameter.
    """

    name: str = field()
    type: CtyType[Any] = field()
    description: str = field(default="")
    allow_null: bool = field(default=False)
    allow_unknown: bool = field(default=False)

    @name.validator
    def _validate_name(self, attribute: Any, value: str) -> None:
        """Ensure parameter name is a valid Python identifier."""
        if not value or not value.isidentifier():
            raise ValueError(f"Invalid parameter name: '{value}'. Must be a valid identifier.")

    @type.validator
    def _validate_type(self, attribute: Any, value: CtyType[object]) -> None:
        """Ensure the type is a valid CtyType instance."""
        if not isinstance(value, CtyType):
            raise TypeError(f"Parameter type must be an instance of CtyType, got {type(value).__name__}")


@define(frozen=True, kw_only=True)
class FunctionReturnType:
    """
    Definition of a Terraform function's return type using attrs.

    Attributes:
        type: The CTY type constraint for the function's return value.
    """

    type: CtyType[Any] = field()

    @type.validator
    def _validate_type(self, attribute: Any, value: CtyType[object]) -> None:
        """Ensure the type is a valid CtyType instance."""
        if not isinstance(value, CtyType):
            raise TypeError(f"Return type must be an instance of CtyType, got {type(value).__name__}")


@define()
class BaseFunction(ABC):
    """
    Abstract Base Class for Terraform function implementations in Pyvider.

    Subclasses must implement `get_parameters`, `get_return_type`, and `call`.
    This base class is protocol-agnostic.

    Attributes:
        name: Function name exposed to Terraform.
        summary: Short description for documentation.
        description: Detailed description (Markdown supported).
        deprecation_message: If set, marks the function as deprecated.
    """

    name: str = field()
    summary: str = field(default="")
    description: str = field(default="")
    deprecation_message: str = field(default="")

    @abstractmethod
    def get_parameters(self) -> list[FunctionParameter]:
        """
        Abstract method to define the function's parameters.

        Returns:
            A list of FunctionParameter objects describing the expected inputs.
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_return_type(self) -> FunctionReturnType:
        """
        Abstract method to define the function's return type.

        Returns:
            A FunctionReturnType object describing the output type.
        """
        pass  # pragma: no cover

    @abstractmethod
    async def call(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method defining the function's execution logic.

        Implementations should perform the function's calculation based on the
        provided arguments (which will be decoded Python types) and return the result.
        This method *must* be async.

        Args:
            *args: Decoded positional arguments from Terraform.
            **kwargs: Decoded keyword arguments from Terraform.

        Returns:
            The result of the function's computation (must match return type).

        Raises:
            FunctionError: For errors reportable to the Terraform user.
        """
        pass  # pragma: no cover

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Allows BaseFunction instances to be called directly like functions."""
        return await self.call(*args, **kwargs)


class FunctionAdapter:
    """
    Adapts a standard Python callable to the BaseFunction interface using signature
    and type hint inspection. Handles the inference of CTY types from Python types.
    """

    @staticmethod
    def _infer_collection_cty_type(origin_type: Any, args: tuple[Any, ...]) -> CtyType[object]:
        if origin_type in (list, list):
            element_cty: CtyType[object] = CtyDynamic()
            if args and isinstance(args[0], type) and issubclass(args[0], CtyType):
                element_cty = args[0]()
            return CtyList(element_type=element_cty)  # type: ignore[return-value]
        elif origin_type in (dict, dict):
            value_cty: CtyType[object] = CtyDynamic()
            if args and len(args) > 1 and isinstance(args[1], type) and issubclass(args[1], CtyType):
                value_cty = args[1]()
            return CtyMap(element_type=value_cty)  # type: ignore[return-value]
        raise ValueError(f"Unsupported collection type: {origin_type}")

    @staticmethod
    def _infer_union_cty_type(args: tuple[Any, ...]) -> CtyType[object]:
        types_in_union = [t for t in args if t is not type(None)]
        if all(t in (int, float) for t in types_in_union):
            return CtyNumber()  # type: ignore[return-value]
        elif len(types_in_union) == 1 and types_in_union[0] is str:
            return CtyString()  # type: ignore[return-value]
        return CtyDynamic()

    @staticmethod
    def _infer_cty_type_for_hint(hint: Any) -> CtyType[Any]:
        """Infers the CtyType from a given Python type hint."""
        origin_type = typing.get_origin(hint)
        args = typing.get_args(hint)

        if isinstance(hint, type) and issubclass(hint, CtyType):
            return hint()

        if origin_type in (list, dict):
            return FunctionAdapter._infer_collection_cty_type(origin_type, args)

        if origin_type is typing.Union:
            return FunctionAdapter._infer_union_cty_type(args)

        direct_mappings: dict[type, CtyType[object]] = {
            str: CtyString(),  # type: ignore[dict-item]
            int: CtyNumber(),  # type: ignore[dict-item]
            float: CtyNumber(),  # type: ignore[dict-item]
            bool: CtyBool(),  # type: ignore[dict-item]
        }
        return direct_mappings.get(hint, CtyDynamic())

    @staticmethod
    def _process_parameters(
        func: Callable[..., Any],
        sig: inspect.Signature,
        type_hints: dict[str, Any],
        param_descriptions: dict[str, str],
        allow_null: bool | list[str],
        allow_unknown: bool | list[str],
    ) -> list[FunctionParameter]:
        parameters: list[FunctionParameter] = []
        for param_name, _param_obj in sig.parameters.items():
            if param_name == "self":
                continue

            param_hint = type_hints.get(param_name, typing.Any)
            inferred_cty_type = FunctionAdapter._infer_cty_type_for_hint(param_hint)

            origin_type = typing.get_origin(param_hint)
            args = typing.get_args(param_hint)

            allow_null_param = (
                param_name in allow_null if isinstance(allow_null, list) else bool(allow_null)
            ) or (origin_type is typing.Union and type(None) in args)

            allow_unknown_param = (
                param_name in allow_unknown if isinstance(allow_unknown, list) else bool(allow_unknown)
            )

            parameters.append(
                FunctionParameter(
                    name=param_name,
                    type=inferred_cty_type,
                    description=param_descriptions.get(param_name, ""),
                    allow_null=allow_null_param,
                    allow_unknown=allow_unknown_param,
                )
            )
        return parameters

    @staticmethod
    def adapt(
        func: Callable[..., Any],
        name: str | None = None,
        summary: str = "",
        description: str = "",
        param_descriptions: dict[str, str] | None = None,
        return_description: str = "",  # Currently unused
        allow_null: bool | list[str] = False,
        allow_unknown: bool | list[str] = False,
        deprecation_message: str = "",
    ) -> BaseFunction:
        """
        Factory method to create a BaseFunction wrapper around a Python callable.
        """
        func_display_name = name or func.__name__

        docstring = inspect.getdoc(func)
        final_summary = summary or (docstring.strip().split("\n", 1)[0] if docstring else "")
        final_description = description or docstring or ""
        param_descriptions = param_descriptions or {}

        sig = inspect.signature(func)
        try:
            type_hints = typing.get_type_hints(func)
        except Exception as e:
            logger.warning(
                f"Could not get type hints for function '{func_display_name}': {e}. Types will default to CtyDynamic."
            )
            type_hints = {}

        parameters = FunctionAdapter._process_parameters(
            func,
            sig,
            type_hints,
            param_descriptions,
            allow_null,
            allow_unknown,
        )

        return_hint = type_hints.get("return", typing.Any)
        return_tf_type = FunctionAdapter._infer_cty_type_for_hint(return_hint)

        function_return = FunctionReturnType(type=return_tf_type)

        @define()
        class AdaptedFunction(BaseFunction):
            """
            Dynamically created BaseFunction wrapper for a Python callable.
            """

            def get_parameters(self) -> list[FunctionParameter]:
                return parameters

            def get_return_type(self) -> FunctionReturnType:
                return function_return

            async def call(self, *args: Any, **kwargs: Any) -> Any:
                func_name_call = self.name
                try:
                    # THE FIX: Restore logic to handle both sync and async functions.
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)

                    return result
                except FunctionError:
                    raise
                except Exception as e:
                    logger.error(
                        "Error occurred",
                        exc_info=True,
                    )
                    raise FunctionError(f"Function '{func_name_call}' execution failed: {e}") from e

        return AdaptedFunction(
            name=func_display_name,
            summary=final_summary,
            description=final_description,
            deprecation_message=deprecation_message,
        )


# 🐍🏗️🔚
