# pyvider/exceptions/function.py

from typing import Any

from .base import PluginError, PyviderValueError


class FunctionError(PluginError):
    """Base exception for function-related errors during execution."""

    def __init__(
        self,
        message: str,
        function_name: str | None = None,
        argument_index: int | None = None,
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index
        prefix = f"Function '{function_name}'" if function_name else "Function"
        super().__init__(f"{prefix} error: {message}")

    def to_proto(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"text": str(self), "argument_index": self.argument_index}


class FunctionRegistrationError(FunctionError):
    """Exception raised when a function cannot be registered properly."""

    def __init__(self, message: str, function_name: str | None = None) -> None:
        super().__init__(message, function_name=function_name)


class FunctionValidationError(FunctionError, PyviderValueError):
    """Exception raised when function arguments fail validation."""

    def __init__(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
    ) -> None:
        super().__init__(
            message, function_name=function_name, argument_index=argument_index
        )
        self.argument_name = argument_name
        # Enhance message if argument_name is present
        if argument_name and function_name:
            self.args = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}",
            )
        elif argument_name:
            self.args = (f"Argument '{argument_name}' validation error: {message}",)
