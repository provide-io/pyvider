# pyvider/exceptions/__init__.py
"""Pyvider Framework Custom Exceptions"""

from pyvider.exceptions.base import (
    ComponentConfigurationError,
    ConversionError,
    FrameworkConfigurationError,
    InvalidTypeError,
    PluginError,
    PyviderError,
    PyviderValueError,
    UnsupportedTypeError,
    WireFormatError,
)
from pyvider.exceptions.function import (
    FunctionError,
    FunctionRegistrationError,
    FunctionValidationError,
)
from pyvider.exceptions.grpc import (
    GRPCConnectionError,
    GRPCError,
    NetworkError,
    RateLimitError,
)
from pyvider.exceptions.provider import (
    ProviderConfigurationError,
    ProviderError,
    ProviderInitializationError,
)
from pyvider.exceptions.registry import (
    ComponentRegistryError,
    ValidatorRegistrationError,
)
from pyvider.exceptions.resource import (
    CapabilityError,
    DataSourceError,
    ResourceError,
    ResourceLifecycleContractError,
    ResourceNotFoundError,
    ResourceOperationError,
    ResourceValidationError,
)
from pyvider.exceptions.schema import (
    SchemaConversionError,
    SchemaError,
    SchemaParseError,
    SchemaRegistrationError,
    SchemaValidationError,
)
from pyvider.exceptions.serialization import (
    DeserializationError,
    SerializationError,
)
from pyvider.exceptions.validation import (
    AttributeValidationError,
    ValidationError,
)

__all__ = [
    "AttributeValidationError",
    "CapabilityError",
    "ComponentConfigurationError",
    # Registry
    "ComponentRegistryError",
    "ConversionError",
    "DataSourceError",
    "DeserializationError",
    "FrameworkConfigurationError",
    # Function
    "FunctionError",
    "FunctionRegistrationError",
    "FunctionValidationError",
    "GRPCConnectionError",
    # gRPC
    "GRPCError",
    "InvalidTypeError",
    "NetworkError",
    "PluginError",
    "ProviderConfigurationError",
    # Provider
    "ProviderError",
    "ProviderInitializationError",
    # Base
    "PyviderError",
    "PyviderValueError",
    "RateLimitError",
    # Resource
    "ResourceError",
    "ResourceLifecycleContractError",
    "ResourceNotFoundError",
    "ResourceOperationError",
    "ResourceValidationError",
    "SchemaConversionError",
    # Schema
    "SchemaError",
    "SchemaParseError",
    "SchemaRegistrationError",
    "SchemaValidationError",
    # Serialization
    "SerializationError",
    "UnsupportedTypeError",
    # Validation
    "ValidationError",
    "ValidatorRegistrationError",
    "WireFormatError",
]
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

# 🐍🏗️
