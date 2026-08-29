#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Callable
import inspect
from typing import Any, cast

from provide.foundation import logger

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyDynamic, CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.exceptions import FunctionError as PyviderFunctionError
from pyvider.functions.adapters import function_to_dict
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers._metrics import rpc_handler
from pyvider.protocols.tfprotov6.handlers.utils import (
    check_test_only_access,
    create_diagnostic_from_exception,
)
import pyvider.protocols.tfprotov6.protobuf as pb


def _process_function_arguments(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
    func_name: str = "",
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(
        zip(request_arguments[: len(params_meta)], params_meta, strict=False)
    ):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        # `is_unknown` is top-level only: a *list* whose elements are unknown is
        # itself known, so this guard used to let it through, `cty_to_native`
        # rendered those elements as None, and the provider's function received
        # a half-known argument. `join("\n", [resource.a.token, ...])` at plan
        # time then raised TypeError from inside str.join and Terraform reported
        # "Invalid function argument" for a configuration that was perfectly
        # valid. Same rule as `cty_to_attrs_instance`: a provider is never
        # handed a partially known object.
        if not decoded_cty_val.is_wholly_known():
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta) :]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            # Same reasoning as the required parameters above.
            if not decoded_cty_val.is_wholly_known():
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        if not has_unknown:
            _bind_variadic_arguments(
                native_kwargs, func_sig, variadic_meta.get("name"), variadic_args, func_name
            )

    return native_kwargs, has_unknown


def _bind_variadic_arguments(
    native_kwargs: dict[str, Any],
    func_sig: inspect.Signature,
    variadic_param_name: str | None,
    variadic_args: list[Any],
    func_name: str,
) -> None:
    """
    Bind the trailing arguments to the parameter the schema's variadic slot came from.

    `_extract_parameters_meta` fills `variadic_parameter` from two very different
    signature shapes, because tfproto v6 has no optional positional parameter and
    the variadic slot is the only trailing thing a caller may omit: a genuine
    `*args`, which takes every trailing argument, and a plain parameter carrying a
    default, which has exactly one.

    This used to search the signature for a VAR_POSITIONAL and bind nothing when it
    found none -- so `def repeat(text, count=2)` decoded the `count` Terraform sent,
    converted it, and dropped it on the floor. `repeat("ab", 5)` returned "abab"
    with no error and no diagnostic: a silently wrong answer, which is worse than a
    failed apply because nothing reports it. The parameter is now looked up by the
    name the adapter recorded, so both shapes bind.
    """
    param = func_sig.parameters.get(variadic_param_name) if variadic_param_name else None
    if param is None:
        # A signature whose variadic name the adapter could not record still has
        # its *args; fall back to it rather than dropping the arguments.
        param = next(
            (p for p in func_sig.parameters.values() if p.kind == inspect.Parameter.VAR_POSITIONAL),
            None,
        )
    if param is None:
        raise PyviderFunctionError(
            f"Function '{func_name}' declares a variadic parameter "
            f"{variadic_param_name!r} that its signature does not have.\n\n"
            f"Suggestion: this is a bug in the provider, not in the configuration."
        )

    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        native_kwargs[param.name] = tuple(variadic_args)
        return

    # Terraform sends an explicit null for an argument the practitioner left out,
    # so a null here means "omitted" and Python's default stands. Same rule the
    # required-parameter loop above applies, and keyed on the same condition. A
    # null reaching a genuine *args is a real element and is kept.
    if len(variadic_args) == 1 and variadic_args[0] is None:
        return

    # A defaulted parameter is one slot. Terraform will happily send more, because
    # the schema advertises a variadic; refuse rather than bind the first and
    # discard the rest.
    if len(variadic_args) > 1:
        raise PyviderFunctionError(
            f"Incorrect number of arguments for function '{func_name}'.\n\n"
            f"Expected: at most {len(func_sig.parameters)} arguments "
            f"('{param.name}' is optional, not variadic)\n"
            f"Received: {len(variadic_args)} arguments beyond the required ones\n\n"
            f"Suggestion: provide at most one value for '{param.name}'."
        )
    native_kwargs[param.name] = variadic_args[0]


def _inject_capabilities(function_obj: Any, native_kwargs: dict[str, Any], func_name: str) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    logger.info(
        f"FUNCTION_DISPATCH 🔍 Checking capability injection for '{func_name}', parent_capability={parent_capability}"
    )
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", parent_capability)
        logger.info(
            f"FUNCTION_DISPATCH 🔍 Retrieved capability class: {capability_class} (type={type(capability_class)})"
        )
        if capability_class:
            if isinstance(capability_class, type):
                capability_instance = capability_class()
            else:
                capability_instance = capability_class
            native_kwargs[parent_capability] = capability_instance
            logger.info(
                "Injected capability for function",
                capability=parent_capability,
                func_name=func_name,
                instance=str(capability_instance),
            )
        else:
            logger.warning(
                "Capability not found for function", capability=parent_capability, func_name=func_name
            )


def _build_function_arguments(
    func_sig: inspect.Signature, native_kwargs: dict[str, Any]
) -> tuple[list[Any], dict[str, Any]]:
    """Build positional and keyword arguments from native kwargs based on signature."""
    positional_args: list[Any] = []
    variadic_args: list[Any] | tuple[Any, ...] = []
    keyword_only_kwargs: dict[str, Any] = {}

    for param_name, param in func_sig.parameters.items():
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            # This is a *args parameter - extract its tuple
            if param_name in native_kwargs:
                variadic_args = native_kwargs[param_name]
                if not isinstance(variadic_args, (tuple, list)):
                    variadic_args = (variadic_args,)
        elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            # Regular positional parameter - add to ordered list
            if param_name in native_kwargs:
                positional_args.append(native_kwargs[param_name])
        elif param.kind == inspect.Parameter.KEYWORD_ONLY and param_name in native_kwargs:
            # Keyword-only parameter - must be passed as kwarg
            keyword_only_kwargs[param_name] = native_kwargs[param_name]

    # Combine: required positional + variadic
    all_args = positional_args + list(variadic_args)
    return all_args, keyword_only_kwargs


