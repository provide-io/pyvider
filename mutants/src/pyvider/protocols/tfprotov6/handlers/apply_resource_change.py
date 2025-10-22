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
from pyvider.cty.exceptions import CtyValidationError
from pyvider.exceptions import (
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    is_valid_refinement,
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
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_1(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(None):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_2(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = None
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_3(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(None, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_4(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=None)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_5(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_6(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, )
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_7(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = None
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_8(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(None, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_9(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=None)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_10(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_11(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, )
        planned_state_cty = unmarshal(request.planned_state, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_12(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = None
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_13(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(None, schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_14(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, schema=None)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_15(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(schema=resource_schema.block)
    return prior_state_cty, config_cty_unmarked, planned_state_cty


async def x__unmarshal_request_data__mutmut_16(
    request: pb.ApplyResourceChange.Request, resource_schema: Any
) -> tuple[Any, Any, Any]:
    with operation_context(OperationContext.APPLY):
        prior_state_cty = unmarshal(request.prior_state, schema=resource_schema.block)
        config_cty_unmarked = unmarshal(request.config, schema=resource_schema.block)
        planned_state_cty = unmarshal(request.planned_state, )
    return prior_state_cty, config_cty_unmarked, planned_state_cty

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


async def x__process_private_state__mutmut_orig(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_1(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(None)
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_2(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = ""
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_3(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class or planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_4(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class") or resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_5(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(None, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_6(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, None)
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_7(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr("private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_8(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, )
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_9(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "XXprivate_state_classXX")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_10(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "PRIVATE_STATE_CLASS")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_11(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = None
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_12(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(None)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_13(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = None
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_14(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(None, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_15(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=None)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_16(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_17(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, )
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_18(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=True)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_19(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = None
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_20(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = None
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_21(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError(None)
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_22(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("XXFailed to deserialize private state from plan.XX")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_23(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_24(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("FAILED TO DESERIALIZE PRIVATE STATE FROM PLAN.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_25(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context(None, str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_26(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", None)
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_27(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context(str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_28(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", )
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_29(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("XXprivate_state.errorXX", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_30(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("PRIVATE_STATE.ERROR", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_31(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(None))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_32(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context(None, "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_33(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", None)
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_34(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_35(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", )
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_36(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("XXterraform.summaryXX", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_37(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("TERRAFORM.SUMMARY", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_38(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "XXPrivate state deserialization failedXX")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_39(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "private state deserialization failed")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_40(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "PRIVATE STATE DESERIALIZATION FAILED")
            err.add_context(
                "terraform.detail", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_41(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                None, "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_42(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", None
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_43(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_44(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_45(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "XXterraform.detailXX", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_46(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "TERRAFORM.DETAIL", "The provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_47(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "XXThe provider could not deserialize the private state data from the plan.XX"
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_48(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "the provider could not deserialize the private state data from the plan."
            )
            raise err from e
    return private_state_instance


async def x__process_private_state__mutmut_49(resource_class: Any, planned_private: bytes) -> Any | None:
    logger.debug(f"Processing private state. planned_private: {planned_private}")
    private_state_instance = None
    if (
        hasattr(resource_class, "private_state_class")
        and resource_class.private_state_class
        and planned_private
    ):
        try:
            decrypted_private_bytes = decrypt(planned_private)
            private_data = msgpack.unpackb(decrypted_private_bytes, raw=False)
            private_state_instance = resource_class.private_state_class(**private_data)
        except Exception as e:
            err = ResourceError("Failed to deserialize private state from plan.")
            err.add_context("private_state.error", str(e))
            err.add_context("terraform.summary", "Private state deserialization failed")
            err.add_context(
                "terraform.detail", "THE PROVIDER COULD NOT DESERIALIZE THE PRIVATE STATE DATA FROM THE PLAN."
            )
            raise err from e
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
    'x__process_private_state__mutmut_27': x__process_private_state__mutmut_27, 
    'x__process_private_state__mutmut_28': x__process_private_state__mutmut_28, 
    'x__process_private_state__mutmut_29': x__process_private_state__mutmut_29, 
    'x__process_private_state__mutmut_30': x__process_private_state__mutmut_30, 
    'x__process_private_state__mutmut_31': x__process_private_state__mutmut_31, 
    'x__process_private_state__mutmut_32': x__process_private_state__mutmut_32, 
    'x__process_private_state__mutmut_33': x__process_private_state__mutmut_33, 
    'x__process_private_state__mutmut_34': x__process_private_state__mutmut_34, 
    'x__process_private_state__mutmut_35': x__process_private_state__mutmut_35, 
    'x__process_private_state__mutmut_36': x__process_private_state__mutmut_36, 
    'x__process_private_state__mutmut_37': x__process_private_state__mutmut_37, 
    'x__process_private_state__mutmut_38': x__process_private_state__mutmut_38, 
    'x__process_private_state__mutmut_39': x__process_private_state__mutmut_39, 
    'x__process_private_state__mutmut_40': x__process_private_state__mutmut_40, 
    'x__process_private_state__mutmut_41': x__process_private_state__mutmut_41, 
    'x__process_private_state__mutmut_42': x__process_private_state__mutmut_42, 
    'x__process_private_state__mutmut_43': x__process_private_state__mutmut_43, 
    'x__process_private_state__mutmut_44': x__process_private_state__mutmut_44, 
    'x__process_private_state__mutmut_45': x__process_private_state__mutmut_45, 
    'x__process_private_state__mutmut_46': x__process_private_state__mutmut_46, 
    'x__process_private_state__mutmut_47': x__process_private_state__mutmut_47, 
    'x__process_private_state__mutmut_48': x__process_private_state__mutmut_48, 
    'x__process_private_state__mutmut_49': x__process_private_state__mutmut_49
}

def _process_private_state(*args, **kwargs):
    result = _mutmut_trampoline(x__process_private_state__mutmut_orig, x__process_private_state__mutmut_mutants, args, kwargs)
    return result 

_process_private_state.__signature__ = _mutmut_signature(x__process_private_state__mutmut_orig)
x__process_private_state__mutmut_orig.__name__ = 'x__process_private_state'


def x__create_resource_context__mutmut_orig(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_1(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = None
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_2(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(None, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_3(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, None)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_4(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_5(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, )
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_6(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = None
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_7(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(None, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_8(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, None)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_9(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_10(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, )
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_11(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = None

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_12(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(None, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_13(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, None)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_14(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_15(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, )

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_16(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=None,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_17(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=None,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_18(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=None,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_19(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=None,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_20(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=None,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_21(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=None,
    )


def x__create_resource_context__mutmut_22(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_23(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_24(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_25(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        config_cty=config_cty,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_26(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        capabilities=provider_instance.metadata.capabilities,
    )


def x__create_resource_context__mutmut_27(
    config_cty: Any,
    prior_state_cty: Any,
    planned_state_cty: Any,
    private_state_instance: Any,
    resource_class: Any,
    provider_instance: Any,
) -> ResourceContext:
    config_instance = cty_to_attrs_instance(config_cty, resource_class.config_class)
    prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)
    planned_state_instance = cty_to_attrs_instance(planned_state_cty, resource_class.state_class)

    return ResourceContext(
        config=config_instance,
        state=prior_state_instance,
        planned_state=planned_state_instance,
        private_state=private_state_instance,
        config_cty=config_cty,
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
    'x__create_resource_context__mutmut_27': x__create_resource_context__mutmut_27
}

def _create_resource_context(*args, **kwargs):
    result = _mutmut_trampoline(x__create_resource_context__mutmut_orig, x__create_resource_context__mutmut_mutants, args, kwargs)
    return result 

_create_resource_context.__signature__ = _mutmut_signature(x__create_resource_context__mutmut_orig)
x__create_resource_context__mutmut_orig.__name__ = 'x__create_resource_context'


def x__handle_apply_result__mutmut_orig(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_1(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_2(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = None
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_3(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(None)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_4(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = None
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_5(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = None

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_6(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(None)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_7(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_8(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = None
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_9(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(None, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_10(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, None)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_11(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_12(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, )
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_13(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_14(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = None
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_15(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    None,
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_16(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=None,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_17(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_18(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_19(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "XXThe final state returned by the resource's apply method is not a valid refinement of the planned state.XX",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_20(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "the final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_21(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "THE FINAL STATE RETURNED BY THE RESOURCE'S APPLY METHOD IS NOT A VALID REFINEMENT OF THE PLANNED STATE.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_22(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    None, resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_23(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", None
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_24(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_25(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_26(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "XXresource.typeXX", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_27(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "RESOURCE.TYPE", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_28(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(None, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_29(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, None) else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_30(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr("name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_31(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, ) else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_32(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "XXnameXX") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_33(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "NAME") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_34(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "XXunknownXX"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_35(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "UNKNOWN"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_36(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context(None, "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_37(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", None)
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_38(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_39(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", )
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_40(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("XXlifecycle.operationXX", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_41(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("LIFECYCLE.OPERATION", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_42(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "XXapplyXX")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_43(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "APPLY")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_44(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context(None, reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_45(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", None)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_46(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context(reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_47(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", )
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_48(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("XXvalidation.reasonXX", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_49(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("VALIDATION.REASON", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_50(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context(None, "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_51(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", None)
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_52(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_53(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", )
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_54(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("XXterraform.summaryXX", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_55(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("TERRAFORM.SUMMARY", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_56(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "XXResource state contract violationXX")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_57(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_58(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "RESOURCE STATE CONTRACT VIOLATION")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_59(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    None,
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_60(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    None,
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_61(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_62(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_63(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "XXterraform.detailXX",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_64(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "TERRAFORM.DETAIL",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_65(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = None
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_66(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(None, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_67(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=None)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_68(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_69(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, )
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_70(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = None
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_71(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = None

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_72(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"XX\xc0XX"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_73(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_74(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xC0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_75(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = None
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_76(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(None, use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_77(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=None)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_78(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_79(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), )
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_80(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(None), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_81(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=False)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_82(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = None
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_83(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(None)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_84(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(None)
        logger.debug(f"Serialized private bytes: {serialized_bytes}")


def x__handle_apply_result__mutmut_85(
    new_state_attrs: Any,
    new_private_state_attrs: Any,
    resource_schema: Any,
    planned_state_cty: Any,
    response: pb.ApplyResourceChange.Response,
) -> None:
    if new_state_attrs is not None:
        raw_new_state = attrs_to_dict_for_cty(new_state_attrs)
        validator_type = resource_schema.block.to_cty_type()
        new_state_cty = validator_type.validate(raw_new_state)

        if planned_state_cty is not None:
            is_valid, reason = is_valid_refinement(planned_state_cty, new_state_cty)
            if not is_valid:
                err = ResourceLifecycleContractError(
                    "The final state returned by the resource's apply method is not a valid refinement of the planned state.",
                    detail=reason,
                )
                err.add_context(
                    "resource.type", resource_schema.name if hasattr(resource_schema, "name") else "unknown"
                )
                err.add_context("lifecycle.operation", "apply")
                err.add_context("validation.reason", reason)
                err.add_context("terraform.summary", "Resource state contract violation")
                err.add_context(
                    "terraform.detail",
                    f"The resource implementation violated the Terraform state contract: {reason}",
                )
                # Severity is handled by the error type itself
                raise err

        marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
        response.new_state.msgpack = marshalled_new_state.msgpack
    else:
        response.new_state.msgpack = b"\xc0"

    if new_private_state_attrs:
        serialized_bytes = msgpack.packb(attrs.asdict(new_private_state_attrs), use_bin_type=True)
        response.private = encrypt(serialized_bytes)
        logger.debug(f"Setting response.private: {response.private}")
        logger.debug(None)

x__handle_apply_result__mutmut_mutants : ClassVar[MutantDict] = {
'x__handle_apply_result__mutmut_1': x__handle_apply_result__mutmut_1, 
    'x__handle_apply_result__mutmut_2': x__handle_apply_result__mutmut_2, 
    'x__handle_apply_result__mutmut_3': x__handle_apply_result__mutmut_3, 
    'x__handle_apply_result__mutmut_4': x__handle_apply_result__mutmut_4, 
    'x__handle_apply_result__mutmut_5': x__handle_apply_result__mutmut_5, 
    'x__handle_apply_result__mutmut_6': x__handle_apply_result__mutmut_6, 
    'x__handle_apply_result__mutmut_7': x__handle_apply_result__mutmut_7, 
    'x__handle_apply_result__mutmut_8': x__handle_apply_result__mutmut_8, 
    'x__handle_apply_result__mutmut_9': x__handle_apply_result__mutmut_9, 
    'x__handle_apply_result__mutmut_10': x__handle_apply_result__mutmut_10, 
    'x__handle_apply_result__mutmut_11': x__handle_apply_result__mutmut_11, 
    'x__handle_apply_result__mutmut_12': x__handle_apply_result__mutmut_12, 
    'x__handle_apply_result__mutmut_13': x__handle_apply_result__mutmut_13, 
    'x__handle_apply_result__mutmut_14': x__handle_apply_result__mutmut_14, 
    'x__handle_apply_result__mutmut_15': x__handle_apply_result__mutmut_15, 
    'x__handle_apply_result__mutmut_16': x__handle_apply_result__mutmut_16, 
    'x__handle_apply_result__mutmut_17': x__handle_apply_result__mutmut_17, 
    'x__handle_apply_result__mutmut_18': x__handle_apply_result__mutmut_18, 
    'x__handle_apply_result__mutmut_19': x__handle_apply_result__mutmut_19, 
    'x__handle_apply_result__mutmut_20': x__handle_apply_result__mutmut_20, 
    'x__handle_apply_result__mutmut_21': x__handle_apply_result__mutmut_21, 
    'x__handle_apply_result__mutmut_22': x__handle_apply_result__mutmut_22, 
    'x__handle_apply_result__mutmut_23': x__handle_apply_result__mutmut_23, 
    'x__handle_apply_result__mutmut_24': x__handle_apply_result__mutmut_24, 
    'x__handle_apply_result__mutmut_25': x__handle_apply_result__mutmut_25, 
    'x__handle_apply_result__mutmut_26': x__handle_apply_result__mutmut_26, 
    'x__handle_apply_result__mutmut_27': x__handle_apply_result__mutmut_27, 
    'x__handle_apply_result__mutmut_28': x__handle_apply_result__mutmut_28, 
    'x__handle_apply_result__mutmut_29': x__handle_apply_result__mutmut_29, 
    'x__handle_apply_result__mutmut_30': x__handle_apply_result__mutmut_30, 
    'x__handle_apply_result__mutmut_31': x__handle_apply_result__mutmut_31, 
    'x__handle_apply_result__mutmut_32': x__handle_apply_result__mutmut_32, 
    'x__handle_apply_result__mutmut_33': x__handle_apply_result__mutmut_33, 
    'x__handle_apply_result__mutmut_34': x__handle_apply_result__mutmut_34, 
    'x__handle_apply_result__mutmut_35': x__handle_apply_result__mutmut_35, 
    'x__handle_apply_result__mutmut_36': x__handle_apply_result__mutmut_36, 
    'x__handle_apply_result__mutmut_37': x__handle_apply_result__mutmut_37, 
    'x__handle_apply_result__mutmut_38': x__handle_apply_result__mutmut_38, 
    'x__handle_apply_result__mutmut_39': x__handle_apply_result__mutmut_39, 
    'x__handle_apply_result__mutmut_40': x__handle_apply_result__mutmut_40, 
    'x__handle_apply_result__mutmut_41': x__handle_apply_result__mutmut_41, 
    'x__handle_apply_result__mutmut_42': x__handle_apply_result__mutmut_42, 
    'x__handle_apply_result__mutmut_43': x__handle_apply_result__mutmut_43, 
    'x__handle_apply_result__mutmut_44': x__handle_apply_result__mutmut_44, 
    'x__handle_apply_result__mutmut_45': x__handle_apply_result__mutmut_45, 
    'x__handle_apply_result__mutmut_46': x__handle_apply_result__mutmut_46, 
    'x__handle_apply_result__mutmut_47': x__handle_apply_result__mutmut_47, 
    'x__handle_apply_result__mutmut_48': x__handle_apply_result__mutmut_48, 
    'x__handle_apply_result__mutmut_49': x__handle_apply_result__mutmut_49, 
    'x__handle_apply_result__mutmut_50': x__handle_apply_result__mutmut_50, 
    'x__handle_apply_result__mutmut_51': x__handle_apply_result__mutmut_51, 
    'x__handle_apply_result__mutmut_52': x__handle_apply_result__mutmut_52, 
    'x__handle_apply_result__mutmut_53': x__handle_apply_result__mutmut_53, 
    'x__handle_apply_result__mutmut_54': x__handle_apply_result__mutmut_54, 
    'x__handle_apply_result__mutmut_55': x__handle_apply_result__mutmut_55, 
    'x__handle_apply_result__mutmut_56': x__handle_apply_result__mutmut_56, 
    'x__handle_apply_result__mutmut_57': x__handle_apply_result__mutmut_57, 
    'x__handle_apply_result__mutmut_58': x__handle_apply_result__mutmut_58, 
    'x__handle_apply_result__mutmut_59': x__handle_apply_result__mutmut_59, 
    'x__handle_apply_result__mutmut_60': x__handle_apply_result__mutmut_60, 
    'x__handle_apply_result__mutmut_61': x__handle_apply_result__mutmut_61, 
    'x__handle_apply_result__mutmut_62': x__handle_apply_result__mutmut_62, 
    'x__handle_apply_result__mutmut_63': x__handle_apply_result__mutmut_63, 
    'x__handle_apply_result__mutmut_64': x__handle_apply_result__mutmut_64, 
    'x__handle_apply_result__mutmut_65': x__handle_apply_result__mutmut_65, 
    'x__handle_apply_result__mutmut_66': x__handle_apply_result__mutmut_66, 
    'x__handle_apply_result__mutmut_67': x__handle_apply_result__mutmut_67, 
    'x__handle_apply_result__mutmut_68': x__handle_apply_result__mutmut_68, 
    'x__handle_apply_result__mutmut_69': x__handle_apply_result__mutmut_69, 
    'x__handle_apply_result__mutmut_70': x__handle_apply_result__mutmut_70, 
    'x__handle_apply_result__mutmut_71': x__handle_apply_result__mutmut_71, 
    'x__handle_apply_result__mutmut_72': x__handle_apply_result__mutmut_72, 
    'x__handle_apply_result__mutmut_73': x__handle_apply_result__mutmut_73, 
    'x__handle_apply_result__mutmut_74': x__handle_apply_result__mutmut_74, 
    'x__handle_apply_result__mutmut_75': x__handle_apply_result__mutmut_75, 
    'x__handle_apply_result__mutmut_76': x__handle_apply_result__mutmut_76, 
    'x__handle_apply_result__mutmut_77': x__handle_apply_result__mutmut_77, 
    'x__handle_apply_result__mutmut_78': x__handle_apply_result__mutmut_78, 
    'x__handle_apply_result__mutmut_79': x__handle_apply_result__mutmut_79, 
    'x__handle_apply_result__mutmut_80': x__handle_apply_result__mutmut_80, 
    'x__handle_apply_result__mutmut_81': x__handle_apply_result__mutmut_81, 
    'x__handle_apply_result__mutmut_82': x__handle_apply_result__mutmut_82, 
    'x__handle_apply_result__mutmut_83': x__handle_apply_result__mutmut_83, 
    'x__handle_apply_result__mutmut_84': x__handle_apply_result__mutmut_84, 
    'x__handle_apply_result__mutmut_85': x__handle_apply_result__mutmut_85
}

def _handle_apply_result(*args, **kwargs):
    result = _mutmut_trampoline(x__handle_apply_result__mutmut_orig, x__handle_apply_result__mutmut_mutants, args, kwargs)
    return result 

_handle_apply_result.__signature__ = _mutmut_signature(x__handle_apply_result__mutmut_orig)
x__handle_apply_result__mutmut_orig.__name__ = 'x__handle_apply_result'


@resilient()
async def ApplyResourceChangeHandler(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    """Handle apply resource change request with metrics collection."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ApplyResourceChange")

    try:
        return await _apply_resource_change_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ApplyResourceChange")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ApplyResourceChange")


async def x__apply_resource_change_impl__mutmut_orig(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_1(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = None
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_2(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = ""
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_3(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = None
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_4(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(None)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_5(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = None

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_6(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = None

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_7(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(None, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_8(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, None)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_9(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_10(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, )

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_11(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = None

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_12(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(None, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_13(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, None)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_14(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_15(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, )

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_16(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = None

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_17(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(None, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_18(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, None)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_19(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_20(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, )

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_21(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = None

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_22(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            None,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_23(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            None,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_24(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            None,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_25(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            None,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_26(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            None,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_27(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            None,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_28(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_29(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_30(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_31(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_32(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_33(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_34(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = None
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_35(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = None

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_36(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(None)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_37(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            None,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_38(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            None,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_39(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            None,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_40(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            None,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_41(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            None,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_42(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_43(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_44(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_45(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_46(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_47(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_48(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_49(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_50(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = None
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_51(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_52(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(None)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_53(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context or resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__apply_resource_change_impl__mutmut_54(
    request: pb.ApplyResourceChange.Request, context: Any
) -> pb.ApplyResourceChange.Response:
    response = pb.ApplyResourceChange.Response()
    resource_context = None
    try:
        resource_class, provider_instance = await _get_resource_and_provider_instances(request.type_name)
        resource_schema = resource_class.get_schema()

        (
            prior_state_cty,
            config_cty_unmarked,
            planned_state_cty,
        ) = await _unmarshal_request_data(request, resource_schema)

        config_cty = _apply_schema_marks_iterative(config_cty_unmarked, resource_schema.block)

        private_state_instance = await _process_private_state(resource_class, request.planned_private)

        resource_context = _create_resource_context(
            config_cty,
            prior_state_cty,
            planned_state_cty,
            private_state_instance,
            resource_class,
            provider_instance,
        )

        resource_handler = resource_class()
        new_state_attrs, new_private_state_attrs = await resource_handler.apply(resource_context)

        _handle_apply_result(
            new_state_attrs,
            new_private_state_attrs,
            resource_schema,
            planned_state_cty,
            response,
        )

    except (CtyValidationError, PyviderError) as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(None)

    return response

x__apply_resource_change_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__apply_resource_change_impl__mutmut_1': x__apply_resource_change_impl__mutmut_1, 
    'x__apply_resource_change_impl__mutmut_2': x__apply_resource_change_impl__mutmut_2, 
    'x__apply_resource_change_impl__mutmut_3': x__apply_resource_change_impl__mutmut_3, 
    'x__apply_resource_change_impl__mutmut_4': x__apply_resource_change_impl__mutmut_4, 
    'x__apply_resource_change_impl__mutmut_5': x__apply_resource_change_impl__mutmut_5, 
    'x__apply_resource_change_impl__mutmut_6': x__apply_resource_change_impl__mutmut_6, 
    'x__apply_resource_change_impl__mutmut_7': x__apply_resource_change_impl__mutmut_7, 
    'x__apply_resource_change_impl__mutmut_8': x__apply_resource_change_impl__mutmut_8, 
    'x__apply_resource_change_impl__mutmut_9': x__apply_resource_change_impl__mutmut_9, 
    'x__apply_resource_change_impl__mutmut_10': x__apply_resource_change_impl__mutmut_10, 
    'x__apply_resource_change_impl__mutmut_11': x__apply_resource_change_impl__mutmut_11, 
    'x__apply_resource_change_impl__mutmut_12': x__apply_resource_change_impl__mutmut_12, 
    'x__apply_resource_change_impl__mutmut_13': x__apply_resource_change_impl__mutmut_13, 
    'x__apply_resource_change_impl__mutmut_14': x__apply_resource_change_impl__mutmut_14, 
    'x__apply_resource_change_impl__mutmut_15': x__apply_resource_change_impl__mutmut_15, 
    'x__apply_resource_change_impl__mutmut_16': x__apply_resource_change_impl__mutmut_16, 
    'x__apply_resource_change_impl__mutmut_17': x__apply_resource_change_impl__mutmut_17, 
    'x__apply_resource_change_impl__mutmut_18': x__apply_resource_change_impl__mutmut_18, 
    'x__apply_resource_change_impl__mutmut_19': x__apply_resource_change_impl__mutmut_19, 
    'x__apply_resource_change_impl__mutmut_20': x__apply_resource_change_impl__mutmut_20, 
    'x__apply_resource_change_impl__mutmut_21': x__apply_resource_change_impl__mutmut_21, 
    'x__apply_resource_change_impl__mutmut_22': x__apply_resource_change_impl__mutmut_22, 
    'x__apply_resource_change_impl__mutmut_23': x__apply_resource_change_impl__mutmut_23, 
    'x__apply_resource_change_impl__mutmut_24': x__apply_resource_change_impl__mutmut_24, 
    'x__apply_resource_change_impl__mutmut_25': x__apply_resource_change_impl__mutmut_25, 
    'x__apply_resource_change_impl__mutmut_26': x__apply_resource_change_impl__mutmut_26, 
    'x__apply_resource_change_impl__mutmut_27': x__apply_resource_change_impl__mutmut_27, 
    'x__apply_resource_change_impl__mutmut_28': x__apply_resource_change_impl__mutmut_28, 
    'x__apply_resource_change_impl__mutmut_29': x__apply_resource_change_impl__mutmut_29, 
    'x__apply_resource_change_impl__mutmut_30': x__apply_resource_change_impl__mutmut_30, 
    'x__apply_resource_change_impl__mutmut_31': x__apply_resource_change_impl__mutmut_31, 
    'x__apply_resource_change_impl__mutmut_32': x__apply_resource_change_impl__mutmut_32, 
    'x__apply_resource_change_impl__mutmut_33': x__apply_resource_change_impl__mutmut_33, 
    'x__apply_resource_change_impl__mutmut_34': x__apply_resource_change_impl__mutmut_34, 
    'x__apply_resource_change_impl__mutmut_35': x__apply_resource_change_impl__mutmut_35, 
    'x__apply_resource_change_impl__mutmut_36': x__apply_resource_change_impl__mutmut_36, 
    'x__apply_resource_change_impl__mutmut_37': x__apply_resource_change_impl__mutmut_37, 
    'x__apply_resource_change_impl__mutmut_38': x__apply_resource_change_impl__mutmut_38, 
    'x__apply_resource_change_impl__mutmut_39': x__apply_resource_change_impl__mutmut_39, 
    'x__apply_resource_change_impl__mutmut_40': x__apply_resource_change_impl__mutmut_40, 
    'x__apply_resource_change_impl__mutmut_41': x__apply_resource_change_impl__mutmut_41, 
    'x__apply_resource_change_impl__mutmut_42': x__apply_resource_change_impl__mutmut_42, 
    'x__apply_resource_change_impl__mutmut_43': x__apply_resource_change_impl__mutmut_43, 
    'x__apply_resource_change_impl__mutmut_44': x__apply_resource_change_impl__mutmut_44, 
    'x__apply_resource_change_impl__mutmut_45': x__apply_resource_change_impl__mutmut_45, 
    'x__apply_resource_change_impl__mutmut_46': x__apply_resource_change_impl__mutmut_46, 
    'x__apply_resource_change_impl__mutmut_47': x__apply_resource_change_impl__mutmut_47, 
    'x__apply_resource_change_impl__mutmut_48': x__apply_resource_change_impl__mutmut_48, 
    'x__apply_resource_change_impl__mutmut_49': x__apply_resource_change_impl__mutmut_49, 
    'x__apply_resource_change_impl__mutmut_50': x__apply_resource_change_impl__mutmut_50, 
    'x__apply_resource_change_impl__mutmut_51': x__apply_resource_change_impl__mutmut_51, 
    'x__apply_resource_change_impl__mutmut_52': x__apply_resource_change_impl__mutmut_52, 
    'x__apply_resource_change_impl__mutmut_53': x__apply_resource_change_impl__mutmut_53, 
    'x__apply_resource_change_impl__mutmut_54': x__apply_resource_change_impl__mutmut_54
}

def _apply_resource_change_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__apply_resource_change_impl__mutmut_orig, x__apply_resource_change_impl__mutmut_mutants, args, kwargs)
    return result 

_apply_resource_change_impl.__signature__ = _mutmut_signature(x__apply_resource_change_impl__mutmut_orig)
x__apply_resource_change_impl__mutmut_orig.__name__ = 'x__apply_resource_change_impl'
