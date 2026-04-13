#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


class PyviderSchemaError(Exception):
    """Base class for all schema-related errors."""


class SchemaConversionError(PyviderSchemaError):
    """Error during schema conversion processes."""

    def __init__(self, message: str, schema_name: str | None = None, detail: str | None = None) -> None:
        super().__init__(message)
        self.schema_name = schema_name
        self.detail = detail

    def __str__(self) -> str:
        msg = super().__str__()
        if self.schema_name:
            msg = f"[Schema: {self.schema_name}] {msg}"
        if self.detail:
            msg = f"{msg} (Detail: {self.detail})"
        return msg


class PvsValidationError(PyviderSchemaError):
    """Raised when schema validation fails."""


class PvsSchemaDefinitionError(PyviderSchemaError):
    """Raised when schema definition is invalid."""


class PvsAttributeError(PyviderSchemaError):
    """Raised when an attribute definition is invalid."""


class PvsBlockError(PyviderSchemaError):
    """Raised when a block definition is invalid. (Retained for general block-like errors)."""


# 🐍🏗️🔚
