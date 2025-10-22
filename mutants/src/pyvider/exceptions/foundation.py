#
# pyvider/exceptions/foundation.py
#


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
class PyviderError(Exception):
    """Base class for all Pyvider errors."""

    pass


class CapabilityError(PyviderError):
    pass


class ValueError(PyviderError):
    pass


class ConfigurationError(PyviderError):
    pass


class DataSourceError(PyviderError):
    pass


class FunctionError(PyviderError):
    pass


class InvalidTypeError(PyviderError):
    """Raised when a value does not match the expected type."""

    def xǁInvalidTypeErrorǁ__init____mutmut_orig(self, expected_type: str = "unknown", actual_type: str = "unknown") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")

    def xǁInvalidTypeErrorǁ__init____mutmut_1(self, expected_type: str = "XXunknownXX", actual_type: str = "unknown") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")

    def xǁInvalidTypeErrorǁ__init____mutmut_2(self, expected_type: str = "UNKNOWN", actual_type: str = "unknown") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")

    def xǁInvalidTypeErrorǁ__init____mutmut_3(self, expected_type: str = "unknown", actual_type: str = "XXunknownXX") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")

    def xǁInvalidTypeErrorǁ__init____mutmut_4(self, expected_type: str = "unknown", actual_type: str = "UNKNOWN") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")

    def xǁInvalidTypeErrorǁ__init____mutmut_5(self, expected_type: str = "unknown", actual_type: str = "unknown") -> None:
        super().__init__(None)
    
    xǁInvalidTypeErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInvalidTypeErrorǁ__init____mutmut_1': xǁInvalidTypeErrorǁ__init____mutmut_1, 
        'xǁInvalidTypeErrorǁ__init____mutmut_2': xǁInvalidTypeErrorǁ__init____mutmut_2, 
        'xǁInvalidTypeErrorǁ__init____mutmut_3': xǁInvalidTypeErrorǁ__init____mutmut_3, 
        'xǁInvalidTypeErrorǁ__init____mutmut_4': xǁInvalidTypeErrorǁ__init____mutmut_4, 
        'xǁInvalidTypeErrorǁ__init____mutmut_5': xǁInvalidTypeErrorǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInvalidTypeErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInvalidTypeErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInvalidTypeErrorǁ__init____mutmut_orig)
    xǁInvalidTypeErrorǁ__init____mutmut_orig.__name__ = 'xǁInvalidTypeErrorǁ__init__'


class UnsupportedTypeError(PyviderError):
    """Raised when an unsupported type is encountered."""

    def xǁUnsupportedTypeErrorǁ__init____mutmut_orig(self, type_name: str = "unknown") -> None:
        super().__init__(f"Unsupported type encountered: '{type_name}'.")

    def xǁUnsupportedTypeErrorǁ__init____mutmut_1(self, type_name: str = "XXunknownXX") -> None:
        super().__init__(f"Unsupported type encountered: '{type_name}'.")

    def xǁUnsupportedTypeErrorǁ__init____mutmut_2(self, type_name: str = "UNKNOWN") -> None:
        super().__init__(f"Unsupported type encountered: '{type_name}'.")

    def xǁUnsupportedTypeErrorǁ__init____mutmut_3(self, type_name: str = "unknown") -> None:
        super().__init__(None)
    
    xǁUnsupportedTypeErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnsupportedTypeErrorǁ__init____mutmut_1': xǁUnsupportedTypeErrorǁ__init____mutmut_1, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_2': xǁUnsupportedTypeErrorǁ__init____mutmut_2, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_3': xǁUnsupportedTypeErrorǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁUnsupportedTypeErrorǁ__init____mutmut_orig)
    xǁUnsupportedTypeErrorǁ__init____mutmut_orig.__name__ = 'xǁUnsupportedTypeErrorǁ__init__'


# 🐍🏗
