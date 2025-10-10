import inspect
import time
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyDynamic, CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.exceptions import FunctionError as PyviderFunctionError
from pyvider.functions.adapters import function_to_dict
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import create_diagnostic_from_exception
import pyvider.protocols.tfprotov6.protobuf as pb


def _process_function_arguments(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    native_kwargs = {}
    has_unknown = False
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments, params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val
    return native_kwargs, has_unknown


def _inject_capabilities(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", parent_capability)
        if capability_class:
            if isinstance(capability_class, type):
                capability_instance = capability_class()
            else:
                capability_instance = capability_class
            native_kwargs[parent_capability] = capability_instance
            logger.debug(
                f"FUNCTION_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{function_obj.__name__}'"
            )
        else:
            logger.warning(
                f"FUNCTION_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{function_obj.__name__}'"
            )


async def _invoke_function(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    try:
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(**native_kwargs)
        else:
            result_py_val = function_obj(**native_kwargs)
        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Function '{function_obj.__name__}' failed: {func_err}",
            exc_info=True,
        )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


@resilient()
async def CallFunctionHandler(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """
    Handles the CallFunction RPC request, acting as a robust dispatcher.
    """
    start_time = time.perf_counter()
    handler_requests.inc(handler="CallFunction")

    try:
        return await _call_function_impl(request, context)
    except Exception:
        handler_errors.inc(handler="CallFunction")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="CallFunction")


async def _call_function_impl(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        func_sig = inspect.signature(function_obj)

        if len(request.arguments) != len(params_meta):
            raise PyviderFunctionError(
                f"Incorrect number of arguments for {func_name}: expected {len(params_meta)}, got {len(request.arguments)}."
            )

        native_kwargs, has_unknown = _process_function_arguments(request.arguments, params_meta, func_sig)

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = await _invoke_function(function_obj, native_kwargs)

        marshalled_result = marshal(result_py_val, schema=declared_return_cty_type)
        response.result.CopyFrom(marshalled_result)

        logger.debug(f"FUNCTION_DISPATCH ✅ Successfully executed '{func_name}'.")

    except PyviderFunctionError as fe:
        response.error.text = str(fe)
    except Exception as e:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Unhandled error in CallFunctionHandler for '{request.name}'",
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response
