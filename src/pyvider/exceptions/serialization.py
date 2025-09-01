# pyvider/exceptions/serialization.py
from typing import Any

from provide.foundation.errors import ValidationError as FoundationValidationError
from pyvider.exceptions.base import ConversionError


class SerializationError(FoundationValidationError):
    """Raised when serialization of a value fails."""

    def __init__(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
        **kwargs
    ) -> None:
        self.type_name = type_name
        self.source_value = source_value
        self.detail = detail
        
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        
        if type_name:
            kwargs.setdefault('context', {})['serialization.type'] = type_name
        if source_value is not None:
            kwargs.setdefault('context', {})['serialization.source_type'] = type(source_value).__name__
        if detail:
            kwargs.setdefault('context', {})['serialization.detail'] = detail
            
        super().__init__(full_message, **kwargs)
    
    def _default_code(self) -> str:
        return "SERIALIZATION_ERROR"


class DeserializationError(FoundationValidationError):
    """Raised when deserialization of data into a value fails."""

    def __init__(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
        **kwargs
    ) -> None:
        self.type_name = type_name
        self.source_value = source_value
        self.detail = detail
        
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        
        if type_name:
            kwargs.setdefault('context', {})['deserialization.type'] = type_name
        if source_value is not None:
            kwargs.setdefault('context', {})['deserialization.source_type'] = type(source_value).__name__
        if detail:
            kwargs.setdefault('context', {})['deserialization.detail'] = detail
            
        super().__init__(full_message, **kwargs)
    
    def _default_code(self) -> str:
        return "DESERIALIZATION_ERROR"