async def _invoke_function(function_obj: Any, native_kwargs: dict[str, Any], func_name: str) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        # Get signature of the callable (call method for BaseFunction instances)
        if hasattr(function_obj, "call"):
            func_sig = inspect.signature(function_obj.call)
        else:
            func_sig = inspect.signature(function_obj)
        all_args, keyword_only_kwargs = _build_function_arguments(func_sig, native_kwargs)

        # Invoke with ordered positional args + keyword-only kwargs
        # Check if __call__ method is async (for BaseFunction instances)
        if (
            callable(function_obj) and inspect.iscoroutinefunction(function_obj.__call__)
        ) or inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug("Function executed successfully", func_name=func_name)
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            "Function execution failed",
            func_name=func_name,
            error=str(func_err),
            exc_info=True,
        )
        raise PyviderFunctionError(f"Function '{func_name}' execution failed: {func_err}") from func_err


@rpc_handler("CallFunction")
async def CallFunctionHandler(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """
    Handles the CallFunction RPC request, acting as a robust dispatcher.
    """
    return await _call_function_impl(request, context)


async def _call_function_impl(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(
        "CallFunction handler called",
        operation="call_function",
        function_name=request.name,
        argument_count=len(request.arguments),
    )

    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            logger.error(
                "Function call attempted without function name",
                operation="call_function",
            )
            raise PyviderFunctionError(
                "Function name is required.\n\n"
                "This is an internal error - Terraform should always provide a function name."
            )

        function_cls = hub.get_component("function", func_name)
        if not function_cls:
            logger.error(
                "Function not found",
                operation="call_function",
                function_name=func_name,
                registered_functions=list(hub.get_components("function").keys())
                if hub.get_components("function")
                else [],
            )

            raise PyviderFunctionError(
                f"Function '{func_name}' not found.\n\n"
                f"Suggestion: Ensure the function is registered using the @function decorator "
                f"and that component discovery has completed successfully.\n\n"
                f"Troubleshooting:\n"
                f"  1. Check that the function has the @function decorator\n"
                f"  2. Verify the function module is imported by the provider\n"
                f"  3. Run 'pyvider components list' to see registered functions\n"
                f"  4. Review provider logs for component registration errors"
            )

        # Instantiate the function class if it's a class. inspect.isclass narrows to
        # bare `type`, which drops the constructor signature the hub actually hands
        # back, so the class branch is cast back to a callable factory.
        function_obj: Any = (
            cast("Callable[..., Any]", function_cls)(name=func_name)
            if inspect.isclass(function_cls)
            else function_cls
        )

        # Check if this is a test-only component accessed without test mode
        check_test_only_access(function_obj, func_name, "function")

        func_meta = function_to_dict(function_cls)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        # Support both class-based functions (with .call method) and plain functions
        if hasattr(function_obj, "call"):
            func_sig = inspect.signature(function_obj.call)
        else:
            func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                logger.error(
                    "Function called with too few arguments (variadic)",
                    operation="call_function",
                    function_name=func_name,
                    required_count=num_required,
                    provided_count=num_provided,
                    has_variadic=True,
                )
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for function '{func_name}'.\n\n"
                    f"Expected: at least {num_required} arguments (function accepts variadic arguments)\n"
                    f"Received: {num_provided} arguments\n\n"
                    f"Suggestion: Provide at least {num_required} arguments. This function accepts "
                    f"additional variadic arguments beyond the required ones."
                )
        # Without variadic parameter, must match exactly
        elif num_provided != num_required:
            logger.error(
                "Function called with wrong number of arguments",
                operation="call_function",
                function_name=func_name,
                required_count=num_required,
                provided_count=num_provided,
                has_variadic=False,
            )
            raise PyviderFunctionError(
                f"Incorrect number of arguments for function '{func_name}'.\n\n"
                f"Expected: {num_required} arguments\n"
                f"Received: {num_provided} arguments\n\n"
                f"Suggestion: Provide exactly {num_required} arguments to this function."
            )

        native_kwargs, has_unknown = _process_function_arguments(
            list(request.arguments), params_meta, variadic_meta, func_sig, func_name
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(
                "Function call short-circuited due to unknown argument",
                operation="call_function",
                function_name=func_name,
                reason="unknown_argument",
            )
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs, func_name)

        logger.debug(
            "Invoking function",
            operation="call_function",
            function_name=func_name,
            argument_names=list(native_kwargs.keys()),
        )

        result_py_val = await _invoke_function(function_obj, native_kwargs, func_name)

        marshalled_result = marshal(result_py_val, schema=declared_return_cty_type)
        response.result.CopyFrom(marshalled_result)

        logger.info(
            "Function executed successfully",
            operation="call_function",
            function_name=func_name,
            result_type=type(result_py_val).__name__,
        )

    except PyviderFunctionError as fe:
        logger.error(
            "Function execution failed with PyviderFunctionError",
            operation="call_function",
            function_name=request.name,
            error_message=str(fe),
        )
        response.error.text = str(fe)
    except Exception as e:
        logger.error(
            "Function execution failed with unexpected error",
            operation="call_function",
            function_name=request.name,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


# 🐍🏗️🔚
