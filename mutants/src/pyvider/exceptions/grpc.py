# pyvider/exceptions/grpc.py
from provide.foundation.errors import NetworkError as FoundationNetworkError

from pyvider.exceptions.base import PluginError
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


class GRPCError(PluginError):
    """Base class for gRPC-related errors."""

    def xǁGRPCErrorǁ_default_code__mutmut_orig(self) -> str:
        return "GRPC_ERROR"

    def xǁGRPCErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXGRPC_ERRORXX"

    def xǁGRPCErrorǁ_default_code__mutmut_2(self) -> str:
        return "grpc_error"
    
    xǁGRPCErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGRPCErrorǁ_default_code__mutmut_1': xǁGRPCErrorǁ_default_code__mutmut_1, 
        'xǁGRPCErrorǁ_default_code__mutmut_2': xǁGRPCErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGRPCErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁGRPCErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁGRPCErrorǁ_default_code__mutmut_orig)
    xǁGRPCErrorǁ_default_code__mutmut_orig.__name__ = 'xǁGRPCErrorǁ_default_code'


class GRPCConnectionError(GRPCError):
    """Raised when a gRPC connection fails."""

    def xǁGRPCConnectionErrorǁ_default_code__mutmut_orig(self) -> str:
        return "GRPC_CONNECTION_ERROR"

    def xǁGRPCConnectionErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXGRPC_CONNECTION_ERRORXX"

    def xǁGRPCConnectionErrorǁ_default_code__mutmut_2(self) -> str:
        return "grpc_connection_error"
    
    xǁGRPCConnectionErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGRPCConnectionErrorǁ_default_code__mutmut_1': xǁGRPCConnectionErrorǁ_default_code__mutmut_1, 
        'xǁGRPCConnectionErrorǁ_default_code__mutmut_2': xǁGRPCConnectionErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGRPCConnectionErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁGRPCConnectionErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁGRPCConnectionErrorǁ_default_code__mutmut_orig)
    xǁGRPCConnectionErrorǁ_default_code__mutmut_orig.__name__ = 'xǁGRPCConnectionErrorǁ_default_code'


class NetworkError(FoundationNetworkError):
    """Raised for general gRPC network issues.

    Inherits directly from foundation's NetworkError for
    automatic retry and circuit breaker support.
    """

    def xǁNetworkErrorǁ_default_code__mutmut_orig(self) -> str:
        return "NETWORK_ERROR"

    def xǁNetworkErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXNETWORK_ERRORXX"

    def xǁNetworkErrorǁ_default_code__mutmut_2(self) -> str:
        return "network_error"
    
    xǁNetworkErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁNetworkErrorǁ_default_code__mutmut_1': xǁNetworkErrorǁ_default_code__mutmut_1, 
        'xǁNetworkErrorǁ_default_code__mutmut_2': xǁNetworkErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁNetworkErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁNetworkErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁNetworkErrorǁ_default_code__mutmut_orig)
    xǁNetworkErrorǁ_default_code__mutmut_orig.__name__ = 'xǁNetworkErrorǁ_default_code'


class RateLimitError(NetworkError):
    """Raised when a gRPC operation is rate-limited."""

    def xǁRateLimitErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RATE_LIMIT_ERROR"

    def xǁRateLimitErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRATE_LIMIT_ERRORXX"

    def xǁRateLimitErrorǁ_default_code__mutmut_2(self) -> str:
        return "rate_limit_error"
    
    xǁRateLimitErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitErrorǁ_default_code__mutmut_1': xǁRateLimitErrorǁ_default_code__mutmut_1, 
        'xǁRateLimitErrorǁ_default_code__mutmut_2': xǁRateLimitErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁRateLimitErrorǁ_default_code__mutmut_orig)
    xǁRateLimitErrorǁ_default_code__mutmut_orig.__name__ = 'xǁRateLimitErrorǁ_default_code'
