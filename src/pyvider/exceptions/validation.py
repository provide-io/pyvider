# pyvider/exceptions/validation.py

from provide.foundation.errors import ValidationError as FoundationValidationError


class ValidationError(FoundationValidationError):
    """Raised when general validation fails for a value or operation.

    Inherits directly from foundation's ValidationError for
    consistent validation error handling.
    """

    def __init__(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        if "context" not in kwargs:
            kwargs["context"] = {}
        if context:
            kwargs["context"]["validation.context"] = context  # type: ignore[index]
        if detail:
            kwargs["context"]["validation.detail"] = detail  # type: ignore[index]

        super().__init__(full_message, **kwargs)
        self.context = context
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
