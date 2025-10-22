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
class PyviderSchemaError(Exception):
    """Base class for all schema-related errors."""

    pass


class SchemaConversionError(PyviderSchemaError):
    """Error during schema conversion processes."""

    def xǁSchemaConversionErrorǁ__init____mutmut_orig(self, message: str, schema_name: str | None = None, detail: str | None = None) -> None:
        super().__init__(message)
        self.schema_name = schema_name
        self.detail = detail

    def xǁSchemaConversionErrorǁ__init____mutmut_1(self, message: str, schema_name: str | None = None, detail: str | None = None) -> None:
        super().__init__(None)
        self.schema_name = schema_name
        self.detail = detail

    def xǁSchemaConversionErrorǁ__init____mutmut_2(self, message: str, schema_name: str | None = None, detail: str | None = None) -> None:
        super().__init__(message)
        self.schema_name = None
        self.detail = detail

    def xǁSchemaConversionErrorǁ__init____mutmut_3(self, message: str, schema_name: str | None = None, detail: str | None = None) -> None:
        super().__init__(message)
        self.schema_name = schema_name
        self.detail = None
    
    xǁSchemaConversionErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaConversionErrorǁ__init____mutmut_1': xǁSchemaConversionErrorǁ__init____mutmut_1, 
        'xǁSchemaConversionErrorǁ__init____mutmut_2': xǁSchemaConversionErrorǁ__init____mutmut_2, 
        'xǁSchemaConversionErrorǁ__init____mutmut_3': xǁSchemaConversionErrorǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaConversionErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaConversionErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaConversionErrorǁ__init____mutmut_orig)
    xǁSchemaConversionErrorǁ__init____mutmut_orig.__name__ = 'xǁSchemaConversionErrorǁ__init__'

    def xǁSchemaConversionErrorǁ__str____mutmut_orig(self) -> str:
        msg = super().__str__()
        if self.schema_name:
            msg = f"[Schema: {self.schema_name}] {msg}"
        if self.detail:
            msg = f"{msg} (Detail: {self.detail})"
        return msg

    def xǁSchemaConversionErrorǁ__str____mutmut_1(self) -> str:
        msg = None
        if self.schema_name:
            msg = f"[Schema: {self.schema_name}] {msg}"
        if self.detail:
            msg = f"{msg} (Detail: {self.detail})"
        return msg

    def xǁSchemaConversionErrorǁ__str____mutmut_2(self) -> str:
        msg = super().__str__()
        if self.schema_name:
            msg = None
        if self.detail:
            msg = f"{msg} (Detail: {self.detail})"
        return msg

    def xǁSchemaConversionErrorǁ__str____mutmut_3(self) -> str:
        msg = super().__str__()
        if self.schema_name:
            msg = f"[Schema: {self.schema_name}] {msg}"
        if self.detail:
            msg = None
        return msg
    
    xǁSchemaConversionErrorǁ__str____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaConversionErrorǁ__str____mutmut_1': xǁSchemaConversionErrorǁ__str____mutmut_1, 
        'xǁSchemaConversionErrorǁ__str____mutmut_2': xǁSchemaConversionErrorǁ__str____mutmut_2, 
        'xǁSchemaConversionErrorǁ__str____mutmut_3': xǁSchemaConversionErrorǁ__str____mutmut_3
    }
    
    def __str__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaConversionErrorǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSchemaConversionErrorǁ__str____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __str__.__signature__ = _mutmut_signature(xǁSchemaConversionErrorǁ__str____mutmut_orig)
    xǁSchemaConversionErrorǁ__str____mutmut_orig.__name__ = 'xǁSchemaConversionErrorǁ__str__'


class PvsValidationError(PyviderSchemaError):
    """Raised when schema validation fails."""

    pass


class PvsSchemaDefinitionError(PyviderSchemaError):
    """Raised when schema definition is invalid."""

    pass


class PvsAttributeError(PyviderSchemaError):
    """Raised when an attribute definition is invalid."""

    pass


class PvsBlockError(PyviderSchemaError):
    """Raised when a block definition is invalid. (Retained for general block-like errors)."""

    pass
