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


def x__process_function_arguments__mutmut_orig(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_1(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = None
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_2(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = None

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_3(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = True

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_4(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(None):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_5(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(None, params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_6(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], None, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_7(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=None)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_8(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_9(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_10(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, )):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_11(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=True)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_12(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = None
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_13(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get(None, f"arg{i}")
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_14(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", None)
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_15(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get(f"arg{i}")
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_16(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", )
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_17(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("XXnameXX", f"arg{i}")
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_18(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("NAME", f"arg{i}")
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_19(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = None

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_20(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get(None, CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_21(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", None)

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_22(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get(CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_23(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", )

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_24(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("XXcty_typeXX", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_25(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("CTY_TYPE", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_26(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = None

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_27(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(None, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_28(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=None)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_29(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_30(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, )

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_31(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = None
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_32(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = False
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_33(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            return

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_34(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = None
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_35(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(None)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_36(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = None
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_37(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(None)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_38(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty or native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_39(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param or sig_param.default is not inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_40(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is inspect.Parameter.empty and native_val is None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_41(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is not None:
            continue

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_42(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
        param_name = param_meta.get("name", f"arg{i}")
        param_cty_type = param_meta.get("cty_type", CtyDynamic())

        decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)

        if decoded_cty_val.is_unknown:
            has_unknown = True
            break

        native_val = cty_to_native(decoded_cty_val)
        sig_param = func_sig.parameters.get(param_name)
        if sig_param and sig_param.default is not inspect.Parameter.empty and native_val is None:
            break

        native_kwargs[param_name] = native_val

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_43(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

        native_kwargs[param_name] = None

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_44(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta or len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_45(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) >= len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_46(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = None
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_47(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get(None, "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_48(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", None)
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_49(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_50(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", )
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_51(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("XXnameXX", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_52(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("NAME", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_53(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "XXoptionsXX")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_54(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "OPTIONS")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_55(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = None
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_56(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get(None, CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_57(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", None)
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_58(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get(CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_59(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", )
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_60(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("XXcty_typeXX", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_61(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("CTY_TYPE", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_62(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = None

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_63(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = None

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_64(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(None, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_65(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=None)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_66(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_67(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, )

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_68(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = None
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_69(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = False
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_70(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                return

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_71(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(None)

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_72(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(None))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_73(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind != inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_74(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = None
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_75(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(None)
                break

    return native_kwargs, has_unknown


def x__process_function_arguments__mutmut_76(
    request_arguments: list[pb.DynamicValue],
    params_meta: list[dict[str, Any]],
    variadic_meta: dict[str, Any] | None,
    func_sig: inspect.Signature,
) -> tuple[dict[str, Any], bool]:
    """
    Process function arguments including variadic parameters.

    Returns:
        tuple: (native_kwargs dict, has_unknown bool)
    """
    native_kwargs = {}
    has_unknown = False

    # Process required parameters
    for i, (arg_proto, param_meta) in enumerate(zip(request_arguments[:len(params_meta)], params_meta, strict=False)):
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

    # Process variadic parameters (extra arguments beyond required)
    if variadic_meta and len(request_arguments) > len(params_meta):
        variadic_param_name = variadic_meta.get("name", "options")
        variadic_cty_type = variadic_meta.get("cty_type", CtyDynamic())
        variadic_args = []

        for arg_proto in request_arguments[len(params_meta):]:
            decoded_cty_val = unmarshal(arg_proto, schema=variadic_cty_type)

            if decoded_cty_val.is_unknown:
                has_unknown = True
                break

            variadic_args.append(cty_to_native(decoded_cty_val))

        # Find the variadic parameter in the function signature
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                native_kwargs[param_name] = tuple(variadic_args)
                return

    return native_kwargs, has_unknown

x__process_function_arguments__mutmut_mutants : ClassVar[MutantDict] = {
'x__process_function_arguments__mutmut_1': x__process_function_arguments__mutmut_1, 
    'x__process_function_arguments__mutmut_2': x__process_function_arguments__mutmut_2, 
    'x__process_function_arguments__mutmut_3': x__process_function_arguments__mutmut_3, 
    'x__process_function_arguments__mutmut_4': x__process_function_arguments__mutmut_4, 
    'x__process_function_arguments__mutmut_5': x__process_function_arguments__mutmut_5, 
    'x__process_function_arguments__mutmut_6': x__process_function_arguments__mutmut_6, 
    'x__process_function_arguments__mutmut_7': x__process_function_arguments__mutmut_7, 
    'x__process_function_arguments__mutmut_8': x__process_function_arguments__mutmut_8, 
    'x__process_function_arguments__mutmut_9': x__process_function_arguments__mutmut_9, 
    'x__process_function_arguments__mutmut_10': x__process_function_arguments__mutmut_10, 
    'x__process_function_arguments__mutmut_11': x__process_function_arguments__mutmut_11, 
    'x__process_function_arguments__mutmut_12': x__process_function_arguments__mutmut_12, 
    'x__process_function_arguments__mutmut_13': x__process_function_arguments__mutmut_13, 
    'x__process_function_arguments__mutmut_14': x__process_function_arguments__mutmut_14, 
    'x__process_function_arguments__mutmut_15': x__process_function_arguments__mutmut_15, 
    'x__process_function_arguments__mutmut_16': x__process_function_arguments__mutmut_16, 
    'x__process_function_arguments__mutmut_17': x__process_function_arguments__mutmut_17, 
    'x__process_function_arguments__mutmut_18': x__process_function_arguments__mutmut_18, 
    'x__process_function_arguments__mutmut_19': x__process_function_arguments__mutmut_19, 
    'x__process_function_arguments__mutmut_20': x__process_function_arguments__mutmut_20, 
    'x__process_function_arguments__mutmut_21': x__process_function_arguments__mutmut_21, 
    'x__process_function_arguments__mutmut_22': x__process_function_arguments__mutmut_22, 
    'x__process_function_arguments__mutmut_23': x__process_function_arguments__mutmut_23, 
    'x__process_function_arguments__mutmut_24': x__process_function_arguments__mutmut_24, 
    'x__process_function_arguments__mutmut_25': x__process_function_arguments__mutmut_25, 
    'x__process_function_arguments__mutmut_26': x__process_function_arguments__mutmut_26, 
    'x__process_function_arguments__mutmut_27': x__process_function_arguments__mutmut_27, 
    'x__process_function_arguments__mutmut_28': x__process_function_arguments__mutmut_28, 
    'x__process_function_arguments__mutmut_29': x__process_function_arguments__mutmut_29, 
    'x__process_function_arguments__mutmut_30': x__process_function_arguments__mutmut_30, 
    'x__process_function_arguments__mutmut_31': x__process_function_arguments__mutmut_31, 
    'x__process_function_arguments__mutmut_32': x__process_function_arguments__mutmut_32, 
    'x__process_function_arguments__mutmut_33': x__process_function_arguments__mutmut_33, 
    'x__process_function_arguments__mutmut_34': x__process_function_arguments__mutmut_34, 
    'x__process_function_arguments__mutmut_35': x__process_function_arguments__mutmut_35, 
    'x__process_function_arguments__mutmut_36': x__process_function_arguments__mutmut_36, 
    'x__process_function_arguments__mutmut_37': x__process_function_arguments__mutmut_37, 
    'x__process_function_arguments__mutmut_38': x__process_function_arguments__mutmut_38, 
    'x__process_function_arguments__mutmut_39': x__process_function_arguments__mutmut_39, 
    'x__process_function_arguments__mutmut_40': x__process_function_arguments__mutmut_40, 
    'x__process_function_arguments__mutmut_41': x__process_function_arguments__mutmut_41, 
    'x__process_function_arguments__mutmut_42': x__process_function_arguments__mutmut_42, 
    'x__process_function_arguments__mutmut_43': x__process_function_arguments__mutmut_43, 
    'x__process_function_arguments__mutmut_44': x__process_function_arguments__mutmut_44, 
    'x__process_function_arguments__mutmut_45': x__process_function_arguments__mutmut_45, 
    'x__process_function_arguments__mutmut_46': x__process_function_arguments__mutmut_46, 
    'x__process_function_arguments__mutmut_47': x__process_function_arguments__mutmut_47, 
    'x__process_function_arguments__mutmut_48': x__process_function_arguments__mutmut_48, 
    'x__process_function_arguments__mutmut_49': x__process_function_arguments__mutmut_49, 
    'x__process_function_arguments__mutmut_50': x__process_function_arguments__mutmut_50, 
    'x__process_function_arguments__mutmut_51': x__process_function_arguments__mutmut_51, 
    'x__process_function_arguments__mutmut_52': x__process_function_arguments__mutmut_52, 
    'x__process_function_arguments__mutmut_53': x__process_function_arguments__mutmut_53, 
    'x__process_function_arguments__mutmut_54': x__process_function_arguments__mutmut_54, 
    'x__process_function_arguments__mutmut_55': x__process_function_arguments__mutmut_55, 
    'x__process_function_arguments__mutmut_56': x__process_function_arguments__mutmut_56, 
    'x__process_function_arguments__mutmut_57': x__process_function_arguments__mutmut_57, 
    'x__process_function_arguments__mutmut_58': x__process_function_arguments__mutmut_58, 
    'x__process_function_arguments__mutmut_59': x__process_function_arguments__mutmut_59, 
    'x__process_function_arguments__mutmut_60': x__process_function_arguments__mutmut_60, 
    'x__process_function_arguments__mutmut_61': x__process_function_arguments__mutmut_61, 
    'x__process_function_arguments__mutmut_62': x__process_function_arguments__mutmut_62, 
    'x__process_function_arguments__mutmut_63': x__process_function_arguments__mutmut_63, 
    'x__process_function_arguments__mutmut_64': x__process_function_arguments__mutmut_64, 
    'x__process_function_arguments__mutmut_65': x__process_function_arguments__mutmut_65, 
    'x__process_function_arguments__mutmut_66': x__process_function_arguments__mutmut_66, 
    'x__process_function_arguments__mutmut_67': x__process_function_arguments__mutmut_67, 
    'x__process_function_arguments__mutmut_68': x__process_function_arguments__mutmut_68, 
    'x__process_function_arguments__mutmut_69': x__process_function_arguments__mutmut_69, 
    'x__process_function_arguments__mutmut_70': x__process_function_arguments__mutmut_70, 
    'x__process_function_arguments__mutmut_71': x__process_function_arguments__mutmut_71, 
    'x__process_function_arguments__mutmut_72': x__process_function_arguments__mutmut_72, 
    'x__process_function_arguments__mutmut_73': x__process_function_arguments__mutmut_73, 
    'x__process_function_arguments__mutmut_74': x__process_function_arguments__mutmut_74, 
    'x__process_function_arguments__mutmut_75': x__process_function_arguments__mutmut_75, 
    'x__process_function_arguments__mutmut_76': x__process_function_arguments__mutmut_76
}

def _process_function_arguments(*args, **kwargs):
    result = _mutmut_trampoline(x__process_function_arguments__mutmut_orig, x__process_function_arguments__mutmut_mutants, args, kwargs)
    return result 

_process_function_arguments.__signature__ = _mutmut_signature(x__process_function_arguments__mutmut_orig)
x__process_function_arguments__mutmut_orig.__name__ = 'x__process_function_arguments'


def x__inject_capabilities__mutmut_orig(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
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


def x__inject_capabilities__mutmut_1(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = None
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


def x__inject_capabilities__mutmut_2(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(None, "_parent_capability", None)
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


def x__inject_capabilities__mutmut_3(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, None, None)
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


def x__inject_capabilities__mutmut_4(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr("_parent_capability", None)
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


def x__inject_capabilities__mutmut_5(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, None)
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


def x__inject_capabilities__mutmut_6(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", )
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


def x__inject_capabilities__mutmut_7(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "XX_parent_capabilityXX", None)
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


def x__inject_capabilities__mutmut_8(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_PARENT_CAPABILITY", None)
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


def x__inject_capabilities__mutmut_9(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability or parent_capability != "provider":
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


def x__inject_capabilities__mutmut_10(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability == "provider":
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


def x__inject_capabilities__mutmut_11(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "XXproviderXX":
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


def x__inject_capabilities__mutmut_12(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "PROVIDER":
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


def x__inject_capabilities__mutmut_13(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = None
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


def x__inject_capabilities__mutmut_14(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component(None, parent_capability)
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


def x__inject_capabilities__mutmut_15(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", None)
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


def x__inject_capabilities__mutmut_16(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component(parent_capability)
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


def x__inject_capabilities__mutmut_17(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", )
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


def x__inject_capabilities__mutmut_18(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("XXcapabilityXX", parent_capability)
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


def x__inject_capabilities__mutmut_19(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("CAPABILITY", parent_capability)
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


def x__inject_capabilities__mutmut_20(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", parent_capability)
        if capability_class:
            if isinstance(capability_class, type):
                capability_instance = None
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


def x__inject_capabilities__mutmut_21(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", parent_capability)
        if capability_class:
            if isinstance(capability_class, type):
                capability_instance = capability_class()
            else:
                capability_instance = None
            native_kwargs[parent_capability] = capability_instance
            logger.debug(
                f"FUNCTION_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{function_obj.__name__}'"
            )
        else:
            logger.warning(
                f"FUNCTION_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{function_obj.__name__}'"
            )


def x__inject_capabilities__mutmut_22(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
    parent_capability = getattr(function_obj, "_parent_capability", None)
    if parent_capability and parent_capability != "provider":
        capability_class = hub.get_component("capability", parent_capability)
        if capability_class:
            if isinstance(capability_class, type):
                capability_instance = capability_class()
            else:
                capability_instance = capability_class
            native_kwargs[parent_capability] = None
            logger.debug(
                f"FUNCTION_DISPATCH 🔧 Auto-injected capability '{parent_capability}' for '{function_obj.__name__}'"
            )
        else:
            logger.warning(
                f"FUNCTION_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{function_obj.__name__}'"
            )


def x__inject_capabilities__mutmut_23(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
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
                None
            )
        else:
            logger.warning(
                f"FUNCTION_DISPATCH ⚠️ Capability '{parent_capability}' not found for '{function_obj.__name__}'"
            )


def x__inject_capabilities__mutmut_24(function_obj: Any, native_kwargs: dict[str, Any]) -> None:
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
                None
            )

x__inject_capabilities__mutmut_mutants : ClassVar[MutantDict] = {
'x__inject_capabilities__mutmut_1': x__inject_capabilities__mutmut_1, 
    'x__inject_capabilities__mutmut_2': x__inject_capabilities__mutmut_2, 
    'x__inject_capabilities__mutmut_3': x__inject_capabilities__mutmut_3, 
    'x__inject_capabilities__mutmut_4': x__inject_capabilities__mutmut_4, 
    'x__inject_capabilities__mutmut_5': x__inject_capabilities__mutmut_5, 
    'x__inject_capabilities__mutmut_6': x__inject_capabilities__mutmut_6, 
    'x__inject_capabilities__mutmut_7': x__inject_capabilities__mutmut_7, 
    'x__inject_capabilities__mutmut_8': x__inject_capabilities__mutmut_8, 
    'x__inject_capabilities__mutmut_9': x__inject_capabilities__mutmut_9, 
    'x__inject_capabilities__mutmut_10': x__inject_capabilities__mutmut_10, 
    'x__inject_capabilities__mutmut_11': x__inject_capabilities__mutmut_11, 
    'x__inject_capabilities__mutmut_12': x__inject_capabilities__mutmut_12, 
    'x__inject_capabilities__mutmut_13': x__inject_capabilities__mutmut_13, 
    'x__inject_capabilities__mutmut_14': x__inject_capabilities__mutmut_14, 
    'x__inject_capabilities__mutmut_15': x__inject_capabilities__mutmut_15, 
    'x__inject_capabilities__mutmut_16': x__inject_capabilities__mutmut_16, 
    'x__inject_capabilities__mutmut_17': x__inject_capabilities__mutmut_17, 
    'x__inject_capabilities__mutmut_18': x__inject_capabilities__mutmut_18, 
    'x__inject_capabilities__mutmut_19': x__inject_capabilities__mutmut_19, 
    'x__inject_capabilities__mutmut_20': x__inject_capabilities__mutmut_20, 
    'x__inject_capabilities__mutmut_21': x__inject_capabilities__mutmut_21, 
    'x__inject_capabilities__mutmut_22': x__inject_capabilities__mutmut_22, 
    'x__inject_capabilities__mutmut_23': x__inject_capabilities__mutmut_23, 
    'x__inject_capabilities__mutmut_24': x__inject_capabilities__mutmut_24
}

def _inject_capabilities(*args, **kwargs):
    result = _mutmut_trampoline(x__inject_capabilities__mutmut_orig, x__inject_capabilities__mutmut_mutants, args, kwargs)
    return result 

_inject_capabilities.__signature__ = _mutmut_signature(x__inject_capabilities__mutmut_orig)
x__inject_capabilities__mutmut_orig.__name__ = 'x__inject_capabilities'


async def x__invoke_function__mutmut_orig(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_1(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = None
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_2(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(None)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_3(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = None
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_4(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = None
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_5(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = None

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_6(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind != inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_7(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name not in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_8(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = None
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_9(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_10(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = None
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_11(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind not in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_12(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
        for param_name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                # This is a *args parameter - extract its tuple
                if param_name in native_kwargs:
                    variadic_args = native_kwargs[param_name]
                    if not isinstance(variadic_args, (tuple, list)):
                        variadic_args = (variadic_args,)
            elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                # Regular positional parameter - add to ordered list
                if param_name not in native_kwargs:
                    positional_args.append(native_kwargs[param_name])
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_13(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
                    positional_args.append(None)
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_14(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind != inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_15(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name not in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_16(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = None

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_17(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = None

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_18(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args - list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_19(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(None)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_20(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(None):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_21(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = None
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_22(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(**keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_23(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, )
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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


async def x__invoke_function__mutmut_24(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = None

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


async def x__invoke_function__mutmut_25(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(**keyword_only_kwargs)

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


async def x__invoke_function__mutmut_26(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, )

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


async def x__invoke_function__mutmut_27(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            None
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


async def x__invoke_function__mutmut_28(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(None)} = {result_py_val}"
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


async def x__invoke_function__mutmut_29(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            None,
            exc_info=True,
        )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


async def x__invoke_function__mutmut_30(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Function '{function_obj.__name__}' failed: {func_err}",
            exc_info=None,
        )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


async def x__invoke_function__mutmut_31(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            exc_info=True,
        )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


async def x__invoke_function__mutmut_32(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Function '{function_obj.__name__}' failed: {func_err}",
            )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


async def x__invoke_function__mutmut_33(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

        logger.debug(
            f"FUNCTION_DISPATCH ✅ Function '{function_obj.__name__}' returned: {type(result_py_val)} = {result_py_val}"
        )
        return result_py_val
    except PyviderFunctionError:
        raise
    except Exception as func_err:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Function '{function_obj.__name__}' failed: {func_err}",
            exc_info=False,
        )
        raise PyviderFunctionError(
            f"Function '{function_obj.__name__}' execution failed: {func_err}"
        ) from func_err


async def x__invoke_function__mutmut_34(function_obj: Any, native_kwargs: dict[str, Any]) -> Any:
    """
    Invoke a function with properly ordered positional and variadic arguments.

    Builds positional arguments in signature order, then appends variadic args.
    This prevents "multiple values for parameter" errors when using *args.
    """
    try:
        func_sig = inspect.signature(function_obj)
        positional_args = []
        variadic_args = []
        keyword_only_kwargs = {}

        # Build arguments in signature order
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
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Keyword-only parameter - must be passed as kwarg
                if param_name in native_kwargs:
                    keyword_only_kwargs[param_name] = native_kwargs[param_name]

        # Combine: required positional + variadic
        all_args = positional_args + list(variadic_args)

        # Invoke with ordered positional args + keyword-only kwargs
        if inspect.iscoroutinefunction(function_obj):
            result_py_val = await function_obj(*all_args, **keyword_only_kwargs)
        else:
            result_py_val = function_obj(*all_args, **keyword_only_kwargs)

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
            None
        ) from func_err

x__invoke_function__mutmut_mutants : ClassVar[MutantDict] = {
'x__invoke_function__mutmut_1': x__invoke_function__mutmut_1, 
    'x__invoke_function__mutmut_2': x__invoke_function__mutmut_2, 
    'x__invoke_function__mutmut_3': x__invoke_function__mutmut_3, 
    'x__invoke_function__mutmut_4': x__invoke_function__mutmut_4, 
    'x__invoke_function__mutmut_5': x__invoke_function__mutmut_5, 
    'x__invoke_function__mutmut_6': x__invoke_function__mutmut_6, 
    'x__invoke_function__mutmut_7': x__invoke_function__mutmut_7, 
    'x__invoke_function__mutmut_8': x__invoke_function__mutmut_8, 
    'x__invoke_function__mutmut_9': x__invoke_function__mutmut_9, 
    'x__invoke_function__mutmut_10': x__invoke_function__mutmut_10, 
    'x__invoke_function__mutmut_11': x__invoke_function__mutmut_11, 
    'x__invoke_function__mutmut_12': x__invoke_function__mutmut_12, 
    'x__invoke_function__mutmut_13': x__invoke_function__mutmut_13, 
    'x__invoke_function__mutmut_14': x__invoke_function__mutmut_14, 
    'x__invoke_function__mutmut_15': x__invoke_function__mutmut_15, 
    'x__invoke_function__mutmut_16': x__invoke_function__mutmut_16, 
    'x__invoke_function__mutmut_17': x__invoke_function__mutmut_17, 
    'x__invoke_function__mutmut_18': x__invoke_function__mutmut_18, 
    'x__invoke_function__mutmut_19': x__invoke_function__mutmut_19, 
    'x__invoke_function__mutmut_20': x__invoke_function__mutmut_20, 
    'x__invoke_function__mutmut_21': x__invoke_function__mutmut_21, 
    'x__invoke_function__mutmut_22': x__invoke_function__mutmut_22, 
    'x__invoke_function__mutmut_23': x__invoke_function__mutmut_23, 
    'x__invoke_function__mutmut_24': x__invoke_function__mutmut_24, 
    'x__invoke_function__mutmut_25': x__invoke_function__mutmut_25, 
    'x__invoke_function__mutmut_26': x__invoke_function__mutmut_26, 
    'x__invoke_function__mutmut_27': x__invoke_function__mutmut_27, 
    'x__invoke_function__mutmut_28': x__invoke_function__mutmut_28, 
    'x__invoke_function__mutmut_29': x__invoke_function__mutmut_29, 
    'x__invoke_function__mutmut_30': x__invoke_function__mutmut_30, 
    'x__invoke_function__mutmut_31': x__invoke_function__mutmut_31, 
    'x__invoke_function__mutmut_32': x__invoke_function__mutmut_32, 
    'x__invoke_function__mutmut_33': x__invoke_function__mutmut_33, 
    'x__invoke_function__mutmut_34': x__invoke_function__mutmut_34
}

def _invoke_function(*args, **kwargs):
    result = _mutmut_trampoline(x__invoke_function__mutmut_orig, x__invoke_function__mutmut_mutants, args, kwargs)
    return result 

_invoke_function.__signature__ = _mutmut_signature(x__invoke_function__mutmut_orig)
x__invoke_function__mutmut_orig.__name__ = 'x__invoke_function'


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


async def x__call_function_impl__mutmut_orig(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_1(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(None)
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_2(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = None
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_3(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = None
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_4(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_5(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError(None)

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_6(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("XXFunction name is required.XX")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_7(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_8(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("FUNCTION NAME IS REQUIRED.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_9(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = None
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_10(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component(None, func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_11(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", None)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_12(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component(func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_13(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", )
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_14(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("XXfunctionXX", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_15(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("FUNCTION", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_16(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj and not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_17(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if function_obj or not callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_18(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or callable(function_obj):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_19(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(None):
            raise PyviderFunctionError(f"Function '{func_name}' not found or not callable.")

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_20(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
    """Implementation of CallFunction handler."""
    logger.debug(f"FUNCTION_DISPATCH 📞 Received call for function: '{request.name}'")
    response = pb.CallFunction.Response()
    try:
        func_name = request.name
        if not func_name:
            raise PyviderFunctionError("Function name is required.")

        function_obj = hub.get_component("function", func_name)
        if not function_obj or not callable(function_obj):
            raise PyviderFunctionError(None)

        func_meta = function_to_dict(function_obj)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_21(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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

        func_meta = None
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_22(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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

        func_meta = function_to_dict(None)
        params_meta = func_meta.get("parameters", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_23(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = None
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_24(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get(None, [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_25(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get("parameters", None)
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_26(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get([])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_27(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get("parameters", )
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_28(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get("XXparametersXX", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_29(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        params_meta = func_meta.get("PARAMETERS", [])
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_30(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = None  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_31(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get(None)  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_32(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("XXvariadic_parameterXX")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_33(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("VARIADIC_PARAMETER")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_34(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = None

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_35(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(None)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_36(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = None
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_37(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = None

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_38(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided <= num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_39(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    None
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_40(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided == num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_41(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    None
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_42(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = None

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


async def x__call_function_impl__mutmut_43(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            None, params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_44(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, None, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_45(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, None, func_sig
        )

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


async def x__call_function_impl__mutmut_46(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, None
        )

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


async def x__call_function_impl__mutmut_47(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            params_meta, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_48(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, variadic_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_49(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, func_sig
        )

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


async def x__call_function_impl__mutmut_50(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, )

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


async def x__call_function_impl__mutmut_51(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = None

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


async def x__call_function_impl__mutmut_52(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get(None, CtyDynamic())

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


async def x__call_function_impl__mutmut_53(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", None)

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


async def x__call_function_impl__mutmut_54(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get(CtyDynamic())

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


async def x__call_function_impl__mutmut_55(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", )

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


async def x__call_function_impl__mutmut_56(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get(None, {}).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_57(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", None).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_58(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get({}).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_59(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", ).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_60(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("XXreturnXX", {}).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_61(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("RETURN", {}).get("cty_type", CtyDynamic())

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


async def x__call_function_impl__mutmut_62(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("XXcty_typeXX", CtyDynamic())

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


async def x__call_function_impl__mutmut_63(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("CTY_TYPE", CtyDynamic())

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


async def x__call_function_impl__mutmut_64(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(None)
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


async def x__call_function_impl__mutmut_65(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = None
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


async def x__call_function_impl__mutmut_66(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(None)
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


async def x__call_function_impl__mutmut_67(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(None)
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


async def x__call_function_impl__mutmut_68(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(None, schema=declared_return_cty_type))
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


async def x__call_function_impl__mutmut_69(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=None))
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


async def x__call_function_impl__mutmut_70(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(schema=declared_return_cty_type))
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


async def x__call_function_impl__mutmut_71(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, ))
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


async def x__call_function_impl__mutmut_72(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(None, native_kwargs)

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


async def x__call_function_impl__mutmut_73(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, None)

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


async def x__call_function_impl__mutmut_74(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(native_kwargs)

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


async def x__call_function_impl__mutmut_75(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, )

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


async def x__call_function_impl__mutmut_76(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(None)
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


async def x__call_function_impl__mutmut_77(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(None)}.")
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


async def x__call_function_impl__mutmut_78(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(None)

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


async def x__call_function_impl__mutmut_79(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = None

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


async def x__call_function_impl__mutmut_80(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = await _invoke_function(None, native_kwargs)

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


async def x__call_function_impl__mutmut_81(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = await _invoke_function(function_obj, None)

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


async def x__call_function_impl__mutmut_82(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = await _invoke_function(native_kwargs)

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


async def x__call_function_impl__mutmut_83(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

        declared_return_cty_type = func_meta.get("return", {}).get("cty_type", CtyDynamic())

        if has_unknown:
            logger.debug(f"FUNCTION_DISPATCH ⏭️  Short-circuiting '{func_name}' due to unknown argument.")
            unknown_result = CtyValue.unknown(declared_return_cty_type)
            response.result.CopyFrom(marshal(unknown_result, schema=declared_return_cty_type))
            return response

        _inject_capabilities(function_obj, native_kwargs)

        logger.debug(f"FUNCTION_DISPATCH 🚀 Invoking '{func_name}' with kwargs: {list(native_kwargs.keys())}.")
        logger.debug(f"FUNCTION_DISPATCH 🔍 Function kwargs details: {native_kwargs}")

        result_py_val = await _invoke_function(function_obj, )

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


async def x__call_function_impl__mutmut_84(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        marshalled_result = None
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


async def x__call_function_impl__mutmut_85(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        marshalled_result = marshal(None, schema=declared_return_cty_type)
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


async def x__call_function_impl__mutmut_86(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        marshalled_result = marshal(result_py_val, schema=None)
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


async def x__call_function_impl__mutmut_87(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        marshalled_result = marshal(schema=declared_return_cty_type)
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


async def x__call_function_impl__mutmut_88(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        marshalled_result = marshal(result_py_val, )
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


async def x__call_function_impl__mutmut_89(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        response.result.CopyFrom(None)

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


async def x__call_function_impl__mutmut_90(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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

        logger.debug(None)

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


async def x__call_function_impl__mutmut_91(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        response.error.text = None
    except Exception as e:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Unhandled error in CallFunctionHandler for '{request.name}'",
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_92(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        response.error.text = str(None)
    except Exception as e:
        logger.error(
            f"FUNCTION_DISPATCH 💥 Unhandled error in CallFunctionHandler for '{request.name}'",
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_93(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
            None,
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_94(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
            exc_info=None,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_95(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
            exc_info=True,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_96(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
            )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_97(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
            exc_info=False,
        )
        diag = await create_diagnostic_from_exception(e)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_98(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        diag = None
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_99(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        diag = await create_diagnostic_from_exception(None)
        response.error.text = f"{diag.summary}: {diag.detail}"

    return response


async def x__call_function_impl__mutmut_100(request: pb.CallFunction.Request, context: Any) -> pb.CallFunction.Response:
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
        variadic_meta = func_meta.get("variadic_parameter")  # Optional variadic parameter
        func_sig = inspect.signature(function_obj)

        # Validate argument count
        # - Without variadic: must match exactly
        # - With variadic: must have at least the required parameters
        num_required = len(params_meta)
        num_provided = len(request.arguments)

        if variadic_meta:
            # With variadic parameter, we need AT LEAST the required parameters
            if num_provided < num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected at least {num_required}, got {num_provided}."
                )
        else:
            # Without variadic parameter, must match exactly
            if num_provided != num_required:
                raise PyviderFunctionError(
                    f"Incorrect number of arguments for {func_name}: expected {num_required}, got {num_provided}."
                )

        native_kwargs, has_unknown = _process_function_arguments(
            request.arguments, params_meta, variadic_meta, func_sig
        )

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
        response.error.text = None

    return response

x__call_function_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__call_function_impl__mutmut_1': x__call_function_impl__mutmut_1, 
    'x__call_function_impl__mutmut_2': x__call_function_impl__mutmut_2, 
    'x__call_function_impl__mutmut_3': x__call_function_impl__mutmut_3, 
    'x__call_function_impl__mutmut_4': x__call_function_impl__mutmut_4, 
    'x__call_function_impl__mutmut_5': x__call_function_impl__mutmut_5, 
    'x__call_function_impl__mutmut_6': x__call_function_impl__mutmut_6, 
    'x__call_function_impl__mutmut_7': x__call_function_impl__mutmut_7, 
    'x__call_function_impl__mutmut_8': x__call_function_impl__mutmut_8, 
    'x__call_function_impl__mutmut_9': x__call_function_impl__mutmut_9, 
    'x__call_function_impl__mutmut_10': x__call_function_impl__mutmut_10, 
    'x__call_function_impl__mutmut_11': x__call_function_impl__mutmut_11, 
    'x__call_function_impl__mutmut_12': x__call_function_impl__mutmut_12, 
    'x__call_function_impl__mutmut_13': x__call_function_impl__mutmut_13, 
    'x__call_function_impl__mutmut_14': x__call_function_impl__mutmut_14, 
    'x__call_function_impl__mutmut_15': x__call_function_impl__mutmut_15, 
    'x__call_function_impl__mutmut_16': x__call_function_impl__mutmut_16, 
    'x__call_function_impl__mutmut_17': x__call_function_impl__mutmut_17, 
    'x__call_function_impl__mutmut_18': x__call_function_impl__mutmut_18, 
    'x__call_function_impl__mutmut_19': x__call_function_impl__mutmut_19, 
    'x__call_function_impl__mutmut_20': x__call_function_impl__mutmut_20, 
    'x__call_function_impl__mutmut_21': x__call_function_impl__mutmut_21, 
    'x__call_function_impl__mutmut_22': x__call_function_impl__mutmut_22, 
    'x__call_function_impl__mutmut_23': x__call_function_impl__mutmut_23, 
    'x__call_function_impl__mutmut_24': x__call_function_impl__mutmut_24, 
    'x__call_function_impl__mutmut_25': x__call_function_impl__mutmut_25, 
    'x__call_function_impl__mutmut_26': x__call_function_impl__mutmut_26, 
    'x__call_function_impl__mutmut_27': x__call_function_impl__mutmut_27, 
    'x__call_function_impl__mutmut_28': x__call_function_impl__mutmut_28, 
    'x__call_function_impl__mutmut_29': x__call_function_impl__mutmut_29, 
    'x__call_function_impl__mutmut_30': x__call_function_impl__mutmut_30, 
    'x__call_function_impl__mutmut_31': x__call_function_impl__mutmut_31, 
    'x__call_function_impl__mutmut_32': x__call_function_impl__mutmut_32, 
    'x__call_function_impl__mutmut_33': x__call_function_impl__mutmut_33, 
    'x__call_function_impl__mutmut_34': x__call_function_impl__mutmut_34, 
    'x__call_function_impl__mutmut_35': x__call_function_impl__mutmut_35, 
    'x__call_function_impl__mutmut_36': x__call_function_impl__mutmut_36, 
    'x__call_function_impl__mutmut_37': x__call_function_impl__mutmut_37, 
    'x__call_function_impl__mutmut_38': x__call_function_impl__mutmut_38, 
    'x__call_function_impl__mutmut_39': x__call_function_impl__mutmut_39, 
    'x__call_function_impl__mutmut_40': x__call_function_impl__mutmut_40, 
    'x__call_function_impl__mutmut_41': x__call_function_impl__mutmut_41, 
    'x__call_function_impl__mutmut_42': x__call_function_impl__mutmut_42, 
    'x__call_function_impl__mutmut_43': x__call_function_impl__mutmut_43, 
    'x__call_function_impl__mutmut_44': x__call_function_impl__mutmut_44, 
    'x__call_function_impl__mutmut_45': x__call_function_impl__mutmut_45, 
    'x__call_function_impl__mutmut_46': x__call_function_impl__mutmut_46, 
    'x__call_function_impl__mutmut_47': x__call_function_impl__mutmut_47, 
    'x__call_function_impl__mutmut_48': x__call_function_impl__mutmut_48, 
    'x__call_function_impl__mutmut_49': x__call_function_impl__mutmut_49, 
    'x__call_function_impl__mutmut_50': x__call_function_impl__mutmut_50, 
    'x__call_function_impl__mutmut_51': x__call_function_impl__mutmut_51, 
    'x__call_function_impl__mutmut_52': x__call_function_impl__mutmut_52, 
    'x__call_function_impl__mutmut_53': x__call_function_impl__mutmut_53, 
    'x__call_function_impl__mutmut_54': x__call_function_impl__mutmut_54, 
    'x__call_function_impl__mutmut_55': x__call_function_impl__mutmut_55, 
    'x__call_function_impl__mutmut_56': x__call_function_impl__mutmut_56, 
    'x__call_function_impl__mutmut_57': x__call_function_impl__mutmut_57, 
    'x__call_function_impl__mutmut_58': x__call_function_impl__mutmut_58, 
    'x__call_function_impl__mutmut_59': x__call_function_impl__mutmut_59, 
    'x__call_function_impl__mutmut_60': x__call_function_impl__mutmut_60, 
    'x__call_function_impl__mutmut_61': x__call_function_impl__mutmut_61, 
    'x__call_function_impl__mutmut_62': x__call_function_impl__mutmut_62, 
    'x__call_function_impl__mutmut_63': x__call_function_impl__mutmut_63, 
    'x__call_function_impl__mutmut_64': x__call_function_impl__mutmut_64, 
    'x__call_function_impl__mutmut_65': x__call_function_impl__mutmut_65, 
    'x__call_function_impl__mutmut_66': x__call_function_impl__mutmut_66, 
    'x__call_function_impl__mutmut_67': x__call_function_impl__mutmut_67, 
    'x__call_function_impl__mutmut_68': x__call_function_impl__mutmut_68, 
    'x__call_function_impl__mutmut_69': x__call_function_impl__mutmut_69, 
    'x__call_function_impl__mutmut_70': x__call_function_impl__mutmut_70, 
    'x__call_function_impl__mutmut_71': x__call_function_impl__mutmut_71, 
    'x__call_function_impl__mutmut_72': x__call_function_impl__mutmut_72, 
    'x__call_function_impl__mutmut_73': x__call_function_impl__mutmut_73, 
    'x__call_function_impl__mutmut_74': x__call_function_impl__mutmut_74, 
    'x__call_function_impl__mutmut_75': x__call_function_impl__mutmut_75, 
    'x__call_function_impl__mutmut_76': x__call_function_impl__mutmut_76, 
    'x__call_function_impl__mutmut_77': x__call_function_impl__mutmut_77, 
    'x__call_function_impl__mutmut_78': x__call_function_impl__mutmut_78, 
    'x__call_function_impl__mutmut_79': x__call_function_impl__mutmut_79, 
    'x__call_function_impl__mutmut_80': x__call_function_impl__mutmut_80, 
    'x__call_function_impl__mutmut_81': x__call_function_impl__mutmut_81, 
    'x__call_function_impl__mutmut_82': x__call_function_impl__mutmut_82, 
    'x__call_function_impl__mutmut_83': x__call_function_impl__mutmut_83, 
    'x__call_function_impl__mutmut_84': x__call_function_impl__mutmut_84, 
    'x__call_function_impl__mutmut_85': x__call_function_impl__mutmut_85, 
    'x__call_function_impl__mutmut_86': x__call_function_impl__mutmut_86, 
    'x__call_function_impl__mutmut_87': x__call_function_impl__mutmut_87, 
    'x__call_function_impl__mutmut_88': x__call_function_impl__mutmut_88, 
    'x__call_function_impl__mutmut_89': x__call_function_impl__mutmut_89, 
    'x__call_function_impl__mutmut_90': x__call_function_impl__mutmut_90, 
    'x__call_function_impl__mutmut_91': x__call_function_impl__mutmut_91, 
    'x__call_function_impl__mutmut_92': x__call_function_impl__mutmut_92, 
    'x__call_function_impl__mutmut_93': x__call_function_impl__mutmut_93, 
    'x__call_function_impl__mutmut_94': x__call_function_impl__mutmut_94, 
    'x__call_function_impl__mutmut_95': x__call_function_impl__mutmut_95, 
    'x__call_function_impl__mutmut_96': x__call_function_impl__mutmut_96, 
    'x__call_function_impl__mutmut_97': x__call_function_impl__mutmut_97, 
    'x__call_function_impl__mutmut_98': x__call_function_impl__mutmut_98, 
    'x__call_function_impl__mutmut_99': x__call_function_impl__mutmut_99, 
    'x__call_function_impl__mutmut_100': x__call_function_impl__mutmut_100
}

def _call_function_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__call_function_impl__mutmut_orig, x__call_function_impl__mutmut_mutants, args, kwargs)
    return result 

_call_function_impl.__signature__ = _mutmut_signature(x__call_function_impl__mutmut_orig)
x__call_function_impl__mutmut_orig.__name__ = 'x__call_function_impl'
