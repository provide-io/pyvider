"""
Pyvider Observability Module.

Provides metrics, tracing, and profiling capabilities for the Pyvider framework.
"""

from pyvider.observability.metrics import (
    components_discovered,
    datasource_errors,
    datasource_read_total,
    discovery_duration,
    discovery_errors,
    ephemeral_close_total,
    ephemeral_errors,
    ephemeral_open_total,
    ephemeral_renew_total,
    function_calls,
    function_duration,
    function_errors,
    handler_duration,
    handler_errors,
    handler_requests,
    provider_configure_errors,
    provider_configure_total,
    resource_create_total,
    resource_delete_total,
    resource_errors,
    resource_operations,
    resource_read_total,
    resource_update_total,
    schema_cache_hits,
    schema_generation_duration,
)

__all__ = [
    # Data source metrics
    "components_discovered",
    "datasource_errors",
    "datasource_read_total",
    # Discovery metrics
    "discovery_duration",
    "discovery_errors",
    # Ephemeral metrics
    "ephemeral_close_total",
    "ephemeral_errors",
    "ephemeral_open_total",
    "ephemeral_renew_total",
    # Function metrics
    "function_calls",
    "function_duration",
    "function_errors",
    # Handler metrics
    "handler_duration",
    "handler_errors",
    "handler_requests",
    # Provider metrics
    "provider_configure_errors",
    "provider_configure_total",
    # Resource metrics
    "resource_create_total",
    "resource_delete_total",
    "resource_errors",
    "resource_operations",
    "resource_read_total",
    "resource_update_total",
    # Schema metrics
    "schema_cache_hits",
    "schema_generation_duration",
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
