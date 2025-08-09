#
# pyvider/exceptions/validation.py
#
from .base import PyviderValueError


class ValidationError(PyviderValueError):
    """Raised when general validation fails for a value or operation."""

    def __init__(
        self, message: str, *, context: str | None = None, detail: str | None = None
    ) -> None:
        self.context = context
        self.detail = detail
        full_message = f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message)


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


# 🐍🏗️📄🪄
