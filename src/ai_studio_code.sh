#!/bin/bash
# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_create() { echo -e "✨ $1"; }
log_update() { echo -e "🔄 $1"; }
log_delete() { echo -e "🔥 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying changes to implement provider_testmode..."

log_update "Updating: pyvider/data_sources/decorators.py"
mkdir -p pyvider/data_sources/
cat <<'EOF' > pyvider/data_sources/decorators.py
from collections.abc import Callable

from provide.foundation import logger


def register_data_source(
    name: str, component_of: str | None = None, test_only: bool = False
) -> Callable[[type], type]:
    """
    Decorator to register a data source and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_data_source = True  # type: ignore
        cls._registered_name = name  # type: ignore
        cls._is_test_only = test_only  # type: ignore
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(
            f"📊 Marked data source '{name}' for discovery",
            capability=component_of,
            test_only=test_only,
        )
        return cls

    return decorator
EOF

log_update "Updating: pyvider/functions/decorators.py"
mkdir -p pyvider/functions/
cat <<'EOF' > pyvider/functions/decorators.py
from collections.abc import Callable
from typing import Any

from provide.foundation import logger


def register_function(
    name: str,
    component_of: str | None = None,
    summary: str = "",
    description: str = "",
    param_descriptions: dict[str, str] | None = None,
    deprecation_message: str = "",
    test_only: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function and associate it with a capability.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._is_registered_function = True  # type: ignore
        func._registered_name = name  # type: ignore
        func._is_test_only = test_only  # type: ignore
        if component_of:
            func._parent_capability = component_of  # type: ignore

        metadata = {
            "name": name,
            "type": "function",
            "summary": summary,
            "description": description,
            "param_descriptions": param_descriptions or {},
            "deprecation_message": deprecation_message,
            "function_name": func.__name__,
            "module": func.__module__,
            "discovery_method": "decorator",
            "test_only": test_only,
        }
        func._function_metadata = metadata  # type: ignore

        logger.debug(
            f"🧰 Marked function '{name}' for discovery",
            capability=component_of,
            test_only=test_only,
        )
        return func

    return decorator
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/configure_provider.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/configure_provider.py
import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import unmarshal
from pyvider.exceptions import ProviderConfigurationError, PyviderError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.context import ProviderContext
from pyvider.resources.base import BaseResource


@resilient()
async def ConfigureProviderHandler(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """
    Handles the ConfigureProvider RPC request.

    This handler validates the provider configuration sent by Terraform
    and initializes the provider context, making it available for all
    subsequent component operations.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="ConfigureProvider")

    try:
        return await _configure_provider_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ConfigureProvider")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ConfigureProvider")


