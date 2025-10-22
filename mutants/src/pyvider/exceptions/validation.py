# pyvider/exceptions/validation.py

from typing import Any

from provide.foundation.errors import ValidationError as FoundationValidationError
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


class ValidationError(FoundationValidationError):
    """Raised when general validation fails for a value or operation.

    Inherits directly from foundation's ValidationError for
    consistent validation error handling.
    """

    def xǁValidationErrorǁ__init____mutmut_orig(
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

    def xǁValidationErrorǁ__init____mutmut_1(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = None

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", {})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_2(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else 'XXXX'}{message}{f' - Detail: {detail}' if detail else ''}"
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

    def xǁValidationErrorǁ__init____mutmut_3(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else 'XXXX'}"
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

    def xǁValidationErrorǁ__init____mutmut_4(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = None
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_5(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault(None, {})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_6(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", None)
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_7(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault({})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_8(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", )
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_9(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("XXcontextXX", {})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_10(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("CONTEXT", {})
        if context:
            ctx_dict["validation.context"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_11(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", {})
        if context:
            ctx_dict["validation.context"] = None
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_12(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", {})
        if context:
            ctx_dict["XXvalidation.contextXX"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_13(
        self, message: str, *, context: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        # Build message with old format for compatibility
        full_message = (
            f"{f'Context: {context} - ' if context else ''}{message}{f' - Detail: {detail}' if detail else ''}"
        )

        # Store in foundation context as well
        ctx_dict: dict[str, Any] = kwargs.setdefault("context", {})
        if context:
            ctx_dict["VALIDATION.CONTEXT"] = context
        if detail:
            ctx_dict["validation.detail"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_14(
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
            ctx_dict["validation.detail"] = None

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_15(
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
            ctx_dict["XXvalidation.detailXX"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_16(
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
            ctx_dict["VALIDATION.DETAIL"] = detail

        super().__init__(full_message, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_17(
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

        super().__init__(None, **kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_18(
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

        super().__init__(**kwargs)
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_19(
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

        super().__init__(full_message, )
        self.validation_context = context
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_20(
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
        self.validation_context = None
        self.detail = detail

    def xǁValidationErrorǁ__init____mutmut_21(
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
        self.detail = None
    
    xǁValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidationErrorǁ__init____mutmut_1': xǁValidationErrorǁ__init____mutmut_1, 
        'xǁValidationErrorǁ__init____mutmut_2': xǁValidationErrorǁ__init____mutmut_2, 
        'xǁValidationErrorǁ__init____mutmut_3': xǁValidationErrorǁ__init____mutmut_3, 
        'xǁValidationErrorǁ__init____mutmut_4': xǁValidationErrorǁ__init____mutmut_4, 
        'xǁValidationErrorǁ__init____mutmut_5': xǁValidationErrorǁ__init____mutmut_5, 
        'xǁValidationErrorǁ__init____mutmut_6': xǁValidationErrorǁ__init____mutmut_6, 
        'xǁValidationErrorǁ__init____mutmut_7': xǁValidationErrorǁ__init____mutmut_7, 
        'xǁValidationErrorǁ__init____mutmut_8': xǁValidationErrorǁ__init____mutmut_8, 
        'xǁValidationErrorǁ__init____mutmut_9': xǁValidationErrorǁ__init____mutmut_9, 
        'xǁValidationErrorǁ__init____mutmut_10': xǁValidationErrorǁ__init____mutmut_10, 
        'xǁValidationErrorǁ__init____mutmut_11': xǁValidationErrorǁ__init____mutmut_11, 
        'xǁValidationErrorǁ__init____mutmut_12': xǁValidationErrorǁ__init____mutmut_12, 
        'xǁValidationErrorǁ__init____mutmut_13': xǁValidationErrorǁ__init____mutmut_13, 
        'xǁValidationErrorǁ__init____mutmut_14': xǁValidationErrorǁ__init____mutmut_14, 
        'xǁValidationErrorǁ__init____mutmut_15': xǁValidationErrorǁ__init____mutmut_15, 
        'xǁValidationErrorǁ__init____mutmut_16': xǁValidationErrorǁ__init____mutmut_16, 
        'xǁValidationErrorǁ__init____mutmut_17': xǁValidationErrorǁ__init____mutmut_17, 
        'xǁValidationErrorǁ__init____mutmut_18': xǁValidationErrorǁ__init____mutmut_18, 
        'xǁValidationErrorǁ__init____mutmut_19': xǁValidationErrorǁ__init____mutmut_19, 
        'xǁValidationErrorǁ__init____mutmut_20': xǁValidationErrorǁ__init____mutmut_20, 
        'xǁValidationErrorǁ__init____mutmut_21': xǁValidationErrorǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁValidationErrorǁ__init____mutmut_orig)
    xǁValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁValidationErrorǁ__init__'

    def xǁValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "VALIDATION_ERROR"

    def xǁValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXVALIDATION_ERRORXX"

    def xǁValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "validation_error"
    
    xǁValidationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidationErrorǁ_default_code__mutmut_1': xǁValidationErrorǁ_default_code__mutmut_1, 
        'xǁValidationErrorǁ_default_code__mutmut_2': xǁValidationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁValidationErrorǁ_default_code__mutmut_orig)
    xǁValidationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁValidationErrorǁ_default_code'


class AttributeValidationError(ValidationError):
    """Raised when a specific attribute's value is invalid."""

    def xǁAttributeValidationErrorǁ__init____mutmut_orig(
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

    def xǁAttributeValidationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = None
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, context=context, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = None
        super().__init__(full_message, context=context, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(None, context=context, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, context=None, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, context=context, detail=None)

    def xǁAttributeValidationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(context=context, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, detail=detail)

    def xǁAttributeValidationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        attribute_name: str,
        context: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.attribute_name = attribute_name
        full_message = f"Attribute '{attribute_name}' validation failed: {message}"
        super().__init__(full_message, context=context, )
    
    xǁAttributeValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAttributeValidationErrorǁ__init____mutmut_1': xǁAttributeValidationErrorǁ__init____mutmut_1, 
        'xǁAttributeValidationErrorǁ__init____mutmut_2': xǁAttributeValidationErrorǁ__init____mutmut_2, 
        'xǁAttributeValidationErrorǁ__init____mutmut_3': xǁAttributeValidationErrorǁ__init____mutmut_3, 
        'xǁAttributeValidationErrorǁ__init____mutmut_4': xǁAttributeValidationErrorǁ__init____mutmut_4, 
        'xǁAttributeValidationErrorǁ__init____mutmut_5': xǁAttributeValidationErrorǁ__init____mutmut_5, 
        'xǁAttributeValidationErrorǁ__init____mutmut_6': xǁAttributeValidationErrorǁ__init____mutmut_6, 
        'xǁAttributeValidationErrorǁ__init____mutmut_7': xǁAttributeValidationErrorǁ__init____mutmut_7, 
        'xǁAttributeValidationErrorǁ__init____mutmut_8': xǁAttributeValidationErrorǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAttributeValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAttributeValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAttributeValidationErrorǁ__init____mutmut_orig)
    xǁAttributeValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁAttributeValidationErrorǁ__init__'
