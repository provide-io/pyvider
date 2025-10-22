# pyvider/exceptions/serialization.py
from typing import Any

from pyvider.exceptions.base import ConversionError
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class SerializationError(ConversionError):
    """Raised when serialization of a value fails."""

    def xǁSerializationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = None
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name and 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'XXunknownXX'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'UNKNOWN'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else 'XXXX'}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(None, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=None, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=None)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, )
        self.type_name = type_name
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = None
        self.detail = detail

    def xǁSerializationErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = None
    
    xǁSerializationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSerializationErrorǁ__init____mutmut_1': xǁSerializationErrorǁ__init____mutmut_1, 
        'xǁSerializationErrorǁ__init____mutmut_2': xǁSerializationErrorǁ__init____mutmut_2, 
        'xǁSerializationErrorǁ__init____mutmut_3': xǁSerializationErrorǁ__init____mutmut_3, 
        'xǁSerializationErrorǁ__init____mutmut_4': xǁSerializationErrorǁ__init____mutmut_4, 
        'xǁSerializationErrorǁ__init____mutmut_5': xǁSerializationErrorǁ__init____mutmut_5, 
        'xǁSerializationErrorǁ__init____mutmut_6': xǁSerializationErrorǁ__init____mutmut_6, 
        'xǁSerializationErrorǁ__init____mutmut_7': xǁSerializationErrorǁ__init____mutmut_7, 
        'xǁSerializationErrorǁ__init____mutmut_8': xǁSerializationErrorǁ__init____mutmut_8, 
        'xǁSerializationErrorǁ__init____mutmut_9': xǁSerializationErrorǁ__init____mutmut_9, 
        'xǁSerializationErrorǁ__init____mutmut_10': xǁSerializationErrorǁ__init____mutmut_10, 
        'xǁSerializationErrorǁ__init____mutmut_11': xǁSerializationErrorǁ__init____mutmut_11, 
        'xǁSerializationErrorǁ__init____mutmut_12': xǁSerializationErrorǁ__init____mutmut_12, 
        'xǁSerializationErrorǁ__init____mutmut_13': xǁSerializationErrorǁ__init____mutmut_13
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSerializationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSerializationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSerializationErrorǁ__init____mutmut_orig)
    xǁSerializationErrorǁ__init____mutmut_orig.__name__ = 'xǁSerializationErrorǁ__init__'


class DeserializationError(ConversionError):
    """Raised when deserialization of data into a value fails."""

    def xǁDeserializationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = None
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name and 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'XXunknownXX'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'UNKNOWN'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else 'XXXX'}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(None, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=None, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=None)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, target_type=type_name)
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, )
        self.type_name = type_name
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = None
        self.detail = detail

    def xǁDeserializationErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = None
    
    xǁDeserializationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDeserializationErrorǁ__init____mutmut_1': xǁDeserializationErrorǁ__init____mutmut_1, 
        'xǁDeserializationErrorǁ__init____mutmut_2': xǁDeserializationErrorǁ__init____mutmut_2, 
        'xǁDeserializationErrorǁ__init____mutmut_3': xǁDeserializationErrorǁ__init____mutmut_3, 
        'xǁDeserializationErrorǁ__init____mutmut_4': xǁDeserializationErrorǁ__init____mutmut_4, 
        'xǁDeserializationErrorǁ__init____mutmut_5': xǁDeserializationErrorǁ__init____mutmut_5, 
        'xǁDeserializationErrorǁ__init____mutmut_6': xǁDeserializationErrorǁ__init____mutmut_6, 
        'xǁDeserializationErrorǁ__init____mutmut_7': xǁDeserializationErrorǁ__init____mutmut_7, 
        'xǁDeserializationErrorǁ__init____mutmut_8': xǁDeserializationErrorǁ__init____mutmut_8, 
        'xǁDeserializationErrorǁ__init____mutmut_9': xǁDeserializationErrorǁ__init____mutmut_9, 
        'xǁDeserializationErrorǁ__init____mutmut_10': xǁDeserializationErrorǁ__init____mutmut_10, 
        'xǁDeserializationErrorǁ__init____mutmut_11': xǁDeserializationErrorǁ__init____mutmut_11, 
        'xǁDeserializationErrorǁ__init____mutmut_12': xǁDeserializationErrorǁ__init____mutmut_12, 
        'xǁDeserializationErrorǁ__init____mutmut_13': xǁDeserializationErrorǁ__init____mutmut_13
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDeserializationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDeserializationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDeserializationErrorǁ__init____mutmut_orig)
    xǁDeserializationErrorǁ__init____mutmut_orig.__name__ = 'xǁDeserializationErrorǁ__init__'
