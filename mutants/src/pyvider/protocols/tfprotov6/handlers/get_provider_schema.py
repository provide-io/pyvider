import asyncio
import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import pvs_schema_to_proto
from pyvider.functions.adapters import function_to_dict
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.adapters.function_adapter import (
    dict_to_proto_function,
)
import pyvider.protocols.tfprotov6.protobuf as pb

# --- Module-level Cache using asyncio.Future ---
_schema_future: asyncio.Future[pb.GetProviderSchema.Response] | None = None
_task: asyncio.Task | None = None  # Store a reference to the task
_cache_lock = asyncio.Lock()  # Lock to protect the creation of the Future itself
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


async def x__collect_resource_schemas__mutmut_orig(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_1(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = None
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_2(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components(None).items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_3(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("XXresourceXX").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_4(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("RESOURCE").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_5(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = None
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_6(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = None
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_7(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(None)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_8(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                None
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_9(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=None,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_10(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=None,
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_11(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=None,
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_12(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_13(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    detail=str(e),
                )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_14(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    )
            )
    return resource_schemas


async def x__collect_resource_schemas__mutmut_15(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    for name, resource_class in hub.get_components("resource").items():
        try:
            schema_obj = resource_class.get_schema()
            resource_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for resource '{name}'",
                    detail=str(None),
                )
            )
    return resource_schemas

x__collect_resource_schemas__mutmut_mutants : ClassVar[MutantDict] = {
'x__collect_resource_schemas__mutmut_1': x__collect_resource_schemas__mutmut_1, 
    'x__collect_resource_schemas__mutmut_2': x__collect_resource_schemas__mutmut_2, 
    'x__collect_resource_schemas__mutmut_3': x__collect_resource_schemas__mutmut_3, 
    'x__collect_resource_schemas__mutmut_4': x__collect_resource_schemas__mutmut_4, 
    'x__collect_resource_schemas__mutmut_5': x__collect_resource_schemas__mutmut_5, 
    'x__collect_resource_schemas__mutmut_6': x__collect_resource_schemas__mutmut_6, 
    'x__collect_resource_schemas__mutmut_7': x__collect_resource_schemas__mutmut_7, 
    'x__collect_resource_schemas__mutmut_8': x__collect_resource_schemas__mutmut_8, 
    'x__collect_resource_schemas__mutmut_9': x__collect_resource_schemas__mutmut_9, 
    'x__collect_resource_schemas__mutmut_10': x__collect_resource_schemas__mutmut_10, 
    'x__collect_resource_schemas__mutmut_11': x__collect_resource_schemas__mutmut_11, 
    'x__collect_resource_schemas__mutmut_12': x__collect_resource_schemas__mutmut_12, 
    'x__collect_resource_schemas__mutmut_13': x__collect_resource_schemas__mutmut_13, 
    'x__collect_resource_schemas__mutmut_14': x__collect_resource_schemas__mutmut_14, 
    'x__collect_resource_schemas__mutmut_15': x__collect_resource_schemas__mutmut_15
}

def _collect_resource_schemas(*args, **kwargs):
    result = _mutmut_trampoline(x__collect_resource_schemas__mutmut_orig, x__collect_resource_schemas__mutmut_mutants, args, kwargs)
    return result 

_collect_resource_schemas.__signature__ = _mutmut_signature(x__collect_resource_schemas__mutmut_orig)
x__collect_resource_schemas__mutmut_orig.__name__ = 'x__collect_resource_schemas'


async def x__collect_data_source_schemas__mutmut_orig(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_1(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = None
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_2(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components(None).items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_3(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("XXdata_sourceXX").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_4(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("DATA_SOURCE").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_5(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = None
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_6(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = None
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_7(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(None)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_8(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                None
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_9(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=None,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_10(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=None,
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_11(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=None,
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_12(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_13(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    detail=str(e),
                )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_14(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    )
            )
    return data_source_schemas


async def x__collect_data_source_schemas__mutmut_15(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    for name, ds_class in hub.get_components("data_source").items():
        try:
            schema_obj = ds_class.get_schema()
            data_source_schemas[name] = await pvs_schema_to_proto(schema_obj)
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for data_source '{name}'",
                    detail=str(None),
                )
            )
    return data_source_schemas

x__collect_data_source_schemas__mutmut_mutants : ClassVar[MutantDict] = {
'x__collect_data_source_schemas__mutmut_1': x__collect_data_source_schemas__mutmut_1, 
    'x__collect_data_source_schemas__mutmut_2': x__collect_data_source_schemas__mutmut_2, 
    'x__collect_data_source_schemas__mutmut_3': x__collect_data_source_schemas__mutmut_3, 
    'x__collect_data_source_schemas__mutmut_4': x__collect_data_source_schemas__mutmut_4, 
    'x__collect_data_source_schemas__mutmut_5': x__collect_data_source_schemas__mutmut_5, 
    'x__collect_data_source_schemas__mutmut_6': x__collect_data_source_schemas__mutmut_6, 
    'x__collect_data_source_schemas__mutmut_7': x__collect_data_source_schemas__mutmut_7, 
    'x__collect_data_source_schemas__mutmut_8': x__collect_data_source_schemas__mutmut_8, 
    'x__collect_data_source_schemas__mutmut_9': x__collect_data_source_schemas__mutmut_9, 
    'x__collect_data_source_schemas__mutmut_10': x__collect_data_source_schemas__mutmut_10, 
    'x__collect_data_source_schemas__mutmut_11': x__collect_data_source_schemas__mutmut_11, 
    'x__collect_data_source_schemas__mutmut_12': x__collect_data_source_schemas__mutmut_12, 
    'x__collect_data_source_schemas__mutmut_13': x__collect_data_source_schemas__mutmut_13, 
    'x__collect_data_source_schemas__mutmut_14': x__collect_data_source_schemas__mutmut_14, 
    'x__collect_data_source_schemas__mutmut_15': x__collect_data_source_schemas__mutmut_15
}

def _collect_data_source_schemas(*args, **kwargs):
    result = _mutmut_trampoline(x__collect_data_source_schemas__mutmut_orig, x__collect_data_source_schemas__mutmut_mutants, args, kwargs)
    return result 

_collect_data_source_schemas.__signature__ = _mutmut_signature(x__collect_data_source_schemas__mutmut_orig)
x__collect_data_source_schemas__mutmut_orig.__name__ = 'x__collect_data_source_schemas'


async def x__collect_function_schemas__mutmut_orig(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_1(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = None
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_2(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components(None).items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_3(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("XXfunctionXX").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_4(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("FUNCTION").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_5(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = None
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_6(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(None)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_7(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = None
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_8(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(None)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_9(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = None
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_10(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                None
            )
    return functions


async def x__collect_function_schemas__mutmut_11(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=None,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_12(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=None,
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_13(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=None,
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_14(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_15(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    detail=str(e),
                )
            )
    return functions


async def x__collect_function_schemas__mutmut_16(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    )
            )
    return functions


async def x__collect_function_schemas__mutmut_17(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    for name, func_obj in hub.get_components("function").items():
        try:
            func_dict = function_to_dict(func_obj)
            if func_dict:
                proto_func = dict_to_proto_function(func_dict)
                if proto_func:
                    functions[name] = proto_func
        except Exception as e:
            diagnostics.append(
                pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary=f"Schema collection error for function '{name}'",
                    detail=str(None),
                )
            )
    return functions

x__collect_function_schemas__mutmut_mutants : ClassVar[MutantDict] = {
'x__collect_function_schemas__mutmut_1': x__collect_function_schemas__mutmut_1, 
    'x__collect_function_schemas__mutmut_2': x__collect_function_schemas__mutmut_2, 
    'x__collect_function_schemas__mutmut_3': x__collect_function_schemas__mutmut_3, 
    'x__collect_function_schemas__mutmut_4': x__collect_function_schemas__mutmut_4, 
    'x__collect_function_schemas__mutmut_5': x__collect_function_schemas__mutmut_5, 
    'x__collect_function_schemas__mutmut_6': x__collect_function_schemas__mutmut_6, 
    'x__collect_function_schemas__mutmut_7': x__collect_function_schemas__mutmut_7, 
    'x__collect_function_schemas__mutmut_8': x__collect_function_schemas__mutmut_8, 
    'x__collect_function_schemas__mutmut_9': x__collect_function_schemas__mutmut_9, 
    'x__collect_function_schemas__mutmut_10': x__collect_function_schemas__mutmut_10, 
    'x__collect_function_schemas__mutmut_11': x__collect_function_schemas__mutmut_11, 
    'x__collect_function_schemas__mutmut_12': x__collect_function_schemas__mutmut_12, 
    'x__collect_function_schemas__mutmut_13': x__collect_function_schemas__mutmut_13, 
    'x__collect_function_schemas__mutmut_14': x__collect_function_schemas__mutmut_14, 
    'x__collect_function_schemas__mutmut_15': x__collect_function_schemas__mutmut_15, 
    'x__collect_function_schemas__mutmut_16': x__collect_function_schemas__mutmut_16, 
    'x__collect_function_schemas__mutmut_17': x__collect_function_schemas__mutmut_17
}

def _collect_function_schemas(*args, **kwargs):
    result = _mutmut_trampoline(x__collect_function_schemas__mutmut_orig, x__collect_function_schemas__mutmut_mutants, args, kwargs)
    return result 

_collect_function_schemas.__signature__ = _mutmut_signature(x__collect_function_schemas__mutmut_orig)
x__collect_function_schemas__mutmut_orig.__name__ = 'x__collect_function_schemas'


async def x__compute_schema_once__mutmut_orig() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_1() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug(None)
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_2() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("XXComputing and caching provider schema for the first time...XX")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_3() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_4() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("COMPUTING AND CACHING PROVIDER SCHEMA FOR THE FIRST TIME...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_5() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = None
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_6() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = None
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_7() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component(None, "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_8() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", None)
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_9() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_10() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", )
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_11() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("XXsingletonXX", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_12() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("SINGLETON", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_13() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "XXproviderXX")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_14() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "PROVIDER")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_15() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_16() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError(None)

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_17() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("XXProvider instance not found in hub. Setup may have failed.XX")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_18() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("provider instance not found in hub. setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_19() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("PROVIDER INSTANCE NOT FOUND IN HUB. SETUP MAY HAVE FAILED.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_20() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = None
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_21() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = None

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_22() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(None)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_23() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = None
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_24() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(None)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_25() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = None
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_26() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(None)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_27() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = None

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_28() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(None)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_29() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = None
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_30() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=None,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_31() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=None,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_32() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=None,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_33() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=None,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_34() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=None,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_35() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_36() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_37() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_38() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_39() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_40() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info(None)
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_41() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("XXProvider schema has been computed successfully.XX")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_42() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_43() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("PROVIDER SCHEMA HAS BEEN COMPUTED SUCCESSFULLY.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_44() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(None, exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_45() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=None)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_46() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_47() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", )
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_48() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=False)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_49() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=None
        )


async def x__compute_schema_once__mutmut_50() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=None,
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_51() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary=None,
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_52() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=None,
                )
            ]
        )


async def x__compute_schema_once__mutmut_53() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    summary="Failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_54() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_55() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    )
            ]
        )


async def x__compute_schema_once__mutmut_56() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="XXFailed to compute provider schemaXX",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_57() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="failed to compute provider schema",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_58() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="FAILED TO COMPUTE PROVIDER SCHEMA",
                    detail=str(e),
                )
            ]
        )


async def x__compute_schema_once__mutmut_59() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug("Computing and caching provider schema for the first time...")
    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub. Setup may have failed.")

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        resource_schemas = await _collect_resource_schemas(diagnostics)
        data_source_schemas = await _collect_data_source_schemas(diagnostics)
        functions = await _collect_function_schemas(diagnostics)

        response = pb.GetProviderSchema.Response(
            provider=provider_proto_schema,
            resource_schemas=resource_schemas,
            data_source_schemas=data_source_schemas,
            functions=functions,
            diagnostics=diagnostics,
        )
        logger.info("Provider schema has been computed successfully.")
        return response

    except Exception as e:
        logger.error(f"Failed to compute provider schema: {e}", exc_info=True)
        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Failed to compute provider schema",
                    detail=str(None),
                )
            ]
        )

x__compute_schema_once__mutmut_mutants : ClassVar[MutantDict] = {
'x__compute_schema_once__mutmut_1': x__compute_schema_once__mutmut_1, 
    'x__compute_schema_once__mutmut_2': x__compute_schema_once__mutmut_2, 
    'x__compute_schema_once__mutmut_3': x__compute_schema_once__mutmut_3, 
    'x__compute_schema_once__mutmut_4': x__compute_schema_once__mutmut_4, 
    'x__compute_schema_once__mutmut_5': x__compute_schema_once__mutmut_5, 
    'x__compute_schema_once__mutmut_6': x__compute_schema_once__mutmut_6, 
    'x__compute_schema_once__mutmut_7': x__compute_schema_once__mutmut_7, 
    'x__compute_schema_once__mutmut_8': x__compute_schema_once__mutmut_8, 
    'x__compute_schema_once__mutmut_9': x__compute_schema_once__mutmut_9, 
    'x__compute_schema_once__mutmut_10': x__compute_schema_once__mutmut_10, 
    'x__compute_schema_once__mutmut_11': x__compute_schema_once__mutmut_11, 
    'x__compute_schema_once__mutmut_12': x__compute_schema_once__mutmut_12, 
    'x__compute_schema_once__mutmut_13': x__compute_schema_once__mutmut_13, 
    'x__compute_schema_once__mutmut_14': x__compute_schema_once__mutmut_14, 
    'x__compute_schema_once__mutmut_15': x__compute_schema_once__mutmut_15, 
    'x__compute_schema_once__mutmut_16': x__compute_schema_once__mutmut_16, 
    'x__compute_schema_once__mutmut_17': x__compute_schema_once__mutmut_17, 
    'x__compute_schema_once__mutmut_18': x__compute_schema_once__mutmut_18, 
    'x__compute_schema_once__mutmut_19': x__compute_schema_once__mutmut_19, 
    'x__compute_schema_once__mutmut_20': x__compute_schema_once__mutmut_20, 
    'x__compute_schema_once__mutmut_21': x__compute_schema_once__mutmut_21, 
    'x__compute_schema_once__mutmut_22': x__compute_schema_once__mutmut_22, 
    'x__compute_schema_once__mutmut_23': x__compute_schema_once__mutmut_23, 
    'x__compute_schema_once__mutmut_24': x__compute_schema_once__mutmut_24, 
    'x__compute_schema_once__mutmut_25': x__compute_schema_once__mutmut_25, 
    'x__compute_schema_once__mutmut_26': x__compute_schema_once__mutmut_26, 
    'x__compute_schema_once__mutmut_27': x__compute_schema_once__mutmut_27, 
    'x__compute_schema_once__mutmut_28': x__compute_schema_once__mutmut_28, 
    'x__compute_schema_once__mutmut_29': x__compute_schema_once__mutmut_29, 
    'x__compute_schema_once__mutmut_30': x__compute_schema_once__mutmut_30, 
    'x__compute_schema_once__mutmut_31': x__compute_schema_once__mutmut_31, 
    'x__compute_schema_once__mutmut_32': x__compute_schema_once__mutmut_32, 
    'x__compute_schema_once__mutmut_33': x__compute_schema_once__mutmut_33, 
    'x__compute_schema_once__mutmut_34': x__compute_schema_once__mutmut_34, 
    'x__compute_schema_once__mutmut_35': x__compute_schema_once__mutmut_35, 
    'x__compute_schema_once__mutmut_36': x__compute_schema_once__mutmut_36, 
    'x__compute_schema_once__mutmut_37': x__compute_schema_once__mutmut_37, 
    'x__compute_schema_once__mutmut_38': x__compute_schema_once__mutmut_38, 
    'x__compute_schema_once__mutmut_39': x__compute_schema_once__mutmut_39, 
    'x__compute_schema_once__mutmut_40': x__compute_schema_once__mutmut_40, 
    'x__compute_schema_once__mutmut_41': x__compute_schema_once__mutmut_41, 
    'x__compute_schema_once__mutmut_42': x__compute_schema_once__mutmut_42, 
    'x__compute_schema_once__mutmut_43': x__compute_schema_once__mutmut_43, 
    'x__compute_schema_once__mutmut_44': x__compute_schema_once__mutmut_44, 
    'x__compute_schema_once__mutmut_45': x__compute_schema_once__mutmut_45, 
    'x__compute_schema_once__mutmut_46': x__compute_schema_once__mutmut_46, 
    'x__compute_schema_once__mutmut_47': x__compute_schema_once__mutmut_47, 
    'x__compute_schema_once__mutmut_48': x__compute_schema_once__mutmut_48, 
    'x__compute_schema_once__mutmut_49': x__compute_schema_once__mutmut_49, 
    'x__compute_schema_once__mutmut_50': x__compute_schema_once__mutmut_50, 
    'x__compute_schema_once__mutmut_51': x__compute_schema_once__mutmut_51, 
    'x__compute_schema_once__mutmut_52': x__compute_schema_once__mutmut_52, 
    'x__compute_schema_once__mutmut_53': x__compute_schema_once__mutmut_53, 
    'x__compute_schema_once__mutmut_54': x__compute_schema_once__mutmut_54, 
    'x__compute_schema_once__mutmut_55': x__compute_schema_once__mutmut_55, 
    'x__compute_schema_once__mutmut_56': x__compute_schema_once__mutmut_56, 
    'x__compute_schema_once__mutmut_57': x__compute_schema_once__mutmut_57, 
    'x__compute_schema_once__mutmut_58': x__compute_schema_once__mutmut_58, 
    'x__compute_schema_once__mutmut_59': x__compute_schema_once__mutmut_59
}

def _compute_schema_once(*args, **kwargs):
    result = _mutmut_trampoline(x__compute_schema_once__mutmut_orig, x__compute_schema_once__mutmut_mutants, args, kwargs)
    return result 

_compute_schema_once.__signature__ = _mutmut_signature(x__compute_schema_once__mutmut_orig)
x__compute_schema_once__mutmut_orig.__name__ = 'x__compute_schema_once'


@resilient()
async def GetProviderSchemaHandler(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """
    Handles the GetProviderSchema RPC request using a robust, race-condition-free
    asyncio.Future to ensure the schema is computed only once.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="GetProviderSchema")

    try:
        return await _get_provider_schema_impl(request, context)
    except Exception:
        handler_errors.inc(handler="GetProviderSchema")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="GetProviderSchema")


async def x__get_provider_schema_impl__mutmut_orig(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_1(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug(None)

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_2(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("XXGetProviderSchema handler called, checking cache future.XX")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_3(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("getproviderschema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_4(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GETPROVIDERSCHEMA HANDLER CALLED, CHECKING CACHE FUTURE.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_5(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is not None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_6(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug(None)
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_7(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("XXNo existing schema future found. Creating one.XX")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_8(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("no existing schema future found. creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_9(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("NO EXISTING SCHEMA FUTURE FOUND. CREATING ONE.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_10(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = None
            global _task
            _task = asyncio.create_task(_set_future_result(_schema_future))

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_11(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = None

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_12(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(None)

    # All concurrent callers will await the same Future object.
    return await _schema_future


async def x__get_provider_schema_impl__mutmut_13(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug("GetProviderSchema handler called, checking cache future.")

    # Use a lock to protect the initial creation of the Future object itself.
    # This is a very short-lived lock.
    async with _cache_lock:
        if _schema_future is None:
            logger.debug("No existing schema future found. Creating one.")
            # Create the Future and schedule the expensive computation to run.
            _schema_future = asyncio.Future()
            global _task
            _task = asyncio.create_task(_set_future_result(None))

    # All concurrent callers will await the same Future object.
    return await _schema_future

x__get_provider_schema_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_provider_schema_impl__mutmut_1': x__get_provider_schema_impl__mutmut_1, 
    'x__get_provider_schema_impl__mutmut_2': x__get_provider_schema_impl__mutmut_2, 
    'x__get_provider_schema_impl__mutmut_3': x__get_provider_schema_impl__mutmut_3, 
    'x__get_provider_schema_impl__mutmut_4': x__get_provider_schema_impl__mutmut_4, 
    'x__get_provider_schema_impl__mutmut_5': x__get_provider_schema_impl__mutmut_5, 
    'x__get_provider_schema_impl__mutmut_6': x__get_provider_schema_impl__mutmut_6, 
    'x__get_provider_schema_impl__mutmut_7': x__get_provider_schema_impl__mutmut_7, 
    'x__get_provider_schema_impl__mutmut_8': x__get_provider_schema_impl__mutmut_8, 
    'x__get_provider_schema_impl__mutmut_9': x__get_provider_schema_impl__mutmut_9, 
    'x__get_provider_schema_impl__mutmut_10': x__get_provider_schema_impl__mutmut_10, 
    'x__get_provider_schema_impl__mutmut_11': x__get_provider_schema_impl__mutmut_11, 
    'x__get_provider_schema_impl__mutmut_12': x__get_provider_schema_impl__mutmut_12, 
    'x__get_provider_schema_impl__mutmut_13': x__get_provider_schema_impl__mutmut_13
}

def _get_provider_schema_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__get_provider_schema_impl__mutmut_orig, x__get_provider_schema_impl__mutmut_mutants, args, kwargs)
    return result 

_get_provider_schema_impl.__signature__ = _mutmut_signature(x__get_provider_schema_impl__mutmut_orig)
x__get_provider_schema_impl__mutmut_orig.__name__ = 'x__get_provider_schema_impl'


async def x__set_future_result__mutmut_orig(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_1(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = None
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_2(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(None)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_3(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical(None, exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_4(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=None)
        future.set_exception(e)


async def x__set_future_result__mutmut_5(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical(exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_6(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", )
        future.set_exception(e)


async def x__set_future_result__mutmut_7(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("XXCatastrophic failure during schema computation task.XX", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_8(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_9(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("CATASTROPHIC FAILURE DURING SCHEMA COMPUTATION TASK.", exc_info=True)
        future.set_exception(e)


async def x__set_future_result__mutmut_10(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=False)
        future.set_exception(e)


async def x__set_future_result__mutmut_11(future: asyncio.Future) -> None:
    """
    A helper coroutine that runs the computation and sets the result
    on the shared Future object, unblocking all awaiters.
    """
    try:
        result = await _compute_schema_once()
        future.set_result(result)
    except Exception as e:
        logger.critical("Catastrophic failure during schema computation task.", exc_info=True)
        future.set_exception(None)

x__set_future_result__mutmut_mutants : ClassVar[MutantDict] = {
'x__set_future_result__mutmut_1': x__set_future_result__mutmut_1, 
    'x__set_future_result__mutmut_2': x__set_future_result__mutmut_2, 
    'x__set_future_result__mutmut_3': x__set_future_result__mutmut_3, 
    'x__set_future_result__mutmut_4': x__set_future_result__mutmut_4, 
    'x__set_future_result__mutmut_5': x__set_future_result__mutmut_5, 
    'x__set_future_result__mutmut_6': x__set_future_result__mutmut_6, 
    'x__set_future_result__mutmut_7': x__set_future_result__mutmut_7, 
    'x__set_future_result__mutmut_8': x__set_future_result__mutmut_8, 
    'x__set_future_result__mutmut_9': x__set_future_result__mutmut_9, 
    'x__set_future_result__mutmut_10': x__set_future_result__mutmut_10, 
    'x__set_future_result__mutmut_11': x__set_future_result__mutmut_11
}

def _set_future_result(*args, **kwargs):
    result = _mutmut_trampoline(x__set_future_result__mutmut_orig, x__set_future_result__mutmut_mutants, args, kwargs)
    return result 

_set_future_result.__signature__ = _mutmut_signature(x__set_future_result__mutmut_orig)
x__set_future_result__mutmut_orig.__name__ = 'x__set_future_result'
