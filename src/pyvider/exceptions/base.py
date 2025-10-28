#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from provide.foundation.errors import (
    FoundationError,
)


class PyviderError(FoundationError):
    """Base class for all Pyvider framework errors.

    Inherits from FoundationError to gain:
    - Rich error context with namespace-based metadata
    - Automatic telemetry integration
    - Terraform diagnostic generation support
    """

    def _default_code(self) -> str:
        """Default error code for pyvider errors."""
        return "PYVIDER_ERROR"


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

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "CONVERSION_ERROR"


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

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "WIRE_FORMAT_ERROR"


class FrameworkConfigurationError(PyviderError):
    """Errors related to the overall framework configuration."""

    def _default_code(self) -> str:
        return "FRAMEWORK_CONFIG_ERROR"


class PluginError(PyviderError):
    """Base class for errors originating from plugin operations or lifecycle."""

    pass


class PyviderValueError(PyviderError):
    """Generic value-related errors within Pyvider."""

    def _default_code(self) -> str:
        return "VALUE_ERROR"


class InvalidTypeError(PyviderValueError):
    """Raised when a value does not match the expected type."""

    def __init__(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def _default_code(self) -> str:
        return "INVALID_TYPE"


class UnsupportedTypeError(PyviderValueError):
    """Raised when an unsupported type is encountered."""

    def __init__(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"type.unsupported": type_name})

    def _default_code(self) -> str:
        return "UNSUPPORTED_TYPE"


class ComponentConfigurationError(FrameworkConfigurationError):
    """Errors specific to component configuration (e.g., resource, provider)."""

    def _default_code(self) -> str:
        return "COMPONENT_CONFIG_ERROR"


# 🐍🏗️🔚
