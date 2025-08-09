#
# pyvider/protocols/tfprotov6/protobuf/__init__.py
#
from google.protobuf.empty_pb2 import Empty

from .tfplugin6_pb2 import (  # Core Protobuf Messages; Schema and Attribute Definitions; Capabilities; Functions; Validation Operations; Planning and State Operations; Read Operations; Ephemeral Resource Operations; Provider Configuration
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
from .tfplugin6_pb2_grpc import (
    ProviderServicer,
    ProviderStub,
    add_ProviderServicer_to_server,
    add_ProviderServicer_to_server as add_to_server,  # gRPC service definitions
)

__all__ = [
    # Core Protobuf Messages
    "DynamicValue",
    "Diagnostic",
    "Deferred",
    "RawState",
    # Schema and Attribute Definitions
    "Schema",
    "AttributePath",
    "StringKind",
    "Empty",
    # Capabilities
    "ServerCapabilities",
    "ClientCapabilities",
    # Functions
    "Function",
    "FunctionError",
    "GetFunctions",
    "CallFunction",
    # Validation Operations
    "ValidateResourceConfig",
    "ValidateDataResourceConfig",
    "ValidateEphemeralResourceConfig",
    # Planning and State Operations
    "PlanResourceChange",
    "ApplyResourceChange",
    "UpgradeResourceState",
    "MoveResourceState",
    "ImportResourceState",
    # Read Operations
    "ReadResource",
    "ReadDataSource",
    # Ephemeral Resource Operations
    "OpenEphemeralResource",
    "RenewEphemeralResource",
    "CloseEphemeralResource",
    # Provider Configuration
    "GetMetadata",
    "GetProviderSchema",
    "ValidateProviderConfig",
    "ConfigureProvider",
    "StopProvider",
    # gRPC service definitions
    "ProviderServicer",
    "ProviderStub",
    "add_ProviderServicer_to_server",
    "add_to_server",
]

# 🐍🏗️


# 🐍🏗️🚀🪄
