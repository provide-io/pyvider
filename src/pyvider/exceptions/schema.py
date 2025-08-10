# pyvider/exceptions/schema.py
from typing import Any

from .base import ConversionError, PyviderError, PyviderValueError


class SchemaError(PyviderError):
    """Base class for schema definition or processing errors."""

    def __init__(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        super().__init__(f"{prefix} error: {message}")


class SchemaValidationError(SchemaError, PyviderValueError):
    """Raised when schema validation fails against provided data."""

    def __init__(
        self, message: str, schema_name: str | None = None, detail: str | None = None
    ) -> None:
        full_message = f"{message}{f': {detail}' if detail else ''}"
        super().__init__(full_message, schema_name=schema_name)
        self.detail = detail


class SchemaRegistrationError(SchemaError):
    """Raised when schema registration fails in the framework."""

    pass


class SchemaParseError(SchemaError):
    """Raised when a schema definition cannot be parsed."""

    pass


class SchemaConversionError(ConversionError):
    """Raised when schema conversion to/from another format fails."""

    def __init__(
        self,
        message: str,
        *,
        schema_name: str | None = None,
        source_value: Any = None,
        target_type: Any = None,
    ) -> None:
        self.schema_name = schema_name
        if schema_name:
            message = f"Schema '{schema_name}' conversion failed: {message}"
        super().__init__(message, source_value=source_value, target_type=target_type)
