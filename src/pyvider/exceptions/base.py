#
# pyvider/exceptions/base.py
#
from typing import Any


class PyviderError(Exception):
    """Base class for all Pyvider framework errors."""

    pass


class ConversionError(PyviderError):
    """Base class for data conversion errors within the Pyvider framework."""

    def __init__(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
        if target_type is not None:
            target_name = (
                target_type.__name__
                if hasattr(target_type, "__name__")
                else str(target_type)
            )
            context_parts.append(f"target_type={target_name}")

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"
        super().__init__(message)


class WireFormatError(ConversionError):
    """For errors specific to wire format processing."""

    def __init__(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation
        super().__init__(message, **kwargs)


class FrameworkConfigurationError(PyviderError):
    """Errors related to the overall framework configuration."""

    pass


class PluginError(PyviderError):
    """Base class for errors originating from plugin operations or lifecycle."""

    pass


class PyviderValueError(PyviderError):
    """Generic value-related errors within Pyvider."""

    pass


class InvalidTypeError(PyviderValueError):
    """Raised when a value does not match the expected type."""

    def __init__(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        if message_override:
            super().__init__(message_override)
        else:
            super().__init__(
                f"Invalid type: expected '{expected_type}', got '{actual_type}'."
            )


class UnsupportedTypeError(PyviderValueError):
    """Raised when an unsupported type is encountered."""

    def __init__(
        self, type_name: str = "unknown", message_override: str | None = None
    ) -> None:
        if message_override:
            super().__init__(message_override)
        else:
            super().__init__(f"Unsupported type encountered: '{type_name}'.")


class ComponentConfigurationError(FrameworkConfigurationError):
    """Errors specific to component configuration (e.g., resource, provider)."""

    pass


# 🐍🏗️


# 🐍🏗️🏛️🪄
