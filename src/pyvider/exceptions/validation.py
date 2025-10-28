#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from provide.foundation.errors import ValidationError as FoundationValidationError


class ValidationError(FoundationValidationError):
    """Raised when general validation fails for a value or operation.

    Inherits directly from foundation's ValidationError for
    consistent validation error handling.
    """

    def __init__(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", {})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def _default_code(self) -> str:
        return "VALIDATION_ERROR"


class AttributeValidationError(ValidationError):
    """Raised when a specific attribute's value is invalid."""

    def __init__(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, context=context, detail=detail)


# 🐍🏗️🔚
