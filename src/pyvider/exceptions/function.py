#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    RuntimeError as FoundationRuntimeError,
    ValidationError as FoundationValidationError,
)


class FunctionError(FoundationRuntimeError):
    """Base exception for function-related errors during execution."""

    def __init__(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "FUNCTION_ERROR"

    def to_proto(self) -> dict[str, Any]:
        """The parts of this error that go on the wire.

        `call_function` assembles the protobuf message itself, because
        `function_argument` is an optional field and must be left unset rather
        than sent as zero when the function did not say which argument it meant.
        """
        return {"text": str(self), "argument_index": self.argument_index}


class FunctionRegistrationError(FoundationConfigurationError):
    """Exception raised when a function cannot be registered properly."""

    def __init__(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "FUNCTION_REGISTRATION_ERROR"


class FunctionValidationError(FoundationValidationError):
    """Exception raised when function arguments fail validation."""

    def __init__(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "FUNCTION_VALIDATION_ERROR"


# 🐍🏗️🔚
