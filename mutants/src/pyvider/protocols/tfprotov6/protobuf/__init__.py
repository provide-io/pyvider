#
# protocols/tfprotov6/__init__.py
#

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
