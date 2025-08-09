#
# pyvider/exceptions/__init__.py
#
"""Pyvider Framework Custom Exceptions"""

from .base import (
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
from .function import (
    FunctionError,
    FunctionRegistrationError,
    FunctionValidationError,
)
from .grpc import (
    GRPCConnectionError,
    GRPCError,
    NetworkError,
    RateLimitError,
)
from .provider import (
    ProviderConfigurationError,
    ProviderError,
    ProviderInitializationError,
)
from .registry import (
    ComponentRegistryError,
    ValidatorRegistrationError,
)
from .resource import (
    CapabilityError,
    DataSourceError,
    ResourceError,
    ResourceLifecycleContractError,
    ResourceNotFoundError,
    ResourceOperationError,
    ResourceValidationError,
)
from .schema import (
    SchemaConversionError,
    SchemaError,
    SchemaParseError,
    SchemaRegistrationError,
    SchemaValidationError,
)
from .serialization import (
    DeserializationError,
    SerializationError,
)
from .validation import (
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

# 🐍🏗️


# 🐍🏗️🚀🪄
