# pyvider/exceptions/schema.py
from typing import Any

from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    ValidationError as FoundationValidationError,
)

from pyvider.exceptions.base import ConversionError, PyviderError
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


class SchemaError(PyviderError):
    """Base class for schema definition or processing errors."""

    def xǁSchemaErrorǁ__init____mutmut_orig(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_1(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = None
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_2(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = None
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_3(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "XXSchemaXX"
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_4(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "schema"
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_5(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "SCHEMA"
        super().__init__(f"{prefix} error: {message}")

    def xǁSchemaErrorǁ__init____mutmut_6(self, message: str, schema_name: str | None = None) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        super().__init__(None)
    
    xǁSchemaErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaErrorǁ__init____mutmut_1': xǁSchemaErrorǁ__init____mutmut_1, 
        'xǁSchemaErrorǁ__init____mutmut_2': xǁSchemaErrorǁ__init____mutmut_2, 
        'xǁSchemaErrorǁ__init____mutmut_3': xǁSchemaErrorǁ__init____mutmut_3, 
        'xǁSchemaErrorǁ__init____mutmut_4': xǁSchemaErrorǁ__init____mutmut_4, 
        'xǁSchemaErrorǁ__init____mutmut_5': xǁSchemaErrorǁ__init____mutmut_5, 
        'xǁSchemaErrorǁ__init____mutmut_6': xǁSchemaErrorǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaErrorǁ__init____mutmut_orig)
    xǁSchemaErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaErrorǁ__init__'


class SchemaValidationError(FoundationValidationError):
    """Raised when schema validation fails against provided data."""

    def xǁSchemaValidationErrorǁ__init____mutmut_orig(
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

    def xǁSchemaValidationErrorǁ__init____mutmut_1(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = None
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_2(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = None
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_3(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = None
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_4(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "XXSchemaXX"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_5(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_6(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "SCHEMA"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_7(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = None

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_8(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else 'XXXX'}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_9(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = None
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_10(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault(None, {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_11(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", None)["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_12(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault({})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_13(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", )["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_14(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("XXcontextXX", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_15(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("CONTEXT", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_16(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["XXschema.nameXX"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_17(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["SCHEMA.NAME"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_18(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["schema.detail"] = None

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_19(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault(None, {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_20(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", None)["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_21(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault({})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_22(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", )["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_23(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("XXcontextXX", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_24(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("CONTEXT", {})["schema.detail"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_25(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["XXschema.detailXX"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_26(
        self, message: str, schema_name: str | None = None, detail: str | None = None, **kwargs: Any
    ) -> None:
        self.schema_name = schema_name
        self.detail = detail
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} error: {message}{f': {detail}' if detail else ''}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name
        if detail:
            kwargs.setdefault("context", {})["SCHEMA.DETAIL"] = detail

        super().__init__(full_message, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_27(
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

        super().__init__(None, **kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_28(
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

        super().__init__(**kwargs)

    def xǁSchemaValidationErrorǁ__init____mutmut_29(
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

        super().__init__(full_message, )
    
    xǁSchemaValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidationErrorǁ__init____mutmut_1': xǁSchemaValidationErrorǁ__init____mutmut_1, 
        'xǁSchemaValidationErrorǁ__init____mutmut_2': xǁSchemaValidationErrorǁ__init____mutmut_2, 
        'xǁSchemaValidationErrorǁ__init____mutmut_3': xǁSchemaValidationErrorǁ__init____mutmut_3, 
        'xǁSchemaValidationErrorǁ__init____mutmut_4': xǁSchemaValidationErrorǁ__init____mutmut_4, 
        'xǁSchemaValidationErrorǁ__init____mutmut_5': xǁSchemaValidationErrorǁ__init____mutmut_5, 
        'xǁSchemaValidationErrorǁ__init____mutmut_6': xǁSchemaValidationErrorǁ__init____mutmut_6, 
        'xǁSchemaValidationErrorǁ__init____mutmut_7': xǁSchemaValidationErrorǁ__init____mutmut_7, 
        'xǁSchemaValidationErrorǁ__init____mutmut_8': xǁSchemaValidationErrorǁ__init____mutmut_8, 
        'xǁSchemaValidationErrorǁ__init____mutmut_9': xǁSchemaValidationErrorǁ__init____mutmut_9, 
        'xǁSchemaValidationErrorǁ__init____mutmut_10': xǁSchemaValidationErrorǁ__init____mutmut_10, 
        'xǁSchemaValidationErrorǁ__init____mutmut_11': xǁSchemaValidationErrorǁ__init____mutmut_11, 
        'xǁSchemaValidationErrorǁ__init____mutmut_12': xǁSchemaValidationErrorǁ__init____mutmut_12, 
        'xǁSchemaValidationErrorǁ__init____mutmut_13': xǁSchemaValidationErrorǁ__init____mutmut_13, 
        'xǁSchemaValidationErrorǁ__init____mutmut_14': xǁSchemaValidationErrorǁ__init____mutmut_14, 
        'xǁSchemaValidationErrorǁ__init____mutmut_15': xǁSchemaValidationErrorǁ__init____mutmut_15, 
        'xǁSchemaValidationErrorǁ__init____mutmut_16': xǁSchemaValidationErrorǁ__init____mutmut_16, 
        'xǁSchemaValidationErrorǁ__init____mutmut_17': xǁSchemaValidationErrorǁ__init____mutmut_17, 
        'xǁSchemaValidationErrorǁ__init____mutmut_18': xǁSchemaValidationErrorǁ__init____mutmut_18, 
        'xǁSchemaValidationErrorǁ__init____mutmut_19': xǁSchemaValidationErrorǁ__init____mutmut_19, 
        'xǁSchemaValidationErrorǁ__init____mutmut_20': xǁSchemaValidationErrorǁ__init____mutmut_20, 
        'xǁSchemaValidationErrorǁ__init____mutmut_21': xǁSchemaValidationErrorǁ__init____mutmut_21, 
        'xǁSchemaValidationErrorǁ__init____mutmut_22': xǁSchemaValidationErrorǁ__init____mutmut_22, 
        'xǁSchemaValidationErrorǁ__init____mutmut_23': xǁSchemaValidationErrorǁ__init____mutmut_23, 
        'xǁSchemaValidationErrorǁ__init____mutmut_24': xǁSchemaValidationErrorǁ__init____mutmut_24, 
        'xǁSchemaValidationErrorǁ__init____mutmut_25': xǁSchemaValidationErrorǁ__init____mutmut_25, 
        'xǁSchemaValidationErrorǁ__init____mutmut_26': xǁSchemaValidationErrorǁ__init____mutmut_26, 
        'xǁSchemaValidationErrorǁ__init____mutmut_27': xǁSchemaValidationErrorǁ__init____mutmut_27, 
        'xǁSchemaValidationErrorǁ__init____mutmut_28': xǁSchemaValidationErrorǁ__init____mutmut_28, 
        'xǁSchemaValidationErrorǁ__init____mutmut_29': xǁSchemaValidationErrorǁ__init____mutmut_29
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaValidationErrorǁ__init____mutmut_orig)
    xǁSchemaValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaValidationErrorǁ__init__'

    def xǁSchemaValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "SCHEMA_VALIDATION_ERROR"

    def xǁSchemaValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXSCHEMA_VALIDATION_ERRORXX"

    def xǁSchemaValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "schema_validation_error"
    
    xǁSchemaValidationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidationErrorǁ_default_code__mutmut_1': xǁSchemaValidationErrorǁ_default_code__mutmut_1, 
        'xǁSchemaValidationErrorǁ_default_code__mutmut_2': xǁSchemaValidationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁSchemaValidationErrorǁ_default_code__mutmut_orig)
    xǁSchemaValidationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁSchemaValidationErrorǁ_default_code'


class SchemaRegistrationError(FoundationConfigurationError):
    """Raised when schema registration fails in the framework."""

    def xǁSchemaRegistrationErrorǁ__init____mutmut_orig(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_1(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = None
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_2(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = None
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_3(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "XXSchemaXX"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_4(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_5(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "SCHEMA"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_6(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = None

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_7(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = None

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_8(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault(None, {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_9(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", None)["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_10(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault({})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_11(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", )["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_12(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("XXcontextXX", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_13(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("CONTEXT", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_14(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["XXschema.nameXX"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_15(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["SCHEMA.NAME"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_16(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(None, **kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_17(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(**kwargs)

    def xǁSchemaRegistrationErrorǁ__init____mutmut_18(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} registration error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, )
    
    xǁSchemaRegistrationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaRegistrationErrorǁ__init____mutmut_1': xǁSchemaRegistrationErrorǁ__init____mutmut_1, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_2': xǁSchemaRegistrationErrorǁ__init____mutmut_2, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_3': xǁSchemaRegistrationErrorǁ__init____mutmut_3, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_4': xǁSchemaRegistrationErrorǁ__init____mutmut_4, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_5': xǁSchemaRegistrationErrorǁ__init____mutmut_5, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_6': xǁSchemaRegistrationErrorǁ__init____mutmut_6, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_7': xǁSchemaRegistrationErrorǁ__init____mutmut_7, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_8': xǁSchemaRegistrationErrorǁ__init____mutmut_8, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_9': xǁSchemaRegistrationErrorǁ__init____mutmut_9, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_10': xǁSchemaRegistrationErrorǁ__init____mutmut_10, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_11': xǁSchemaRegistrationErrorǁ__init____mutmut_11, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_12': xǁSchemaRegistrationErrorǁ__init____mutmut_12, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_13': xǁSchemaRegistrationErrorǁ__init____mutmut_13, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_14': xǁSchemaRegistrationErrorǁ__init____mutmut_14, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_15': xǁSchemaRegistrationErrorǁ__init____mutmut_15, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_16': xǁSchemaRegistrationErrorǁ__init____mutmut_16, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_17': xǁSchemaRegistrationErrorǁ__init____mutmut_17, 
        'xǁSchemaRegistrationErrorǁ__init____mutmut_18': xǁSchemaRegistrationErrorǁ__init____mutmut_18
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaRegistrationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaRegistrationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaRegistrationErrorǁ__init____mutmut_orig)
    xǁSchemaRegistrationErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaRegistrationErrorǁ__init__'

    def xǁSchemaRegistrationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "SCHEMA_REGISTRATION_ERROR"

    def xǁSchemaRegistrationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXSCHEMA_REGISTRATION_ERRORXX"

    def xǁSchemaRegistrationErrorǁ_default_code__mutmut_2(self) -> str:
        return "schema_registration_error"
    
    xǁSchemaRegistrationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaRegistrationErrorǁ_default_code__mutmut_1': xǁSchemaRegistrationErrorǁ_default_code__mutmut_1, 
        'xǁSchemaRegistrationErrorǁ_default_code__mutmut_2': xǁSchemaRegistrationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaRegistrationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁSchemaRegistrationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁSchemaRegistrationErrorǁ_default_code__mutmut_orig)
    xǁSchemaRegistrationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁSchemaRegistrationErrorǁ_default_code'


class SchemaParseError(FoundationValidationError):
    """Raised when a schema definition cannot be parsed."""

    def xǁSchemaParseErrorǁ__init____mutmut_orig(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_1(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = None
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_2(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = None
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_3(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "XXSchemaXX"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_4(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_5(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "SCHEMA"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_6(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = None

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_7(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = None

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_8(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault(None, {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_9(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", None)["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_10(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault({})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_11(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", )["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_12(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("XXcontextXX", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_13(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("CONTEXT", {})["schema.name"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_14(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["XXschema.nameXX"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_15(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["SCHEMA.NAME"] = schema_name

        super().__init__(full_message, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_16(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(None, **kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_17(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(**kwargs)

    def xǁSchemaParseErrorǁ__init____mutmut_18(self, message: str, schema_name: str | None = None, **kwargs: Any) -> None:
        self.schema_name = schema_name
        prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
        full_message = f"{prefix} parse error: {message}"

        if schema_name:
            kwargs.setdefault("context", {})["schema.name"] = schema_name

        super().__init__(full_message, )
    
    xǁSchemaParseErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaParseErrorǁ__init____mutmut_1': xǁSchemaParseErrorǁ__init____mutmut_1, 
        'xǁSchemaParseErrorǁ__init____mutmut_2': xǁSchemaParseErrorǁ__init____mutmut_2, 
        'xǁSchemaParseErrorǁ__init____mutmut_3': xǁSchemaParseErrorǁ__init____mutmut_3, 
        'xǁSchemaParseErrorǁ__init____mutmut_4': xǁSchemaParseErrorǁ__init____mutmut_4, 
        'xǁSchemaParseErrorǁ__init____mutmut_5': xǁSchemaParseErrorǁ__init____mutmut_5, 
        'xǁSchemaParseErrorǁ__init____mutmut_6': xǁSchemaParseErrorǁ__init____mutmut_6, 
        'xǁSchemaParseErrorǁ__init____mutmut_7': xǁSchemaParseErrorǁ__init____mutmut_7, 
        'xǁSchemaParseErrorǁ__init____mutmut_8': xǁSchemaParseErrorǁ__init____mutmut_8, 
        'xǁSchemaParseErrorǁ__init____mutmut_9': xǁSchemaParseErrorǁ__init____mutmut_9, 
        'xǁSchemaParseErrorǁ__init____mutmut_10': xǁSchemaParseErrorǁ__init____mutmut_10, 
        'xǁSchemaParseErrorǁ__init____mutmut_11': xǁSchemaParseErrorǁ__init____mutmut_11, 
        'xǁSchemaParseErrorǁ__init____mutmut_12': xǁSchemaParseErrorǁ__init____mutmut_12, 
        'xǁSchemaParseErrorǁ__init____mutmut_13': xǁSchemaParseErrorǁ__init____mutmut_13, 
        'xǁSchemaParseErrorǁ__init____mutmut_14': xǁSchemaParseErrorǁ__init____mutmut_14, 
        'xǁSchemaParseErrorǁ__init____mutmut_15': xǁSchemaParseErrorǁ__init____mutmut_15, 
        'xǁSchemaParseErrorǁ__init____mutmut_16': xǁSchemaParseErrorǁ__init____mutmut_16, 
        'xǁSchemaParseErrorǁ__init____mutmut_17': xǁSchemaParseErrorǁ__init____mutmut_17, 
        'xǁSchemaParseErrorǁ__init____mutmut_18': xǁSchemaParseErrorǁ__init____mutmut_18
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaParseErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaParseErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaParseErrorǁ__init____mutmut_orig)
    xǁSchemaParseErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaParseErrorǁ__init__'

    def xǁSchemaParseErrorǁ_default_code__mutmut_orig(self) -> str:
        return "SCHEMA_PARSE_ERROR"

    def xǁSchemaParseErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXSCHEMA_PARSE_ERRORXX"

    def xǁSchemaParseErrorǁ_default_code__mutmut_2(self) -> str:
        return "schema_parse_error"
    
    xǁSchemaParseErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaParseErrorǁ_default_code__mutmut_1': xǁSchemaParseErrorǁ_default_code__mutmut_1, 
        'xǁSchemaParseErrorǁ_default_code__mutmut_2': xǁSchemaParseErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaParseErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁSchemaParseErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁSchemaParseErrorǁ_default_code__mutmut_orig)
    xǁSchemaParseErrorǁ_default_code__mutmut_orig.__name__ = 'xǁSchemaParseErrorǁ_default_code'


class SchemaConversionError(ConversionError):
    """Raised when schema conversion to/from another format fails."""

    def xǁSchemaConversionErrorǁ__init____mutmut_orig(
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

    def xǁSchemaConversionErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        schema_name: str | None = None,
        source_value: Any = None,
        target_type: Any = None,
    ) -> None:
        self.schema_name = None
        if schema_name:
            message = f"Schema '{schema_name}' conversion failed: {message}"
        super().__init__(message, source_value=source_value, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        schema_name: str | None = None,
        source_value: Any = None,
        target_type: Any = None,
    ) -> None:
        self.schema_name = schema_name
        if schema_name:
            message = None
        super().__init__(message, source_value=source_value, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_3(
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
        super().__init__(None, source_value=source_value, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_4(
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
        super().__init__(message, source_value=None, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_5(
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
        super().__init__(message, source_value=source_value, target_type=None)

    def xǁSchemaConversionErrorǁ__init____mutmut_6(
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
        super().__init__(source_value=source_value, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_7(
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
        super().__init__(message, target_type=target_type)

    def xǁSchemaConversionErrorǁ__init____mutmut_8(
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
        super().__init__(message, source_value=source_value, )
    
    xǁSchemaConversionErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaConversionErrorǁ__init____mutmut_1': xǁSchemaConversionErrorǁ__init____mutmut_1, 
        'xǁSchemaConversionErrorǁ__init____mutmut_2': xǁSchemaConversionErrorǁ__init____mutmut_2, 
        'xǁSchemaConversionErrorǁ__init____mutmut_3': xǁSchemaConversionErrorǁ__init____mutmut_3, 
        'xǁSchemaConversionErrorǁ__init____mutmut_4': xǁSchemaConversionErrorǁ__init____mutmut_4, 
        'xǁSchemaConversionErrorǁ__init____mutmut_5': xǁSchemaConversionErrorǁ__init____mutmut_5, 
        'xǁSchemaConversionErrorǁ__init____mutmut_6': xǁSchemaConversionErrorǁ__init____mutmut_6, 
        'xǁSchemaConversionErrorǁ__init____mutmut_7': xǁSchemaConversionErrorǁ__init____mutmut_7, 
        'xǁSchemaConversionErrorǁ__init____mutmut_8': xǁSchemaConversionErrorǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaConversionErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaConversionErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaConversionErrorǁ__init____mutmut_orig)
    xǁSchemaConversionErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaConversionErrorǁ__init__'