async def _configure_provider_impl(
    request: pb.ConfigureProvider.Request, context: Any
) -> pb.ConfigureProvider.Response:
    """Implementation of ConfigureProvider handler."""
    response = pb.ConfigureProvider.Response()

    logger.debug(
        "ConfigureProvider handler called",
        operation="configure_provider",
        has_config=bool(request.config.msgpack),
        terraform_version=request.terraform_version if hasattr(request, "terraform_version") else "unknown",
    )

    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            logger.error(
                "Provider instance not found in hub during configuration",
                operation="configure_provider",
            )

            err = ProviderConfigurationError(
                "Provider instance not found in hub.\n\n"
                "This is an internal framework error. The provider should be registered "
                "during server initialization before ConfigureProvider is called.\n\n"
                "Suggestion: Report this issue - it indicates a provider initialization problem.\n\n"
                "Troubleshooting:\n"
                "  1. Ensure the provider class has the @provider decorator\n"
                "  2. Verify the provider's setup() method completed successfully\n"
                "  3. Check provider logs for initialization errors\n"
                "  4. Verify component discovery completed without errors"
            )
            err.add_context("hub.dimension", "singleton")
            err.add_context("hub.component_type", "provider")
            err.add_context("terraform.summary", "Provider not registered")
            err.add_context(
                "terraform.detail", "The provider has not been properly registered with the framework."
            )
            raise err

        logger.debug(
            "Provider instance retrieved for configuration",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
            provider_version=provider_instance.metadata.version,
        )

        provider_schema = provider_instance.schema
        config_cty = unmarshal(request.config, schema=provider_schema.block)

        if config_cty.is_unknown:
            logger.warning(
                "Provider configuration contains unknown values, deferring configuration",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )
            return response

        logger.debug(
            "Parsing provider configuration",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
        )

        config_instance = BaseResource.from_cty(config_cty, provider_instance.config_class)

        if config_instance is None:
            logger.error(
                "Failed to parse provider configuration into attrs instance",
                operation="configure_provider",
                provider_name=provider_instance.metadata.name,
            )

            err = ProviderConfigurationError(
                f"Failed to instantiate provider configuration for '{provider_instance.metadata.name}'.\n\n"
                f"Suggestion: Ensure all required provider configuration fields are provided with valid types.\n\n"
                f"Troubleshooting:\n"
                f"  1. Review the provider schema for required vs optional fields\n"
                f"  2. Check that all field values have the correct type\n"
                f"  3. Ensure no required fields are unknown/computed during configuration\n"
                f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG"
            )
            err.add_context("config.schema", str(provider_schema.block) if provider_schema else "None")
            err.add_context("provider.name", provider_instance.metadata.name)
            err.add_context("terraform.summary", "Invalid provider configuration")
            err.add_context(
                "terraform.detail", "The provider configuration could not be parsed into the expected format."
            )
            raise err

        logger.debug(
            "Creating provider context",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
        )

        test_mode_enabled = getattr(config_instance, "provider_testmode", False)
        provider_context = ProviderContext(config=config_instance, test_mode_enabled=test_mode_enabled)
        hub.register("singleton", "provider_context", provider_context)

        logger.info(
            "Provider configured successfully",
            operation="configure_provider",
            provider_name=provider_instance.metadata.name,
            provider_version=provider_instance.metadata.version,
            test_mode_enabled=test_mode_enabled,
        )

    except PyviderError as e:
        logger.error(
            "ConfigureProvider failed with framework error",
            operation="configure_provider",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        logger.error(
            "ConfigureProvider failed with unexpected error",
            operation="configure_provider",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    return response
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/get_metadata.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/get_metadata.py
#
# pyvider/protocols/tfprotov6/handlers/get_metadata.py
#

import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.handlers.utils import get_filtered_components


@resilient()
async def GetMetadataHandler(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Get provider metadata with dynamically discovered resources."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="GetMetadata")

    try:
        return await _get_metadata_impl(request, context)
    except Exception:
        handler_errors.inc(handler="GetMetadata")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="GetMetadata")


async def _get_metadata_impl(request: pb.GetMetadata.Request, context: Any) -> pb.GetMetadata.Response:
    """Implementation of GetMetadata handler."""
    logger.debug(
        "GetMetadata handler called",
        operation="get_metadata",
        handler="GetMetadata",
    )

    try:
        # Dynamically discover registered resources, filtered by test mode
        filtered_resources = get_filtered_components("resource")
        resources = []
        for resource_name in filtered_resources:
            resources.append(pb.GetMetadata.ResourceMetadata(type_name=resource_name))
            logger.debug(
                "Resource discovered during metadata collection",
                operation="get_metadata",
                component_type="resource",
                component_name=resource_name,
            )

        # Get data sources, filtered by test mode
        filtered_data_sources = get_filtered_components("data_source")
        data_sources = []
        for ds_name in filtered_data_sources:
            data_sources.append(pb.GetMetadata.DataSourceMetadata(type_name=ds_name))
            logger.debug(
                "Data source discovered during metadata collection",
                operation="get_metadata",
                component_type="data_source",
                component_name=ds_name,
            )

        # Get functions, filtered by test mode
        filtered_functions = get_filtered_components("function")
        functions = []
        for func_name in filtered_functions:
            functions.append(pb.GetMetadata.FunctionMetadata(name=func_name))
            logger.debug(
                "Function discovered during metadata collection",
                operation="get_metadata",
                component_type="function",
                component_name=func_name,
            )

        logger.info(
            "GetMetadata completed successfully",
            operation="get_metadata",
            resource_count=len(resources),
            data_source_count=len(data_sources),
            function_count=len(functions),
        )

        response = pb.GetMetadata.Response(
            server_capabilities=pb.ServerCapabilities(
                plan_destroy=True,
                get_provider_schema_optional=True,
                move_resource_state=True,
            ),
            resources=resources,
            data_sources=data_sources,
            functions=functions,
            diagnostics=[],
        )

        return response

    except Exception as e:
        logger.error(
            "GetMetadata handler failed",
            operation="get_metadata",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Failed to discover provider metadata: {e!s}\n\n"
            f"Suggestion: Ensure all resources, data sources, and functions are properly registered "
            f"using @resource, @data_source, and @function decorators.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that component decorators are applied correctly\n"
            f"  2. Verify that the hub discovery process completed successfully\n"
            f"  3. Review provider logs for component registration errors\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {e!s}"
        )

        return pb.GetMetadata.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Provider metadata discovery failed",
                    detail=error_detail,
                )
            ]
        )


