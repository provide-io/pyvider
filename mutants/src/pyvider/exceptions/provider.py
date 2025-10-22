# pyvider/exceptions/provider.py
from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    RuntimeError as FoundationRuntimeError,
)

from pyvider.exceptions.base import ComponentConfigurationError
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


class ProviderError(FoundationConfigurationError):
    """Base class for provider-specific errors."""

    def xǁProviderErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PROVIDER_ERROR"

    def xǁProviderErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPROVIDER_ERRORXX"

    def xǁProviderErrorǁ_default_code__mutmut_2(self) -> str:
        return "provider_error"
    
    xǁProviderErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProviderErrorǁ_default_code__mutmut_1': xǁProviderErrorǁ_default_code__mutmut_1, 
        'xǁProviderErrorǁ_default_code__mutmut_2': xǁProviderErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProviderErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁProviderErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁProviderErrorǁ_default_code__mutmut_orig)
    xǁProviderErrorǁ_default_code__mutmut_orig.__name__ = 'xǁProviderErrorǁ_default_code'


class ProviderConfigurationError(ProviderError, ComponentConfigurationError):
    """Raised when provider configuration is invalid."""

    pass


class ProviderInitializationError(FoundationRuntimeError):
    """Raised when provider initialization fails."""

    def xǁProviderInitializationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PROVIDER_INITIALIZATION_ERROR"

    def xǁProviderInitializationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPROVIDER_INITIALIZATION_ERRORXX"

    def xǁProviderInitializationErrorǁ_default_code__mutmut_2(self) -> str:
        return "provider_initialization_error"
    
    xǁProviderInitializationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProviderInitializationErrorǁ_default_code__mutmut_1': xǁProviderInitializationErrorǁ_default_code__mutmut_1, 
        'xǁProviderInitializationErrorǁ_default_code__mutmut_2': xǁProviderInitializationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProviderInitializationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁProviderInitializationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁProviderInitializationErrorǁ_default_code__mutmut_orig)
    xǁProviderInitializationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁProviderInitializationErrorǁ_default_code'
