#
# pyvider/protocols/tfprotov6/handlers/__init__.py
#

from pyvider.protocols.tfprotov6.handlers.apply_resource_change import ApplyResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.call_function import CallFunctionHandler
from pyvider.protocols.tfprotov6.handlers.close_ephemeral_resource import CloseEphemeralResourceHandler
from pyvider.protocols.tfprotov6.handlers.configure_provider import ConfigureProviderHandler
from pyvider.protocols.tfprotov6.handlers.get_functions import GetFunctionsHandler
from pyvider.protocols.tfprotov6.handlers.get_metadata import GetMetadataHandler
from pyvider.protocols.tfprotov6.handlers.get_provider_schema import GetProviderSchemaHandler
from pyvider.protocols.tfprotov6.handlers.import_resource_state import ImportResourceStateHandler
from pyvider.protocols.tfprotov6.handlers.move_resource_state import MoveResourceStateHandler
from pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource import OpenEphemeralResourceHandler
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import PlanResourceChangeHandler
from pyvider.protocols.tfprotov6.handlers.read_data_source import ReadDataSourceHandler
from pyvider.protocols.tfprotov6.handlers.read_resource import ReadResourceHandler
from pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource import RenewEphemeralResourceHandler
from pyvider.protocols.tfprotov6.handlers.stop_provider import StopProviderHandler
from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import UpgradeResourceStateHandler
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    ValidateDataResourceConfigHandler,
)
from pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config import (
    ValidateEphemeralResourceConfigHandler,
)
from pyvider.protocols.tfprotov6.handlers.validate_provider_config import ValidateProviderConfigHandler
from pyvider.protocols.tfprotov6.handlers.validate_resource_config import ValidateResourceConfigHandler

__all__ = [
    "ApplyResourceChangeHandler",
    "CallFunctionHandler",
    "CloseEphemeralResourceHandler",
    "ConfigureProviderHandler",
    "GetFunctionsHandler",
    "GetMetadataHandler",
    "GetProviderSchemaHandler",
    "ImportResourceStateHandler",
    "MoveResourceStateHandler",
    "OpenEphemeralResourceHandler",
    "PlanResourceChangeHandler",
    "ReadDataSourceHandler",
    "ReadResourceHandler",
    "RenewEphemeralResourceHandler",
    "StopProviderHandler",
    "UpgradeResourceStateHandler",
    "ValidateDataResourceConfigHandler",
    "ValidateEphemeralResourceConfigHandler",
    "ValidateProviderConfigHandler",
    "ValidateResourceConfigHandler",
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

# 🐍🏗⛮️
