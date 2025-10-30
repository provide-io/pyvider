#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from google.protobuf.empty_pb2 import Empty

from pyvider.protocols.tfprotov6.protobuf.tfplugin6_pb2 import (  # Core Protobuf Messages; Schema and Attribute Definitions; Capabilities; Functions; Validation Operations; Planning and State Operations; Read Operations; Ephemeral Resource Operations; Provider Configuration
    ApplyResourceChange,
    AttributePath,
    CallFunction,
    ClientCapabilities,
    CloseEphemeralResource,
    ConfigureProvider,
    Deferred,
    Diagnostic,
    DynamicValue,
    Function,
    FunctionError,
    GetFunctions,
    GetMetadata,
    GetProviderSchema,
    ImportResourceState,
    MoveResourceState,
    OpenEphemeralResource,
    PlanResourceChange,
    RawState,
    ReadDataSource,
    ReadResource,
    RenewEphemeralResource,
    Schema,
    ServerCapabilities,
    StopProvider,
    StringKind,
    UpgradeResourceState,
    ValidateDataResourceConfig,
    ValidateEphemeralResourceConfig,
    ValidateProviderConfig,
    ValidateResourceConfig,
)
from pyvider.protocols.tfprotov6.protobuf.tfplugin6_pb2_grpc import (
    ProviderServicer,
    ProviderStub,
    add_ProviderServicer_to_server,
    add_ProviderServicer_to_server as add_to_server,  # gRPC service definitions
)

__all__ = [
    # Capabilities
    "ApplyResourceChange",
    "AttributePath",
    # Functions
    "CallFunction",
    "ClientCapabilities",
    # Ephemeral Resource Operations
    "CloseEphemeralResource",
    # Provider Configuration
    "ConfigureProvider",
    # Core Protobuf Messages
    "Deferred",
    "Diagnostic",
    "DynamicValue",
    "Empty",
    "Function",
    "FunctionError",
    "GetFunctions",
    "GetMetadata",
    "GetProviderSchema",
    # Planning and State Operations
    "ImportResourceState",
    "MoveResourceState",
    "OpenEphemeralResource",
    "PlanResourceChange",
    # gRPC service definitions
    "ProviderServicer",
    "ProviderStub",
    "RawState",
    # Read Operations
    "ReadDataSource",
    "ReadResource",
    "RenewEphemeralResource",
    # Schema and Attribute Definitions
    "Schema",
    "ServerCapabilities",
    "StopProvider",
    "StringKind",
    "UpgradeResourceState",
    # Validation Operations
    "ValidateDataResourceConfig",
    "ValidateEphemeralResourceConfig",
    "ValidateProviderConfig",
    "ValidateResourceConfig",
    "add_ProviderServicer_to_server",
    "add_to_server",
]

# 🐍🏗️🔚