# 🐍🏗⛮️
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/get_provider_schema.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/get_provider_schema.py
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
from pyvider.protocols.tfprotov6.handlers.utils import get_filtered_components

# --- Module-level Cache using asyncio.Future ---
_schema_future: asyncio.Future[pb.GetProviderSchema.Response] | None = None
_task: asyncio.Task | None = None  # Store a reference to the task
_cache_lock = asyncio.Lock()  # Lock to protect the creation of the Future itself


async def _collect_resource_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    resource_schemas = {}
    filtered_resources = get_filtered_components("resource")
    for name, resource_class in filtered_resources.items():
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


async def _collect_data_source_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Schema]:
    data_source_schemas = {}
    filtered_data_sources = get_filtered_components("data_source")
    for name, ds_class in filtered_data_sources.items():
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


async def _collect_function_schemas(
    diagnostics: list[pb.Diagnostic],
) -> dict[str, pb.Function]:
    functions = {}
    filtered_functions = get_filtered_components("function")
    for name, func_obj in filtered_functions.items():
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


async def _compute_schema_once() -> pb.GetProviderSchema.Response:
    """
    The core, expensive computation logic for building the provider schema.
    This function is now only ever called once.
    """
    logger.debug(
        "Computing provider schema for the first time",
        operation="compute_schema",
    )

    diagnostics = []
    try:
        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            logger.error(
                "Provider instance not found during schema computation",
                operation="compute_schema",
            )
            raise RuntimeError(
                "Provider instance not found in hub.\n\n"
                "This indicates the provider's setup() method may have failed or "
                "the provider was not properly registered.\n\n"
                "Troubleshooting:\n"
                "  1. Ensure the provider class has the @provider decorator\n"
                "  2. Verify the provider's setup() method completed successfully\n"
                "  3. Check provider logs for initialization errors\n"
                "  4. Verify component discovery completed without errors"
            )

        logger.debug(
            "Converting provider schema to protocol buffer format",
            operation="compute_schema",
            provider_name=provider_instance.metadata.name,
        )

        provider_schema = provider_instance.schema
        provider_proto_schema = await pvs_schema_to_proto(provider_schema)

        logger.debug(
            "Collecting component schemas",
            operation="compute_schema",
        )

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

        logger.info(
            "Provider schema computed and cached successfully",
            operation="compute_schema",
            provider_name=provider_instance.metadata.name,
            resource_count=len(resource_schemas),
            data_source_count=len(data_source_schemas),
            function_count=len(functions),
            warning_count=len([d for d in diagnostics if d.severity == pb.Diagnostic.WARNING]),
        )

        return response

    except Exception as e:
        logger.error(
            "Failed to compute provider schema",
            operation="compute_schema",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )

        error_detail = (
            f"Failed to compute provider schema: {e}\n\n"
            f"Suggestion: This usually indicates an issue with provider initialization "
            f"or schema definition.\n\n"
            f"Troubleshooting:\n"
            f"  1. Check that all resources/data sources have valid schema definitions\n"
            f"  2. Verify component discovery completed successfully\n"
            f"  3. Review provider logs for initialization errors\n"
            f"  4. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG\n\n"
            f"Error details: {type(e).__name__}: {e}"
        )

        return pb.GetProviderSchema.Response(
            diagnostics=[
                pb.Diagnostic(
                    severity=pb.Diagnostic.ERROR,
                    summary="Provider schema computation failed",
                    detail=error_detail,
                )
            ]
        )


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


