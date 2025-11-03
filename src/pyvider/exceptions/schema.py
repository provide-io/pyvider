#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    ValidationError as FoundationValidationError,
)

from pyvider.exceptions.base import ConversionError, PyviderError


class SchemaError(PyviderError):
    """Base class for schema definition or processing errors."""

    def __init__(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        super().__init__(f"{prefix} error: {message}")


class SchemaValidationError(FoundationValidationError):
    """Raised when schema validation fails against provided data."""

    def __init__(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "SCHEMA_VALIDATION_ERROR"


class SchemaRegistrationError(FoundationConfigurationError):
    """Raised when schema registration fails in the framework."""

    def __init__(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "SCHEMA_REGISTRATION_ERROR"


class SchemaParseError(FoundationValidationError):
    """Raised when a schema definition cannot be parsed."""

    def __init__(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def _default_code(self) -> str:
        return "SCHEMA_PARSE_ERROR"


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


# 🐍🏗️🔚
