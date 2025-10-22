import time
from typing import Any

import attrs
import msgpack
from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.common.encryption import decrypt, encrypt
from pyvider.common.operation_context import OperationContext, operation_context
from pyvider.conversion import marshal, unmarshal
from pyvider.conversion.marshaler import _apply_schema_marks_iterative
from pyvider.cty import CtyObject, CtyValue
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
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


async def x__get_resource_and_provider_instances__mutmut_orig(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_1(type_name: str) -> tuple[Any, Any]:
    resource_class = None
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_2(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component(None, type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_3(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", None)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_4(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component(type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_5(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", )
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_6(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("XXresourceXX", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_7(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("RESOURCE", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_8(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_9(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = None
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_10(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(None)
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_11(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context(None, type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_12(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", None)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_13(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context(type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_14(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", )
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_15(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("XXresource.type_nameXX", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_16(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("RESOURCE.TYPE_NAME", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_17(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context(None, "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_18(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", None)
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_19(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_20(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", )
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_21(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("XXterraform.summaryXX", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_22(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("TERRAFORM.SUMMARY", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_23(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "XXUnknown resource typeXX")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_24(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_25(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "UNKNOWN RESOURCE TYPE")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_26(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            None, f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_27(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", None
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_28(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_29(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_30(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "XXterraform.detailXX", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_31(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "TERRAFORM.DETAIL", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_32(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = None
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_33(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component(None, "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_34(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", None)
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_35(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_36(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", )
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_37(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("XXsingletonXX", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_38(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("SINGLETON", "provider")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_39(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "XXproviderXX")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_40(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "PROVIDER")
    if not provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_41(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if provider_instance:
        raise RuntimeError("Provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_42(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError(None)
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_43(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("XXProvider instance not found in hub.XX")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_44(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("provider instance not found in hub.")
    return resource_class, provider_instance


async def x__get_resource_and_provider_instances__mutmut_45(type_name: str) -> tuple[Any, Any]:
    resource_class = hub.get_component("resource", type_name)
    if not resource_class:
        err = ResourceError(f"Resource type '{type_name}' not registered")
        err.add_context("resource.type_name", type_name)
        err.add_context("terraform.summary", "Unknown resource type")
        err.add_context(
            "terraform.detail", f"The resource type '{type_name}' is not registered with this provider."
        )
        raise err

    provider_instance = hub.get_component("singleton", "provider")
    if not provider_instance:
        raise RuntimeError("PROVIDER INSTANCE NOT FOUND IN HUB.")
    return resource_class, provider_instance

x__get_resource_and_provider_instances__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_resource_and_provider_instances__mutmut_1': x__get_resource_and_provider_instances__mutmut_1, 
    'x__get_resource_and_provider_instances__mutmut_2': x__get_resource_and_provider_instances__mutmut_2, 
    'x__get_resource_and_provider_instances__mutmut_3': x__get_resource_and_provider_instances__mutmut_3, 
    'x__get_resource_and_provider_instances__mutmut_4': x__get_resource_and_provider_instances__mutmut_4, 
    'x__get_resource_and_provider_instances__mutmut_5': x__get_resource_and_provider_instances__mutmut_5, 
    'x__get_resource_and_provider_instances__mutmut_6': x__get_resource_and_provider_instances__mutmut_6, 
    'x__get_resource_and_provider_instances__mutmut_7': x__get_resource_and_provider_instances__mutmut_7, 
    'x__get_resource_and_provider_instances__mutmut_8': x__get_resource_and_provider_instances__mutmut_8, 
    'x__get_resource_and_provider_instances__mutmut_9': x__get_resource_and_provider_instances__mutmut_9, 
    'x__get_resource_and_provider_instances__mutmut_10': x__get_resource_and_provider_instances__mutmut_10, 
    'x__get_resource_and_provider_instances__mutmut_11': x__get_resource_and_provider_instances__mutmut_11, 
    'x__get_resource_and_provider_instances__mutmut_12': x__get_resource_and_provider_instances__mutmut_12, 
    'x__get_resource_and_provider_instances__mutmut_13': x__get_resource_and_provider_instances__mutmut_13, 
    'x__get_resource_and_provider_instances__mutmut_14': x__get_resource_and_provider_instances__mutmut_14, 
    'x__get_resource_and_provider_instances__mutmut_15': x__get_resource_and_provider_instances__mutmut_15, 
    'x__get_resource_and_provider_instances__mutmut_16': x__get_resource_and_provider_instances__mutmut_16, 
    'x__get_resource_and_provider_instances__mutmut_17': x__get_resource_and_provider_instances__mutmut_17, 
    'x__get_resource_and_provider_instances__mutmut_18': x__get_resource_and_provider_instances__mutmut_18, 
    'x__get_resource_and_provider_instances__mutmut_19': x__get_resource_and_provider_instances__mutmut_19, 
    'x__get_resource_and_provider_instances__mutmut_20': x__get_resource_and_provider_instances__mutmut_20, 
    'x__get_resource_and_provider_instances__mutmut_21': x__get_resource_and_provider_instances__mutmut_21, 
    'x__get_resource_and_provider_instances__mutmut_22': x__get_resource_and_provider_instances__mutmut_22, 
    'x__get_resource_and_provider_instances__mutmut_23': x__get_resource_and_provider_instances__mutmut_23, 
    'x__get_resource_and_provider_instances__mutmut_24': x__get_resource_and_provider_instances__mutmut_24, 
    'x__get_resource_and_provider_instances__mutmut_25': x__get_resource_and_provider_instances__mutmut_25, 
    'x__get_resource_and_provider_instances__mutmut_26': x__get_resource_and_provider_instances__mutmut_26, 
    'x__get_resource_and_provider_instances__mutmut_27': x__get_resource_and_provider_instances__mutmut_27, 
    'x__get_resource_and_provider_instances__mutmut_28': x__get_resource_and_provider_instances__mutmut_28, 
    'x__get_resource_and_provider_instances__mutmut_29': x__get_resource_and_provider_instances__mutmut_29, 
    'x__get_resource_and_provider_instances__mutmut_30': x__get_resource_and_provider_instances__mutmut_30, 
    'x__get_resource_and_provider_instances__mutmut_31': x__get_resource_and_provider_instances__mutmut_31, 
    'x__get_resource_and_provider_instances__mutmut_32': x__get_resource_and_provider_instances__mutmut_32, 
    'x__get_resource_and_provider_instances__mutmut_33': x__get_resource_and_provider_instances__mutmut_33, 
    'x__get_resource_and_provider_instances__mutmut_34': x__get_resource_and_provider_instances__mutmut_34, 
    'x__get_resource_and_provider_instances__mutmut_35': x__get_resource_and_provider_instances__mutmut_35, 
    'x__get_resource_and_provider_instances__mutmut_36': x__get_resource_and_provider_instances__mutmut_36, 
    'x__get_resource_and_provider_instances__mutmut_37': x__get_resource_and_provider_instances__mutmut_37, 
    'x__get_resource_and_provider_instances__mutmut_38': x__get_resource_and_provider_instances__mutmut_38, 
    'x__get_resource_and_provider_instances__mutmut_39': x__get_resource_and_provider_instances__mutmut_39, 
    'x__get_resource_and_provider_instances__mutmut_40': x__get_resource_and_provider_instances__mutmut_40, 
    'x__get_resource_and_provider_instances__mutmut_41': x__get_resource_and_provider_instances__mutmut_41, 
    'x__get_resource_and_provider_instances__mutmut_42': x__get_resource_and_provider_instances__mutmut_42, 
    'x__get_resource_and_provider_instances__mutmut_43': x__get_resource_and_provider_instances__mutmut_43, 
    'x__get_resource_and_provider_instances__mutmut_44': x__get_resource_and_provider_instances__mutmut_44, 
    'x__get_resource_and_provider_instances__mutmut_45': x__get_resource_and_provider_instances__mutmut_45
}

def _get_resource_and_provider_instances(*args, **kwargs):
    result = _mutmut_trampoline(x__get_resource_and_provider_instances__mutmut_orig, x__get_resource_and_provider_instances__mutmut_mutants, args, kwargs)
    return result 

_get_resource_and_provider_instances.__signature__ = _mutmut_signature(x__get_resource_and_provider_instances__mutmut_orig)
x__get_resource_and_provider_instances__mutmut_orig.__name__ = 'x__get_resource_and_provider_instances'


async def x__unmarshal_request_data__mutmut_orig(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_1(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(None):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_2(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = None
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_3(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(None, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_4(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=None)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_5(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_6(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, )
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_7(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = None
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_8(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(None, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_9(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=None)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_10(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_11(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, )
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_12(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = None
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_13(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(None, schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_14(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, schema=None)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_15(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(schema=resource_schema.block)
    return config_cty, prior_state_cty, proposed_new_state_cty


async def x__unmarshal_request_data__mutmut_16(
    request: pb.PlanResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.PLAN):
        config_cty = unmarshal(request.config, schema=resource_schema.block)
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        proposed_new_state_cty = unmarshal(request.proposed_new_state, )
    return config_cty, prior_state_cty, proposed_new_state_cty

x__unmarshal_request_data__mutmut_mutants : ClassVar[MutantDict] = {
'x__unmarshal_request_data__mutmut_1': x__unmarshal_request_data__mutmut_1, 
    'x__unmarshal_request_data__mutmut_2': x__unmarshal_request_data__mutmut_2, 
    'x__unmarshal_request_data__mutmut_3': x__unmarshal_request_data__mutmut_3, 
    'x__unmarshal_request_data__mutmut_4': x__unmarshal_request_data__mutmut_4, 
    'x__unmarshal_request_data__mutmut_5': x__unmarshal_request_data__mutmut_5, 
    'x__unmarshal_request_data__mutmut_6': x__unmarshal_request_data__mutmut_6, 
    'x__unmarshal_request_data__mutmut_7': x__unmarshal_request_data__mutmut_7, 
    'x__unmarshal_request_data__mutmut_8': x__unmarshal_request_data__mutmut_8, 
    'x__unmarshal_request_data__mutmut_9': x__unmarshal_request_data__mutmut_9, 
    'x__unmarshal_request_data__mutmut_10': x__unmarshal_request_data__mutmut_10, 
    'x__unmarshal_request_data__mutmut_11': x__unmarshal_request_data__mutmut_11, 
    'x__unmarshal_request_data__mutmut_12': x__unmarshal_request_data__mutmut_12, 
    'x__unmarshal_request_data__mutmut_13': x__unmarshal_request_data__mutmut_13, 
    'x__unmarshal_request_data__mutmut_14': x__unmarshal_request_data__mutmut_14, 
    'x__unmarshal_request_data__mutmut_15': x__unmarshal_request_data__mutmut_15, 
    'x__unmarshal_request_data__mutmut_16': x__unmarshal_request_data__mutmut_16
}

def _unmarshal_request_data(*args, **kwargs):
    result = _mutmut_trampoline(x__unmarshal_request_data__mutmut_orig, x__unmarshal_request_data__mutmut_mutants, args, kwargs)
    return result 

_unmarshal_request_data.__signature__ = _mutmut_signature(x__unmarshal_request_data__mutmut_orig)
x__unmarshal_request_data__mutmut_orig.__name__ = 'x__unmarshal_request_data'


async def x__process_private_state__mutmut_orig(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_1(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = ""
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_2(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class or prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_3(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") or resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_4(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(None, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_5(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, None) and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_6(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr("private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_7(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, ) and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_8(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "XXprivate_state_classXX") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_9(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "PRIVATE_STATE_CLASS") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_10(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = ""
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_11(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(None)
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_12(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = None
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_13(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(None)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_14(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = None
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_15(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(None, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_16(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=None)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_17(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_18(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, )
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_19(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=True)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_20(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = None
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_21(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(None)
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_22(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                None,
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_23(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=None,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_24(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                decrypted_bytes=None,
            )
    return private_state_instance


async def x__process_private_state__mutmut_25(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                prior_private=prior_private,
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_26(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                decrypted_bytes=decrypted_bytes,
            )
    return private_state_instance


async def x__process_private_state__mutmut_27(resource_class: Any, prior_private: bytes) -> Any | None:
    private_state_instance = None
    if hasattr(resource_class, "private_state_class") and resource_class.private_state_class and prior_private:
        decrypted_bytes = None
        try:
            logger.debug(f"Attempting to decrypt prior_private: {prior_private}")
            decrypted_bytes = decrypt(prior_private)
            private_data = msgpack.unpackb(decrypted_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
            logger.debug(f"Successfully deserialized prior private state: {private_state_instance}")
        except Exception as e:
            logger.warning(
                f"Could not deserialize prior private state for {resource_class.__name__}: {e}",
                prior_private=prior_private,
                )
    return private_state_instance

x__process_private_state__mutmut_mutants : ClassVar[MutantDict] = {
'x__process_private_state__mutmut_1': x__process_private_state__mutmut_1, 
    'x__process_private_state__mutmut_2': x__process_private_state__mutmut_2, 
    'x__process_private_state__mutmut_3': x__process_private_state__mutmut_3, 
    'x__process_private_state__mutmut_4': x__process_private_state__mutmut_4, 
    'x__process_private_state__mutmut_5': x__process_private_state__mutmut_5, 
    'x__process_private_state__mutmut_6': x__process_private_state__mutmut_6, 
    'x__process_private_state__mutmut_7': x__process_private_state__mutmut_7, 
    'x__process_private_state__mutmut_8': x__process_private_state__mutmut_8, 
    'x__process_private_state__mutmut_9': x__process_private_state__mutmut_9, 
    'x__process_private_state__mutmut_10': x__process_private_state__mutmut_10, 
    'x__process_private_state__mutmut_11': x__process_private_state__mutmut_11, 
    'x__process_private_state__mutmut_12': x__process_private_state__mutmut_12, 
    'x__process_private_state__mutmut_13': x__process_private_state__mutmut_13, 
    'x__process_private_state__mutmut_14': x__process_private_state__mutmut_14, 
    'x__process_private_state__mutmut_15': x__process_private_state__mutmut_15, 
    'x__process_private_state__mutmut_16': x__process_private_state__mutmut_16, 
    'x__process_private_state__mutmut_17': x__process_private_state__mutmut_17, 
    'x__process_private_state__mutmut_18': x__process_private_state__mutmut_18, 
    'x__process_private_state__mutmut_19': x__process_private_state__mutmut_19, 
    'x__process_private_state__mutmut_20': x__process_private_state__mutmut_20, 
    'x__process_private_state__mutmut_21': x__process_private_state__mutmut_21, 
    'x__process_private_state__mutmut_22': x__process_private_state__mutmut_22, 
    'x__process_private_state__mutmut_23': x__process_private_state__mutmut_23, 
    'x__process_private_state__mutmut_24': x__process_private_state__mutmut_24, 
    'x__process_private_state__mutmut_25': x__process_private_state__mutmut_25, 
    'x__process_private_state__mutmut_26': x__process_private_state__mutmut_26, 
    'x__process_private_state__mutmut_27': x__process_private_state__mutmut_27
}

def _process_private_state(*args, **kwargs):
    result = _mutmut_trampoline(x__process_private_state__mutmut_orig, x__process_private_state__mutmut_mutants, args, kwargs)
    return result 

_process_private_state.__signature__ = _mutmut_signature(x__process_private_state__mutmut_orig)
x__process_private_state__mutmut_orig.__name__ = 'x__process_private_state'


def x__create_resource_context__mutmut_orig(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_1(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = None
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_2(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(None, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_3(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, None)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_4(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_5(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, )
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_6(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = None
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_7(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(None, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_8(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, None)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_9(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_10(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, )
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_11(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = None

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_12(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(None, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_13(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, None)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_14(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_15(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, )

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_16(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=None,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_17(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=None,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_18(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=None,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_19(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=None,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_20(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=None,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_21(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=None,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_22(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=None,
    )


def x__create_resource_context__mutmut_23(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_24(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_25(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_26(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_27(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        planned_state_cty=proposed_new_state_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_28(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_29(
    config_cty_marked: Any,
    prior_state_cty: Any,
    proposed_new_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    # Try to create attrs instances, but they may return None if values are unknown/computed
    config_instance = cty_to_attrs_instance(config_cty_marked, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    proposed_new_state_instance = cty_to_attrs_instance(proposed_new_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=proposed_new_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty_marked,
        planned_state_cty=proposed_new_state_cty,
        )

x__create_resource_context__mutmut_mutants : ClassVar[MutantDict] = {
'x__create_resource_context__mutmut_1': x__create_resource_context__mutmut_1, 
    'x__create_resource_context__mutmut_2': x__create_resource_context__mutmut_2, 
    'x__create_resource_context__mutmut_3': x__create_resource_context__mutmut_3, 
    'x__create_resource_context__mutmut_4': x__create_resource_context__mutmut_4, 
    'x__create_resource_context__mutmut_5': x__create_resource_context__mutmut_5, 
    'x__create_resource_context__mutmut_6': x__create_resource_context__mutmut_6, 
    'x__create_resource_context__mutmut_7': x__create_resource_context__mutmut_7, 
    'x__create_resource_context__mutmut_8': x__create_resource_context__mutmut_8, 
    'x__create_resource_context__mutmut_9': x__create_resource_context__mutmut_9, 
    'x__create_resource_context__mutmut_10': x__create_resource_context__mutmut_10, 
    'x__create_resource_context__mutmut_11': x__create_resource_context__mutmut_11, 
    'x__create_resource_context__mutmut_12': x__create_resource_context__mutmut_12, 
    'x__create_resource_context__mutmut_13': x__create_resource_context__mutmut_13, 
    'x__create_resource_context__mutmut_14': x__create_resource_context__mutmut_14, 
    'x__create_resource_context__mutmut_15': x__create_resource_context__mutmut_15, 
    'x__create_resource_context__mutmut_16': x__create_resource_context__mutmut_16, 
    'x__create_resource_context__mutmut_17': x__create_resource_context__mutmut_17, 
    'x__create_resource_context__mutmut_18': x__create_resource_context__mutmut_18, 
    'x__create_resource_context__mutmut_19': x__create_resource_context__mutmut_19, 
    'x__create_resource_context__mutmut_20': x__create_resource_context__mutmut_20, 
    'x__create_resource_context__mutmut_21': x__create_resource_context__mutmut_21, 
    'x__create_resource_context__mutmut_22': x__create_resource_context__mutmut_22, 
    'x__create_resource_context__mutmut_23': x__create_resource_context__mutmut_23, 
    'x__create_resource_context__mutmut_24': x__create_resource_context__mutmut_24, 
    'x__create_resource_context__mutmut_25': x__create_resource_context__mutmut_25, 
    'x__create_resource_context__mutmut_26': x__create_resource_context__mutmut_26, 
    'x__create_resource_context__mutmut_27': x__create_resource_context__mutmut_27, 
    'x__create_resource_context__mutmut_28': x__create_resource_context__mutmut_28, 
    'x__create_resource_context__mutmut_29': x__create_resource_context__mutmut_29
}

def _create_resource_context(*args, **kwargs):
    result = _mutmut_trampoline(x__create_resource_context__mutmut_orig, x__create_resource_context__mutmut_mutants, args, kwargs)
    return result 

_create_resource_context.__signature__ = _mutmut_signature(x__create_resource_context__mutmut_orig)
x__create_resource_context__mutmut_orig.__name__ = 'x__create_resource_context'


def x__handle_planned_state_dict__mutmut_orig(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_1(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(None)
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_2(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(None)}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_3(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(None)

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_4(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = None
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_5(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_6(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError(None)

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_7(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("XXResource schema must be an object type for planning.XX")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_8(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_9(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("RESOURCE SCHEMA MUST BE AN OBJECT TYPE FOR PLANNING.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_10(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = None

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_11(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        None
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_12(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) or v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_13(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = None
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_14(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed or not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_15(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_16(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(None)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_17(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict and planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_18(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_19(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is not None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_20(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = None
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_21(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(None)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_22(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = None

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_23(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(None)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_24(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = None

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_25(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(None)

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_26(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(None)}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_27(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = None
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_28(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(None)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_29(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = None
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_30(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(None, schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_31(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=None)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_32(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(schema=resource_schema.block)
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_33(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, )
    response.planned_state.msgpack = marshalled_planned_state.msgpack


def x__handle_planned_state_dict__mutmut_34(
    planned_state_dict: dict[str, Any],
    resource_schema: Any,
    response: pb.PlanResourceChange.Response,
) -> None:
    logger.debug(f"_handle_planned_state_dict received: {list(planned_state_dict.keys())}")
    logger.debug(f"Planned state dict values: {planned_state_dict}")

    validator_type = resource_schema.block.to_cty_type()
    if not isinstance(validator_type, CtyObject):
        raise TypeError("Resource schema must be an object type for planning.")

    # Mark unset computed fields as unknown when there are unknown values in the plan
    # This allows resources to skip setting computed fields when dependencies are unknown
    has_unknown_values = any(
        isinstance(v, CtyValue) and v.is_unknown for v in planned_state_dict.values()
    )

    if has_unknown_values:
        # Get computed attributes from schema
        computed_attrs = set()
        for attr in resource_schema.block.attributes.values():
            if attr.computed and not attr.required:
                computed_attrs.add(attr.name)

        # Mark unset computed fields as unknown
        for attr_name in computed_attrs:
            if attr_name not in planned_state_dict or planned_state_dict[attr_name] is None:
                attr_type = validator_type.attribute_types.get(attr_name)
                if attr_type:
                    planned_state_dict[attr_name] = CtyValue.unknown(attr_type)

    # Pass unknown CtyValues directly to validation - CTY knows how to handle them
    # Don't convert to None, as that creates null CtyValues which fail validation for required fields
    raw_values_for_validation = planned_state_dict.copy()

    logger.debug(f"Raw values for validation: {list(raw_values_for_validation.keys())}")

    # Validate the planned state - unknown values will be preserved by CTY
    planned_state_cty_final = validator_type.validate(raw_values_for_validation)
    marshalled_planned_state = marshal(planned_state_cty_final, schema=resource_schema.block)
    response.planned_state.msgpack = None

x__handle_planned_state_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x__handle_planned_state_dict__mutmut_1': x__handle_planned_state_dict__mutmut_1, 
    'x__handle_planned_state_dict__mutmut_2': x__handle_planned_state_dict__mutmut_2, 
    'x__handle_planned_state_dict__mutmut_3': x__handle_planned_state_dict__mutmut_3, 
    'x__handle_planned_state_dict__mutmut_4': x__handle_planned_state_dict__mutmut_4, 
    'x__handle_planned_state_dict__mutmut_5': x__handle_planned_state_dict__mutmut_5, 
    'x__handle_planned_state_dict__mutmut_6': x__handle_planned_state_dict__mutmut_6, 
    'x__handle_planned_state_dict__mutmut_7': x__handle_planned_state_dict__mutmut_7, 
    'x__handle_planned_state_dict__mutmut_8': x__handle_planned_state_dict__mutmut_8, 
    'x__handle_planned_state_dict__mutmut_9': x__handle_planned_state_dict__mutmut_9, 
    'x__handle_planned_state_dict__mutmut_10': x__handle_planned_state_dict__mutmut_10, 
    'x__handle_planned_state_dict__mutmut_11': x__handle_planned_state_dict__mutmut_11, 
    'x__handle_planned_state_dict__mutmut_12': x__handle_planned_state_dict__mutmut_12, 
    'x__handle_planned_state_dict__mutmut_13': x__handle_planned_state_dict__mutmut_13, 
    'x__handle_planned_state_dict__mutmut_14': x__handle_planned_state_dict__mutmut_14, 
    'x__handle_planned_state_dict__mutmut_15': x__handle_planned_state_dict__mutmut_15, 
    'x__handle_planned_state_dict__mutmut_16': x__handle_planned_state_dict__mutmut_16, 
    'x__handle_planned_state_dict__mutmut_17': x__handle_planned_state_dict__mutmut_17, 
    'x__handle_planned_state_dict__mutmut_18': x__handle_planned_state_dict__mutmut_18, 
    'x__handle_planned_state_dict__mutmut_19': x__handle_planned_state_dict__mutmut_19, 
    'x__handle_planned_state_dict__mutmut_20': x__handle_planned_state_dict__mutmut_20, 
    'x__handle_planned_state_dict__mutmut_21': x__handle_planned_state_dict__mutmut_21, 
    'x__handle_planned_state_dict__mutmut_22': x__handle_planned_state_dict__mutmut_22, 
    'x__handle_planned_state_dict__mutmut_23': x__handle_planned_state_dict__mutmut_23, 
    'x__handle_planned_state_dict__mutmut_24': x__handle_planned_state_dict__mutmut_24, 
    'x__handle_planned_state_dict__mutmut_25': x__handle_planned_state_dict__mutmut_25, 
    'x__handle_planned_state_dict__mutmut_26': x__handle_planned_state_dict__mutmut_26, 
    'x__handle_planned_state_dict__mutmut_27': x__handle_planned_state_dict__mutmut_27, 
    'x__handle_planned_state_dict__mutmut_28': x__handle_planned_state_dict__mutmut_28, 
    'x__handle_planned_state_dict__mutmut_29': x__handle_planned_state_dict__mutmut_29, 
    'x__handle_planned_state_dict__mutmut_30': x__handle_planned_state_dict__mutmut_30, 
    'x__handle_planned_state_dict__mutmut_31': x__handle_planned_state_dict__mutmut_31, 
    'x__handle_planned_state_dict__mutmut_32': x__handle_planned_state_dict__mutmut_32, 
    'x__handle_planned_state_dict__mutmut_33': x__handle_planned_state_dict__mutmut_33, 
    'x__handle_planned_state_dict__mutmut_34': x__handle_planned_state_dict__mutmut_34
}

def _handle_planned_state_dict(*args, **kwargs):
    result = _mutmut_trampoline(x__handle_planned_state_dict__mutmut_orig, x__handle_planned_state_dict__mutmut_mutants, args, kwargs)
    return result 

_handle_planned_state_dict.__signature__ = _mutmut_signature(x__handle_planned_state_dict__mutmut_orig)
x__handle_planned_state_dict__mutmut_orig.__name__ = 'x__handle_planned_state_dict'


@resilient()
async def PlanResourceChangeHandler(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Handle plan resource change request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="PlanResourceChange")

    try:
        return await _plan_resource_change_impl(request, context)
    except Exception:
        handler_errors.inc(handler="PlanResourceChange")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="PlanResourceChange")


async def x__plan_resource_change_impl__mutmut_orig(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_1(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = None
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_2(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = ""
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_3(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = None
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_4(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(None)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_5(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = None
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_6(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = None

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_7(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = None

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_8(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(None, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_9(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, None)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_10(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_11(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, )

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_12(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = None

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_13(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(None, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_14(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, None)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_15(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_16(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, )

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_17(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = None

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_18(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(None, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_19(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, None)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_20(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_21(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, )

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_22(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = None

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_23(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            None,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_24(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            None,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_25(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            None,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_26(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            None,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_27(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            None,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_28(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            None,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_29(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_30(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_31(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_32(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_33(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_34(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_35(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = None

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_36(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(None)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_37(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(None)
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_38(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(None)

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_39(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(None) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_40(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(None)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_41(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(None):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_42(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity != pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_43(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(None, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_44(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, None, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_45(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, None)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_46(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_47(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_48(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, )

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_49(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = None
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_50(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                None, use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_51(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=None
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_52(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_53(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_54(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(None), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_55(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=False
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_56(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = None
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_57(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(None)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_58(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(None)

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_59(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_60(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_61(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_62(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = None
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_63(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    return response


async def x__plan_resource_change_impl__mutmut_64(
    request: pb.PlanResourceChange.Request, context: Any
) -> pb.PlanResourceChange.Response:
    """Implementation of PlanResourceChange handler."""
    response = pb.PlanResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()
        resource_handler = resource_class()

        (
            config_cty,
            prior_state_cty,
            proposed_new_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty_marked = _apply_schema_marks_iterative(config_cty, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.prior_private)

        resource_context = _create_resource_context(
            config_cty_marked,
            prior_state_cty,
            proposed_new_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        planned_state_dict, planned_private_state_attrs = await resource_handler.plan(resource_context)

        logger.debug(f"Resource.plan() returned planned_state_dict: {planned_state_dict}")
        logger.debug(f"Keys in planned_state_dict: {list(planned_state_dict.keys()) if planned_state_dict else None}")

        if resource_context.diagnostics:
            response.diagnostics.extend(resource_context.diagnostics)
            if any(d.severity == pb.Diagnostic.ERROR for d in resource_context.diagnostics):
                return response

        if planned_state_dict:
            _handle_planned_state_dict(planned_state_dict, resource_schema, response)

        if planned_private_state_attrs:
            serialized_private_bytes = msgpack.packb(
                attrs.asdict(planned_private_state_attrs), use_bin_type=True
            )
            response.planned_private = encrypt(serialized_private_bytes)
            logger.debug(f"Setting response.planned_private: {response.planned_private}")

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)

    return response

x__plan_resource_change_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__plan_resource_change_impl__mutmut_1': x__plan_resource_change_impl__mutmut_1, 
    'x__plan_resource_change_impl__mutmut_2': x__plan_resource_change_impl__mutmut_2, 
    'x__plan_resource_change_impl__mutmut_3': x__plan_resource_change_impl__mutmut_3, 
    'x__plan_resource_change_impl__mutmut_4': x__plan_resource_change_impl__mutmut_4, 
    'x__plan_resource_change_impl__mutmut_5': x__plan_resource_change_impl__mutmut_5, 
    'x__plan_resource_change_impl__mutmut_6': x__plan_resource_change_impl__mutmut_6, 
    'x__plan_resource_change_impl__mutmut_7': x__plan_resource_change_impl__mutmut_7, 
    'x__plan_resource_change_impl__mutmut_8': x__plan_resource_change_impl__mutmut_8, 
    'x__plan_resource_change_impl__mutmut_9': x__plan_resource_change_impl__mutmut_9, 
    'x__plan_resource_change_impl__mutmut_10': x__plan_resource_change_impl__mutmut_10, 
    'x__plan_resource_change_impl__mutmut_11': x__plan_resource_change_impl__mutmut_11, 
    'x__plan_resource_change_impl__mutmut_12': x__plan_resource_change_impl__mutmut_12, 
    'x__plan_resource_change_impl__mutmut_13': x__plan_resource_change_impl__mutmut_13, 
    'x__plan_resource_change_impl__mutmut_14': x__plan_resource_change_impl__mutmut_14, 
    'x__plan_resource_change_impl__mutmut_15': x__plan_resource_change_impl__mutmut_15, 
    'x__plan_resource_change_impl__mutmut_16': x__plan_resource_change_impl__mutmut_16, 
    'x__plan_resource_change_impl__mutmut_17': x__plan_resource_change_impl__mutmut_17, 
    'x__plan_resource_change_impl__mutmut_18': x__plan_resource_change_impl__mutmut_18, 
    'x__plan_resource_change_impl__mutmut_19': x__plan_resource_change_impl__mutmut_19, 
    'x__plan_resource_change_impl__mutmut_20': x__plan_resource_change_impl__mutmut_20, 
    'x__plan_resource_change_impl__mutmut_21': x__plan_resource_change_impl__mutmut_21, 
    'x__plan_resource_change_impl__mutmut_22': x__plan_resource_change_impl__mutmut_22, 
    'x__plan_resource_change_impl__mutmut_23': x__plan_resource_change_impl__mutmut_23, 
    'x__plan_resource_change_impl__mutmut_24': x__plan_resource_change_impl__mutmut_24, 
    'x__plan_resource_change_impl__mutmut_25': x__plan_resource_change_impl__mutmut_25, 
    'x__plan_resource_change_impl__mutmut_26': x__plan_resource_change_impl__mutmut_26, 
    'x__plan_resource_change_impl__mutmut_27': x__plan_resource_change_impl__mutmut_27, 
    'x__plan_resource_change_impl__mutmut_28': x__plan_resource_change_impl__mutmut_28, 
    'x__plan_resource_change_impl__mutmut_29': x__plan_resource_change_impl__mutmut_29, 
    'x__plan_resource_change_impl__mutmut_30': x__plan_resource_change_impl__mutmut_30, 
    'x__plan_resource_change_impl__mutmut_31': x__plan_resource_change_impl__mutmut_31, 
    'x__plan_resource_change_impl__mutmut_32': x__plan_resource_change_impl__mutmut_32, 
    'x__plan_resource_change_impl__mutmut_33': x__plan_resource_change_impl__mutmut_33, 
    'x__plan_resource_change_impl__mutmut_34': x__plan_resource_change_impl__mutmut_34, 
    'x__plan_resource_change_impl__mutmut_35': x__plan_resource_change_impl__mutmut_35, 
    'x__plan_resource_change_impl__mutmut_36': x__plan_resource_change_impl__mutmut_36, 
    'x__plan_resource_change_impl__mutmut_37': x__plan_resource_change_impl__mutmut_37, 
    'x__plan_resource_change_impl__mutmut_38': x__plan_resource_change_impl__mutmut_38, 
    'x__plan_resource_change_impl__mutmut_39': x__plan_resource_change_impl__mutmut_39, 
    'x__plan_resource_change_impl__mutmut_40': x__plan_resource_change_impl__mutmut_40, 
    'x__plan_resource_change_impl__mutmut_41': x__plan_resource_change_impl__mutmut_41, 
    'x__plan_resource_change_impl__mutmut_42': x__plan_resource_change_impl__mutmut_42, 
    'x__plan_resource_change_impl__mutmut_43': x__plan_resource_change_impl__mutmut_43, 
    'x__plan_resource_change_impl__mutmut_44': x__plan_resource_change_impl__mutmut_44, 
    'x__plan_resource_change_impl__mutmut_45': x__plan_resource_change_impl__mutmut_45, 
    'x__plan_resource_change_impl__mutmut_46': x__plan_resource_change_impl__mutmut_46, 
    'x__plan_resource_change_impl__mutmut_47': x__plan_resource_change_impl__mutmut_47, 
    'x__plan_resource_change_impl__mutmut_48': x__plan_resource_change_impl__mutmut_48, 
    'x__plan_resource_change_impl__mutmut_49': x__plan_resource_change_impl__mutmut_49, 
    'x__plan_resource_change_impl__mutmut_50': x__plan_resource_change_impl__mutmut_50, 
    'x__plan_resource_change_impl__mutmut_51': x__plan_resource_change_impl__mutmut_51, 
    'x__plan_resource_change_impl__mutmut_52': x__plan_resource_change_impl__mutmut_52, 
    'x__plan_resource_change_impl__mutmut_53': x__plan_resource_change_impl__mutmut_53, 
    'x__plan_resource_change_impl__mutmut_54': x__plan_resource_change_impl__mutmut_54, 
    'x__plan_resource_change_impl__mutmut_55': x__plan_resource_change_impl__mutmut_55, 
    'x__plan_resource_change_impl__mutmut_56': x__plan_resource_change_impl__mutmut_56, 
    'x__plan_resource_change_impl__mutmut_57': x__plan_resource_change_impl__mutmut_57, 
    'x__plan_resource_change_impl__mutmut_58': x__plan_resource_change_impl__mutmut_58, 
    'x__plan_resource_change_impl__mutmut_59': x__plan_resource_change_impl__mutmut_59, 
    'x__plan_resource_change_impl__mutmut_60': x__plan_resource_change_impl__mutmut_60, 
    'x__plan_resource_change_impl__mutmut_61': x__plan_resource_change_impl__mutmut_61, 
    'x__plan_resource_change_impl__mutmut_62': x__plan_resource_change_impl__mutmut_62, 
    'x__plan_resource_change_impl__mutmut_63': x__plan_resource_change_impl__mutmut_63, 
    'x__plan_resource_change_impl__mutmut_64': x__plan_resource_change_impl__mutmut_64
}

def _plan_resource_change_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__plan_resource_change_impl__mutmut_orig, x__plan_resource_change_impl__mutmut_mutants, args, kwargs)
    return result 

_plan_resource_change_impl.__signature__ = _mutmut_signature(x__plan_resource_change_impl__mutmut_orig)
x__plan_resource_change_impl__mutmut_orig.__name__ = 'x__plan_resource_change_impl'