async def _get_provider_schema_impl(
    request: pb.GetProviderSchema.Request, context: Any
) -> pb.GetProviderSchema.Response:
    """Implementation of GetProviderSchema handler."""
    global _schema_future
    logger.debug(
        "GetProviderSchema handler called",
        operation="get_provider_schema",
        cache_exists=_schema_future is not None,
    )

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


async def _set_future_result(future: asyncio.Future) -> None:
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
EOF

log_update "Updating: pyvider/protocols/tfprotov6/handlers/utils.py"
mkdir -p pyvider/protocols/tfprotov6/handlers/
cat <<'EOF' > pyvider/protocols/tfprotov6/handlers/utils.py
import inspect
import re
from typing import Any

import attrs
from provide.foundation import logger
from provide.foundation.errors import FoundationError

from pyvider.cty import CtyList, CtyObject, CtyTuple, CtyValue
from pyvider.cty.exceptions import (
    CtyAttributeValidationError,
    CtyBoolValidationError,
    CtyListValidationError,
    CtyMapValidationError,
    CtyNumberValidationError,
    CtySetValidationError,
    CtyStringValidationError,
    CtyTupleValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
from pyvider.exceptions import (
    DataSourceError,
    FunctionError,
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource

# Regex to parse attribute paths like `attr`, `attr[0]`, `attr["key"]`
PATH_STEP_REGEX = re.compile(r"(\.?)(\w+)|\[(\d+)\]|\[['\"]([^'\"]+)['\"]\]")


def get_filtered_components(component_type: str) -> dict[str, Any]:
    """
    Retrieves components of a given type, filtering out test-only components
    if the provider is not in test mode.
    """
    provider_context = hub.get_component("singleton", "provider_context")
    test_mode_enabled = getattr(provider_context, "test_mode_enabled", False)

    all_components = hub.get_components(component_type)

    if test_mode_enabled:
        logger.debug(f"Test mode enabled, returning all {component_type} components.")
        return all_components

    production_components = {
        name: comp
        for name, comp in all_components.items()
        if not getattr(comp, "_is_test_only", False)
    }
    logger.debug(
        f"Filtered {component_type} components for production mode.",
        total=len(all_components),
        production=len(production_components),
    )
    return production_components


def _process_instance(instance: Any, _visited: set[int]) -> Any:
    obj_id = id(instance)
    if obj_id in _visited:
        if attrs.has(type(instance)):
            return {"__circular_ref__": type(instance).__name__}
        else:
            return f"<circular_ref:{type(instance).__name__}>"

    if not isinstance(instance, str | int | float | bool | type(None)):
        _visited.add(obj_id)

    try:
        if attrs.has(type(instance)):
            res = {}
            for a in attrs.fields(type(instance)):
                value = getattr(instance, a.name)
                res[a.name] = attrs_to_dict_for_cty(value, _visited)
            return res
        elif isinstance(instance, tuple):
            return tuple(attrs_to_dict_for_cty(item, _visited) for item in instance)
        elif isinstance(instance, list):
            return [attrs_to_dict_for_cty(item, _visited) for item in instance]
        elif isinstance(instance, dict):
            return {k: attrs_to_dict_for_cty(v, _visited) for k, v in instance.items()}
        else:
            return instance
    finally:
        if not isinstance(instance, str | int | float | bool | type(None)) and obj_id in _visited:
            _visited.remove(obj_id)


def attrs_to_dict_for_cty(instance: Any, _visited: set[int] | None = None) -> Any:
    """
    Recursively converts an object into a structure of dictionaries, lists,
    and primitives suitable for CTY validation. It correctly handles nested
    attrs instances, preserves tuples, and passes through CtyValue objects.
    Includes recursion detection to prevent infinite loops.
    """
    if _visited is None:
        _visited = set()

    if isinstance(instance, CtyValue):
        return instance

    return _process_instance(instance, _visited)


def _check_type_and_unknown(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if not plan.type.equal(result.type):
        return (
            False,
            f"Type mismatch: plan was {plan.type}, but result was {result.type}.",
        )

    # If the plan is UNREFINED_UNKNOWN, it can be refined to any concrete value.
    if plan.value is UNREFINED_UNKNOWN:
        return True, ""

    if plan.is_unknown:
        return True, ""

    if result.is_unknown:
        return False, "Value was known in plan but became unknown in result."

    return True, ""


def _check_null_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.is_null:
        return True, ""

    if result.is_null:
        return False, "Value was non-null in plan but became null in result."

    return True, ""


def _check_object_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if plan.value.keys() != result.value.keys():
        return (
            False,
            f"Object attribute mismatch. Plan keys: {plan.value.keys()}, Result keys: {result.value.keys()}",
        )

    for attr_name in plan.value:
        is_valid, reason = is_valid_refinement(plan.value[attr_name], result.value[attr_name])
        if not is_valid:
            return False, f"Attribute '{attr_name}': {reason}"
    return True, ""


def _check_collection_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    if len(plan.value) != len(result.value):
        return (
            False,
            f"Collection length changed: was {len(plan.value)}, now {len(result.value)}.",
        )
    for i in range(len(plan.value)):
        is_valid, reason = is_valid_refinement(plan.value[i], result.value[i])
        if not is_valid:
            return False, f"Index [{i}]: {reason}"
    return True, ""


def is_valid_refinement(plan: CtyValue, result: CtyValue) -> tuple[bool, str]:
    """
    Checks if the `result` state is a valid refinement of the `plan` state.
    A value can be refined from unknown to null/concrete, or from null to concrete.
    It cannot be refined from a concrete value to a different value, null, or unknown.
    """
    is_valid, reason = _check_type_and_unknown(plan, result)
    if not is_valid:
        return False, reason

    is_valid, reason = _check_null_refinement(plan, result)
    if not is_valid:
        return False, reason

    # If plan is null, refinement to any concrete value is valid
    if plan.is_null:
        return True, ""

    if isinstance(plan.type, CtyObject):
        return _check_object_refinement(plan, result)

    if isinstance(plan.type, CtyList | CtyTuple):
        return _check_collection_refinement(plan, result)

    if plan.is_unknown:
        return True, ""

    if plan.value != result.value:
        return (
            False,
            f"Value mismatch: planned value was '{plan.value}', result was '{result.value}'.",
        )

    return True, ""


def str_path_to_proto_path(path_str: str | None) -> pb.AttributePath | None:
    if not path_str:
        return None

    proto_steps = []
    normalized_path = path_str.replace("].", "][")

    for match in PATH_STEP_REGEX.finditer(normalized_path):
        _dot, attr, index, key = match.groups()
        if attr:
            proto_steps.append(pb.AttributePath.Step(attribute_name=attr))
        elif index:
            proto_steps.append(pb.AttributePath.Step(element_key_int=int(index)))
        elif key:
            proto_steps.append(pb.AttributePath.Step(element_key_string=key))

    return pb.AttributePath(steps=proto_steps)


def cty_path_to_proto_path(cty_path: CtyPath | None) -> pb.AttributePath | None:
    if not cty_path or not cty_path.steps:
        return None
    proto_steps = []
    for step in cty_path.steps:
        match step:
            case GetAttrStep(name=name):
                proto_steps.append(pb.AttributePath.Step(attribute_name=name))
            case IndexStep(index=index):
                proto_steps.append(pb.AttributePath.Step(element_key_int=index))
            case KeyStep(key=key):
                proto_steps.append(pb.AttributePath.Step(element_key_string=str(key)))
    return pb.AttributePath(steps=proto_steps)


async def create_diagnostic_from_exception(exc: Exception) -> pb.Diagnostic:  # noqa: C901
    """Create a Terraform diagnostic from an exception.

    Uses foundation's ErrorContext when available for richer diagnostics.
    """
    summary = "An unexpected error occurred"
    detail = str(exc)
    attribute_path: CtyPath | None = None
    severity = pb.Diagnostic.ERROR

    # First handle specific CTY validation errors
    specific_validation_errors = (
        CtyAttributeValidationError,
        CtyListValidationError,
        CtySetValidationError,
        CtyTupleValidationError,
        CtyMapValidationError,
        CtyNumberValidationError,
        CtyStringValidationError,
        CtyBoolValidationError,
    )

    if isinstance(exc, specific_validation_errors):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = f"Validation failed for a value of type '{exc.type_name}'."
        if hasattr(exc, "value") and exc.value is not None:
            value_repr = repr(exc.value)
            if len(value_repr) > 100:
                value_repr = value_repr[:97] + "..."
            detail += f" The invalid value provided was {value_repr}."
        attribute_path = exc.path
    elif isinstance(exc, CtyValidationError):
        summary = f"🐍🏗️ ⚠️ {exc.message}"
        detail = "A configuration validation error occurred."
        attribute_path = exc.path
    # Check if this is a foundation error with context
    elif isinstance(exc, FoundationError) and hasattr(exc, "context"):
        # Use foundation's error context for richer diagnostics
        context = exc.context

        # Check for severity in context dict
        if isinstance(context, dict):
            # Default to ERROR severity
            severity = pb.Diagnostic.ERROR

            # Check for Terraform-specific metadata
            if "terraform.summary" in context:
                summary = context["terraform.summary"]

            # Build detail including original message and terraform detail
            detail_parts = [str(exc)]
            if "terraform.detail" in context:
                detail_parts.append(context["terraform.detail"])

            # Add other context items
            for key, value in context.items():
                if not key.startswith("terraform.") and key != "private_state.error" and value:
                    detail_parts.append(f"{key}: {value}")

            detail = "\n".join(detail_parts) if detail_parts else str(exc)
    else:
        # Handle other specific exception types
        if isinstance(exc, ResourceLifecycleContractError):
            summary = "🐍🏗️ ⚠️ Resource Lifecycle Contract Violation"
            detail = str(exc)
            if hasattr(exc, "detail") and exc.detail:
                detail += f"\n\nDetails:\n{exc.detail}"
        elif isinstance(exc, FunctionError):
            summary = "🐍🏗️ ❌ Function Execution Error"
            detail = str(exc)
        elif isinstance(exc, ResourceError | DataSourceError):
            summary = "🐍🏗️ ❌ Provider Operation Error"
            detail = str(exc)
        elif isinstance(exc, PyviderError):
            summary = "🐍🏗️ ❌ Provider Framework Error"
            detail = str(exc)
        else:
            summary = f"🐍🏗️ 🐛 Internal Provider Error: {type(exc).__name__}"
            detail = (
                "The provider encountered an unexpected error. This is likely a bug in the provider."
                "\nPlease report this issue to the provider developers."
            )
            logger.error(
                f"Creating diagnostic for unhandled exception type: {type(exc).__name__}",
                exc_info=True,
            )

    return pb.Diagnostic(
        severity=severity,
        summary=summary,
        detail=detail,
        attribute=cty_path_to_proto_path(attribute_path),
    )


def cty_to_attrs_instance(cty_val: CtyValue | None, attrs_cls: type[Any] | None) -> Any | None:
    if attrs_cls is None:
        return None
    if not inspect.isclass(attrs_cls):
        raise TypeError("Internal validation error: Passed object must be a class.")

    return BaseResource.from_cty(cty_val, attrs_cls)
EOF

log_update "Updating: pyvider/providers/context.py"
mkdir -p pyvider/providers/
cat <<'EOF' > pyvider/providers/context.py
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import define, field
from provide.foundation import logger

from pyvider.common.context import BaseContext

if TYPE_CHECKING:
    from pyvider.providers.base import BaseProvider


@define
class ProviderContext(BaseContext):
    """
    Holds the configured state of the provider. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: Any = field()
    provider: BaseProvider | None = field(default=None, init=False)
    test_mode_enabled: bool = field(default=False, kw_only=True)

    def __attrs_post_init__(self) -> None:
        logger.info(
            "ProviderContext initialized",
            config_type=type(self.config).__name__,
            test_mode=self.test_mode_enabled,
        )
EOF

log_update "Updating: pyvider/providers/provider.py"
mkdir -p pyvider/providers/
cat <<'EOF' > pyvider/providers/provider.py
from typing import ClassVar

from provide.foundation import logger

from pyvider.capabilities import BaseCapability
from pyvider.common.utils.attrs_factory import create_attrs_class_from_schema
from pyvider.exceptions import FrameworkConfigurationError
from pyvider.hub import hub
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.providers.decorators import register_provider
from pyvider.schema import a_bool, s_provider


@register_provider("pyvider")
class PyviderProvider(BaseProvider):
    capabilities: ClassVar[dict[str, BaseCapability]] = {}

    def __init__(self) -> None:
        provider_metadata = ProviderMetadata(name="pyvider", version="0.1.0")
        super().__init__(metadata=provider_metadata)
        logger.info("PyviderProvider orchestrator initialized.")

    async def setup(self) -> None:
        final_attributes = {
            "provider_testmode": a_bool(
                description="If true, enables test-only resources and data sources for development purposes.",
                optional=True,
            )
        }
        capability_classes = hub.get_components("capability")

        provider_ctx = hub.get_component("singleton", "provider_context")
        provider_config = provider_ctx.config if provider_ctx else None

        for name, cap_class in capability_classes.items():
            cap_instance = cap_class(config=provider_config)
            self.capabilities[name] = cap_instance
            if hasattr(cap_instance, "get_schema_contribution"):
                final_attributes.update(cap_instance.get_schema_contribution())

        self.capabilities["provider"] = self

        self._final_schema = s_provider(attributes=final_attributes)
        self.config_class = create_attrs_class_from_schema(
            "ProviderConfig", self._final_schema.block.attributes
        )

        all_components = {
            **hub.get_components("resource"),
            **hub.get_components("data_source"),
            **hub.get_components("function"),
        }
        for name, comp in all_components.items():
            parent_cap_name = getattr(comp, "_parent_capability", "provider")
            if parent_cap_name not in self.capabilities:
                raise FrameworkConfigurationError(
                    f"Component '{name}' is associated with capability '{parent_cap_name}', but that capability is not registered."
                )
EOF

log_update "Updating: pyvider/resources/decorators.py"
mkdir -p pyvider/resources/
cat <<'EOF' > pyvider/resources/decorators.py
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from provide.foundation import logger

P = ParamSpec("P")
T = TypeVar("T")


def register_resource(
    name: str, component_of: str | None = None, test_only: bool = False
) -> Callable[[type], type]:
    """
    Decorator to register a resource and associate it with a capability.
    """

    def decorator(cls: type) -> type:
        cls._is_registered_resource = True  # type: ignore[attr-defined]
        cls._registered_name = name  # type: ignore[attr-defined]
        cls._is_test_only = test_only  # type: ignore[attr-defined]
        if component_of:
            cls._parent_capability = component_of  # type: ignore
        logger.debug(
            f"🔧 Marked resource '{name}' for discovery",
            capability=component_of,
            test_only=test_only,
        )
        return cls

    return decorator
EOF

log_success "Project update for provider_testmode complete."