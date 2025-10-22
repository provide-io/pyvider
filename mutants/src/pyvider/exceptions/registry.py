# pyvider/exceptions/registry.py
from provide.foundation.errors import ConfigurationError as FoundationConfigurationError
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


class ComponentRegistryError(FoundationConfigurationError):
    """Raised for errors during component registration or retrieval."""

    def xǁComponentRegistryErrorǁ_default_code__mutmut_orig(self) -> str:
        return "COMPONENT_REGISTRY_ERROR"

    def xǁComponentRegistryErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCOMPONENT_REGISTRY_ERRORXX"

    def xǁComponentRegistryErrorǁ_default_code__mutmut_2(self) -> str:
        return "component_registry_error"
    
    xǁComponentRegistryErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentRegistryErrorǁ_default_code__mutmut_1': xǁComponentRegistryErrorǁ_default_code__mutmut_1, 
        'xǁComponentRegistryErrorǁ_default_code__mutmut_2': xǁComponentRegistryErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentRegistryErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁComponentRegistryErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁComponentRegistryErrorǁ_default_code__mutmut_orig)
    xǁComponentRegistryErrorǁ_default_code__mutmut_orig.__name__ = 'xǁComponentRegistryErrorǁ_default_code'


class ValidatorRegistrationError(FoundationConfigurationError):
    """Raised when a non-callable is registered as a validator, or other validator issues."""

    def xǁValidatorRegistrationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "VALIDATOR_REGISTRATION_ERROR"

    def xǁValidatorRegistrationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXVALIDATOR_REGISTRATION_ERRORXX"

    def xǁValidatorRegistrationErrorǁ_default_code__mutmut_2(self) -> str:
        return "validator_registration_error"
    
    xǁValidatorRegistrationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidatorRegistrationErrorǁ_default_code__mutmut_1': xǁValidatorRegistrationErrorǁ_default_code__mutmut_1, 
        'xǁValidatorRegistrationErrorǁ_default_code__mutmut_2': xǁValidatorRegistrationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidatorRegistrationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁValidatorRegistrationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁValidatorRegistrationErrorǁ_default_code__mutmut_orig)
    xǁValidatorRegistrationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁValidatorRegistrationErrorǁ_default_code'
