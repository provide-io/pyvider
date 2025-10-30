#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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

# 🐍🏗️🔚
