# pyvider/exceptions/resource.py
from typing import Any

from provide.foundation.errors import (
    NotFoundError as FoundationNotFoundError,
    RuntimeError as FoundationRuntimeError,
    StateError as FoundationStateError,
)

from pyvider.exceptions.base import PluginError, PyviderValueError
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


class ResourceError(PluginError):
    """Base class for resource-related errors."""

    pass


class DataSourceError(ResourceError):
    """Errors specific to data source operations."""

    pass


class CapabilityError(PluginError):  # Or could be ResourceError if capabilities are tied to resources
    """Errors related to component capabilities."""

    pass


class ResourceValidationError(ResourceError, PyviderValueError):
    """Raised when resource configuration or state validation fails."""

    pass


class ResourceNotFoundError(FoundationNotFoundError):
    """Raised when a resource cannot be found."""

    def xǁResourceNotFoundErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RESOURCE_NOT_FOUND"

    def xǁResourceNotFoundErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRESOURCE_NOT_FOUNDXX"

    def xǁResourceNotFoundErrorǁ_default_code__mutmut_2(self) -> str:
        return "resource_not_found"
    
    xǁResourceNotFoundErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceNotFoundErrorǁ_default_code__mutmut_1': xǁResourceNotFoundErrorǁ_default_code__mutmut_1, 
        'xǁResourceNotFoundErrorǁ_default_code__mutmut_2': xǁResourceNotFoundErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceNotFoundErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁResourceNotFoundErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁResourceNotFoundErrorǁ_default_code__mutmut_orig)
    xǁResourceNotFoundErrorǁ_default_code__mutmut_orig.__name__ = 'xǁResourceNotFoundErrorǁ_default_code'


class ResourceOperationError(FoundationRuntimeError):
    """Raised for errors during resource lifecycle operations (plan, apply, etc.)."""

    def xǁResourceOperationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RESOURCE_OPERATION_ERROR"

    def xǁResourceOperationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRESOURCE_OPERATION_ERRORXX"

    def xǁResourceOperationErrorǁ_default_code__mutmut_2(self) -> str:
        return "resource_operation_error"
    
    xǁResourceOperationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceOperationErrorǁ_default_code__mutmut_1': xǁResourceOperationErrorǁ_default_code__mutmut_1, 
        'xǁResourceOperationErrorǁ_default_code__mutmut_2': xǁResourceOperationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceOperationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁResourceOperationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁResourceOperationErrorǁ_default_code__mutmut_orig)
    xǁResourceOperationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁResourceOperationErrorǁ_default_code'


class ResourceLifecycleContractError(FoundationStateError):
    """
    Raised when the state returned by apply() differs from the planned state.
    This indicates a bug in the resource implementation where the outcome of an
    apply operation did not match its proposed plan.
    """

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_orig(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_1(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = None
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_2(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = None
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_3(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault(None, {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_4(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", None)["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_5(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault({})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_6(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", )["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_7(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("XXcontextXX", {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_8(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("CONTEXT", {})["lifecycle.detail"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_9(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["XXlifecycle.detailXX"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_10(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["LIFECYCLE.DETAIL"] = detail
        super().__init__(message, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_11(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(None, **kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_12(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(**kwargs)

    def xǁResourceLifecycleContractErrorǁ__init____mutmut_13(self, message: str, *, detail: str | None = None, **kwargs: Any) -> None:
        self.detail = detail
        if detail:
            kwargs.setdefault("context", {})["lifecycle.detail"] = detail
        super().__init__(message, )
    
    xǁResourceLifecycleContractErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceLifecycleContractErrorǁ__init____mutmut_1': xǁResourceLifecycleContractErrorǁ__init____mutmut_1, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_2': xǁResourceLifecycleContractErrorǁ__init____mutmut_2, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_3': xǁResourceLifecycleContractErrorǁ__init____mutmut_3, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_4': xǁResourceLifecycleContractErrorǁ__init____mutmut_4, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_5': xǁResourceLifecycleContractErrorǁ__init____mutmut_5, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_6': xǁResourceLifecycleContractErrorǁ__init____mutmut_6, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_7': xǁResourceLifecycleContractErrorǁ__init____mutmut_7, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_8': xǁResourceLifecycleContractErrorǁ__init____mutmut_8, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_9': xǁResourceLifecycleContractErrorǁ__init____mutmut_9, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_10': xǁResourceLifecycleContractErrorǁ__init____mutmut_10, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_11': xǁResourceLifecycleContractErrorǁ__init____mutmut_11, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_12': xǁResourceLifecycleContractErrorǁ__init____mutmut_12, 
        'xǁResourceLifecycleContractErrorǁ__init____mutmut_13': xǁResourceLifecycleContractErrorǁ__init____mutmut_13
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceLifecycleContractErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁResourceLifecycleContractErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁResourceLifecycleContractErrorǁ__init____mutmut_orig)
    xǁResourceLifecycleContractErrorǁ__init____mutmut_orig.__name__ = 'xǁResourceLifecycleContractErrorǁ__init__'

    def xǁResourceLifecycleContractErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RESOURCE_LIFECYCLE_CONTRACT_ERROR"

    def xǁResourceLifecycleContractErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRESOURCE_LIFECYCLE_CONTRACT_ERRORXX"

    def xǁResourceLifecycleContractErrorǁ_default_code__mutmut_2(self) -> str:
        return "resource_lifecycle_contract_error"
    
    xǁResourceLifecycleContractErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceLifecycleContractErrorǁ_default_code__mutmut_1': xǁResourceLifecycleContractErrorǁ_default_code__mutmut_1, 
        'xǁResourceLifecycleContractErrorǁ_default_code__mutmut_2': xǁResourceLifecycleContractErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceLifecycleContractErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁResourceLifecycleContractErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁResourceLifecycleContractErrorǁ_default_code__mutmut_orig)
    xǁResourceLifecycleContractErrorǁ_default_code__mutmut_orig.__name__ = 'xǁResourceLifecycleContractErrorǁ_default_code'
